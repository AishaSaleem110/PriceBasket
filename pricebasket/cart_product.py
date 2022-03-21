import pickle
import uuid

from logs.logging import CustomLogging
from mock_services.offer import Offer
from mock_services.price import Price
from typing import List, Optional


class CartProduct:
    """
      This class represents a state which makes products self sufficient as it combines information
      for product, offers, price together in one entity
      It is required by PriceBasket unit
          ...
      Attributes
      ----------
       _product_id : str
          Name of the SKU/Product being priced
      _product_description : str
          Name of the SKU/Product being priced
      _price : float
          price of the product sku
      _product_type
          product category as in future we can have an offer which is applicable on a category of product such as
          off on all fruits
      _offers : list
          All valid offers for this product SKU
      _product_unit : str
          Unit in which product is sold and priced
    """

    # Slots are used to use memory efficiently
    __slots__ = ['_product_id', '_product_description', '_price', '_product_type', '_offers', '_product_unit']

    def __init__(self,
                 product_id: uuid,
                 description: str,
                 product_type: str = None,
                 price: float = 0.0,
                 product_unit: str = None,
                 offers=None):

        if offers is None:
            offers = []
        self._product_id = product_id
        self._product_description = description
        self._price = price
        self._product_type = product_type
        self._offers = offers
        self._product_unit = product_unit

    def __repr__(self):
        return f"Product: _product_id = {self._product_id}," \
               f"_product_description = {self._product_description}, " \
               f"_price = {self._price}," \
               f"_product_type = {self._product_type}," \
               f"_offers = {self._offers}," \
               f"_product_unit = {self._product_unit}"

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id

    @property
    def product_unit(self):
        return self._product_unit

    @product_unit.setter
    def product_unit(self, product_unit):
        self._product_unit = product_unit

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def product_description(self):
        return self._product_description

    @product_description.setter
    def product_description(self, product_description):
        self._product_description = product_description

    @property
    def offers(self):
        return self._offers

    @offers.setter
    def offers(self, offers):
        self._offers = offers

    @staticmethod
    def prepare_cart_products() -> None:
        """
        This function prepares the cart products from data from all other entities such as product, price and offers
        and saves the processed cart products in a cache

        The idea is to not do the extensive calculation again and again
        It considers not fetching all these information from Services again and again so save resources such as network bandwidth
        and Api calls

        Making products self sufficient and saving it in Cache increases speed

        This method is not thread safe, should be executed on a single thread

        :return: None
        """
        products = CartProduct.get_updated_products()
        offers = CartProduct.get_updated_offers()
        price_list = CartProduct.get_updated_price_list()

        updated_products = []

        try:
            if products is not None:
                for product in products:
                    cart_product = CartProduct(product.product_id, product.product_description,
                                               product.product_type, product.price, product.product_unit)

                    price = CartProduct.get_price_by_product(cart_product.product_id, price_list)
                    if price is not None:
                        cart_product.price = price.price_per_unit

                    valid_offers = CartProduct.get_offer_by_product(product.product_id, offers)
                    if valid_offers is not None:
                        cart_product.offers = valid_offers

                    updated_products.append(cart_product)

                with open('Cache/cartProducts.pkl', 'wb') as out_file:
                    pickle.dump(updated_products, out_file)
        except Exception as e:
            CustomLogging.log_error(e)

    @staticmethod
    def get_updated_products() -> Optional:
        try:
            with open('Cache/products.pkl', 'rb') as in_file:
                return pickle.load(in_file)
        except Exception as e:
            CustomLogging.log_error(e)
            return None

    @staticmethod
    def get_updated_price_list() -> Optional:
        try:
            with open('Cache/pricelist.pkl', 'rb') as in_file:
                return pickle.load(in_file)
        except Exception as e:
            CustomLogging.log_error(e)
            return None

    @staticmethod
    def get_updated_offers() -> Optional:
        try:
            with open('Cache/offers.pkl', 'rb') as in_file:
                return pickle.load(in_file)
        except Exception as e:
            CustomLogging.log_error(e)
            return None

    @staticmethod
    # using lambda instead of comprehension to avoid extra initialization of memory
    def get_product_by_description(description: str, products: List['CartProduct']) -> Optional:
        product = CartProduct.get_filtered_data(lambda x: x.product_description.lower() == description.lower(),
                                                products)
        if product is not None:
            return product[0]
        else:
            return None

    # using lambda instead of comprehension to avoid extra initialization of memory
    @staticmethod
    def get_product_by_id(product_id, products) -> Optional:
        product = CartProduct.get_filtered_data(lambda x: x.product_id == product_id,
                                                products)
        if product is not None:
            return product[0]
        else:
            return None

    @staticmethod
    def get_offer_by_product(product_id: uuid, offers: List[Offer]) -> tuple[Offer, ...] | None:
        promotions = CartProduct.get_filtered_data(lambda x: product_id in x.product_id, offers)

        if promotions is not None:
            return promotions
        else:
            return None

    @staticmethod
    def get_price_by_product(product_id: uuid, price_list: List[Price]) -> Optional:
        price = CartProduct.get_filtered_data(lambda x: (x.product_id == product_id),
                                              price_list)
        if price is not None:
            return price[0]
        else:
            return None


    @staticmethod
    def get_filtered_data(function, data) -> Optional:
        try:
            filtered_list = tuple(filter(function, data))
            return filtered_list
        except Exception as e:
            CustomLogging.log_error(e)
            return None
