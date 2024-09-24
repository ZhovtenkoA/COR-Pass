# import logging
# import sys
# from cor_pass.config.config import settings
# from logging.handlers import TimedRotatingFileHandler

# DEBUG = settings.debug

# logger = logging.getLogger(__name__)
# if DEBUG:
#     logger.setLevel(logging.DEBUG)
# else:
#     logger.setLevel(logging.INFO)


# def handle_exception(exc_type, exc_value, exc_traceback):
#     # Логирование информации об исключении
#     logger.error(
#         "An unhandled exception occurred", exc_info=(exc_type, exc_value, exc_traceback)
#     )


# # Регистрация обработчика исключений
# sys.excepthook = handle_exception


# file_handler = TimedRotatingFileHandler("logs.log", when="M", backupCount=7)
# file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s"))
# logger.addHandler(file_handler)


# stream_handler = logging.StreamHandler(sys.stdout)
# log_formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
# stream_handler.setFormatter(log_formatter)
# logger.addHandler(stream_handler)


from loguru import logger
import sys
from cor_pass.config.config import settings

# Настройка уровня логирования
logger_level = "DEBUG" if settings.debug else "INFO"

# Удаление стандартного обработчика
logger.remove()

# Добавление обработчика для логирования в файл
logger.add(
    "logs/application.log",  # Путь к файлу логов
    rotation="500 MB",       # Размер файла перед ротацией
    retention="10 days",     # Хранение логов в течение 10 дней
    compression="zip",       # Сжатие старых логов
    level=logger_level,      # Уровень логирования
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Добавление обработчика для вывода логов в консоль
logger.add(
    sys.stdout,              # Вывод в консоль
    level=logger_level,      # Уровень логирования
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Пример использования
logger.info("Loguru start working")  