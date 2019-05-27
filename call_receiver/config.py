class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://call_receiver:call_receiver123@localhost:5432/call_receiver_db' # NOQA


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
