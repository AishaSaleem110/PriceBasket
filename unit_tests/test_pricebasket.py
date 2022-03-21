import unittest
from basket.basket_state import BasketState, BilledState
from pricebasket.discount_product_detail import DiscountProductDetail
from pricebasket.price_basket import PriceBasket
from typing import List


class TestPriceBasket(unittest.TestCase):

    # testing case PriceBasket Apples Milk Bread
    def test_price_basket_case1(self):
        b1 = BasketState('apples', 1, BilledState.Unprocessed)
        b2 = BasketState('milk', 1, BilledState.Unprocessed)
        b3 = BasketState('bread', 1, BilledState.Unprocessed)
        basket_products_list: List[BasketState] = [b1, b2, b3]

        # expected
        sub_total = "3.10"
        total = "3.00"
        d1 = [DiscountProductDetail('apples', '10', '10p')]
        expected = (sub_total, total)

        # output
        sub_total_out, total_out, list_out = PriceBasket().price_basket(basket_products_list)

        self.assertTupleEqual(expected, (sub_total_out, total_out)) and self.assertEqual(len(d1), len(list_out))

    # testing case PriceBasket Bread Bread
    def test_price_basket_case2(self):
        basket_products_list: List[BasketState] = [BasketState('bread', 2, BilledState.Unprocessed)]

        # expected
        sub_total = "1.60"
        total = "1.60"
        d1 = []
        expected = (sub_total, total)

        # output
        sub_total_out, total_out, list_out = PriceBasket().price_basket(basket_products_list)

        self.assertTupleEqual(expected, (sub_total_out, total_out)) and self.assertEqual(len(d1), len(list_out))

        # testing case PriceBasket Soup Soup Bread

    # testing soup soup bread
    def test_price_basket_case3(self):
        b1 = BasketState('soup', 2, BilledState.Unprocessed)
        b3 = BasketState('bread', 1, BilledState.Unprocessed)
        basket_products_list: List[BasketState] = [b1, b3]

        # expected
        sub_total = "0.80"
        total = "0.40"
        d1 = [DiscountProductDetail('bread', '50', '40p')]
        expected = (sub_total, total)

        # output
        sub_total_out, total_out, list_out = PriceBasket().price_basket(basket_products_list)

        self.assertTupleEqual(expected, (sub_total_out, total_out)) and self.assertEqual(len(d1), len(list_out))

    if __name__ == '__main__':
        # begin the unittest.main()
        unittest.main()
