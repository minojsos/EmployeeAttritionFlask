import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Dataset:
    def __init__(self, name, purpose, user, dataFile=None, id=None, uploadedOn=None):
        self.id = id
        self.name = name
        self.dataFile = dataFile
        self.purpose = purpose
        self.uploadedOn = uploadedOn
        self.user = user

    def setName(self, name):
        self.name = name
    
    def setDataFile(self, dataFile):
        self.dataFile = dataFile

    def setPurpose(self, purpose):
        self.purpose = purpose

    def setUploadedOn(self, uploadedOn):
        self.uploadedOn = uploadedOn

    def setUser(self, user):
        self.user = user

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getDataFile(self):
        return self.dataFile

    def getPurpose(self):
        return self.purpose

    def getUploadedOn(self):
        return self.uploadedOn

    def getUser(self):
        return self.user

    @staticmethod
    def getDataset(dataset_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dataset WHERE id = %s', (dataset_id, ))

        dataset = cursor.fetchone()

        return dataset

    @staticmethod
    def getAllDatasets(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM dataset')

        datasets = cursor.fetchall()

        return datasets
    
    @staticmethod
    def addDataset(dataset, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO dataset VALUES (NULL, % s, % s, % s, % s)', (dataset.getName(), dataset.getDataFile(), dataset.getPurpose(), dataset.getUser(), ))

        mysql.connection.commit()

        return True

    @staticmethod
    def updateDataset(dataset, dataset_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursor.DictCursor)
        cursor.execute('UPDATE dataset SET name = % s, purpose = % s WHERE id = % s', (dataset.getName(), dataset.getPurpose(), dataset.getId(), ))

        mysql.connection.commit()

        return True

    @staticmethod
    def deleteDataset(dataset_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursor.DictCursor)
        cursor.execute('DELETE FROM dataset WHERE id = % s', (dataset_id, ))

        mysql.connection.commit()
        
        return True