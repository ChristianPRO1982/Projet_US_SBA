from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from model_utils import load_model, prediction

app = FastAPI()

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

class FeaturesInput(BaseModel):
    sepal_length: float
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
    category: int

@app.post("/predict")
def prediction_root(features_input:FeaturesInput):
    model = load_model('model.pkl')

    data_input = []
    data_input.append(features_input.sepal_length)
    data_input.append(features_input.sepal_width)
    data_input.append(features_input.petal_length)
    data_input.append(features_input.petal_width)
    data_input = [data_input]

    predictions = prediction(model, data_input)
    
    return PredictionOutput(category=predictions)