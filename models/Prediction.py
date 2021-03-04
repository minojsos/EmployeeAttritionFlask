import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Prediction:
    def __init__(self, id, employee):
        self.id = id
        self.employee = employee

    def setEmployee(self, employee):
        self.employee

    def getId(self):
        return self.id

    def getEmployee(self):
        return self.employee

    @staticmethod
    def getPrediction(id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM prediction WHERE id = %s', (id, ))

        prediction = cursor.fetchone()

        return prediction
    
    @staticmethod
    def getPredictionByEmployee(employee_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM prediction WHERE employee_id = % s ORDER BY id', (employee_id, ))

        predictions = cursor.fetchall()

        return predictions
    
    @staticmethod
    def getAllPredictions(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM prediction ORDER BY id')

        predictions = cursor.fetchall()

        return predictions
    
    @staticmethod
    def addPrediction(prediction, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO prediction VALUES (NULL, % s, % s, % s)', (prediction[''], prediction[''], prediction['']))
        
        mysql.connection.commit()

        return True

    @staticmethod
    def updatePrediction(prediction, prediction_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE prediction SET name = % s WHERE id = % s', (prediction[''], prediction_id))

        mysql.connection.commit()

        return True

    @staticmethod
    def deletePrediction(prediction_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM prediction WHERE id = % s', (prediction_id))

        mysql.connection.commit()
        
        return True