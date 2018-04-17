class BaseConfig(object):
    INDEX_PER_PAGE = 9
    SECRET_KEY = "000000"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:67119299Mj!@localhost:3306/jobplus?charset=utf8"


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
