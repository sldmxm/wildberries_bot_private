import logging
import logging.config
import logging.handlers

from bot.core.settings import settings
from bot.error_handler import error_handler # noqa
from tgbot.settings import BASE_DIR

LOG_PATH = BASE_DIR / '.data' / 'logs'
LOG_PATH.mkdir(parents=True, exist_ok=True)
LOG_FILENAME = LOG_PATH / settings.log_filename


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILENAME,
            'when': 'D',
            'interval': 1,
            'backupCount': 60,
            'formatter': 'default_formatter',
            'encoding': 'utf-8'
        },
        'console_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'stream': 'ext://sys.stdout'
        },
        'error_handler': {
            'class': 'logging.NullHandler'  # Используем NullHandler для игнорирования логирования ошибок по умолчанию
        },
    },
    'loggers': {
        '': {
            'handlers': ['file_handler', 'console_handler', 'error_handler'],
            'level': settings.log_level,
            'propagate': True
        }
    },
    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s, %(levelname)s, %(name)s, %(message)s'
        }
    }
}

logging.config.dictConfig(LOGGING)

logger = logging.getLogger('tgbot')
