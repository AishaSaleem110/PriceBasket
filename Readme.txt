# Pricing Basket Unit

### The Code

This code is written in Python 3.10 (using PyCharm IDE)

### Running The Code
*To run the code, open the terminal and go to the directory where the code resides and run the following code
 python main.py

*To run the unit tests,  Then, open the terminal and go to the directory where the code resides and run the following code
python -m unittest discover

### Sample inputs
**To price the basket
PriceBasket Apples Milk Bread
pricebasket apples milk bread
pricebasket apples apples
pricebasket soup soup bread
pricebaket soup Soup

** To quit
q

*The file is self-contained and all necessary libraries are imported.


### What is in the code
-The code contains a prototype of a basket pricing unit which:
-Takes products as input from the user using console
-check if any offers are applicable on the products
-Price the basket containing all products (assuming getting price data, offers data and products data from other microservices
-displays output to the user on console

## Assumptions
-mock_services package mocks api data from other microservices
-Cache folder mocks a local cache
-logs package represents server/local file where logs are stored for debugging

###Future Improvements
Files in local cache can be in csv format instead of pickle as it can be easy to import and export files directly, couldn't do it as it
required using a 3rd party library
