from logs.logging import CustomLogging


class CurrencyUtilityMethods:
    """
    This class contains all utility methods for the currency related calculations and formatting
    """

    @staticmethod
    def percentage(percent, whole) -> float:
        try:
            return (percent * whole) / 100.0
        except Exception as e:
            CustomLogging.log_error(e)
            return 0.0

    @staticmethod
    def format_decimal_currency(currency_in_decimal: float) -> int:
        try:
            return int(currency_in_decimal * 100)
        except Exception as e:
            CustomLogging.log_error(e)
            return 0

    @staticmethod
    def get_currency_with_unit(currency: float) -> str:
        try:
            if currency < 1:
                return format(CurrencyUtilityMethods.format_decimal_currency(currency)) + "p"
            else:
                return "£" + "{:.2f}".format(currency)
        except Exception as e:
            CustomLogging.log_error(e)
            return ""

    @staticmethod
    def get_two_decimal_formatted_string(value) -> str:
        try:
            return "{:.2f}".format(value)
        except Exception as e:
            CustomLogging.log_error(e)
            return ""