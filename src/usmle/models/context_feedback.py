from pydantic import BaseModel, Field, validator
class context_fb_aspects(BaseModel):
    relevant: str =  Field(description="The context should be relevant to the topic provided.")
    concision : str = Field(description="The context should be concise and shouldn't include extraneous information or just be a copy of the clinical note.")
    coherent: str =  Field(description="The context should be coherent enough and should organically be built for the question in the end.")
    consistent: str =  Field(description="The context is consistent with the information in the clinical note and the topic.")
    specific: str =  Field(description="The context should be specific and address the topic." )
    fluent: str = Field(description="The context is fluent in terms of grammar and flow of words and ideas.")
    clueing: str = Field(description="Instead of directly mentioning the diagnosis of a medical condition, it should be clued in through the mention of symptoms.")
    completeness: str= Field(description="The context should be complete and free from gaps or missing information that could lead to ambiguity in answering the question accurately.")
    misdirection: str=  Field(description="Does the context avoid misleading the test taker intentionally or unintentionally?")

class context_feedback(BaseModel):
    context_feedback : context_fb_aspects = Field(description="Aspects upon which the context should be judged")
    context_score: str = Field(description="Total score for the context, summing up each of the aspect scores")
