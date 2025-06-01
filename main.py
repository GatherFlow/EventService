
from app import start_app

from app.logger import setup_logger
from config import get_settings


def main():
    settings = get_settings()

    setup_logger(settings.logger.path, settings.logger.level)
    start_app()


if __name__ == '__main__':
    main()
