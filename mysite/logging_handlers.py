# website/logging_handlers.py
import logging
from logging.handlers import RotatingFileHandler

class CustomFileHandler(RotatingFileHandler):
    def emit(self, record):
        # Додаємо роздільник перед кожною новою помилкою
        separator = "\n----------------------\n\n\n"
        record.msg = separator + record.msg
        super().emit(record)