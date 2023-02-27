import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"\..\main_code")
from FeeCalculator import FeeCalculator
from parameterized import parameterized

class FeeCalculatorTests(unittest.TestCase):
    def setUp(self):
        self.FeeCalculator = FeeCalculator()


    @parameterized.expand([
        [10100, True],
        [10000, True],
        [999, False], 
        [0, False]
    ])
    def test_is_eligible_to_free_delivery(self, cart_value, expected_result):
        result = self.FeeCalculator._is_eligible_to_free_delivery(cart_value)
        self.assertEqual(result, expected_result)


    @parameterized.expand([
        [1000, 0],
        [1100, 0],
        [890, 110],
    ])
    def test_cart_value_charge(self, cart_value, expected_result):
        result = self.FeeCalculator._cart_value_charge(cart_value)
        self.assertEqual(result, expected_result)


    @parameterized.expand([
        [1499, 300],
        [1500, 300],
        [1501, 400],
        [1, 200]
    ])
    def test_distance_charge(self, distance, expected_result):
        result = self.FeeCalculator._distance_charge(distance)
        self.assertEqual(result, expected_result)


    @parameterized.expand([
        [4, 0],
        [5, 50],
        [10, 300],
        [13, 570],
        [12, 400]
    ])
    def test_number_of_items_charge(self, number_of_items, expected_result):
        result = self.FeeCalculator._number_of_items_charge(number_of_items)
        self.assertEqual(result, expected_result)


    @parameterized.expand([
        ["2021-10-12T13:00:00Z", False],
        ["2021-10-12T17:00:00Z", False],
        ["2021-10-15T13:00:00Z", False],
        ["2021-10-15T17:00:00Z", True],
        ["2021-10-15T15:00:00Z", True],
        ["2021-10-15T15:01:00Z", True],
        ["2021-10-15T19:00:00Z", False],
        ["2021-10-15T19:01:00Z", False],
    ])
    def test_is_rush_time(self, time, expected_result):
        result = self.FeeCalculator._is_rush_time(time)
        self.assertEqual(result, expected_result)


    @parameterized.expand([
        [1500, False],
        [1499, False],
        [0, False],
        [1599, True],
        [1600, True]
    ])
    def test_is_over_max_delivery_fee(self, delivery_fee, expected_result):
        result = self.FeeCalculator._is_over_max_delivery_fee(delivery_fee)
        self.assertEqual(result, expected_result)


    @parameterized.expand([
        [790, 2235, 4, "2021-10-12T13:00:00Z", 710], #example
        [790, 2235, 4, "2021-10-15T15:00:00Z", 710*1.2], #rush time == True
        [10000, 2235, 4, "2021-10-15T15:00:00Z", 0], #cart value >= 100e
        [790, 2235, 5, "2021-10-15T15:00:00Z", (710 + 50)*1.2], #rush time == True AND one item with extra charge
        [790, 2235, 12, "2021-10-15T15:00:00Z", (710 + 50*8)*1.2], #rush time == True AND eight items with extra charge
        [790, 2235, 13, "2021-10-15T15:00:00Z", 1500], #(nine items with extra charge + bulk fee AND rush time == True) = (710 + 50*9 + 120)*1.2 = 1536, over max delivery fee
        [790, 0, 4, "2021-10-15T13:00:00Z", 710 - 300], #delivery distance = 0, 300 = charge for extra 500 meters unit
        [790, 1499, 4, "2021-10-15T13:00:00Z", 710 - 300 + 100], #delivery distance = 1499, 100 = charge for one extra 500 unit
        [790, 30000, 4, "2021-10-15T13:00:00Z", 1500], #delivery distance = 30000, 710 - 300 + 100 *  58 = 6210, over max delivery fee
    ])
    def test_calculate_fee(self, cart_value, delivery_distance, number_of_items, time, expected_result):
        result = self.FeeCalculator.calculate_fee(cart_value, delivery_distance, number_of_items, time)
        self.assertEqual(result, expected_result, "calculation of delivery fee is wrong")

if __name__ == '__main__':
    print(os.path.dirname(os.path.realpath(__file__))+"../main_code")
    unittest.main()

