#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Indago
Python framework for numerical optimization
https://indago.readthedocs.io/
https://pypi.org/project/Indago/

Description: Indago contains several modern methods for real fitness function optimization over a real parameter domain
and supports multiple objectives and constraints. It was developed at the University of Rijeka, Faculty of Engineering.
Authors: Stefan Ivić, Siniša Družeta, Luka Grbčić
Contact: stefan.ivic@riteh.uniri.hr
License: MIT

File content: Definition of Particle Swarm Optimization (PSO) optimizer.
Usage: from indago import PSO

"""


import numpy as np
from ._optimizer import Optimizer, Candidate, Status
from scipy.interpolate import interp1d # need this for akb_model


class Particle(Candidate):
    """PSO Particle class. PSO Particle is a member of a PSO swarm.

    Reference: Eberhart, R., Kennedy, J. (1995). A new optimizer using particle swarm theory. MHS'95.
    Proceedings of the Sixth International Symposium on Micro Machine and Human Science, Nagoya, Japan, 39-43.
    
    Attributes
    ----------
    V : ndarray
        Particle velocity.
         
    Returns
    -------
    particle : Particle
        Particle instance.
    """
    
    def __init__(self, optimizer: Optimizer):
        super().__init__(optimizer)
        
        self.V = np.full(optimizer.dimensions, np.nan)


class PSO(Optimizer):
    """Particle Swarm Optimization method class.
    
    Attributes
    ----------
    variant : str
        Name of the PSO variant (``Vanilla``, ``TVAC``, or ``Chaotic``). Default: ``Vanilla``.
    params : dict
        A dictionary of PSO parameters.
    _v_max : ndarray
        Maximum particle velocities.
    _swarm : ndarray
        Array of Particle instances.
    _dF : ndarray
        Fitness differences, used in anakatabatic inertia.
    _pbests : ndarray
        Personal best solutions.
    _gbest_idx : ndarray
        Indices of neighborhood best solutions.
    _topo : ndarray
        Topology of the swarm (connection matrix).
        
    Returns
    -------
    optimizer : PSO
        PSO optimizer instance.
        
    """

    def __init__(self):
        super().__init__()


    def _check_params(self):
        """Private method which performs some PSO-specific parameter checks
        and prepares the parameters to be validated by Optimizer._check_params.

        Returns
        -------
        None
            Nothing
            
        """

        if not self.variant:
            self.variant = 'Vanilla'

        defined_params = list(self.params.keys())
        mandatory_params, optional_params = [], []
        
        if 'swarm_size' in self.params:
            self.params['swarm_size'] = int(self.params['swarm_size'])

        if self.variant == 'Vanilla':
            mandatory_params = 'swarm_size inertia cognitive_rate social_rate'.split()
            if 'swarm_size' not in self.params:
                self.params['swarm_size'] = max(10, self.dimensions)
                defined_params += 'swarm_size'.split()
            if 'inertia' not in self.params:
                self.params['inertia'] = 0.72
                defined_params += 'inertia'.split()
            if 'cognitive_rate' not in self.params:
                self.params['cognitive_rate'] = 1.0
                defined_params += 'cognitive_rate'.split()
            if 'social_rate' not in self.params:
                self.params['social_rate'] = 1.0
                defined_params += 'social_rate'.split()
            optional_params = 'akb_model akb_fun_start akb_fun_stop'.split()
        
        elif self.variant == 'TVAC':
            mandatory_params = 'swarm_size inertia'.split()
            if 'swarm_size' not in self.params:
                self.params['swarm_size'] = max(10, self.dimensions)
                defined_params += 'swarm_size'.split()
            if 'inertia' not in self.params:
                self.params['inertia'] = 0.72
                defined_params += 'inertia'.split()
            optional_params = 'akb_model akb_fun_start akb_fun_stop'.split()

        elif self.variant == 'Chaotic':
            mandatory_params = 'swarm_size inertia cognitive_rate social_rate max_cls_it chaotic_elite'.split()
            if 'swarm_size' not in self.params:
                self.params['swarm_size'] = max(10, self.dimensions)
                defined_params += 'swarm_size'.split()
            if 'inertia' not in self.params:
                self.params['inertia'] = 0.72
                defined_params += 'inertia'.split()
            if 'cognitive_rate' not in self.params:
                self.params['cognitive_rate'] = 1.0
                defined_params += 'cognitive_rate'.split()
            if 'social_rate' not in self.params:
                self.params['social_rate'] = 1.0
                defined_params += 'social_rate'.split()
            if 'max_cls_it' not in self.params:
                self.params['max_cls_it'] = 10
                defined_params += 'max_cls_it'.split()
            if 'chaotic_elite' not in self.params:
                self.params['chaotic_elite'] = 0.2
                defined_params += 'chaotic_elite'.split()
        
        else:
            assert False, f'Unknown variant! {self.variant}'

        """ Anakatabatic Inertia a.k.a. Polynomial PFIDI """
        if self.params['inertia'] == 'anakatabatic':
            optional_params += 'akb_fun_start akb_fun_stop'.split()
            
            if 'akb_model' in defined_params:
                optional_params += 'akb_model'.split()

                if self.params['akb_model'] in ['FlyingStork', 'MessyTie', 'TipsySpider', 'RightwardPeaks', 'OrigamiSnake']:   # w-list-based named akb_models                
                    if self.params['akb_model'] == 'FlyingStork':
                        w_start = [-0.86, 0.24, -1.10, 0.75, 0.72]
                        w_stop = [-0.81, -0.35, -0.26, 0.64, 0.60]
                        if self.variant != 'Vanilla':
                            self.log('Warning: akb_model \'FlyingStork\' was designed for Vanilla PSO')                    
                    elif self.params['akb_model'] == 'MessyTie':
                        w_start = [-0.62, 0.18, 0.65, 0.32, 0.77]
                        w_stop = [0.36, 0.73, -0.62, 0.40, 1.09]
                        if self.variant != 'Vanilla':
                            self.log('Warning: akb_model \'MessyTie\' was designed for Vanilla PSO') 
                    elif self.params['akb_model'] == 'TipsySpider':
                        w_start = [-0.32, 0.10, -0.81, 1.19, 0.55]
                        w_stop = [0.34, 0.36, 0.28, 0.75, 0.08]
                        if self.variant != 'Vanilla':
                            self.log('Warning: akb_model \'TipsySpider\' was designed for Vanilla PSO') 
                    elif self.params['akb_model'] == 'RightwardPeaks':
                        w_start = [-1.79, -0.33, 2.00, -0.67, 1.30]
                        w_stop = [-0.91, -0.88, -0.84, 0.67, -0.36]
                        if self.variant != 'TVAC':
                            self.log('Warning: akb_model \'RightwardPeaks\' was designed for TVAC PSO')
                    elif self.params['akb_model'] == 'OrigamiSnake':
                        w_start = [-1.36, 2.00, 1.00, -0.60, 1.22]
                        w_stop = [0.30, 1.03, -0.21, 0.40, 0.06]
                        if self.variant != 'TVAC':
                            self.log('Warning: akb_model \'OrigamiSnake\' was designed for TVAC PSO')                      # code shared for all w-list-based named akb_models
                    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
                    self.params['akb_fun_start'] = \
                                        interp1d(Th, w_start, kind='linear')
                    self.params['akb_fun_stop'] = \
                                        interp1d(Th, w_stop, kind='linear') 
                else:
                    if self.params['akb_model'] != 'Languid':
                        self.log('Warning: Unknown akb_model. Defaulting to \'Languid\'')
                        self.params['akb_model'] = 'Languid'
                    
            elif not ('akb_fun_start' in defined_params and 'akb_fun_stop' in defined_params):
                self.params['akb_model'] = 'Languid'
                optional_params += 'akb_model'.split()
                
            if self.params['akb_model'] == 'Languid':
                def akb_fun_languid(Th):
                    w = (0.72 + 0.05) * np.ones_like(Th)
                    for i, th in enumerate(Th):
                        if th < 4*np.pi/4: 
                            w[i] = 0
                    return w
                self.params['akb_fun_start'] = akb_fun_languid
                self.params['akb_fun_stop'] = akb_fun_languid 

        Optimizer._check_params(self, mandatory_params, optional_params, defined_params)

    def _init_method(self):
        """Private method for initializing the PSO optimizer instance.
        Initializes and evaluates the swarm.

        Returns
        -------
        None
            Nothing
            
        """

        if self.variant == 'TVAC' or self.params['inertia'] == 'anakatabatic':
            assert self.max_iterations or self.max_evaluations or self.max_elapsed_time, \
                'optimizer.max_iteration, optimizer.max_evaluations, or optimizer.max_elapsed_time should be provided for this method/variant'

        self._evaluate_initial_candidates()
        
        # Bounds for position and velocity
        self._v_max = 0.2 * (self.ub - self.lb)

        # Generate a swarm
        self._swarm = np.array([Particle(self) for c in range(self.params['swarm_size'])], dtype=Particle)
        
        # Prepare arrays
        self._dF = np.full(self.params['swarm_size'], np.nan)

        # Generate initial positions
        self._initialize_X(self._swarm)
        n0 = 0 if self._initial_candidates is None else self._initial_candidates.size
        for p in range(len(self._swarm)):
            
            # Random position
            # self._swarm[p].X = np.random.uniform(self.lb, self.ub)
            # self._initialize_X([self._swarm[p]]) # instead of the above
            
            # Using specified particles initial positions
            if p < n0:
                self._swarm[p] = self._initial_candidates[p].copy()
                    
            # Generate velocity
            self._swarm[p].V = np.random.uniform(-self._v_max, self._v_max)

            # No fitness change at the start
            self._dF[p] = 0.0

        # Evaluate
        if n0 < self.params['swarm_size']:
            self._collective_evaluation(self._swarm[n0:])
            
        # if all candidates are NaNs       
        if np.isnan([particle.f for particle in self._swarm]).all():
            self._err_msg = 'ALL CANDIDATES FAILED TO EVALUATE'
        
        # Use initial particles as best ones
        self._pbests = np.array([particle.copy() for particle in self._swarm], dtype=Particle)

        self._gbest_idx = np.zeros(self.params['swarm_size'], dtype=int)
        self._topo = np.zeros([self.params['swarm_size'], self.params['swarm_size']], dtype=bool)

        self._reinitialize_topology()
        self._find_neighborhood_best()

        self._finalize_iteration()
        
    def _reinitialize_topology(self, k=3):
        """Method for reinitializing the PSO swarm topology.
        Removes existing and creates new connections in the swarm topology.
        
        Attributes
        ----------
        k : int
            Size of PSO swarm neighborhood.

        Returns
        -------
        None
            Nothing
        """
        
        self._topo[:, :] = False
        for p in range(self.params['swarm_size']):
            links = np.random.randint(self.params['swarm_size'], size=k)
            self._topo[p, links] = True
            self._topo[p, p] = True

    def _find_neighborhood_best(self):
        """Method for determining the best particle of each neighborhood.

        Returns
        -------
        None
            Nothing
            
        """
        
        for p in range(self.params['swarm_size']):
            links = np.where(self._topo[p, :])[0]
            #best = np.argmin(self.BF[links])
            p_best = np.argmin(self._pbests[links])
            p_best = links[p_best]
            self._gbest_idx[p] = p_best

    def _run(self):
        """Main loop of PSO method.

        Returns
        -------
        optimum: Particle
            Best solution found during the PSO optimization.
            
        """

        # for EEEO
        if self._inject:
            worst = np.max(self._swarm)
            worst.X = np.copy(self._inject.X)
            worst.O = np.copy(self._inject.O)
            worst.C = np.copy(self._inject.C)
            worst.f = self._inject.f

            # PSO specific
            worst._dF = 0
            self._find_neighborhood_best()

        self._check_params()

        if self.status == Status.RESUMED:
            # TODO inspect why this is necessary for resume to work:
            if self._stopping_criteria():
                return self.best
            self.it += 1
        else:
            self._init_method()

        if 'inertia' in self.params:
            w = self.params['inertia']
        if 'cognitive_rate' in self.params:
            c1 = self.params['cognitive_rate']
        if 'social_rate' in self.params:
            c2 = self.params['social_rate']

        while True:
            
            R1 = np.random.uniform(0, 1, [self.params['swarm_size'], self.dimensions])
            R2 = np.random.uniform(0, 1, [self.params['swarm_size'], self.dimensions])
              
            if self.params['inertia'] == 'LDIW':                
                w = 1.0 - (1.0 - 0.4) * self._progress_factor()
            
            elif self.params['inertia'] == 'HSIW':
                w = 0.5 + (0.75 - 0.5) * np.sin(np.pi * self._progress_factor())

            elif self.params['inertia'] == 'anakatabatic':
                theta = np.arctan2(self._dF, np.min(self._dF))
                theta[theta < 0] = theta[theta < 0] + 2 * np.pi  # 3rd quadrant
                # fix for atan2(0,0)=0
                theta0 = theta < 1e-300
                theta[theta0] = np.pi / 4 + \
                    np.random.rand(np.sum(theta0)) * np.pi
                w_start = self.params['akb_fun_start'](theta)
                w_stop = self.params['akb_fun_stop'](theta)
                w = w_start * (1 - self._progress_factor()) + w_stop * self._progress_factor()
            
            w = w * np.ones(self.params['swarm_size']) # ensure w is a vector
            
            if self.variant == 'TVAC':
                c1 = 2.5 - (2.5 - 0.5) * self._progress_factor()
                c2 = 0.5 + (2.5 - 0.5) * self._progress_factor()

            # Calculate new velocity and new position
            for p, particle in enumerate(self._swarm):
                particle.V = w[p] * particle.V + \
                               c1 * R1[p, :] * (self._pbests[p].X - particle.X) + \
                               c2 * R2[p, :] * (self._pbests[self._gbest_idx[p]].X - particle.X)
                particle.X = particle.X + particle.V                       
                # Correct position to the bounds
                particle.clip(self)
                
            # Get old fitness
            f_old = np.array([particle.f for particle in self._swarm])

            # Evaluate swarm
            self._collective_evaluation(self._swarm)

            for p, particle in enumerate(self._swarm):
                # Calculate dF
                if np.isnan(particle.f):
                    self._dF[p] = np.inf
                elif np.isnan(f_old[p]):
                    self._dF[p] = -np.inf
                else:
                    self._dF[p] = particle.f - f_old[p]
                
            for p, particle in enumerate(self._swarm):
                # Update personal best
                if particle <= self._pbests[p]:
                    self._pbests[p] = particle.copy()  
                    
            # Update swarm topology
            if np.max(self._dF) >= 0.0:
                self._reinitialize_topology()
                
            # Find best particles in neighborhood 
            self._find_neighborhood_best()
            
            if self.variant == 'Chaotic':               
                # reinitialize non-elite candidates
                sorted_order = np.argsort(self._swarm)
                elite_swarm_size = max(1, round(self.params['chaotic_elite'] * len(self._swarm)))
                for p, particle in enumerate(self._swarm[sorted_order]):
                    if p >= elite_swarm_size:
                        particle.X = np.random.uniform(self.lb, self.ub)
                        particle.V = np.random.uniform(-self._v_max, self._v_max)
                
                # perform Chaotic Local Search on gbest
                gbest_cls = self.best.copy()
                gbest_before_cls = self.best.copy()
                X_unit = (gbest_cls.X - self.lb) / (self.ub - self.lb)
                for _ in range(self.params['max_cls_it']):
                    X_unit = 4 * X_unit * (1 - X_unit)
                    gbest_cls.X = self.lb + X_unit * (self.ub - self.lb)
                    self._collective_evaluation([gbest_cls])
                    if gbest_cls < gbest_before_cls: 
                        self._swarm[sorted_order[0]] = gbest_cls.copy()
                        break
        
            if self._finalize_iteration():
                break
        
        return self.best
