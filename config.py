class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    UPLOAD_PATH= r"/app/CS_Project/upload"
    RSA_PATH= r"/app/CS_Project/rsa_files"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    
    PRIVATE_KEY={
        "userid":"private key"
    }
    PUBLIC_KEY={
        "userid":"public key"
    }


class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    


class TestingConfig(Config):
    TESTING = True