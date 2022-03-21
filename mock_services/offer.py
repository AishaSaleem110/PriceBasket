import datetime
import uuid
from typing import List

from rule_engine.condition_rule import ConditionRule


class Offer:
    """
      This class represents Offer entity in the system
      This is the base class which has been extended for the specific Offer types
      ...
      Attributes
      ----------
      _offer_id : uuid
          To represent a unique offer
      _offer_description : str
          Offer description to be shown to the users
      _product_id : uuid
         The product id on which this offer is applicable
      _date : tuple
        Collectively defines the start date and end date of the offer
      _active : bool
         To represent if offer is active, offer can be in the system but can be deactivated
      _offer_type : str
         To represent different types of offers
      """

    # slots are used for faster attribute access and space saving in memory resources
    __slots__ = ['_offer_id', '_offer_description', '_product_id', '_date', '_active', '_offer_type']

    def __init__(self,
                 offer_id: uuid,
                 offer_description: str,
                 product_id,
                 start_date: datetime,
                 end_date: datetime,
                 active: bool = False,
                 offer_type=None):
        self._offer_id = offer_id
        self._offer_description = offer_description
        self._product_id = product_id
        self._active = active
        self._date = (start_date, end_date)
        self._offer_type = offer_type

    @property
    def product_id(self):
        return self._product_id

    @property
    def offer_description(self):
        return self._offer_description

    @offer_description.setter
    def product_description(self, offer_description):
        self._offer_description = offer_description

    @property
    def offer_type(self):
        return self._offer_type

    def __repr__(self):
        return f"offer_id = {self._offer_id},"\
               f"offer_description = {self._offer_description}",\
               f"product_id = {self._product_id}," \
               f"date = {self._date}" \
               f"active = {self._active}"


# we need to add capability to apply flat promotion on product category as well
class OfferFlat(Offer):
    """
        This class represents Flat Offers entity in the system
        This is the sub class of Offer class
        ...
        Attributes
        ----------
        _discount_percent : float
            Flat discount available on the product
    """

    __slots__ = ['_discount_percent']

    def __init__(self,
                 offer_id: uuid,
                 offer_description:str,
                 product_id,
                 start_date: datetime,
                 end_date: datetime,
                 active: bool,
                 discount_percent: float):
        super().__init__(offer_id,offer_description, product_id, start_date, end_date, active, "OfferFlat")
        self._discount_percent = discount_percent

    @property
    def discount_percent(self):
        return self._discount_percent

    @staticmethod
    def offer_class() -> str:
        return "OfferFlat"

    def __repr__(self):
        return f" PromotionFlat {super().__str__()}," \
               f" '_discount_percent {self._discount_percent}'"


class OfferGroup(Offer):
    """
        This class represents Group Offers entity in the system

        This class handles cases when discounts are conditional
        Condition can be on a different product while if conditions are satisfied,
        discount can be given on a different product
        ...
        Attributes
        ----------
        _discounted_product_id : uuid
            Product id on which discounted will be given
        _discount_percent : float
            Discount in percentage available on the discounted product
        _conditions : ConditionRule
            List of conditions that needs to be satisfied for this discount to be eligible
    """
    __slots__ = ['_discounted_product_id', '_discount_percent', '_conditions']

    def __init__(self,
                 offer_id: uuid,
                 offer_description: str,
                 eligible_product_ids,
                 start_date: datetime,
                 end_date: datetime,
                 active: bool,
                 discounted_product_id: uuid,
                 discount_percent: float = 0.0,
                 conditions: List[ConditionRule] = []):
        super().__init__(offer_id,offer_description, eligible_product_ids, start_date, end_date, active, "OfferGroup")

        self._discounted_product_id = discounted_product_id
        self._discount_percent = discount_percent
        self._conditions = conditions

    @property
    def discount_percent(self):
        return self._discount_percent

    @property
    def conditions(self):
        return self._conditions

    @property
    def discounted_product_id(self):
        return self._discounted_product_id

    @staticmethod
    def offer_class() -> str:
        return "OfferGroup"

    def __repr__(self):
        return f" OfferGroup {super().__str__()} ," \
               f"_discounted_product_id {self._discounted_product_id} ," \
               f"_discount_percent {self._discount_percent} ," \
               f"_conditions {self._conditions}"
