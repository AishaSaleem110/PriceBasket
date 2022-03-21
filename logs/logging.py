import logging
from logging.handlers import TimedRotatingFileHandler


class CustomLogging:
    """
       This class is used for configuring details regarding logging in the project.
       It can be extended/modified in future without making in other classes.
       In improves cohesiveness, code reusability and code maintainability.

       Currently, it creates a date appended file for each day to maintain day wise logs
    """
    def __init__(self):
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)
        log_level = 10
        handler = TimedRotatingFileHandler("logs/app.log", when="midnight", interval=1)
        handler.suffix = "%Y%m%d"
        handler.setLevel(log_level)
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)

    @staticmethod
    def log_error(e: Exception):
        logging.exception("Exception occured")
