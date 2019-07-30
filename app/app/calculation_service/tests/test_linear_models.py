import unittest

import numpy as np
from app.calculation_service.model.repeated_measure import RepeatedMeasure
from app.calculation_service.model.linear_model import LinearModel
from app.calculation_service.model.isu_factors import IsuFactors
from app.calculation_service.model.contrast_matrix import ContrastMatrix
from app.calculation_service.model.enums import HypothesisType


class LinearModelsTestCase(unittest.TestCase):

    def test_get_repeated_measures_u_matrix(self):
        """Should return a orthnormal u matrix"""
        expected = np.matrix([[0.5, 0.2886751, 0.2041241, 0, 0, 0],
                              [-0.5, -0.288675, -0.204124, 0, 0, 0],
                              [-0.5, 0.2886751, 0.2041241, 0, 0, 0],
                              [0.5, -0.288675, -0.204124, 0, 0, 0],
                              [0, -0.57735, 0.2041241, 0, 0, 0],
                              [0, 0.5773503, -0.204124, 0, 0, 0],
                              [0, 0, -0.612372, 0, 0, 0],
                              [0, 0, 0.6123724, 0, 0, 0],
                              [0, 0, 0, 0.5, 0.2886751, 0.2041241],
                              [0, 0, 0, -0.5, -0.288675, -0.204124],
                              [0, 0, 0, -0.5, 0.2886751, 0.2041241],
                              [0, 0, 0, 0.5, -0.288675, -0.204124],
                              [0, 0, 0, 0, -0.57735, 0.2041241],
                              [0, 0, 0, 0, 0.5773503, -0.204124],
                              [0, 0, 0, 0, 0, -0.612372],
                              [0, 0, 0, 0, 0, 0.6123724]])

        repeated_measure1 = RepeatedMeasure()
        repeated_measure1.hypothesis_type = HypothesisType.CUSTOM_U_MATRIX
        repeated_measure1.partial_u_matrix = np.matrix([[1, 0],
                                                        [0, 1]])
        repeated_measure2 = RepeatedMeasure()
        repeated_measure2.hypothesis_type = HypothesisType.CUSTOM_U_MATRIX
        repeated_measure2.partial_u_matrix = np.matrix([[1, 1, 1],
                                                        [-1, 0, 0],
                                                        [0, -1, 0],
                                                        [0, 0, -1]])
        repeated_measure3 = RepeatedMeasure()
        repeated_measure3.hypothesis_type = HypothesisType.CUSTOM_U_MATRIX
        repeated_measure3.partial_u_matrix = np.matrix([[1],
                                                        [-1]])
        repeated_measure1.in_hypothesis = True
        repeated_measure2.in_hypothesis = True
        repeated_measure3.in_hypothesis = True
        isufactors1 = IsuFactors()
        isufactors1.variables = [repeated_measure1, repeated_measure2, repeated_measure3]

        model = LinearModel()
        model.u_matrix = ContrastMatrix()
        model.u_matrix.hypothesis_type = HypothesisType.USER_DEFINED
        model.orthonormalize_u_matrix = True

        actual = model._get_repeated_measures_u_matrix(isufactors1)

        np.testing.assert_array_almost_equal(expected, actual, decimal=6)
