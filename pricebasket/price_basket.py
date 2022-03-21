import pickle
from typing import Optional, List

from basket.basket_state import BasketState, BilledState
from logs.logging import CustomLogging
from mock_services.offer import OfferFlat, OfferGroup
from pricebasket.cart_product import CartProduct
from pricebasket.currency_utility_methods import CurrencyUtilityMethods
from pricebasket.discount_product_detail import DiscountProductDetail
from rule_engine.rule_inference_engine import RuleInferenceEngine


class PriceBasket:
    """
    This is the main entity which prices the baskets containing products

    price_basket method is called to price a basket which encapsulates all details regarding pricing

    It does not print the result of basket pricing as it is a separate functionality and is dedicated to
    PriceBasketResultDisplay class

    """
    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_cart_products']

    def __init__(self):
        # using tuples because it consumes less memory and we don't need to update it either
        cart_prods = PriceBasket.get_cart_products()
        if cart_prods is not None:
            self._cart_products = tuple(cart_prods)
        else:
            self._cart_products = tuple([])

    @property
    def cart_products(self):
        return self._cart_products

    @cart_products.setter
    def cart_products(self, cart_products):
        self._cart_products = cart_products

    def price_basket(self, basket: List[BasketState]) -> tuple[str, str, list]:
        """
        This method prices the basket

        This method checks if there are any offers on the product and if conditions for offers are satisfied then
        calculate discounted bill Or of conditions are not satisfied then price the products regularly

        This method is thread safe and if there are thousands of baskets to be priced, this method can be called in
        parallel for pricing multiple baskets at the same time.

        It loads cart products from cache and use them to price the basket which increases the speed

        :param basket: list of products in BasketState containing quantity of each product purchased
        :return: It returns total bill, Subtotal bill and the list of discounted items
        """

        total = 0.0
        sub_total = 0.0
        discounted_items = []

        for item in basket:
            if item.billing_state == BilledState.Unprocessed:

                try:

                    cart_product: CartProduct = PriceBasket.get_product_by_description(item.product_description,
                                                                                       self._cart_products)
                    if cart_product is not None:
                        # offer available on the product purchased
                        if cart_product.offers:
                            for offer in cart_product.offers:

                                if offer.offer_type == OfferFlat.offer_class():

                                    regular_price, discounted_price, discounted_item = PriceBasket.bill_calculation_with_offer(
                                        item.purchased_quantity,
                                        cart_product,
                                        offer)
                                    item.change_billing_state()

                                    discounted_items.append(discounted_item)
                                    sub_total = sub_total + regular_price
                                    total = total + discounted_price

                                elif offer.offer_type == OfferGroup.offer_class():
                                    # case when conditional discount is NOT  offered on same product
                                    # Eg: Buy 2 tins of soup and get a loaf of bread for half price
                                    if offer.product_id != offer.discounted_product_id:

                                        # check if discounted product exist in basket
                                        discounted_product = CartProduct.get_product_by_id(offer.discounted_product_id,
                                                                                           self.cart_products)

                                        discounted_product_purchased = PriceBasket.get_product_by_description(
                                            discounted_product.product_description, basket)

                                        # if discounted product has not been purchased, then price current item in
                                        # basket on regular price
                                        if discounted_product_purchased is None:

                                            regular_bill = PriceBasket.bill_calculation_without_offer(
                                                cart_product.price,
                                                item.purchased_quantity)
                                            sub_total = sub_total + regular_bill
                                            total = total + regular_bill
                                            item.change_billing_state()

                                        else:
                                            # if discounted product is found in purchased basket, we need to check
                                            # two more cases

                                            # Now check if all conditions are satisfied to get eligible for discount
                                            if RuleInferenceEngine.all_conditions_satisfy(offer.conditions, item):

                                                # check if discounted product has NOT yet been processed
                                                if discounted_product_purchased.billing_state == BilledState.Unprocessed:

                                                    # apply discount
                                                    regular_price, discounted_price, discounted_item = PriceBasket.bill_calculation_with_offer(
                                                        discounted_product_purchased.purchased_quantity,
                                                        discounted_product,
                                                        offer)

                                                    discounted_items.append(discounted_item)
                                                    sub_total = sub_total + regular_price
                                                    total = total + discounted_price

                                                    # update basket so that it doesn't get processed again
                                                    basket.remove(discounted_product_purchased)
                                                    discounted_product_purchased.change_billing_state()
                                                    basket.append(discounted_product_purchased)

                                                    # also update product for which offer is being processed
                                                    item.change_billing_state()

                                                # discounted product has already been processed on regular price and
                                                # needs adjustment
                                                elif discounted_product_purchased.billing_state == BilledState.Processed:

                                                    regular_price, discounted_price, discounted_item = PriceBasket.bill_calculation_with_offer(
                                                        discounted_product_purchased.purchased_quantity,
                                                        discounted_product,
                                                        offer)

                                                    # adjusting eligible discount in the bill
                                                    discounted_items.append(discounted_item)
                                                    adjustment = regular_price - discounted_price
                                                    total = total - adjustment

                                                    item.change_billing_state()
                                            else:
                                                # conditions are not satisfied , hence discount is not eligible
                                                regular_bill = PriceBasket.bill_calculation_without_offer(
                                                    cart_product.price,
                                                    item.purchased_quantity)
                                                sub_total = sub_total + regular_bill
                                                total = total + regular_bill
                                                item.change_billing_state()

                                    # case when conditions required and discount available is on same product
                                    # Eg Buy 2 tins of soup get 50 percent off on soup
                                    else:
                                        regular_price, discounted_price, discounted_item = PriceBasket.bill_calculation_with_offer(
                                            item.purchased_quantity,
                                            cart_product,
                                            offer)

                                        discounted_items.append(discounted_item)
                                        sub_total = sub_total + regular_price
                                        total = total + discounted_price
                                        item.change_billing_state()

                        # there is no offer available on the product purchased
                        else:

                            regular_bill = PriceBasket.bill_calculation_without_offer(cart_product.price,
                                                                                      item.purchased_quantity)
                            sub_total = sub_total + regular_bill
                            total = total + regular_bill
                            item.change_billing_state()

                except Exception as e:
                    CustomLogging.log_error(e)

        sub_total = CurrencyUtilityMethods.get_two_decimal_formatted_string(sub_total)
        total = CurrencyUtilityMethods.get_two_decimal_formatted_string(total)

        return sub_total, total, discounted_items


    @staticmethod
    def bill_calculation_with_offer(purchased_quantity, cart_product, offer) -> tuple[float, float,
                                                                                      DiscountProductDetail]:
        """
        This method calculated bills if any offer is applied on the product
        :param purchased_quantity: amount in which product is purchased
        :param cart_product: product which has been purchased and bill is calculated for
        :param offer: what is the offer on this item
        :return: a tuples containing regular price, final price and discounted item
        """
        regular_price = purchased_quantity * cart_product.price

        try:
            discount_offered = CurrencyUtilityMethods.percentage(offer.discount_percent,
                                                                 regular_price)

        except Exception as e:
            CustomLogging.log_error(e)
            discount_offered = 0.0

        final_price = regular_price - discount_offered

        discounted_item = DiscountProductDetail(cart_product.product_description, offer.discount_percent,
                                                CurrencyUtilityMethods.get_currency_with_unit(discount_offered))

        return regular_price, final_price, discounted_item

    @staticmethod
    def bill_calculation_without_offer(price: float, quantity: int) -> float:
        """
        This method calculates bill using regular price as no offer is applied
        :param price: price of the product
        :param quantity: amount of product purchased
        :return: returns the bill of the purchased product
        """
        return price * quantity

    @staticmethod
    def get_cart_products() -> Optional[tuple]:
        """
        This method fetches cart_products from the local cache
        :return:
        """
        with open('Cache/cartProducts.pkl', 'rb') as in_file:
            try:
                products = tuple(pickle.load(in_file))
                return products
            except Exception as e:
                CustomLogging.log_error(e)
                return None

    @staticmethod
    def get_product_by_description(description, products) -> Optional:

        # using lambda instead of comprehension to avoid extra initialization of memory
        product = PriceBasket.get_filtered_data(lambda x: x.product_description.lower() in description, products)
        if product is not None:
            return product[0]
        else:
            return None

    @staticmethod
    def get_filtered_data(function, data) -> Optional:
        try:
            filtered_list = tuple(filter(function, data))
            if not filtered_list:
                return None
            else:
                return filtered_list
        except Exception as e:
            CustomLogging.log_error(e)
            return None
