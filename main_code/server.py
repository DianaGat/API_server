from flask import Flask, jsonify, request
from FeeCalculator import FeeCalculator
from jsonschema import exceptions, validators, FormatChecker

app = Flask(__name__)
fee_calculator = FeeCalculator()
@app.route('/calculateDeliveryFee', methods=['POST'])
def calculate_delivery_fee():
    data = request.get_json()
    message = validate_data(data)
    if message != None:
        return jsonify(message_response = message), 400

    cart_value = data["cart_value"]
    delivery_distance = data["delivery_distance"]
    number_of_items = data["number_of_items"]
    time = data["time"]

    delivery_fee = fee_calculator.calculate_fee(cart_value, delivery_distance, number_of_items, time)

    return jsonify({"delivery_fee": delivery_fee}), 200



schema = {
  "type": "object",
  "properties": {
    "cart_value": {"type": "integer",
                   "minimum": 0},
    "delivery_distance": {"type": "integer",
                          "minimum": 0},
    "number_of_items": {"type": "integer",
                        "minimum": 1},
    "time": {"type": "string",
             "format": "date-time"}
  },
  "required": ["cart_value", "delivery_distance", "number_of_items", "time"]
}

def validate_data(data):
    validator = validators.Draft7Validator(schema, format_checker=FormatChecker())
    try:
        validator.validate(instance=data)
    except exceptions.ValidationError as error:
        error_message = error.message
        return f"The data is invalid: {error_message}"
    return None

if __name__ == '__main__':
    app.run()
