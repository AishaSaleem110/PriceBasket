import unittest
from price_basket_result_display.PriceBasketResultDisplay import PriceBasketResultDisplay
from pricebasket.discount_product_detail import DiscountProductDetail


class TestPriceBasketResultDisplay(unittest.TestCase):

    def test_basket_result_display_discounts(self):
        expected = "Subtotal: £2.30\nApples 10 % off: -10p\nTotal: £2.20"

        output = repr(PriceBasketResultDisplay("2.30", [DiscountProductDetail('apples', '10', '10p')], "2.20"))

        self.assertEqual(expected, output)

    def test_basket_result_display_no_discounts(self):
        expected = "Subtotal: £0.80\nno offers available\nTotal: £0.80"
        output = repr(PriceBasketResultDisplay("0.80", [], "0.80"))

        self.assertEqual(expected, output)

    def test_basket_result_display_negative_case(self):
        expected = "Subtotal: £2.30\nApples 10 % off: -10p\nTotal: £2.20"
        output = repr(PriceBasketResultDisplay("0.80", [], "0.80"))

        self.assertNotEqual(expected, output)

    if __name__ == '__main__':
        # begin the unittest.main()
        unittest.main()
