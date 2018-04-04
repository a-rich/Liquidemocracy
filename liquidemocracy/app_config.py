from datetime import timedelta

class DevelopmentConfig():
    DEBUG = True
    SERIALIZATION_KEY = "q!f='YUyK:|:;>`7"
    JWT_SECRET_KEY = ",o`qA#LI`*V_@+%C"
    JWT_EXPIRES = timedelta(days=365)
    MONGODB_SETTINGS = {
           "db": "liquidemocracy"
    }
