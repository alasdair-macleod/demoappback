import unittest
import numpy as np
from pyglimmpse import unirep, multirep


from app.calculation_service.model.cluster import Cluster, ClusterLevel
from app.calculation_service.model.enums import TargetEvent, SolveFor, Tests, HypothesisType
from app.calculation_service.model.isu_factors import IsuFactors, OutcomeRepeatedMeasureStDev
from app.calculation_service.model.linear_model import LinearModel
from app.calculation_service.model.outcome import Outcome
from app.calculation_service.model.predictor import Predictor
from app.calculation_service.model.repeated_measure import RepeatedMeasure
from app.calculation_service.model.study_design import StudyDesign
from app.calculation_service.models import Matrix
from pyglimmpse.constants import Constants

from app.calculation_service.model.scenario_inputs import ScenarioInputs
from app.calculation_service.model.contrast_matrix import ContrastMatrix


class StudyDesignTestCase(unittest.TestCase):
    m = Matrix('M')

    def setUp(self):
        self.m = Matrix('M')

    def tearDown(self):
        pass

    def test___init__(self):
        """Should return a matrix with name M and vaules _SAMPLE"""
        expected = StudyDesign(
                isu_factors=None,
                target_event=None,
                solve_for=None,
                confidence_interval_width=None,
                sample_size=2,
                gaussian_covariate= None,
                power_curve=None)
        actual = StudyDesign()
        self.assertEqual(vars(expected), vars(actual))

    def test___str__(self):
        """Should print a statement containing name and values as a list"""
        expected = False
        if self.m.name in str(self.m) and str(self.m.matrix) in str(self.m):
            expected = True
        self.assertTrue(expected)

    def test_load_from_json(self):
        """Should read the study design correctly from the model on model_2.json"""
        outcome_1 = Outcome(name='one')
        outcome_1.hypothesis_type = HypothesisType.CUSTOM_U_MATRIX
        outcome_2 = Outcome(name='teo')
        outcome_2.hypothesis_type = HypothesisType.CUSTOM_U_MATRIX

        rep_meas_1 = RepeatedMeasure(name='repMeas', values=[0, 1], units='time', type='Numeric', partial_u_matrix=np.matrix([[1],[-1]]), correlation_matrix=np.matrix([[1, 0],[0, 1]]))
        rep_meas_1.hypothesis_type = HypothesisType.CUSTOM_U_MATRIX

        cluster_1 = Cluster(name='clstr', levels=[ClusterLevel(level_name='1'), ClusterLevel(level_name='2', no_elements=2)])
        predictor_1 = Predictor(name='prdctr', values=['grp1', 'grp2'])

        isu_factors = IsuFactors(variables=[outcome_1, outcome_2, rep_meas_1, cluster_1, predictor_1],
                                 smallest_group_size=2,
                                 outcome_correlation_matrix=np.matrix([[1, 0], [0, 1]]),
                                 outcome_repeated_measure_st_devs=[
                                     OutcomeRepeatedMeasureStDev(outcome='one', repeated_measure='repMeas', values=[2, 3]),
                                     OutcomeRepeatedMeasureStDev(outcome='teo', repeated_measure='repMeas', values=[4, 5])])

        expected = StudyDesign(isu_factors=isu_factors,
                               target_event=TargetEvent.REJECTION,
                               solve_for=SolveFor.POWER,
                               confidence_interval_width=1,
                               sample_size=10,
                               gaussian_covariate=None)

        inputs = ScenarioInputs(
                 alpha = 0.05,
                 target_power = 0.5,
                 smallest_group_size = 10,
                 scale_factor = 1,
                 test = Tests.HOTELLING_LAWLEY,
                 variance_scale_factor = 3
                 )


        json_data = open("model_2.json")
        data = json_data.read()
        json_data.close()
        actual = StudyDesign().load_from_json(data)
        actual.orthonormalize_u_matrix = False
        model = LinearModel()
        model.c_matrix = ContrastMatrix()
        model.c_matrix.hypothesis_type = HypothesisType.GLOBAL_TRENDS
        model.u_matrix = ContrastMatrix()
        model.u_matrix.hypothesis_type = HypothesisType.GLOBAL_TRENDS

        model.from_study_design(actual, inputs, False)
        expected_epsilon = unirep._chi_muller_muller_barton_1989(sigma_star=model.sigma_star,
                                                      rank_U=np.linalg.matrix_rank(model.u_matrix),
                                                      total_N=model.total_n,
                                                      rank_X=model.get_rank_x())

        self.assertEqual(1.075938008286021, expected_epsilon)

    def test_load_multiple_outcomes(self):
        """Should read the study design correctly from the model on model_3.json"""
        outcome_1 = Outcome(name='one')
        outcome_2 = Outcome(name='teo')
        rep_meas_1 = RepeatedMeasure(name='repMeas', values=[0, 1], units='time', type='Numeric', partial_u_matrix=np.matrix([[1],[-1]]), correlation_matrix=np.matrix([[1, 0],[0, 1]]))
        cluster_1 = Cluster(name='clstr', levels=[ClusterLevel(level_name='1'), ClusterLevel(level_name='2', no_elements=2)])
        predictor_1 = Predictor(name='prdctr', values=['grp1', 'grp2'])

        isu_factors = IsuFactors(variables=[outcome_1, outcome_2, rep_meas_1, cluster_1, predictor_1],
                                 smallest_group_size=2,
                                 outcome_correlation_matrix=np.matrix([[1, 0], [0, 1]]),
                                 outcome_repeated_measure_st_devs=[
                                     OutcomeRepeatedMeasureStDev(outcome='one', repeated_measure='repMeas', values=[2, 3]),
                                     OutcomeRepeatedMeasureStDev(outcome='teo', repeated_measure='repMeas', values=[4, 5])])

        expected = StudyDesign(isu_factors=isu_factors,
                               target_event=TargetEvent.REJECTION,
                               solve_for=SolveFor.POWER,
                               confidence_interval_width=1,
                               sample_size=10,
                               )

        inputs = ScenarioInputs(
            alpha=0.05,
            target_power=0.5,
            smallest_group_size=10,
            scale_factor=1,
            test=Tests.HOTELLING_LAWLEY,
            variance_scale_factor=3
        )


        json_data = open("model_3.json")
        data = json_data.read()
        json_data.close()
        actual = StudyDesign().load_from_json(data)
        model = LinearModel()
        model.from_study_design(actual, inputs, False)
        expected_epsilon = unirep._chi_muller_muller_barton_1989(sigma_star=model.sigma_star,
                                                      rank_U=np.linalg.matrix_rank(model.u_matrix),
                                                      total_N=model.total_n,
                                                      rank_X=model.get_rank_x())

        self.assertEqual(1.1024872940866097, expected_epsilon)


    def test_warning_wlk_two_moment_null_approx(self):
        """Should return undefined power an error messages"""

        rank_C = 3
        rank_U = 2
        rank_X = 4
        total_N = 20
        error_sum_square = np.matrix([[9.59999999999999000000000000, 0.000000000000000444089209850],
                                      [0.000000000000000444089209850, 9.59999999999999000000000000]])
        hypothesis_sum_square = np.matrix([[1.875, 1.08253175473054], [1.08253175473054, 0.625]])
        alpha = 0.05
        deliberately_fail_tolerance = 100

        actual = multirep.wlk_two_moment_null_approx(rank_C=rank_C,
                                                     rank_X=rank_X,
                                                     relative_group_sizes=[1],
                                                     rep_N=20,
                                                     alpha=alpha,
                                                     sigma_star=error_sum_square,
                                                     delta_es=hypothesis_sum_square,
                                                     tolerance=deliberately_fail_tolerance)

        self.assertEqual(np.isnan(actual.power), True)
        self.assertEqual(np.isnan(actual.noncentrality_parameter), True)
        self.assertEqual(actual.fmethod, Constants.FMETHOD_MISSING)
        self.assertEqual(actual.error_message,'Power is missing because because the noncentrality could not be computed.')

    def test_warning_pbt_two_moment_null_approx_obrien_shieh(self):
        """Should return undefined power an error messages"""

        rank_C = 3
        rank_U = 2
        rank_X = 4
        rep_N = 20
        error_sum_square = np.matrix([[9.59999999999999000000000000, 0.000000000000000444089209850],
                                      [0.000000000000000444089209850, 9.59999999999999000000000000]])
        hypothesis_sum_square = np.matrix([[1.875, 1.08253175473054], [1.08253175473054, 0.625]])
        alpha = 0.05
        deliberately_fail_tolerance = 100

        actual = multirep.pbt_two_moment_null_approx_obrien_shieh(rank_C=rank_C,
                                                                  rank_X=rank_X,
                                                                  relative_group_sizes=[1],
                                                                  rep_N=20,
                                                                  alpha=alpha,
                                                                  sigma_star=error_sum_square,
                                                                  delta_es=hypothesis_sum_square,
                                                                  tolerance=deliberately_fail_tolerance)
        self.assertEqual(np.isnan(actual.power), True)
        self.assertEqual(np.isnan(actual.noncentrality_parameter), True)
        self.assertEqual(actual.fmethod, Constants.FMETHOD_MISSING)
        self.assertEqual(actual.error_message, 'Power is missing because df2 or eval_HINVE is not valid.')


if __name__ == '__main__':
    unittest.main()
