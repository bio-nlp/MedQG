from pydantic import BaseModel, Field, validator

class UsmleQtnAns(BaseModel):
    context: str = Field(description="Extract from the clinical note based on the topic provided.")
    question: str = Field(description="Question based on the context, and the topic and keypoint provided.")
    correct_answer: str = Field(description="Correct answer to the question.")

    @validator('question')
    def question_ends_with_question_mark(cls, field):
        if field[-1] != '?':
            raise ValueError("Badly formed question!")
        return field
    