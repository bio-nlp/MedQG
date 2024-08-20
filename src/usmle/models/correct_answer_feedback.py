from pydantic import BaseModel, Field, validator
class correct_answer_fb_aspects(BaseModel):
    relevant:str = Field(description="The correct answer should be either the keypoint or very related to it.")
    occurrence: str =Field(description="the correct answer or any of its semantic or syntactic forms and directly related medical concepts should not occur in the context.")
    justification:str = Field(description="Is the correct answer logically supported by the context and aligned with the provided information?")
    depth_of_understanding: str =Field(description="Does the correct answer demand nuanced understanding of the context or concepts, ensuring the test taker genuinely grasps the material?")
    prevention_of_guesswork:str = Field(description="Does the correct answer deter guessing and align with the context, avoiding common misconceptions?")
class correct_answer_feedback(BaseModel):
    correct_answer_feedback : correct_answer_fb_aspects = Field(description="Aspects upon which the correct answer should be judged")
    correct_answer_score: str = Field(description="Total score for the correct answer, summing up each of the aspect scores")
