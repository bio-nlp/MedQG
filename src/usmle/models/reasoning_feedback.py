from pydantic import BaseModel, Field, validator
class reasoning_fb_aspects(BaseModel):
    correctness : str =Field (description="If the attempted answer is exactly same as the correct answer, give full points otherwise zero.")
    logical_flow: str =Field (description="Does the chain of thought exhibit a coherent sequence of steps or considerations that are easy to follow?")
    evidence_based_reasoning: str =Field (description="Is the answer supported by evidence or information from the context, justifying the chosen response?")
    consideration_of_options: str =Field (description="Does the chain of thought demonstrate critical evaluation of each option, employing a systematic process to eliminate distractors with supporting evidence?")
class reasoning_feedback(BaseModel):
    reasoning_feedback : reasoning_fb_aspects = Field(description="Aspects upon which the reasoning should be judged")
    reasoning_score: str = Field(description="Total score for the reasoning, summing up each of the aspect scores")