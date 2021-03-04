import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Department:
    def __init__(self, name, id=None, createdOn=None, updatedOn=None):
        self.id = id
        self.name = name
        self.createdOn =createdOn

    def setName(self, name):
        self.name = name

    def setCreatedOn(self, createdOn):
        self.createdOn = createdOn

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getCreatedOn(self):
        return self.createdOn

    @staticmethod
    def getDepartment(department_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM department WHERE id = %s', (department_id, ))

        department = cursor.fetchone()

        return department

    @staticmethod
    def getAllDepartments(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM department')

        departments = cursor.fetchall()

        return departments
    
    @staticmethod
    def addDepartment(department, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO department VALUES(NULL, % s)', (department.getName()))

        mysql.connection.commit()

        return True

    @staticmethod
    def updateDepartment(department, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE department SET name = % s WHERE id = % s', (department.getName(), department.getId()))

        mysql.connection.commit()
        
        return True
    
    @staticmethod
    def deleteDepartment(department_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM department WHERE id = % s', (department_id))

        mysql.connection.commit()
        
        return True