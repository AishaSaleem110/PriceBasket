import uuid


class Price:
    """
          This class represents Price entity in the system

          This class can be extended to include geographical locations as pricelists
          can be different for different regions
          ...
          Attributes
          ----------
          _product_id : uuid
              unique identifier for the product
          _price_per_unit : float
              Price is stored per unit of the product
    """

    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_product_id', '_price_per_unit']

    def __init__(self,
                 product_id: uuid,
                 price: float):
        self._product_id = product_id
        self._price_per_unit = price

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id

    @property
    def price_per_unit(self):
        return self._price_per_unit

    @price_per_unit.setter
    def price_per_unit(self, price_per_unit):
        self._price_per_unit = price_per_unit

    def __repr__(self):
        return f"_product_id {self._product_id}," \
               f"price_per_unit {self._price_per_unit}"
