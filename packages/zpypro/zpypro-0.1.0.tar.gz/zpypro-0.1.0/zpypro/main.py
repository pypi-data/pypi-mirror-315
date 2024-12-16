# zpypro/main.py
import logging.config
import yaml
from zpypro.module1 import example_function


def setup_logging():
    """Set up logging using a YAML configuration file."""
    with open("zpypro/logging_config.yaml", "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)


def main():
    """Main entry point of the application."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application started")
    example_function()


if __name__ == "__main__":
    main()
