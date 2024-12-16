# pypro/module1.py
import logging

logger = logging.getLogger(__name__)


def example_function():
    logger.debug("This is a debug message from module1")
    logger.info("This is an info message from module1")
