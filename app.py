from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from models.User import User
from models.User import User
from models.Employee import Employee
from models.Model import Model
from models.Prediction import Prediction
from models.Dataset import Dataset
from models.Preference import Preference
from models.Department import Department
from flask import request
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import (accuracy_score, log_loss, classification_report)
import pickle
from sklearn.svm import SVR
import lime

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'qUIMVsVzyj'
app.config['MYSQL_PASSWORD'] = '4iAXz7Ifmq'
app.config['MYSQL_DB'] = 'qUIMVsVzyj'
  
mysql = MySQL(app)

CORS(app)

TURNOVER_MODEL = 'ml/xgb_turnover.bin'
TIMETILLTURNOVER_MODEL = 'ml/svr_model.sav'

@app.route('/', methods=['GET'])
@cross_origin(origin='*')
def index():
    endpoints = {
        'User':
        {
            "Login":"http://localhost:5000/login POST (email, password)",
            "Add New User":"http://localhost:5000/user POST (name, email, password, role)",
            "Update User":"http://localhost:5000/user/(userId) POST (name, email, role)"
        },
        'Employees':
        {
            "Get All Employees":"http://localhost:5000/employees GET",
            "Get a Employee":"http://localhost:5000/employee/(employeeId) GET",
            "Add Employee":"http://localhost:5000/employee POST (..)",
            "Update Employee":"http://localhost:5000/employee/(employeeId) PUT (..)",
            "Delete Employee":"http://localhost:5000/employee/(employeeId) DELETE",
        },
        'Departments':
        {
            "Get All Departments":"http://localhost:5000/departments GET",
            "Get a Department":"http://localhost:5000/department/(departmentId) GET",
            "Add Department":"http://localhost:5000/department POST (name)",
            "Update Department":"http://localhost:5000/department/(departmentId) PUT (name)",
            "Delete Department":"http://localhost:5000/department/(departmentId) DELETE",
        },
        'Datasets':
        {
            "Get All Datasets":"http://localhost:5000/datasets GET",
            "Get a Dataset":"http://localhost:5000/dataset/(datasetId) GET",
            "Add Dataset":"http://localhost:5000/dataset POST (name, purpose, user, datafile)",
            "Update Dataset":"http://localhost:5000/dataset/(datasetId) PUT (name, purpose, user, datafile)",
            "Delete Dataset":"http://localhost:5000/dataset/(datasetId) DELETE",
        },
        'Models':
        {
            "Get All Models":"http://localhost:5000/models GET",
            "Get a Model":"http://localhost:5000/model/(datasetId) GET",
            "Add Model":"http://localhost:5000/model POST (name, dataset)",
            "Update Model":"http://localhost:5000/model/(datasetId) PUT (name, dataset)",
            "Delete Model":"http://localhost:5000/model/(datasetId) DELETE",
        },
        'Preferences':
        {
            "Get All Preferences":"http://localhost:5000/preference GET",
            "Update Preference":"http://localhost:5000/preference/(preferenceId) PUT (model_id)"
        }
    }

    return jsonify({'endpoints':endpoints})
'''
This Function is to allow the user to login to the application.
The email and password are obtained from the user and checked against the database.
Their user role is also obtained from the database to ensure that the views shown to them are only based on their User Role.
0 => HR Personnel
1 => Manager
2 => IT Manager
'''
@app.route('/login', methods=['POST'])
@cross_origin(origin='*')
def login():
    # Read the Login Credentials
    data = request.json
    
    result = User.login(data['email'],data['password'], mysql)

    if (result == None):
        return jsonify({"result": False, "msg": "Incorrect Username or Password"})
    
    return jsonify({"result": True, "id": result, "msg": "Logged in Successfully!"})

'''

'''
@app.route('/users', methods=['GET'])
@cross_origin(origin='*')
def getAllUsers():
    return jsonify({"users": User.getAllUsers(mysql)})

'''

'''
@app.route('/user/<int:user_id>', methods=['GET'])
@cross_origin(origin='*')
def getUser(user_id):
    user = User.getUser(user_id, mysql)

    if (user == None):
        return jsonify({"user":None,"msg":"User Not Found!"})

    return jsonify({"user": user, "msg": "User Found Successfully!"})

