
class DiscountProductDetail:
    """
        This class represents discounted product details as displayed to the user
        Created a separate entity as it might be extended in future
        __repr__ method abstracts the details of how a discounted product should be displayed
        on console
        Separating concern as price_basket_result_display will just call str method of this class to display details
    """

    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_description', '_discount_percentage', '_discount_in_currency']

    def __init__(self,
                 description: str,
                 discount_percentage: str = None,
                 discount_in_currency: str = None):
        self._description = description
        self._discount_percentage = discount_percentage
        self._discount_in_currency = discount_in_currency

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def discount_percentage(self):
        return self._discount_percentage

    @discount_percentage.setter
    def discount_percentage(self, discount_percentage):
        self._discount_percentage = discount_percentage

    @property
    def discount_in_currency(self):
        return self._discount_in_currency

    @discount_in_currency.setter
    def discount_in_currency(self, discount_in_currency):
        self._discount_in_currency = discount_in_currency

    def __repr__(self):
        return f"{self.description.capitalize()} {self._discount_percentage} % off: -{self._discount_in_currency}"
