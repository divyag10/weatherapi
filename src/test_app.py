import unittest
from routes.weatherapis import outfit_recommendation_call
from sql_app.core import get_activity_recommendation

class TestRecommendation(unittest.TestCase):

    def test_outfit_recommendation(self):
        result = outfit_recommendation_call(38, 25, 56)
        expected_value = 'Cottons'
        self.assertEqual(result, expected_value)

    def test_activity_recommendation(self):
        result = get_activity_recommendation(27,32,12)
        expected_value = 'picnic'
        self.assertEqual(result,expected_value)

if __name__ == "__main__":
    unittest.main()