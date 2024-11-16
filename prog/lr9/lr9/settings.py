import os

# Подключение к базе данных PostgreSQL
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5438/bonus_program_db?sslmode=disable')  # URI для подключения
SQLALCHEMY_TRACK_MODIFICATIONS = False  

# Конфигурация JWT для аутентификации
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  
ALGORITHM = 'HS256'  
ACCESS_TOKEN_EXPIRE_MINUTES = 60  

BONUS_TIERS = {
    'silver': {'min_spend': 1000, 'cashback': 5},
    'gold': {'min_spend': 5000, 'cashback': 10},
    'platinum': {'min_spend': 10000, 'cashback': 15},
}

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'DELETE']

users = {
    'item_title': 'user',
    'schema': {
        'username': {'type': 'string', 'minlength': 3, 'maxlength': 50, 'unique': True, 'required': True},
        'password': {'type': 'string', 'minlength': 6, 'required': True},
        'total_spent': {'type': 'float', 'min': 0, 'default': 0.0},
        'bonus_level': {
            'type': 'string',
            'allowed': ['silver', 'gold', 'platinum'],
            'default': 'silver'
        },
        'cashback_percentage': {'type': 'float', 'default': 0.0},
    },
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'DELETE']
}


transactions = {
    'item_title': 'transaction',
    'schema': {
        'user_id': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'field': '_id',
                'embeddable': True
            },
            'required': True,
        },
        'amount': {'type': 'float', 'min': 0, 'required': True},
        'timestamp': {'type': 'datetime', 'default': 'now'},
    },
    'resource_methods': ['POST'],
}


DOMAIN = {
    'users': users,
    'transactions': transactions,
}


CORS_ORIGINS = [
    "http://localhost:3000",  # frontend maybe
]


ERRORS = {
    'invalid_token': {
        'message': 'Token is invalid or expired.',
        'status': 401,
        'payload': {'message': 'Invalid token'}
    },
    'forbidden': {
        'message': 'You are not authorized to access this resource.',
        'status': 403,
        'payload': {'message': 'Forbidden'}
    }
}

LOGGING = {
    'loggers': {
        'eve': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
}
