from enum import Enum
from typing import List


class BilledState(Enum):
    """
    Enum values to represent billing state of the products in the basket

    Using strings to represent different states causes implicit decoupling between several classes,
     causes code duplication, causes difficulty to add new states in future.

    BilledState.Unprocessed - represents the state when product has not been billed
    BilledState.Processed -represents the state when product has been billed
    """
    Processed = "processed"
    Unprocessed = "unprocessed"


class BasketState:
    """
    This class represents an intermediate state representation during the basket pricing process
    This information is important during pricing process

    ...
    Attributes
    ----------
    _product_description : str
        Name of the SKU/Product being priced
    _purchased_quantity : int
        Quantity purchased of SKU/Product being priced
    _billing_state : BilledState(enum) which has two possible values
        BilledState.Processed - represents it has been billed
        BilledState.Unprocessed - represents it has not yet been billed
    """

    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_product_description', '_purchased_quantity', '_billing_state']

    def __init__(self,
                 product_name: str,
                 purchased_quantity: int,
                 billing_state: BilledState = BilledState.Unprocessed):
        self._product_description = product_name
        self._purchased_quantity = purchased_quantity
        self._billing_state = billing_state

    @property
    def product_description(self):
        return self._product_description

    @product_description.setter
    def product_description(self, product_name):
        self._product_description = product_name

    @property
    def purchased_quantity(self):
        return self._purchased_quantity

    @purchased_quantity.setter
    def purchased_quantity(self, purchased_quantity):
        self._purchased_quantity = purchased_quantity

    @property
    def billing_state(self):
        return self._billing_state

    @billing_state.setter
    def billing_state(self, billing_state):
        self._billing_state = billing_state

    @staticmethod
    def get_products_in_basket_state(item_list: List[str]) -> List['BasketState']:
        """
        This function converts items entered on console to basketState clubbing together important information
        such as  quantity purchased and its billing state. Initially billingState is set to BillingState.Unprocessed.

        :param item_list - is the list of product names entered from console
        :return: returns converted list of product names entered through theconsole into BasketState
        """
        basket_products = []

        for x in set(item_list):
            basket_product = BasketState(x, item_list.count(x), BilledState.Unprocessed)
            basket_products.append(basket_product)

        return basket_products

    def change_billing_state(self):
        if self._billing_state == BilledState.Unprocessed:
            self._billing_state = BilledState.Processed
        else:
            self._billing_state = BilledState.Unprocessed

    def __repr__(self):
        return f"product_description {self.product_description}," \
               f"product_quantity {self._purchased_quantity}," \
               f"billing_state {self._billing_state}"
