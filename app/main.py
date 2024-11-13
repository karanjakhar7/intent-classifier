from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from .intent_classifier import get_intent_openai_few_shot_partial


class IntentRequest(BaseModel):
    query: str = Field(
        ...,
        title="User Query",
        description="User query to predict intent",
        max_length=100,
    )


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict_intent", status_code=status.HTTP_200_OK)
async def predict_intent(data: IntentRequest):
    intent = get_intent_openai_few_shot_partial(data.query)
    return {"intent": intent}
