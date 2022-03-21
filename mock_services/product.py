import uuid


class Product:

    """
          This class represents Price entity in the system

          This class can be extended to include geographical locations as pricelists
          can be different for different regions
          ...
          Attributes
          ----------
          _product_id : uuid
                unique identifier for the product
          _product_description : str
                product name/description to be shown to the users
          _price : float
                price of the product sku
          _product_type
                product category as in future we can have an offer which is applicable on a category of product such as
                off on all fruits
          _product_unit
                To store the smallest unit of the product for which price is defined in the price list
    """

    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_product_id', '_product_description', '_price', '_product_type', '_product_unit']

    def __init__(self, product_id: uuid,
                 product_description: str,
                 product_type: str = None,
                 price: float = 0.0,
                 unit: str = None):

        self._product_id = product_id
        self._product_description = product_description
        self._price = price
        self._product_type = product_type
        self._product_unit = unit

    def __repr__(self):
        return f"Product: _product_id = {self._product_id}," \
               f"_product_description = {self._product_description}," \
               f"_price = {self._price}," \
               f" _product_type = {self._product_type}," \
               f"_product_unit = {self._product_unit}"

    @property
    def product_id(self):
        return self._product_id

    @property
    def product_unit(self):
        return self._product_unit

    @property
    def product_description(self):
        return self._product_description

    @property
    def price(self):
        return self._price

    @property
    def product_id(self):
        return self._product_id

    @property
    def product_type(self):
        return self._product_type
