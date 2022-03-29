# Pricing Basket Unit

Write a program and associated unit tests that can price a basket of goods, accounting for special
offers.
The goods that can be purchased, which are all priced in GBP, are:
Soup – 65p per tin
Bread – 80p per loaf
Milk – £1.30 per bottle
Apples – £1.00 per bag

Current special offers are:
Apples have 10% off their normal price this week
Buy 2 tins of soup and get a loaf of bread for half price

The program should accept a list of items in the basket and output the subtotal, the special offer
discounts and the final price.

Input should be via the command line in the form PriceBasket item1 item2 item3 ...
For example: PriceBasket Apples Milk Bread
Output should be to the console, for example:
Subtotal: £3.10
Apples 10% off: -10p
Total: £3.00
If no special offers are applicable, the code should output:
Subtotal: £1.30
(no offers available)
Total: £1.30

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

##Future Improvements
Files in local cache can be in csv format instead of pickle as it can be easy to import and export files directly, couldn't do it as it
required using a 3rd party library
