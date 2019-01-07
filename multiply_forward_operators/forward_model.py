from abc import ABCMeta, abstractmethod
from gp_emulator import GaussianProcess
import numpy as np
from scipy.sparse import csr_matrix
from typing import List, Optional, Tuple

__author__ = 'Tonio Fincke (Brockmann Consult GmbH)'


class VariableDescriptor(object):

    def __init__(self, short_name: str, long_name: str, description: str, unit: str):
        self._short_name = short_name
        self._long_name = long_name
        self._description = description
        self._unit = unit

    @property
    def short_name(self) -> str:
        return self._short_name

    @property
    def long_name(self) -> str:
        return self._long_name

    @property
    def description(self) -> str:
        return self._description

    @property
    def unit(self) -> str:
        return self._unit


class ForwardModelOperator(metaclass=ABCMeta):
    """Base class for all forward model operators that can derive estimates of a signal
    from biophysical land parameters."""

    @abstractmethod
    def get_list_of_supported_variables(self) -> List[VariableDescriptor]:
        """Returns a list of descriptions of the parameters supported by this forward model """
        pass

    @abstractmethod
    def get_list_of_supported_data_types(self) -> List[str]:
        """Returns a list of the supported data types."""
        pass

    @abstractmethod
    def get_list_of_required_bands(self, data_types: Optional[List[str]]) -> dict:
        """
        :param data_types: A list of data types. If not given, the band names for all supported data types will be
        returned.
        :return: A dictionary where the keys are data types and the values are the band names expected by the
        forward model to work with the data type
        """
        pass

    @abstractmethod
    def create_observation_operator(self, num_params: int, emulator: GaussianProcess, metadata: dict, mask: np.array,
                                    state_mask: np.array, x_prev: np.array, band: int, calc_hess: bool) -> \
            Tuple[np.array, csr_matrix, Optional[np.array]]:
        """
        Creates an observation operator.
        :param num_params: The number of bio-physical parameters provided by this model.
        :param emulator: The Gaussian Process that is supposed to be used by the forward model.
        :param metadata: A dictionary which holds values that can be considered during the creation of the obervation
        operator. Usual values are observation and solar angles.
        :param mask: A boolean array stating whether valid observations exist for the pixel.
        :param state_mask: A boolean array stating whether values shall be retrieved for the specific pixel.
        :param x_prev: An estimate of the parameter values for every pixel that is not masked out by the state mask
        :param band: An index stating which band the observation operator shall work with.
        :param calc_hess: If true, a hessian matrix is returned as third parameter.
        :return: A tuple consisting of two to three elements: First is a numpy array with state vector estimates for
        every pixel of the specified band which has not been masked out. Second is a sparse matrix with matrices with
        partial derivatives for each pixel that has not been masked out. Third is a hessian matrix. It is only returned
        if the respective parameter has been set to true.
        """
        pass
