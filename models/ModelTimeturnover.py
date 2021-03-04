import os
from flask import Flask
from flask_cors import CORS

class ModelTimeturnover(Model):
    def __init__(self, id, name, createdOn, dataset):
        Model.__init__(self, id, name, createdOn, dataset)

