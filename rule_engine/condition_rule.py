import uuid
from rule_engine.custom_operator import CustomOperator


class ConditionRule:
    """
        This class logically represents conditions for the offers
        It can be extended in future hence creating a separate entity
        Conditions can be logically represented as this class as there will always be a product on which
        an attribute needs to be checked

        Example: Buy 2 tins of soup can be represented as:
             Product_id : soup
             operator : Equal
             quantity : 2

        All offers needs to be logically represented to get checked

    """
    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_product_id', '_operator', '_quantity']

    def __init__(self,
                 operator: CustomOperator,
                 product_id: uuid,
                 quantity: int):
        self._operator = operator
        self._product_id = product_id
        self._quantity = quantity

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, operator):
        self._operator = operator

    @property
    def product(self):
        return self._product_id

    @product.setter
    def _product(self, product):
        self._product_id = product

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def _product(self, quantity):
        self._quantity = quantity

    def __repr__(self):
        return f"_product: {self._product} , _operator: {self._operator}, _quantity {self._quantity}"
