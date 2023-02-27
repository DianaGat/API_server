import requests

url = "http://localhost:5000//calculateDeliveryFee"
data = {
    "cart_value": 790, 
    "delivery_distance": 2235, 
    "number_of_items": 4, 
    "time": "2021-10-12T13:00:00Z"
    }

print("Sending this request payload: ", data)
response = requests.post(url, json=data)
print("HTTP response code:", response.status_code)
print("Response payload: ", response.text)