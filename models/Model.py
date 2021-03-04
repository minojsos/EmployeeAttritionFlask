import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Model:
    def __init__(self, name, dataset, id=None, createdOn=None):
        self.id = id
        self.name = name
        self.createdOn =createdOn
        self.dataset = dataset

    def setName(self, name):
        self.name = name

    def setCreatedOn(self, createdOn):
        self.createdOn = createdOn

    def setDataset(self, dataset):
        self.dataset = dataset

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getCreatedOn(self):
        return self.createdOn

    def getDataset(self):
        return self.dataset

    @staticmethod
    def getModel(id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM model WHERE id = %s', (id, ))

        model = cursor.fetchone()

        return model

    @staticmethod
    def getAllModels(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM model ORDER BY id')

        models = cursor.fetchall()

        return models
    
    @staticmethod
    def addModel(model, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO model VALUES(NULL, % s, % s, % s)', (model['']. model[''], model['']))
        mysql.connection.commit()

        return True

    @staticmethod
    def updateModel(model, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE model SET name = % s WHERE id = % s', (model.getName(), model.getid()))
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteModel(model_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM model WHERE id = %s', (model_id, ))
        mysql.connection.commit()
        
        return True