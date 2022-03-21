from enum import Enum


class CustomOperator(Enum):

    """
    This class represents operators used in the logical representation of Offers
    Only simple operators have been represented here but it can be extended easily
    """
    Equal = "Equal"
    EqualOrGreater = "EqualOrGreater"
