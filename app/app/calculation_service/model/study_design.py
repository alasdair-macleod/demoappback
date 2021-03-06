import json
import traceback
from json import JSONDecoder
from pyglimmpse.constants import Constants
from pyglimmpse.exceptions.glimmpse_exception import GlimmpseValidationException

from app.calculation_service.model.enums import TargetEvent, SolveFor, Nature, OptionalArgs, Tests
from app.calculation_service.model.isu_factors import IsuFactors
from app.calculation_service.model.power_curve import PowerCurve
from app.calculation_service.model.confidence_interval import ConfidenceInterval
from app.calculation_service.validators import check_options, repn_positive, parameters_positive, valid_approximations, valid_internal_pilot
from app.calculation_service.model.gaussian_covariate import GaussianCovariate


class StudyDesign:
    """contains hypothesis and properties"""
    def __init__(self,
                 isu_factors: IsuFactors = None,
                 target_event: TargetEvent = None,
                 solve_for: SolveFor = None,
                 confidence_interval_width: int = None,
                 sample_size: int = 2,
                 gaussian_covariate: GaussianCovariate = None,
                 confidence_interval: ConfidenceInterval = None,
                 power_curve: int = None,
                 full_beta: bool = False):

        # fed in
        self.isu_factors = isu_factors
        self.target_event = target_event
        self.solve_for = solve_for
        self.confidence_interval_width = confidence_interval_width
        self.confidence_interval = confidence_interval
        self.sample_size = sample_size
        self.gaussian_covariate = gaussian_covariate
        self.power_curve = power_curve
        self.full_beta = full_beta

    def __eq__(self, other):
        comp = []
        for key in self.__dict__:
            if key not in other.__dict__:
                comp.append(False)
            elif key == 'isu_factors':
                comp.append(self.isu_factors.__eq__(other.isu_factors))
            elif key == 'power_curve':
                comp.append(True)
            else:
                comp.append(self.__dict__[key] == other.__dict__[key])
        return False not in comp

    @check_options
    @repn_positive
    @parameters_positive
    @valid_approximations
    @valid_internal_pilot
    def __pre_calc_validation(self):
        """Runs pre-calculation validation checks. Throws exceptions if any fail. Perhaps this should live in the validators module???"""
        pass

    def validate_design(self):
        """ Valudates the study design. returns True is valid. Returns False and stores exceptions on object if invalid. """
        self.exceptions = []
        try:
            self.__pre_calc_validation()
        except GlimmpseValidationException as e:
            self.exceptions.push(e)
        except Exception:
            traceback.print_exc()
            self.exceptions.push(GlimmpseValidationException("Sorry, something seems to have gone wron with out calculations. Please contact us."))
        if len(self.exceptions) > 0:
            return False
        else:
            return True

    def load_from_json(self, json_str: str):
        return json.loads(json_str, cls=StudyDesignDecoder)

    def calculate_c_matrix(self):
        """Calculate the C Matrix from the hypothesis"""
        partials = [p for p in self.isu_factors.get_hypothesis() if p.nature == Nature.BETWEEN]
        averages = [p for p in self.isu_factors.variables if p.nature == Nature.BETWEEN and not p.in_hypothesis]


class StudyDesignDecoder(JSONDecoder):

    def decode(self, s: str) -> StudyDesign:
        study_design = StudyDesign()
        d = json.loads(s)
        if d.get('_isuFactors'):
            study_design.isu_factors = IsuFactors(source=d['_isuFactors'])
        if d.get('_targetEvent'):
            study_design.target_event = TargetEvent(d['_targetEvent'])
        if d.get('_solveFor'):
            study_design.solve_for = SolveFor(d['_solveFor'])
        if d.get('_ciwidth'):
            study_design.confidence_interval_width = d['_ciwidth']
        if d.get('_gaussianCovariate'):
            study_design.gaussian_covariate = GaussianCovariate(source=d['_gaussianCovariate'])
        if d.get('_powerCurve'):
            study_design.power_curve = PowerCurve(source=d['_powerCurve'])
        if d.get('_define_full_beta'):
            study_design.full_beta = d['_define_full_beta']
        if d.get('_scaleFactor'):
            study_design.beta_scalar = d['_scaleFactor']
        if d.get('_varianceScaleFactors'):
            study_design.sigma_scalar = d['_varianceScaleFactors']
        if d.get('_confidence_interval'):
            study_design.unirepmethod = Constants.SIGMA_ESTIMATED
            if d['_confidence_interval']['beta_known']:
                study_design.unirepmethod = Constants.SIGMA_KNOWN
        return study_design
