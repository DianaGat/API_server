# Wolt backend assignment  
## Introduction
The API_server folder contains the code for the Wolt Backend assignment. The purpose of the assignment is to build a HTTP API that calculates the delivery fee based on request payload data and certain criteria described in the GitHub of Wolt assignment: <https://github.com/woltapp/engineering-summer-intern-2023#specification>.

## Requirements

For scripts from main_code folder:
* Python 3.11
Some dependencies just work with the Python version 3.11 or newer.

The rest of the requirements can be installed from the requirements.txt file.

## Contents

The API_server folder that you unzipped contains the following objects:
1. main_code folder
    * server.py: The app for the HTTP API.
    * FeeCalculator.py: The function that calculates the delivery fee.
2. tests folder
    * test_server.py: Script containing unit tests for the server.py script. 
    * test_FeeCalculator.py: Script containing unit tests for the FeeCalculator.py script.
    * test_server_integration.py: Script containing unit tests that check the integration between the server.py and FeeCalculator.py scripts.
    * http_request_test.py: Script that sends a request payload to a launched server and displays the calculated delivery fee in the response payload.
3. requirements.txt: File containing necessary dependencies for the assignment's scripts.
4. readme.md: Markdown file with instructions

## Usage

1. Open the API_server folder using the following command in your favorite terminal:

> cd path-to-folder\API_server

Replace "path-to-folder" with the path to the API_server folder on your machine.

2. Install the required packages using the following command:

> pip install -r requirements.txt

To use this and the rest of the commands, Python should be added to PATH. If Python is not added to PATH on your machine, you could install requirements and execute the scripts manually in your favorite IDE.

3. Launch the server using the following command (or run server.py script manually):

> python main_code\server.py

4. Send a request payload to the launched server using the following command (or run http_request_test.py script manually): 

> python tests\http_request_test.py   

Note, while your terminal is running the server, it blocks any other scripts from executing. To run another script, you need to run the script in a separate terminal or environment repeating all the steps except the step 3 and continuing with the steps 4 and 5.  
In my case, to check the http_request_test, I run it in a different IDE or cmd. Additionally, I used Postman desk app to check it separately.

5. Run the unit tests using the following command (or run test_FeeCalculator.py, test_server_integration.py, test_server.py scripts manually):

> python -m unittest discover .\tests

The command executes unit tests for FeeCalculator class and the server. Also, it runs the integration test of the server.


## API Endpoint

The API endpoint is /calculateDeliveryFee and it accepts a POST request with a JSON payload containing the following parameters:

* cart_value: int, the value of the cart in EUR cents.
* delivery_distance: int, the delivery distance in meters.
* number_of_items: int the number of items in the cart.
* time: str, the time of the delivery in ISO time format.

The API returns a JSON payload containing the calculated delivery fee.
* delivery_fee: int, the value of the delivery fee in EUR cents
