#++++++++++++++++++++++++++++++++++++
# Libraries and modules
#++++++++++++++++++++++++++++++++++++

import numpy as np

#++++++++++++++++++++++++++++++++++++
# Bee class
#++++++++++++++++++++++++++++++++++++

class Bee():
    """
    Instantiates a bee object for the artificial bee colony algorithm.

    Attributes:
        position (numpy-array) : The current position of the bee in the search space, provided as numpy array of shape `(D,)`, `(D,1)` or `(1,D)`.
        function (callable)    : The objective function to evaluate the position.
        bounds (numpy-array)   : Bounds for each dimension of the search space,provided as a numpy array of shape `(D,2)` or `(2,D)`.
        trial (int)            : Counter to track the number of trials or unsuccessful updates for the bee.
    
    .. warning::
        AssertionError: If the length of the position and bounds arrays are not equal.
    """
    #--------------------------------------------------------------------------------
    def __init__(self,position,function,bounds):
        """
        Initializes a Bee instance with a position, an objective function, and search space bounds.

        Args:
            position (numpy-array): The initial position of the bee in the search space, provided as numpy array of shape `(D,)`, `(D,1)` or `(1,D)`.
            function (callable)   : The objective function to evaluate the position
            bounds (numpy-array)  : Bounds for each dimension of the search space, provided as a numpy array of shape `(D,2)` or `(2,D)`.
            trial (int)           : Counter to track the number of trials or unsuccessful updates for the bee.
        
        Raises:
            TypeError  : If `function` is not callable.
            TypeError  : If `position` is not a numpy array.
            TypeError  : If `bounds` is not a numpy array.
            ValueError : If `bounds` does not have shape `(D, 2)` or `(2, D)`.
            ValueError : If any dimension has its lower bound greater than the upper bound.
            ValueError : If `position` and `bounds` do not have compatible dimensions.
        """
    
        if not callable(function):
            raise TypeError("`function` must be callable.")
        self.function = function
        
        if not isinstance(bounds, np.ndarray):
            raise TypeError("`bounds` must be a numpy array.")
        if not ((bounds.shape[0] == 2) or (bounds.shape[1] == 2)):
            raise ValueError(f"`bounds` must have shape `(D, 2)` or `(2, D)`,  but got but got shape {bounds.shape}.")            
        if not np.all(bounds.reshape(-1,2)[:, 0] <= bounds.reshape(-1,2)[:, 1]):
            raise ValueError("Each lower bound must be less than or equal to its upper bound.")
        self.bounds = bounds.reshape(-1,2) 
        
        if not isinstance(position, np.ndarray):
            raise TypeError("`position` must be a numpy array.")
        if position.reshape(-1, 1).shape[0] != self.bounds.shape[0]:
            raise ValueError(f"`position` dimensionality ({position.reshape(-1, 1).shape[0]}) is not compatible with the bounds provided.")
        self.position = position
        
        self.trial = 0
    #--------------------------------------------------------------------------------
    @property
    def value(self):
        """
        Computes the value of the objective function at the bee's current position.

        Returns:
            float: The objective function value for the current position.
        """
        return self.function(self.position) 
    #--------------------------------------------------------------------------------
    @property
    def fitness(self):
        """
        Computes the fitness of the bee based on the value of the objective function

        Returns:
            float: The fitness value at the bee's current position.
        """
        if self.value >= 0:
            return 1/(1+self.value)
        else:
            return 1 + np.abs(self.value)
    #--------------------------------------------------------------------------------