import os
import sys
import logging
import logging.config


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
APP_NAME = 'peeringdb_agent'
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default_formatter': {
            #'format': '[%(levelname)s:%(asctime)s] %(message)s'
            'format': '%(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': f"{APP_NAME}.log",
            'mode': 'a',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        APP_NAME: {
            'handlers': ['stream_handler', 'file_handler'],
            'level': LOGLEVEL,
            'propagate': True
        }
    }
}

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
