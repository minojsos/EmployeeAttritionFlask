import os
from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb

class Employee:
    def __init__(self, name, age, department, phone, email, address, distFromHome, education, gender, jobSatisfaction, maritalStatus, children, salary, numCompaniesWorked, overtime, performanceRating, standardHours, training, workLifeBalance, yearsAtCompany, yearsInCurrentRole, yearsSinceLastPromo, yearsWithCurSupervisor, absenteeism, recruitmentDate, employer, turnover=None, timetillturnover=None, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.age = age
        self.department = department
        self.distFromHome = distFromHome
        self.education = education
        self.gender = gender
        self.jobSatisfaction = jobSatisfaction
        self.maritalStatus = maritalStatus
        self.children = children
        self.salary = salary
        self.numCompaniesWorked = numCompaniesWorked
        self.overtime = overtime
        self.performanceRating = performanceRating
        self.standardHours = standardHours
        self.training = training
        self.workLifeBalance = workLifeBalance
        self.yearsAtCompany = yearsAtCompany
        self.yearsInCurrentRole = yearsInCurrentRole
        self.yearsSinceLastPromo = yearsSinceLastPromo
        self.yearsWithCurSupervisor = yearsWithCurSupervisor
        self.absenteeism = absenteeism
        self.recruitmentDate = recruitmentDate
        self.employer = employer 
        self.turnover = turnover
        self.timetillturnover = timetillturnover

    @staticmethod
    def getEmployee(id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE id = %s', (id, ))

        employee = cursor.fetchone()

        return employee
    
    @staticmethod
    def getAllEmployees(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee') 

        employees = cursor.fetchall()
        
        return employees

    @staticmethod
    def getEmployeesPerformers(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee ORDER BY performanceRating ASC LIMIT 5') 

        employees = cursor.fetchall()
        
        return employees

    @staticmethod
    def getEmployeesHighRisk(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM employee WHERE turnover > 0.7 AND performanceRating = 'A' ORDER BY performanceRating DESC LIMIT 5") 

        employees = cursor.fetchall()
        
        return employees

    @staticmethod
    def getEmployeesLowRisk(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE turnover < 0.4 AND performanceRating = "C" OR performanceRating = "D" ORDER BY turnover DESC LIMIT 5') 

        employees = cursor.fetchall()
        
        return employees

    @staticmethod
    def getEmployeesCount(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS count_emp FROM employee') 

        employees = cursor.fetchall()
        
        return employees

    @staticmethod
    def getEmployeesPerformance(performance, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS count FROM employee WHERE performanceRating = % s', (performance, )) 

        employees = cursor.fetchone()
                
        return employees

    @staticmethod
    def getEmployeesSatisfaction(satisfaction, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS count FROM employee WHERE jobSatisfaction = % s', (satisfaction, )) 

        employees = cursor.fetchone()
        
        return employees

    @staticmethod
    def getEmployeesManager(mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE manager = % s', (1,)) 

        employees = cursor.fetchall()
        
        return employees

    @staticmethod
    def searchEmployees(term, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE name LIKE % s', ("%"+term+"%", ))

        employees = cursor.fetchall()

        return employees

    @staticmethod
    def addEmployee(employee, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO employee (name, age, department, phone, email, address, distFromHome, education, gender, maritalStatus, children, salary, numCompaniesWorked, overtime, performanceRating, standardHours, training, workLifeBalance, yearsAtCompany, yearsCurrentRole, yearsSinceLastPromo, yearsCurrentSupe, absenteeismRate, recruitmentDate, jobSatisfaction, turnover, timetillturnover, employerId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
        (employee.name, employee.age, employee.department, employee.phone, employee.email, employee.address, employee.distFromHome, employee.education, employee.gender, employee.maritalStatus, employee.children, employee.salary, employee.numCompaniesWorked, employee.overtime, employee.performanceRating, employee.standardHours, employee.training, employee.workLifeBalance, employee.yearsAtCompany, employee.yearsInCurrentRole, employee.yearsSinceLastPromo, employee.yearsWithCurSupervisor, employee.absenteeism, employee.recruitmentDate, employee.jobSatisfaction, employee.turnover, employee.timetillturnover, employee.employer,))
        
        mysql.connection.commit()

        return True

    @staticmethod
    def deleteEmployee(employee, employee_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM employee WHERE id = % s', (employee_id))
        
        mysql.connection.commit()
        
        return True

    @staticmethod
    def updateEmployee(employee, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE employee SET name = % s WHERE id = % s')

        mysql.connection.commit()
        
        return True

    @staticmethod
    def assignEmployee(employee_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE employee SET manager = % s WHERE id = % s', (1, employee_id))

        mysql.connection.commit()

        return True

    @staticmethod
    def unassignEmployee(employee_id, mysql):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE employee SET manager = % s WHERE id = % s', (0, employee_id))

        mysql.connection.commit()

        return True