import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Get SECRET_Key
    JWT_SECRET_KEY =  os.environ.get("SECRET_KEY")
    JSON_SORT_KEYS=False
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Get DATABASE_URL
        URL = os.environ.get("DATABASE_URL")

        if not URL:
            raise ValueError("Please set DATABASE_URL")

        return URL

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    pass

environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
elif environment == "development":
    app_config = DevelopmentConfig()