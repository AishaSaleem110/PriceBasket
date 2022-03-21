# separate entity so that if in future user interface changes from console then changes only need to be done in this
# class to change the display method
from logs.logging import CustomLogging


class PriceBasketResultDisplay:
    """
        To encapsulate all the information about user interface in one class so that
        if in future company wants to switch to any other user interface from console based UI,
        it can easily make changes in one class only. Possible future Extensibility is kept into mind
        All other modules should should send values to PriceBasketResultDisplay class and printing on console
        should only be done from PriceBasketResultDisplay class.

        Separate module has been created for the separation of concern/Responsibilty Driven Design Principle
        as Basket Pricing Unit should only be responsible for calculations. Displaying the results to user
        should be handled separately.

     """

    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_sub_total', '_discounted_items', '_total']

    def __init__(self,
                 subtotal: str = "0.0",
                 discounted_items: list = None,
                 total: str = "0.0"):

        self._sub_total = subtotal
        self._discounted_items = discounted_items
        self._total = total

    @property
    def sub_total(self):
        return self._sub_total

    @sub_total.setter
    def sub_total(self, subtotal):
        self._sub_total = subtotal

    @property
    def discounted_items(self):
        return self._discounted_items

    @discounted_items.setter
    def discounted_items(self, discounted_items):
        self._discounted_items = discounted_items

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, total):
        self._total = total

    def __repr__(self):
        return f"_sub_total {self._sub_total}," \
               f"_total {self._total}," \
               f"_discounted_items {self._discounted_items}"

    def display_result(self):
        """
        This method prints the pricing result on the console
        print statement calls the __repr__ method of this class which returns
        the formatted string and print it on console.
        :return: None
        """
        print(self)

    def __repr__(self):
        try:
            result = f"Subtotal: £{self.sub_total}\n"
            if len(self.discounted_items) > 0:
                for item in self.discounted_items:
                    result = result + str(item)
            else:
                result = result + str('no offers available')

            result = result + str(f"\nTotal: £{self._total}")

            return result
        except Exception as e:
            CustomLogging.log_error(e)
