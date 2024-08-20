from pydantic import BaseModel, Field, validator
class distractor_options_fb_aspects(BaseModel):
    format:str = Field(description="The distractors should be in similar formats as the correct answer, i.e. if it is an abbreviation or an explanation.")
    length:str = Field(description="The distractors should have similar length as the correct answer.")
    relation: str = Field(description="The distractors should be related to the correct answer through some medical concepts or they should be the same kind of medical entities.")
    variation: str = Field(description="Distractors should be distinct from each other and from the correct answer.")
    plausibility: str = Field(description="Do the options align with the context and challenge critical thinking")
    differentiation: str = Field(description="Are the options distinct and does the correct answer clearly outshine the distractors based on context and available information?")
    common_mistakes:str = Field(description="Distractors should align with common misconceptions to test genuine understanding?")
class distractor_options_feedback(BaseModel):
    distractor_options_feedback : distractor_options_fb_aspects = Field(description="Aspects upon which the distractor options should be judged")
    distractor_options_score: str = Field(description="Total score for the distractor options, summing up each of the aspect scores")
