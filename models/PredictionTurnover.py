import os
from flask import Flask
from flask_cors import CORS

class PredictionTurnover(Prediction):
    def __init__(self, id, employee):
        Prediction.__init__(self, id, employee)