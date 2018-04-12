class BaseConfig(object):

    SECRET_KEY = '000000'


class DevelopmentConfig(BaseConfig):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost:3306/simpledu?charset=utf8'


class ProductionConfig(BaseConfig):

    pass


class TestingConfig(BaseConfig):

    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

