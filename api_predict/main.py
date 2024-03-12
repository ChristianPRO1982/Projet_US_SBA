from pydantic import BaseModel
from fastapi import FastAPI
from model_utils import load_model, prediction
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
import random
import numpy as np
import xgboost

'''
City	EVANSVILLE
State	IN
Zip	47711
Bank	FIFTH THIRD BANK
BankState	IN
NAICS	451120
ApprovalDate	1997-02-28
ApprovalFY	1997-01-01
Term	84
NoEmp	4
NewExist	2.0
CreateJob	0
RetainedJob	0
DiffJobs	0
FranchiseCode	0
UrbanRural	0
RevLineCr	N
LowDoc	Y
GrAppv	60000.0
SBA_Appv	48000.0
MIS_Status	P I F
'''

app = FastAPI()

class FeaturesInput(BaseModel):
    City: str
    State: str
    Zip: float
    Bank: str
    BankState: str
    NAICS: float
    ApprovalDate: str
    ApprovalFY: str
    Term: float
    NoEmp: float
    NewExist: float
    CreateJob: float
    RetainedJob: float
    DiffJobs: float
    FranchiseCode: float
    UrbanRural: float
    RevLineCr: str
    LowDoc: str
    GrAppv: float
    SBA_Appv: float

class PredictionOutput(BaseModel):
    predict: int

@app.post("/predict")
def prediction_root(features_input: FeaturesInput):
    model = load_model('modelXGB.pkl')

    data_input_dict = features_input.dict()
    data_input_df = pd.DataFrame(data_input_dict, index=[0])

    predictions = prediction(model, data_input_df)
    
    return PredictionOutput(predict=predictions)

    data = {
        "City": features_input.City,
        "State": features_input.State,
        "Zip": features_input.Zip,
        "Bank": features_input.Bank,
        "BankState": features_input.BankState,
        "NAICS": features_input.NAICS,
        "ApprovalDate": features_input.ApprovalDate,
        "ApprovalFY": features_input.ApprovalFY,
        "Term": features_input.Term,
        "NoEmp": features_input.NoEmp,
        "NewExist": features_input.NewExist,
        "CreateJob": features_input.CreateJob,
        "RetainedJob": features_input.RetainedJob,
        "DiffJobs": features_input.DiffJobs,
        "FranchiseCode": features_input.FranchiseCode,
        "UrbanRural": features_input.UrbanRural,
        "RevLineCr": features_input.RevLineCr,
        "LowDoc": features_input.LowDoc,
        "GrAppv": features_input.GrAppv,
        "SBA_Appv": features_input.SBA_Appv
    }
    data_df = pd.DataFrame([data])
    print (data_df)

    return random.choice([0, 1])
