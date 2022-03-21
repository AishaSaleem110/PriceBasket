import unittest
from basket.basket_state import BasketState, BilledState


class TestBasketState(unittest.TestCase):

    def test_get_products_in_basket_state_method(self):
        items = ['Apples', 'Milk', 'Bread']
        b1 = BasketState('Apples', 1, BilledState.Unprocessed)
        b2 = BasketState('Milk', 1, BilledState.Unprocessed)
        b3 = BasketState('Bread', 1, BilledState.Unprocessed)
        expected = [b1, b2, b3]
        output = BasketState.get_products_in_basket_state(items)
        self.assertEqual(len(expected), len(output))

    def test_get_products_in_basket_state_method_case2(self):
        self.assertEqual([], BasketState.get_products_in_basket_state([]))

    def test_get_products_in_basket_state_method_case3(self):
        self.assertNotEqual([], BasketState.get_products_in_basket_state(["apples", "apples", "bread"]))

    if __name__ == '__main__':
        # begin the unittest.main()
        unittest.main()