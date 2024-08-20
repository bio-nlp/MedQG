from pydantic import BaseModel, Field, validator

class UsmleDistr(BaseModel):
    distractor_options: str = Field(description="Distractor options which are incorrect but related to the context and question. ")
