import main
import unittest
from json import loads

class MainTestCase(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_Hello_World(self):
        """Should response Hello World!"""
        get_test = self.app.get('/')

        self.assertEqual(b'Hello World!', get_test.data)

    def test_calculate_success(self):
        json_content = """{"_isuFactors":{"variables":[{"valueNames":[],"name":"1","inHypothesis":false,"isuFactorNature":"GLOBAL_TRENDS","nature":"Within","origin":"Outcome","standardDeviation":1},{"valueNames":[],"name":"2","inHypothesis":false,"isuFactorNature":"GLOBAL_TRENDS","nature":"Within","origin":"Outcome","standardDeviation":1},{"valueNames":["1","2"],"inHypothesis":true,"isuFactorNature":"GLOBAL_TRENDS","nature":"Between","origin":"Between ISU Predictor","name":"p1","type":"ORDINAL","units":"","child":{"valueNames":["3","4"],"inHypothesis":true,"isuFactorNature":"GLOBAL_TRENDS","nature":"Between","origin":"Between ISU Predictor","name":"p2","type":"ORDINAL","units":"","child":null}},{"valueNames":["3","4"],"inHypothesis":true,"isuFactorNature":"GLOBAL_TRENDS","nature":"Between","origin":"Between ISU Predictor","name":"p2","type":"ORDINAL","units":"","child":null}],"betweenIsuRelativeGroupSizes":[{"_tableId":null,"dimensions":[{"order":0,"factorName":"p1","factorType":"Between ISU Predictor","value":"1"},{"order":0,"factorName":"p2","factorType":"Between ISU Predictor","value":"3"}],"_table":[[{"value":1,"id":[{"order":0,"factorName":"p1","factorType":"Between ISU Predictor","value":"1"},{"order":0,"factorName":"p2","factorType":"Between ISU Predictor","value":"3"}]},{"value":1,"id":[{"order":0,"factorName":"p1","factorType":"Between ISU Predictor","value":"1"},{"order":1,"factorName":"p2","factorType":"Between ISU Predictor","value":"4"}]}],[{"value":1,"id":[{"order":1,"factorName":"p1","factorType":"Between ISU Predictor","value":"2"},{"order":0,"factorName":"p2","factorType":"Between ISU Predictor","value":"3"}]},{"value":1,"id":[{"order":1,"factorName":"p1","factorType":"Between ISU Predictor","value":"2"},{"order":1,"factorName":"p2","factorType":"Between ISU Predictor","value":"4"}]}]]}],"marginalMeans":[{"_tableId":{"value":1,"id":[{"order":0,"factorName":"1","factorType":"Outcome","value":""}]},"_table":[[{"value":1,"id":[{"order":0,"factorName":"1","factorType":"Outcome","value":""},{"order":0,"factorName":"p1","factorType":"Between ISU Predictor","value":"1"},{"order":0,"factorName":"p2","factorType":"Between ISU Predictor","value":"3"}]}],[{"value":1,"id":[{"order":0,"factorName":"1","factorType":"Outcome","value":""},{"order":0,"factorName":"p1","factorType":"Between ISU Predictor","value":"1"},{"order":1,"factorName":"p2","factorType":"Between ISU Predictor","value":"4"}]}],[{"value":1,"id":[{"order":0,"factorName":"1","factorType":"Outcome","value":""},{"order":1,"factorName":"p1","factorType":"Between ISU Predictor","value":"2"},{"order":0,"factorName":"p2","factorType":"Between ISU Predictor","value":"3"}]}],[{"value":1,"id":[{"order":0,"factorName":"1","factorType":"Outcome","value":""},{"order":1,"factorName":"p1","factorType":"Between ISU Predictor","value":"2"},{"order":1,"factorName":"p2","factorType":"Between ISU Predictor","value":"4"}]}]]},{"_tableId":{"value":1,"id":[{"order":0,"factorName":"2","factorType":"Outcome","value":""}]},"_table":[[{"value":1,"id":[{"order":0,"factorName":"2","factorType":"Outcome","value":""},{"order":0,"factorName":"p1","factorType":"Between ISU Predictor","value":"1"},{"order":0,"factorName":"p2","factorType":"Between ISU Predictor","value":"3"}]}],[{"value":1,"id":[{"order":0,"factorName":"2","factorType":"Outcome","value":""},{"order":0,"factorName":"p1","factorType":"Between ISU Predictor","value":"1"},{"order":1,"factorName":"p2","factorType":"Between ISU Predictor","value":"4"}]}],[{"value":1,"id":[{"order":0,"factorName":"2","factorType":"Outcome","value":""},{"order":1,"factorName":"p1","factorType":"Between ISU Predictor","value":"2"},{"order":0,"factorName":"p2","factorType":"Between ISU Predictor","value":"3"}]}],[{"value":1,"id":[{"order":0,"factorName":"2","factorType":"Outcome","value":""},{"order":1,"factorName":"p1","factorType":"Between ISU Predictor","value":"2"},{"order":1,"factorName":"p2","factorType":"Between ISU Predictor","value":"4"}]}]]}],"smallestGroupSize":3,"theta0":[[0,0]],"outcomeCorrelationMatrix":{"_values":{"mathjs":"DenseMatrix","data":[[1,0],[0,1]],"size":[2,2]}}},"_targetEvent":"REJECTION","_solveFor":"POWER","_ciwidth":1,"_power":0.5,"_selectedTests":["Hotelling Lawley Trace"],"_typeOneErrorRate":0.01,"_gaussianCovariate":null,"_scaleFactor":1,"_varianceScaleFactors":[1,2],"_powerCurve":{"_confidenceInterval":{"assumptions":"Beta Fixed","lowerTailProbability":0,"upperTailProbability":1,"betaSamplesize":10,"betasigmaRank":1},"_xAxis":"DesiredPower","_dataSeries":[]}}"""
        post_test = self.app.post('/api/calculate',
                                  data=json_content,
                                  content_type='application/json')
        result = loads(post_test.data)

        self.assertEqual(result['message'], 'OK')
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['model']['errors'], [])

if __name__ == '__main__':
    unittest.main()
