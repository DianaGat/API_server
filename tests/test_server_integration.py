import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"\..\main_code")
from server import app
import unittest

class ServerIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_delivery_fee(self):
        data = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2021-10-12T13:00:00Z"
        }
        
        response = self.client.post('/calculateDeliveryFee', json=data)
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertEqual(response.get_json(), {"delivery_fee": 710}, f"Expected delivery fee 710, but got {response.get_json()}")

if __name__ == '__main__':
    unittest.main()