'''
Add New User Given their Details. This can only be accessed by an HR Manager Only.
IT Managers and HR Employees cannot access this data.
'''
@app.route('/user', methods=['POST'])
@cross_origin(origin='*')
def addUser():
    if not request.json or not 'name' in request.json:
        return jsonify({"result":False, "msg":"Failed to Add User!"})
    
    user = User(request.json['name'], request.json['email'], request.json['password'], request.json['phone'], request.json['address'], request.json['role'])
    
    result = User.addUser(user, mysql)

    return jsonify({"result": True, "msg":"Successfully Added User!"})

"""
====================================================
                EMPLOYEE API FUNCTIONS
====================================================
The following section contains the API functions for Employee functionality.
"""
'''
This Function is to retrieve all the employees in the database. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/employees', methods=['GET'])
@cross_origin(origin='*')
def getAllEmployees():
    # Retrieve all the Employees from the Database
    return jsonify({"employees": Employee.getAllEmployees(mysql)})


'''
This Function is to retrieve an Individual Employee given the ID of the Employee. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/employee/<int:employee_id>', methods=['GET'])
@cross_origin(origin='*')
def getEmployee(employee_id):
    employee = Employee.getEmployee(employee_id, mysql)
    
    if (employee == None):
        return jsonify({"employee": None, "msg": "Employee Not Found!"})
    
    return jsonify({"employee": employee, "msg": "Employee Found Successfully!"})

'''
This Function is to retrieve all High Performing Employees. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/employees/performers', methods=['GET'])
@cross_origin(origin='*')
def getAllEmployeesPerformers():
    # Retrieve all the Employees from the Database
    return jsonify({"employees": Employee.getEmployeesPerformers(mysql)})

'''
This Function is to retrieve all High Risk Employees. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/employees/risk/high', methods=['GET'])
@cross_origin(origin='*')
def getAllEmployeesHighRisk():
    # Retrieve all the Employees from the Database
    return jsonify({"employees": Employee.getEmployeesHighRisk(mysql)})

'''
This Function is to retrieve all Low Risk Employees. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/employees/risk/low', methods=['GET'])
@cross_origin(origin='*')
def getAllEmployeesLowRisk():
    # Retrieve all the Employees from the Database
    return jsonify({"employees": Employee.getEmployeesLowRisk(mysql)})

'''
This Function is to retrieve the number of Employees. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/employees/count', methods=['GET'])
@cross_origin(origin='*')
def getEmployeesCount():
    # Retrieve all the Employees from the Database
    return jsonify({"employees": Employee.getEmployeesCount(mysql)})

@app.route('/employees/performance', methods=['GET'])
@cross_origin(origin='*')
def getEmployeesPerformance():
    # Retrieve all the Employees from the Database
    employees_A = Employee.getEmployeesPerformance('A', mysql)
    employees_B = Employee.getEmployeesPerformance('B', mysql)
    employees_C = Employee.getEmployeesPerformance('C', mysql)
    employees_D = Employee.getEmployeesPerformance('D', mysql)
    print(employees_D)

    return jsonify({"A":employees_A, "B":employees_B, "C":employees_C, "D":employees_D})

@app.route('/employees/satisfaction', methods=['GET'])
@cross_origin(origin='*')
def getEmployeesSatisfaction():
    # Retrieve all the Employees from the Database
    employees_1 = Employee.getEmployeesSatisfaction(1, mysql)
    employees_2 = Employee.getEmployeesSatisfaction(2, mysql)
    employees_3 = Employee.getEmployeesSatisfaction(3, mysql)
    employees_4 = Employee.getEmployeesSatisfaction(4, mysql)

    return jsonify({"A": employees_1, "B": employees_2, "C": employees_3, "D": employees_4,})

@app.route('/employees/manager', methods=['GET'])
@cross_origin(origin='*')
def getEmployeesManager():
    # Retrieve all the Employees from the Database
    return jsonify({"employees": Employee.getEmployeesManager(mysql)})


@app.route('/search/<query>', methods=['GET'])
@cross_origin(origin='*')
def search(query):
    # Retrieve all the Employees from the Database
    return jsonify({"employees": Employee.searchEmployees(query,mysql)})

