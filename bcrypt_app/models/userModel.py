from bcrypt_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('bcrypt_user_schema').query_db(query)

        users = []

        for user in results:
            users.append(cls(user))

        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (firstname, lastname, email, password, created_at, updated_at) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('bcrypt_user_schema').query_db(query, data)

    @classmethod
    def findUserByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('bcrypt_user_schema').query_db(query, data)

        user = None

        if results:
            # print(results)
            if len(results) > 0:
                user = cls(results[0])

        return user

    @classmethod
    def findUserById(cls, data):
        query = "SELECT * FROM users WHERE id = %(userId)s;"
        results = connectToMySQL('bcrypt_user_schema').query_db(query, data)

        user = None

        if results:
            # print(results)
            if len(results) > 0:
                user = cls(results[0])

        return user

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(userId)s"
        return connectToMySQL('bcrypt_user_schema').query_db(query, data)

    @staticmethod
    def validateRegister(user):
        is_valid = True

        email = user['email']

        if len(user['firstname']) < 3:
            flash('First name must be at least 3 characters long', 'register_error')
            is_valid = False

        if len(user['lastname']) < 3:
            flash('First name must be at least 3 characters long', 'register_error')
            is_valid = False

        if not EMAIL_REGEX.match(email):
            flash('Invalid email address!', 'register_error')
            is_valid = False

        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long', 'register_error')
            is_valid = False

        if user['password'] != user['password_confirmation']:
            flash('Password and confirmation do not match!', 'register_error')
            is_valid = False
        
        if User.findUserByEmail({'email': email}) != None:
            flash('Email address is already taken!', 'register_error')
            is_valid = False

        return is_valid

    @staticmethod
    def validateLogin(user):
        is_valid = True

        email = user['email']

        if not EMAIL_REGEX.match(email):
            flash('Invalid email address!', 'login_error')
            is_valid = False

        if User.findUserByEmail({'email': email}) == None:
            flash('Invalid Email / Password', 'login_error')
            is_valid = False
        
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long', 'login_error')
            is_valid = False

        return is_valid