from pydantic import BaseModel, Field, validator
class question_fb_aspects(BaseModel):
    relevant: str =Field(description="The question should be answerable from the information provided in the context and should not be abrupt.")
    clear: str =Field(description="The question should not be vague or ambiguous. ")
    concluding: str =Field(description="the flow of ideas from the context should organically result into the question.")
    difficulty : str =Field(description="The question should not be too easy.")
    clarity:str = Field(description="Is the question clear and unambiguous to avoid incorrect interpretations caused by ambiguity or poor wording?")
class question_feedback(BaseModel):
    question_feedback : question_fb_aspects = Field(description="Aspects upon which the question should be judged")
    question_score: str = Field(description="Total score for the question, summing up each of the aspect scores")
