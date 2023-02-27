import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"\..\main_code")
from server import app, validate_data
import unittest
import unittest.mock
from parameterized import parameterized

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @unittest.mock.patch('server.FeeCalculator.calculate_fee')
    def test_delivery_fee(self, mock_calculate_fee):
        expected_value = 710
        mock_calculate_fee.return_value = expected_value
        data = {
          "cart_value": 790,
          "delivery_distance": 2235,
          "number_of_items": 4,
          "time": "2021-10-12T13:00:00Z"
        }
        response = self.client.post('/calculateDeliveryFee', json=data)
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}, {response.text}")
        self.assertEqual(response.get_json(), {"delivery_fee": expected_value}, f"Expected delivery fee 710, but got {response.get_json()}")
        mock_calculate_fee.assert_called_once_with(data["cart_value"], data["delivery_distance"], data["number_of_items"], data["time"])

    def test_calculate_fee_without_data(self):
        response = self.client.post("/calculateDeliveryFee")
        self.assertEqual(response.status_code, 400, f"Error: Expected status code 400")


    @parameterized.expand([
        [{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}, None],
        [{"cart_value": -5, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-15T15:00:00Z"}, "The data is invalid: -5 is less than the minimum of 0"],
        [{"cart_value": "a", "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-15T15:00:00Z"}, "The data is invalid: 'a' is not of type 'integer'"],
        [{"cart_value": "2021-10-12T13:00:00Z", "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}, "The data is invalid: '2021-10-12T13:00:00Z' is not of type 'integer'"],
        [{"cart_value": 790, "delivery_distance": -5, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}, "The data is invalid: -5 is less than the minimum of 0"],
        [{"cart_value": 790, "delivery_distance": 2235, "number_of_items": -5, "time": "2021-10-12T13:00:00Z"}, "The data is invalid: -5 is less than the minimum of 1"],
        [{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-113:00:00Z"}, "The data is invalid: '2021-10-113:00:00Z' is not a 'date-time'"],
        [{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": 3}, "The data is invalid: 3 is not of type 'string'"],
        [{"delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}, "The data is invalid: 'cart_value' is a required property"]
    ])
    def test_validate_data(self, data, expected_result):
        result = validate_data(data)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()