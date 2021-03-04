import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Preference:
    def __init__(self, model_id, id=None, createdOn=None, upatedOn=None):
        self.id =id
        self.model_id =model_id
        self.createdOn =createdOn
        self.updatedOn =updatedOn

    def setModel(self, model):
        self.model = model

    def setCreatedOn(self, createdOn):
        self.createdOn = createdOn

    def setUpdatedOn(self, updatedOn):
        self.updatedOn = updatedOn

    def getModel(self):
        return self.model

    def getCreatedOn(self):
        return self.createdOn

    def getUpdatedOn(self):
        return self.updatedOn

    @staticmethod
    def getPreference(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM preference WHERE id = %s', (1, ))

        department = cursor.fetchone()

        return department

    @staticmethod
    def updatePreference(model_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE preference SET model_id = % s WHERE id = % s', (model_id, 1))

        mysql.connection.commit()
        
        return True