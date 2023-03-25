import os
import datetime


class Config:
    try:
        MONGODB_SETTINGS = {
            'username': os.environ['MONGODB_USERNAME'],
            'password': os.environ['MONGODB_PASSWORD'],
            'db': os.environ['MONGODB_DATABASE'],
            'host': os.environ['MONGODB_HOST'],
            'authentication_source': 'admin'
        } if os.environ['CI'] not in ['True', 'true'] else {}
        JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=14)
    except KeyError:
        pass
