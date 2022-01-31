from bcrypt_app import app
from bcrypt_app.controllers import usersController

if __name__ == '__main__':
    app.run( debug = True, port = 8091 )