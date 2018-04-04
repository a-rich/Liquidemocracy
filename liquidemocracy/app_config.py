from datetime import timedelta

class DevelopmentConfig():
    DEBUG = True
    SERIALIZATION_KEY = "q!f='YUyK:|:;>`7"
    JWT_SECRET_KEY = ",o`qA#LI`*V_@+%C"
    JWT_EXPIRES = timedelta(days=365)
    MONGODB_SETTINGS = {
           "db": "heroku_x1mkjt4n",
           "username": "heroku_x1mkjt4n",
           "password": "i7mrai4vnkf2r7klr7m3adb0i0",
           "host": "ds121238.mlab.com",
           "port" "21238",
    }
