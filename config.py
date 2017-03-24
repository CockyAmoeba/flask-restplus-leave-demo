class Config(object):
    """
    Common configurations
    """
    DEBUG = True
    PORT=8888


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}