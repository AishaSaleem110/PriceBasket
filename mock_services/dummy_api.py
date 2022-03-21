import datetime as dt
import uuid
from typing import Optional

from logs.logging import CustomLogging
from mock_services.price import Price
from mock_services.product import Product
from rule_engine.custom_operator import CustomOperator
from rule_engine.condition_rule import ConditionRule
from mock_services.offer import OfferFlat, OfferGroup


class DummyApi:

    """
    This class represents Mock APIs from other Services
    Microservices architecture has been assumed so there are separate units for managing
    Products, Offers, Prices.

    This class represents getting mock data by calling Services of respective units

    """

    @staticmethod
    def get_updated_products() -> Optional:
        """
        This function mocks fetching products data from a microservice
        :return: the list of products available in the inventory, if no products found or
        exception occurs, it returns None

        """

        try:
            products = [Product("3944c2df-6a87-46e6-86a4-da45b0d371d3", "soup", "drinks", 0.0, "tin"),

                        Product("a7c77b26-a41b-4ff7-ae8d-d8ec312eddae", "bread", "bakery", 0.0, "loaf"),

                        Product("e115773a-bcfe-4c8d-9c39-89e4a43098fa", "milk", "bakery", 0.0, "bottle"),

                        Product("67e69f18-db75-464d-9cd1-a60183279f41", "apples", "fruit", 0.0, "bag")]

            return products
        except Exception as e:
            CustomLogging.log_error(e)
            return None

    @staticmethod
    def get_updated_price_list() -> Optional:
        """
             This function mocks fetching pricelist data from a microservice
             :return: the list of product-wise prices available in the inventory, if no price-list found or
             exception occurs, it returns None

        """
        try:
            products = DummyApi.get_updated_products()
            updated_price_list = [Price(products[0].product_id, 0.65),
                                  Price(products[1].product_id, 0.80),
                                  Price(products[2].product_id, 1.30),
                                  Price(products[3].product_id, 1.00)
                                  ]

            return updated_price_list
        except Exception as e:
            CustomLogging.log_error(e)
            return None

    @staticmethod
    def get_updated_offers() -> Optional:
        """
               This function mocks fetching offers data from a microservice
               :return: the list of offers available in the inventory, if no offer-list found or
               exception occurs, it returns None

               It is assumed this microservice returns only valid offers that are currently active to save
               network bandwidth as there can be thousands of offers in the system. Microservice can be configured
               to return current-date/ weekly/monthly valid offers

        """
        try:
            products = DummyApi.get_updated_products()

            p1 = OfferFlat(uuid.uuid4(), "Apples have 10% off their normal price this week", products[3].product_id,
                           dt.datetime(2022, 2, 12), dt.datetime(2022, 3, 12), True, 10)

            c2 = ConditionRule(CustomOperator.Equal, products[0].product_id, 2)

            p2 = OfferGroup(uuid.uuid4(), "Buy 2 tins of soup and get a loaf of bread for half price",
                            [products[0].product_id], dt.datetime(2022, 2, 12),
                            dt.datetime(2022, 3, 12), True, products[1].product_id, 50, [c2])
            return [p1, p2]
        except Exception as e:
            CustomLogging.log_error(e)
            return None