'''
Add New Employee Given their Details. This can only be accessed by an HR Employee Only.
IT Managers and Managers cannot access this data.
'''
@app.route('/employee', methods=['POST'])
@cross_origin(origin='*')
def addEmployee():
    if not request.json or not 'name' in request.json:
        return jsonify({"result":False, "msg":"Failed to Add Employee!"})
    
    # Get Prediction for the Employee Turnover - Create Dataframe
    df = pd.DataFrame()
    print(request.json)

    df['Age'] = [request.json['age']]
    df['DistanceFromHome'] = [request.json['distFromHome']]
    df['Children'] = [request.json['children']]
    df['Num CompaniesWorked'] = [request.json['numCompaniesWorked']]
    df['Training '] = [request.json['trainingHours']]
    df['Years At Company'] = [request.json['yearsAtCompany']]
    df['Years In Current Role'] = [request.json['yearsInCurrentRole']]
    df['YearsSinceLastPromotion'] = [request.json['yearsSinceLastPromo']]
    df['YearsWithCurSupervisor'] = [request.json['yearsWithCurrSupervisor']]
    df['StandardHours'] = [request.json['standardHours']]
    
    if (request.json['department'] == '1'):
        df['Department_Cutting'] = [1]
        df['Department_Pressing'] = [0]
        df['Department_Sewing'] = [0]
    if (request.json['department'] == '2'):
        df['Department_Cutting'] = [0]
        df['Department_Pressing'] = [1]
        df['Department_Sewing'] = [0]
    if (request.json['department'] == '3'):
        df['Department_Cutting'] = [0]
        df['Department_Pressing'] = [0]
        df['Department_Sewing'] = [1]
    
    if (request.json['gender'] == '1'):
        df['Gender_Female'] = [1]
        df['Gender_Male'] = [0]
    if (request.json['gender'] == '2'):
        df['Gender_Female'] = [0]
        df['Gender_Male'] = [1]
    
    if (request.json['jobSatisfaction'] == '1'):
        df['Job_Satisfaction_1'] = [1]
        df['Job_Satisfaction_2'] = [0]
        df['Job_Satisfaction_3'] = [0]
        df['Job_Satisfaction_4'] = [0]
    if (request.json['jobSatisfaction'] == '2'):
        df['Job_Satisfaction_1'] = [0]
        df['Job_Satisfaction_2'] = [1]
        df['Job_Satisfaction_3'] = [0]
        df['Job_Satisfaction_4'] = [0]
    if (request.json['jobSatisfaction'] == '3'):
        df['Job_Satisfaction_1'] = [0]
        df['Job_Satisfaction_2'] = [0]
        df['Job_Satisfaction_3'] = [1]
        df['Job_Satisfaction_4'] = [0]
    if (request.json['jobSatisfaction'] == '4'):
        df['Job_Satisfaction_1'] = [0]
        df['Job_Satisfaction_2'] = [0]
        df['Job_Satisfaction_3'] = [0]
        df['Job_Satisfaction_4'] = [1]
    
    if (request.json['maritalStatus'] == '0'):
        df['Martial_Status_Single'] = [1]
        df['Martial_Status_Married'] = [0]
        df['Martial_Status_Divorced'] = [0]
    if (request.json['maritalStatus'] == '1'):
        df['Martial_Status_Single'] = [0]
        df['Martial_Status_Married'] = [1]
        df['Martial_Status_Divorced'] = [0]
    if (request.json['maritalStatus'] == '2'):
        df['Martial_Status_Single'] = [0]
        df['Martial_Status_Married'] = [0]
        df['Martial_Status_Divorced'] = [1]
    
    if (request.json['salary'] == '0'):
        df['Salary_Low'] = [1]
        df['Salary_Average'] = [0]
        df['Salary_High'] = [0]
    if (request.json['salary'] == '1'):
        df['Salary_Low'] = [0]
        df['Salary_Average'] = [1]
        df['Salary_High'] = [0]
    if (request.json['salary'] == '2'):
        df['Salary_Low'] = [0]
        df['Salary_Average'] = [0]
        df['Salary_High'] = [1]

    if (request.json['overtime'] == '0'):
        df['OverTime_No'] = [1]
        df['OverTime_Yes'] = [0]
    if (request.json['overtime'] == '1'):
        df['OverTime_No'] = [0]
        df['OverTime_Yes'] = [1]

    if (request.json['absenteeism'] == '0'):
        df['Absenteeism Rate_Low'] = [1]
        df['Absenteeism Rate_Medium'] = [0]
        df['Absenteeism Rate_High'] = [0]
    if (request.json['absenteeism'] == '1'):
        df['Absenteeism Rate_Low'] = [0]
        df['Absenteeism Rate_Medium'] = [1]
        df['Absenteeism Rate_High'] = [0]
    if (request.json['absenteeism'] == '2'):
        df['Absenteeism Rate_Low'] = [0]
        df['Absenteeism Rate_Medium'] = [0]
        df['Absenteeism Rate_High'] = [1]

    if (request.json['performanceRating'] == 'A'):
        df['PerformanceRating_A'] = [1]
        df['PerformanceRating_B'] = [0]
        df['PerformanceRating_C'] = [0]
        df['PerformanceRating_D'] = [0]
    if (request.json['performanceRating'] == 'B'):
        df['PerformanceRating_A'] = [0]
        df['PerformanceRating_B'] = [1]
        df['PerformanceRating_C'] = [0]
        df['PerformanceRating_D'] = [0]
    if (request.json['performanceRating'] == 'C'):
        df['PerformanceRating_A'] = [0]
        df['PerformanceRating_B'] = [0]
        df['PerformanceRating_C'] = [1]
        df['PerformanceRating_D'] = [0]
    if (request.json['performanceRating'] == 'D'):
        df['PerformanceRating_A'] = [0]
        df['PerformanceRating_B'] = [0]
        df['PerformanceRating_C'] = [0]
        df['PerformanceRating_D'] = [1]
    
    if (request.json['education'] == '1'):
        df['Education_1'] = [1]
        df['Education_2'] = [0]
        df['Education_3'] = [0]
        df['Education_4'] = [0]
    if (request.json['education'] == '2'):
        df['Education_1'] = [0]
        df['Education_2'] = [1]
        df['Education_3'] = [0]
        df['Education_4'] = [0]
    if (request.json['education'] == '3'):
        df['Education_1'] = [0]
        df['Education_2'] = [0]
        df['Education_3'] = [1]
        df['Education_4'] = [0]
    if (request.json['education'] == '4'):
        df['Education_1'] = [0]
        df['Education_2'] = [0]
        df['Education_3'] = [0]
        df['Education_4'] = [1]
    
    if (request.json['workLifeBalance'] == '1'):
        df['Work Life Balance_1'] = [1]
        df['Work Life Balance_2'] = [0]
        df['Work Life Balance_3'] = [0]
        df['Work Life Balance_4'] = [0]
    if (request.json['workLifeBalance'] == '2'):
        df['Work Life Balance_1'] = [0]
        df['Work Life Balance_2'] = [1]
        df['Work Life Balance_3'] = [0]
        df['Work Life Balance_4'] = [0]
    if (request.json['workLifeBalance'] == '3'):
        df['Work Life Balance_1'] = [0]
        df['Work Life Balance_2'] = [0]
        df['Work Life Balance_3'] = [1]
        df['Work Life Balance_4'] = [0]
    if (request.json['workLifeBalance'] == '4'):
        df['Work Life Balance_1'] = [0]
        df['Work Life Balance_2'] = [0]
        df['Work Life Balance_3'] = [0]
        df['Work Life Balance_4'] = [1]
    
    # Load the XGBoost Model
    param_dist = {'objective':'binary:logistic', 'n_estimators':180, 'eta':0.1, 'gamma': 0.05, 'max_depth': 3}

    clf = xgb.XGBModel(**param_dist)
    clf.load_model(TURNOVER_MODEL)

    # Predict Turnover from the XGBoost Model
    prediction = clf.predict(df.to_numpy())
    print(prediction)

    # Get Turnover Drivers
    # explainer = lime.lime_tabular(df.to_numpy(), feature_names=df.columns, class_names=[0,1], kernel_width=3)
    
    # Load the SVR Model
    svr = pickle.load(open(TIMETILLTURNOVER_MODEL, 'rb'))

    # Predict Time Till Turnover
    timetillturnover = svr.predict(df.to_numpy())[0]

    employee = Employee(request.json['name'], request.json['age'], request.json['department'], request.json['phone'], request.json['email'], request.json['address'], request.json['distFromHome'], request.json['education'], 
                        request.json['gender'], request.json['jobSatisfaction'], request.json['maritalStatus'], request.json['children'], request.json['salary'], request.json['numCompaniesWorked'], request.json['overtime'], 
                        request.json['performanceRating'], request.json['standardHours'], request.json['trainingHours'], request.json['workLifeBalance'], request.json['yearsAtCompany'], request.json['yearsInCurrentRole'], 
                        request.json['yearsSinceLastPromo'], request.json['yearsWithCurrSupervisor'], request.json['absenteeism'], request.json['recruitmentDate'], request.json['loggedInId'], turnover=prediction[0], timetillturnover=timetillturnover)

    result = Employee.addEmployee(employee, mysql)

    return jsonify({"result": True, "msg":"Successfully Added Employee!"})

