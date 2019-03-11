from enum import Enum


class Constants(Enum):
    # errors in linear model creation
    ERR_ERROR_DEG_FREEDOM = 'Error degrees of freedom must be positive. To achieve this increase smallest group size'
    ERR_NOT_POSITIVE_DEFINITE = 'Sigma star is not positive definite.'
