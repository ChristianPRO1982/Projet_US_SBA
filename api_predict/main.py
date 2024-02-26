from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from model_utils import load_model, prediction

app = FastAPI()


class LanguageInput(BaseModel):
    language: str

class FeaturesInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionOutput(BaseModel):
    category: int

@app.post("/predict")
def prediction_root(features_input:FeaturesInput):
    model = load_model('super_model.pkl')

    data_input = []
    data_input.append(features_input.sepal_length)
    data_input.append(features_input.sepal_width)
    data_input.append(features_input.petal_length)
    data_input.append(features_input.petal_width)
    data_input = [data_input]

    predictions = prediction(model, data_input)
    
    return PredictionOutput(category=predictions)

@app.post("/language")
def language_root(language_input:LanguageInput):
    if language_input.language.lower() == 'english':
        return {'message':'Hello!'}
    elif language_input.language.lower() == 'french':
        return {'message':'Bonjour !'}
    else:
        return {'message':'Puting, il est con dit !'}









@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}