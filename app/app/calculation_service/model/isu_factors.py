import numpy as np

from app.calculation_service.model.cluster import Cluster
from app.calculation_service.model.enums import IsuFactorType
from app.calculation_service.model.outcome import Outcome
from app.calculation_service.model.predictor import Predictor
from app.calculation_service.model.repeated_measure import RepeatedMeasure
from app.calculation_service.utilities import list_compare
from app.calculation_service.model.contrast_matrix import ContrastMatrix


class OutcomeRepeatedMeasureStDev(object):
    """Class to describe outcome repeated measure st deviations"""

    def __init__(self,
                 outcome: str=None,
                 repeated_measure: str=None,
                 values: []=None,
                 **kwargs):
        self.outcome = outcome
        self.repeated_measure = repeated_measure
        self.values = values

        if kwargs.get('source'):
            self.from_dict(kwargs['source'])

    def __eq__(self, other):
        comp = []
        for key in self.__dict__:
            if key not in other.__dict__:
                comp.append(False)
            elif key == 'values':
                comp.append(self.values.__eq__(other.values))
            else:
                comp.append(self.__dict__[key] == other.__dict__[key])
        return False not in comp

    def from_dict(self, source):
        if source['outcome']:
            self.outcome = source['outcome']
        if source['repMeasure']:
            self.repeated_measure = source['repMeasure']
        if source['values']:
            self.values = np.matrix(source['values'])

class IsuFactors(object):
    """
    Parent class for indepenent sampling unit factors (ISUs).

    Outcomes
    Repeated Measures
    Clusters
    """

    def __init__(self,
                 variables: []=None,
                 between_isu_relative_group_sizes: []=None,
                 marginal_means: []=None,
                 smallest_group_size: int=None,
                 theta0: [] = None,
                 outcome_correlation_matrix=None,
                 outcome_repeated_measure_st_devs=None,
                 cMatrix: ContrastMatrix = None,
                 uMatrix: ContrastMatrix = None,
                 full_beta: bool = False,
                 **kwargs):
        self.variables = variables
        self.between_isu_relative_group_sizes = between_isu_relative_group_sizes
        self.marginal_means = marginal_means
        self.smallest_group_size = smallest_group_size
        self.theta0 = theta0
        self.outcome_correlation_matrix = outcome_correlation_matrix
        self.outcome_repeated_measure_st_devs = outcome_repeated_measure_st_devs
        self.cMatrix = cMatrix
        self.uMatrix = uMatrix
        self.full_beta = full_beta

        if kwargs.get('source'):
            self.from_dict(kwargs['source'])

    def __eq__(self, other):
        comp = []
        for key in self.__dict__:
            if key not in other.__dict__:
                comp.append(False)
            if key == 'variables':
                comp.append(list_compare(self.variables, other.variables))
            elif key == 'outcome_correlation_matrix':
                comp.append(np.array_equal(self.outcome_correlation_matrix.data, other.outcome_correlation_matrix.data))
            else:
                comp.append(self.__dict__[key] == other.__dict__[key])
        return False not in comp

    def parse_factor(self, source):
        if source.get('origin'):
            factor_type = IsuFactorType(source['origin'])
            if factor_type == IsuFactorType.OUTCOME:
                return Outcome(source=source)
            if factor_type == IsuFactorType.REPEATED_MEASURE:
                return RepeatedMeasure(source=source)
            if factor_type == IsuFactorType.CLUSTER:
                return Cluster(source=source)
            if factor_type == IsuFactorType.PREDICTOR:
                return Predictor(source=source)

    def from_dict(self, source):
        if source.get('variables'):
            self.variables = [self.parse_factor(factor) for factor in source['variables']]
        if source.get('betweenIsuRelativeGroupSizes'):
            self.between_isu_relative_group_sizes = source['betweenIsuRelativeGroupSizes']
        if source.get('marginalMeans'):
            self.marginal_means = source['marginalMeans']
        if source.get('smallestGroupSize'):
            self.smallest_group_size = source['smallestGroupSize']
        if source.get('theta0'):
            self.theta0 = np.matrix(source['theta0'])
        if (source.get('outcomeCorrelationMatrix')
                and source['outcomeCorrelationMatrix'].get('_values')
                and source['outcomeCorrelationMatrix']['_values'].get('data')):
            self.outcome_correlation_matrix = np.matrix(source['outcomeCorrelationMatrix']['_values']['data'])
        if source.get('outcomeRepeatedMeasureStDevs'):
            self.outcome_repeated_measure_st_devs = \
                [OutcomeRepeatedMeasureStDev(source=stdev) for stdev in source['outcomeRepeatedMeasureStDevs']]
        if source.get('cMatrix'):
            self.cMatrix = ContrastMatrix()
            self.cMatrix.from_dict(source.get('cMatrix'))
        if source.get('uMatrix'):
            self.uMatrix = ContrastMatrix()
            self.uMatrix.from_dict(source.get('uMatrix'))

    def get_hypothesis(self):
        return [f for f in self.variables if f.in_hypothesis]

    def get_outcomes(self):
        return [f for f in self.variables if type(f) == Outcome]

    def get_predictors(self):
        return [f for f in self.variables if type(f) == Predictor]

    def get_repeated_measures(self):
        return [f for f in self.variables if type(f) == RepeatedMeasure]

    def get_clusters(self):
        return [f for f in self.variables if type(f) == Cluster]
