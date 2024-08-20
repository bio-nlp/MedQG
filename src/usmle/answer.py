import re
from typing import Set, List
import pandas as pd
from src.prompt_lib.prompt_lib.backends import openai_api
import json
from src.utils import Prompt


class UsmleQgenAnswer(Prompt):
    def __init__(self, engine: str, prompt_examples: str, max_tokens: int = 2048) -> None:
        super().__init__(
            question_prefix="",
            answer_prefix="",
            intra_example_sep="\n\n",
            inter_example_sep="\n\n###\n\n",
        )
        self.engine = engine
        self.max_tokens = max_tokens
        self.setup_prompt_from_examples_file(prompt_examples)

    def setup_prompt_from_examples_file(self, examples_path: str) -> str:
        template = """Context: {context}

Question: {question}

Options: {options}

Correct answer: {answer}

Reasoning: {reasoning}"""

        #examples_df = pd.read_json(examples_path, orient="records", lines=True)
        # with open(examples_path) as f:
        #     dictt = json.load(f)
        # examples_df = pd.DataFrame.from_dict(dictt, orient="index").T
        examples_df = pd.read_json(examples_path, lines=True, orient="records")
        prompt = []
        for _, row in examples_df.iterrows():
            prompt.append(
                template.format(
                    context=row["context"],
                    question=row["question"],
                    options = row["options"],
                    answer=row["correct_answer"],
                    reasoning = row["reasoning" ]
                )
            )

        instruction = """Answer the USMLE question and provide a step by step reasoning for reaching that particular answer and rejecting other options."""
        self.prompt = instruction +self.intra_example_sep+ self.inter_example_sep.join(prompt)
        #self.prompt = self.inter_example_sep.join(prompt) + self.inter_example_sep
        #print(self.prompt)
    def setup_feedback(self,feedback):
        fb = ''
        for key in feedback.keys():
            fb += '\n' + key + ':' + feedback[key] 
        return fb
    def __call__(self, context: str, question:str, options:str):
        print("The options are ")
        print(options)
        prompt = self.make_query(context, question, options)
        #print(prompt)
        output = openai_api.OpenaiAPIWrapper.call(
            prompt=prompt,
            engine=self.engine,
            max_tokens=self.max_tokens,
            stop_token="###",
            temperature=0.7,
        )
        attempted_answer = openai_api.OpenaiAPIWrapper.get_first_response(output)
        print(attempted_answer)
        correct_answer = "Correct answer: "+ re.search(r"(.*?)(?=\n\n)", attempted_answer, re.DOTALL).group(1)
        reasoning = re.search(r"Reasoning:(.*)", attempted_answer, re.DOTALL).group(1).strip()
        return correct_answer.strip(), reasoning.strip()

    def make_query(self, context: str, question:str, options:str):
        question = f"""Context: {context}

                Question: {question}

                Options: {options}

                Correct answer: """
        return f"""{self.prompt}{question}"""


if __name__ == "__main__":
    task_feedback = UsmleQgenAnswer(
        prompt_examples="data/prompt/usmle/answer.jsonl",
        engine="davinci-code-002"
    )
    
    print(task_feedback.prompt)
    
 