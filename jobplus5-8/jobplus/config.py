class BaseConfig(object):
    INDEX_PER_PAGE = 9
    ADMIN_PER_PAGE = 15
    SECRET_KEY = "000000"
    ADMIN_REQUIRED = True
    COMPANY_REQUIRED = True
    LOGIN_DISABLED = False

    DEFAULT_PASSWORD = '********'



class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:67119299Mj!@localhost:3306/jobplus?charset=utf8"
    ADMIN_REQUIRED = False
    COMPANY_REQUIRED = False
    LOGIN_DISABLED = True


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    LOGIN_DISABLED = True
    pass


configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
