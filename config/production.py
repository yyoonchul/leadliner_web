from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'leadliner.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b':\x0e\xba\x86\x8b\xed\xe7dc\xe2\x16\xef\xbd+\n='