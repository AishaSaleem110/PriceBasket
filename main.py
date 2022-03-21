import pickle
from typing import Optional

from basket.basket_state import BasketState
from logs.logging import CustomLogging
from mock_services.dummy_api import DummyApi
from price_basket_result_display.PriceBasketResultDisplay import PriceBasketResultDisplay
from pricebasket.cart_product import CartProduct
from pricebasket.price_basket import PriceBasket


def main():
    # initializing custom logging class
    CustomLogging()
    update_inventory(False)
    display_inventory()
    get_basket_to_price()
    return 0


def update_inventory(update: bool = False) -> None:
    """
    This method fetches the updated products list, price list and updated offers
    and updated the data in the local cache if update value is True

    Idea is to have another service that periodically checks with other Entities(Product/Price/Offers)
    if there data has been updated and if true then update inventory is called to update the local cache.
    The benefit is reduced bandwidth usage (resource usage) as instead of fetching data everyday we can
    only fetch data if inventory is updated.

    Instead of fetching everything we are storing data in local cache as these data usually doesn't
    get updated very often which also reduces api calls and caching increases speed


    :param update:
    :return:
    """
    if update:
        try:
            get_updated_products()
            get_updated_offers()
            get_updated_price_list()

            if update:
                # if any update then local cart products also need to be recalculated and updated
                CartProduct.prepare_cart_products()

        except Exception as e:
            CustomLogging.log_error(e)


def get_updated_products() -> None:
    """
    Fetches updated products from micro services and stores in local cache
    :return: None
    """
    try:
        products = DummyApi.get_updated_products()
        if products is not None:
            with open('Cache/products.pkl', 'wb') as out_file:
                pickle.dump(products, out_file)

    except Exception as e:
        CustomLogging.log_error(e)


def get_updated_price_list() -> None:
    """
    Fetches updated pricelist from micro services and stores in local cache
    :return: None
    """
    try:
        updated_price_list = DummyApi.get_updated_price_list()
        if updated_price_list is not None:
            with open('Cache/pricelist.pkl', 'wb') as out_file:
                pickle.dump(updated_price_list, out_file)
    except Exception as e:
        CustomLogging.log_error(e)


def get_updated_offers() -> Optional:
    """
    Fetches updated valid offers from a micro service and stores in local cache

    :return: list of offers
    """
    try:
        offers = DummyApi.get_updated_offers()
        if offers is not None:
            with open('Cache/offers.pkl', 'wb') as out_file:
                pickle.dump(offers, out_file)
                return offers

    except Exception as e:
        CustomLogging.log_error(e)
        return None


def get_cart_products() -> Optional[tuple]:
    """
    Fetches cart products from local cache
    :return: tuple of Products if list is not empty else return None
    """
    with open('Cache/cartProducts.pkl', 'rb') as in_file:
        try:
            products = tuple(pickle.load(in_file))
            return products
        except Exception as e:
            CustomLogging.log_error(e)
            return None


def display_inventory() -> None:
    """
    Displays inventory to the user on console
    :return: None
    """
    try:
        cart_products = get_cart_products()
        if cart_products is not None:
            print("Available Items:")
            for product in cart_products:
                if product.price < 0:
                    print(f"{product.product_description} - {product.price}p per {product.product_unit}")
                else:
                    print(f"{product.product_description} - £{product.price} per {product.product_unit}")

        offers = get_updated_offers()
        if offers is not None:
            print()
            print("Available offers:")
            for offer in offers:
                print(offer.offer_description)
            print()
    except Exception as e:
        CustomLogging.log_error(e)


def get_basket_to_price() -> None:
    """
    Asks users to input products in their basket to be priced and send baskets to be priced
    and then display output to the users
    :return:None
    """
    while True:
        text = input("Please enter the basket to price as PriceBasket item1 item2 etc or q to quit:")
        if text in ['q']:
            break
        else:
            input_list = text.lower().split()

            if len(input_list) > 0 and input_list[0] in ['pricebasket']:
                # used array as in future new commands can also be added
                # Could be replaced by Command Design Pattern in future

                basket_products_list = BasketState.get_products_in_basket_state(input_list[1:])
                sub_total, total, discounted_items = PriceBasket().price_basket(basket_products_list)
                PriceBasketResultDisplay(sub_total, discounted_items, total).display_result()
            else:
                print("Please enter valid input")
    print("Thank you")


if __name__ == '__main__':
    exit(main())
