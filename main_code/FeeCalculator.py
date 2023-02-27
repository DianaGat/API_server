from datetime import datetime, time
import math

class FeeCalculator:
    def __init__(self):
        self.__MAX_DELIVERY_FEE = 1500
        self.__FREE_DELIVERY_CART_VALUE = 10000
        self.__NO_SURCHARGE_CART_VALUE = 1000
        self.__BASE_DISTANCE = 1000
        self.__BASE_DISTANCE_FEE = 200
        self.__OVER_BASE_DISTANCE_FEE = 100
        self.__OVER_BASE_DISTANCE_UNIT = 500
        self.__NOT_CHARGABLE_NUMBER_OF_ITEMS = 4
        self.__EXTRA_ITEMS_SURCHARGE = 50
        self.__BULK_FEE_NUMBER_OF_ITEMS = 12
        self.__BULK_FEE = 120
        self.__RUSH_TIME_MILTIPLICATOR = 1.2
        self.__RUSH_TIME_START = time.fromisoformat("15:00:00")
        self.__RUSH_TIME_END = time.fromisoformat("19:00:00")
        self.__RUSH_WEEKDAY = "Friday"
        self.__DAYS_OF_WEEK = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7
        }

    def calculate_fee(self, cart_value: int, distance: int, number_of_items: int, time: str):
        if self._is_eligible_to_free_delivery(cart_value):
            return 0

        delivery_fee = self._cart_value_charge(cart_value)

        delivery_fee += self._distance_charge(distance)

        delivery_fee += self._number_of_items_charge(number_of_items)
        
        if self._is_rush_time(time):
            delivery_fee = delivery_fee * self.__RUSH_TIME_MILTIPLICATOR
        
        if self._is_over_max_delivery_fee(delivery_fee):
            delivery_fee = self.__MAX_DELIVERY_FEE
        return delivery_fee

    def _is_eligible_to_free_delivery(self, cart_value: int):
        if cart_value >= self.__FREE_DELIVERY_CART_VALUE:
            return True
        return False

    def _cart_value_charge(self, cart_value: int):
        charge = 0
        if cart_value < self.__NO_SURCHARGE_CART_VALUE: 
            surcharge = self.__NO_SURCHARGE_CART_VALUE - cart_value
            charge += surcharge
        return charge

    def _distance_charge(self, distance: int):
        charge = self.__BASE_DISTANCE_FEE
        distance_over_base_distance = distance - self.__BASE_DISTANCE
        if  distance_over_base_distance > 0:
            charge += math.ceil(distance_over_base_distance / self.__OVER_BASE_DISTANCE_UNIT) * self.__OVER_BASE_DISTANCE_FEE
        return charge

    def _number_of_items_charge(self, number_of_items: int):
        charge = 0
        number_of_items_with_extra_charge = number_of_items - self.__NOT_CHARGABLE_NUMBER_OF_ITEMS
        if number_of_items_with_extra_charge > 0:
            charge += number_of_items_with_extra_charge * self.__EXTRA_ITEMS_SURCHARGE
            if number_of_items > self.__BULK_FEE_NUMBER_OF_ITEMS:
                charge += self.__BULK_FEE
        return charge

    def _is_rush_time(self, time: str):
        date = datetime.fromisoformat(time)
        if date.isoweekday() == self.__DAYS_OF_WEEK[self.__RUSH_WEEKDAY]:
            if date.time() >= self.__RUSH_TIME_START and date.time() < self.__RUSH_TIME_END:
                return True
        return False

    def _is_over_max_delivery_fee(self, delivery_fee: int):
        if delivery_fee > self.__MAX_DELIVERY_FEE:
            return True
        return False

