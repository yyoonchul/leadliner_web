import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'leadliner.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "rhaudwls2002"