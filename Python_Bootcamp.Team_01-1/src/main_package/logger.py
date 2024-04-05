import logging


"""
The module contains some logging settings, as well as additional functions.
"""


formatter = logging.Formatter('[LOG] %(levelname)8s: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.CRITICAL)


def logging_messages(func):
    """
    The decorator logs the string value returned by the function or a list of strings.
    """

    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if isinstance(result, list):
            for msg in result:
                logging.info(msg)
        elif isinstance(result, str):
            logging.info(result)
        return result
    return wrapper
