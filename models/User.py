import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class User:
    def __init__ (self, name, email, password, phone, address, role, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.password = password
        self.role = role

    def setName(self, name=None):
        self.name = name

    def setEmail(self, email=None):
        self.email = email
    
    def setPhone(self, phone=None):
        self.phone = phone

    def setAddress(self, address=None):
        self.address = address

    def setPassword(self, password=None):
        self.password = password

    def setRole(self, role=None):
        self.role = role

    def getId(self):
        return self.id
    
    def getName(self):
        return self.name

    def getEmail(self):
        return self.email

    def getPhone(self):
        return self.phone

    def getAddress(self):
        return self.address

    def getPassword(self):
        return self.password

    def getRole(self):
        return self.role

    @staticmethod
    def getAllUsers(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user ORDER BY id')
        accounts = cursor.fetchall()

        return accounts
    
    @staticmethod
    def getUser(id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM user WHERE id = % s', (id, ))
        account = cursor.fetchone()

        return account
    
    @staticmethod
    def addUser(user, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('INSERT INTO user (name, email, password, phone, address, role) VALUES (% s, % s, % s, % s, % s, % s)', (user.getName(), user.getEmail(), user.getPassword(), user.getPhone(), user.getAddress(), user.getRole()))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateUser(user, user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('UPDATE user SET name = % s, email = % s, phone = % s, address = % s WHERE id = % s', (user.getName(), user.getEmail(), user.getPhone(), user.getAddress(), user_id))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteUser(user_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('DELETE FROM user WHERE id = % s', (user_id))
        mysql.connection.commit()
        
        return True

    @staticmethod
    def login(email, password, mysql):

        print(email)
        print(password)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        msg = ''

        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, )) 
        account = cursor.fetchone()
        
        if account:
            return {"id":account['id'], "role":account['role'], "email":account['email'], "name":account['name']}
        else:
            return None
    