'''
Update an Existing Employee Given their updated details. This can only be accessed by an HR Employee.
IT Managers and Managers cannot access this data.
'''
@app.route('/employee/<int:employee_id>', methods=['PUT'])
@cross_origin(origin='*')
def updateEmployee(employee_id):
    employee = Employee(request.json['name'], request.json['age'], request.json['department'], request.json['phone'], request.json['email'], request.json['address'], request.json['distFromHome'], request.json['education'], 
                        request.json['gender'], request.json['jobSatisfaction'], request.json['maritalStatus'], request.json['children'], request.json['salary'], request.json['numCompaniesWorked'], request.json['overtime'], 
                        request.json['performanceRating'], request.json['standardHours'], request.json['trainingHours'], request.json['workLifeBalance'], request.json['yearsAtCompany'], request.json['yearsInCurrentRole'], 
                        request.json['yearsSinceLastPromo'], request.json['yearsWithCurrSupervisor'], request.json['absenteeism'], request.json['recruitmentDate'])
    result = Employee.updateEmployee(employee_id, employee, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Updated Employee!"})
    
    return jsonify({"result":False, "msg":"Failed to Update Employee!"})

@app.route('/employee/assign/<int:employee_id>', methods=['PUT'])
@cross_origin(origin='*')
def assignEmployee(employee_id):
    result = Employee.assignEmployee(employee_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Assigned Employee!"})

    return jsonify({"result":False, "msg":"Failed to Assign Employee!"})

@app.route('/employee/unassign/<int:employee_id>', methods=['PUT'])
@cross_origin(origin='*')
def unassignEmployee(employee_id):
    result = Employee.unassignEmployee(employee_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Assigned Employee!"})

    return jsonify({"result":False, "msg":"Failed to Assign Employee!"})

'''
Delete an Existing Employee given their ID. This can only be accessed by an HR Employee.
IT Managers and Managers cannot access this data.
'''
@app.route('/employee/<int:employee_id>', methods=['DELETE'])
@cross_origin(origin='*')
def deleteEmployee(employee_id):
    result = Employee.deleteEmployee(employee_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Deleted Employee!"})

    return jsonify({"result":False, "msg":"Failed to Delete Employee!"})

"""
====================================================
              DEPARTMENT API FUNCTIONS
====================================================
The following section contains the API functions for Department functionality.
"""
'''
This Function is to retrieve all the departments in the database. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/departments', methods=['GET'])
@cross_origin(origin='*')
def getAllDepartments():
    # Retrieve all the Employees from the Database
    return jsonify({"departments": Department.getAllDepartments(mysql)})

'''
This Function is to retrieve an Individual Department given the ID of the Department. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/department/<int:department_id>', methods=['GET'])
@cross_origin(origin='*')
def getDepartment(department_id):
    department = Department.getDepartment(department_id, mysql)
    
    if (department == None):
        return jsonify({"department": None, "msg": "Department Not Found"})
    
    return jsonify({"department": department, "msg": "Department Found Successfully!"})

'''
Add New Department Given their Details. This can only be accessed by an HR Employee or Manager.
IT Managers cannot access this data.
'''
@app.route('/department', methods=['POST'])
@cross_origin(origin='*')
def addDepartment():
    if not request.json or not 'name' in request.json:
        return jsonify({"result":False, "msg":"Failed to Add Department"})
    
    department = Department(request.json['name'])

    result = Department.addDepartment(department, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Department Added Successfully!"})
    
    return jsonify({"result":False, "msg":"Failed to Add Department!"})

'''
Update an Existing Department Given their updated details. This can only be accessed by an HR Employee and Manager.
IT Managers cannot access this data.
'''
@app.route('/department/<int:department_id>', methods=['PUT'])
@cross_origin(origin='*')
def updateDepartment(department_id):
    if not request.json or not 'name' in request.json or not 'id' in request.json:
        return jsonify({"result":False, "msg":"Failed to Update Department"})

    department = Department(request.json['name'], request.json['id'])

    result = Department.updateDepartment(department, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Updated Department!"})

    return jsonify({"result":False, "msg":"Failed to Update Department!"})

'''
Delete an Existing Department given their ID. This can only be accessed by an HR Employee and Manager.
IT Managers cannot access this data.
'''
@app.route('/department/<int:department_id>', methods=['DELETE'])
@cross_origin(origin='*')
def deleteDepartment(department_id):
    result = Department.deleteDepartment(department_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Deleted Department!"})
    
    return jsonify({"result":False, "msg":"Failed to Delete Department!"})

"""
====================================================
                DATASET API FUNCTIONS
====================================================
The following section contains the API functions for Dataset functionality.
"""
'''
This Function is to retrieve all the datasets in the database. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/datasets', methods=['GET'])
@cross_origin(origin='*')
def getAllDataset():
    result = Dataset.getAllDatasets(mysql)
    return jsonify({"datasets": result})

'''
This Function is to retrieve an Individual Dataset given the ID of the Dataset. The User should be either a Manager or an HR Employee.
IT Managers cannot access this data.
'''
@app.route('/dataset/<int:dataset_id>', methods=['GET'])
@cross_origin(origin='*')
def getDataset(dataset_id):
    result = Dataset.getDataset(dataset_id, mysql)
    return jsonify({"dataset" : result})

'''
This Function is to upload a new dataset to the database. The User should the IT Manager Only.
HR Employee and Manager cannot access this data.
'''
@app.route('/dataset', methods=['POST'])
@cross_origin(origin='*')
def uploadDataset():
    if not request.json or not 'name' in request.json:
        return jsonify({"result":False, "msg":"Failed to Upload Dataset!"})

    dataset = Dataset(request.json['name'], request.json['purpose'], request.json['user'], request.json['datafile'])
    
    result = Dataset.addDataset(dataset, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Uploaded Dataset!"})

    return jsonify({"result":False, "msg":"Failed to Upload Dataset!"})

'''
Update an Existing Dataset Given their updated details. This can only be accessed by the IT Manager.
HR Employee and Manager cannot access this data.
'''
@app.route('/dataset/<int:dataset_id>', methods=['PUT'])
@cross_origin(origin='*')
def updateDataset(dataset_id):
    if not request.json or not 'name' in request.json or not 'id' in request.json:
        return jsonify({"result":False, "msg":"Failed to Update Dataset!"})

    dataset = Dataset(request.json['name'], request.json['purpose'], request.json['user'], id=request.json['id'])
    
    result = Dataset.updateDataset(dataset_id, dataset, mysql)
    
    if result is True:
        return jsonify({"result":True, "msg":"Successfully Updated Dataset!"})
    
    return jsonify({"result":False, "msg":"Failed to Update Dataset!"})

'''
Delete an Existing Dataset given their ID. This can only be accessed by the IT Manager.
HR Employee and Managers cannot access this data.
'''
@app.route('/dataset/<int:dataset_id>', methods=['DELETE'])
@cross_origin(origin='*')
def deleteDataset(dataset_id):
    result = Dataset.deleteDataset(dataset_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Deleted Dataset!"})
    
    return jsonify({"result":False, "msg":"Failed to Delete Dataset!"})

"""
====================================================
                MODEL API FUNCTIONS
====================================================
The following section contains the API functions for Model functionality.
"""
'''
This Function is to retrieve all the models in the database. The User should be an IT Manager.
HR Employee and Managers cannot access this data.
'''
@app.route('/models', methods=['GET'])
@cross_origin(origin='*')
def getAllModels():
    result = Model.getAllModels(mysql)
    return jsonify({"models": result})

'''
This Function is to retrieve an Individual Model given the ID of the Model. The User should be an IT Manager.
HR Employee and Managers cannot access this data.
'''
@app.route('/model/<int:model_id>', methods=['GET'])
@cross_origin(origin='*')
def getModel(model_id):
    result = Model.getModel(model_id, mysql)
    return jsonify({"model" : result})

'''

'''
@app.route('/model', methods=['POST'])
@cross_origin(origin='*')
def addModel():
    if not request.json or not 'name' in request.json:
        return jsonify({"result":False, "msg":"Failed to Create Model!"})

    model = Model(request.json['name'], request.json['dataset'])

    result = Model.addModel(model, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Created Model!"})

    return jsonify({"result":False, "msg":"Failed to Create Model!"})
'''
Update an Existing Model given their updated details. This can only be accessed by an IT Manager.
HR Employee and Managers cannot access this data.
'''
@app.route('/model/<int:model_id>', methods=['PUT'])
@cross_origin(origin='*')
def updateModel(model_id):
    if not request.json or not 'name' in request.json or not 'id' in request.json:
        return jsonify({"result":False, "msg":"Failed to Update Model!"})

    model = Model(request.json['name'], request.json['dataset'])

    result = Model.updateModel(model, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Updated Model!"})

    return jsonify({"result":False, "msg":"Failed to Update Model!"})

'''
Delete an Existing Model given their ID. This can only be accessed by an IT Manager.
HR Employee and Managers cannot access this data.
'''
@app.route('/model/<int:model_id>', methods=['DELETE'])
@cross_origin(origin='*')
def deleteModel(model_id):
    result = Model.deleteModel(model_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Deleted Model!"})
    
    return jsonify({"result":False, "msg":"Failed to Delete Model!"})

"""
====================================================
              PREDICTION API FUNCTIONS
====================================================
The following section contains the API functions for Prediction functionality.
"""
'''
This Function is to retrieve all the predictions in the database. The User should be either a HR Employee or Manager.
IT Managers cannot access this data.
'''
@app.route('/predictions', methods=['GET'])
@cross_origin(origin='*')
def getAllPredictions():
    result = Prediction.getAllPredictions(mysql)
    return jsonify({"predictions": result})

'''
This Function is to retrieve an Individual Prediction given the ID of the Prediction. The User should be either a HR Employee or Manager.
IT Manager cannot access this data.
'''
@app.route('/prediction/<int:prediction_id>', methods=['GET'])
@cross_origin(origin='*')
def getPrediction(prediction_id):
    result = Prediction.getPrediction(prediction_id)
    return jsonify({"prediction": result})

'''
This Function is to retrieve Predictions given the ID of the Employee. The User should be either a HR Employee or Manager.
IT Manager cannot access this data.
'''
@app.route('/prediction/employee/<int:employee_id>', methods=['GET'])
@cross_origin(origin='*')
def getPredictionByEmployee(employee_id):
    result = Prediction.getPredictionByEmployee(employee_id)
    return jsonify({"prediction": result})

'''
Update an Existing Prediction given their updated details. This can be accessed by HR Employee and Manager.
IT Manager cannot access this data.
'''
@app.route('/prediction/<int:prediction_id>', methods=['PUT'])
@cross_origin(origin='*')
def updatePrediction(prediction_id):
    if not request.json or not 'name' in request.json or not 'id' in request.json:
        return jsonify({"result":False, "msg":"Failed to Update Model!"})

    model = Model(request.json['name'], request.json['dataset'])

    result = Prediction.updatePrediction(prediction_id, prediction, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Updated Prediction!"})

    return jsonify({"result":False, "msg":"Failed to Update Prediction!"})

'''
Delete an Existing Prediction given their ID. This can be accessed by HR Employee and Manager.
IT Manager cannot access this data.
'''
@app.route('/prediction/<int:prediction_id>', methods=['DELETE'])
@cross_origin(origin='*')
def deletePrediction(prediction_id):
    result = Prediction.deletePrediction(prediction_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Deleted Prediction!"})

    return jsonify({"result":False, "msg":"Failed to Delete Prediction!"})

"""
====================================================
               APP CONFIGURATIONS
====================================================
The following section contains the API functions for changing the App Configurations.
"""
'''
This Function is to retrieve all the preferences in the database. The User should be an IT Manager.
HR Employee or Manager cannot access this data.
'''
@app.route('/preference', methods=['GET'])
@cross_origin(origin='*')
def getPreference():
    result = Preference.getPreference(mysql)
    return jsonify({"preferences": result})

'''
Update the Preferences of the System
'''
@app.route('/preference/<int:preference_id>', methods=['PUT'])
@cross_origin(origin='*')
def updatePreference(preference_id):
    if not request.json or not 'model_id' in request.json:
        return jsonify({"result":False, "msg":"Failed to Update Preference!"})
    
    result = Preference.updatePreference(preference_id, model_id, mysql)

    if result is True:
        return jsonify({"result":True, "msg":"Successfully Updated Preferences!"})

    return jsonify({"result":False, "msg":"Failed to Update Perferences!"})

if __name__ == '__main__':
    app.debug = True
    app.run(host="127.0.0.1",port="8080")