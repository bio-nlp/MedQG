import json
import pathlib
import random
from tqdm import tqdm
from typing import List
import re
from usmle.archive.task_init import UsmleQgenTaskInit
from src.usmle.task_iterate import UsmleQgenTaskIterate
from usmle.archive.feedback import UsmleQgenFeedback
from src.usmle.answer import UsmleQgenAnswer
from src.utils import retry_parse_fail_prone_cmd
import ast
from src.usmle.feedback_lgc import UsmleQgenFeedbackLgc
from src.usmle.gen_order import gen_order

from src.usmle.task_init_lgc import UsmleQgenTaskInitLgc
CODEX = "code-davinci-002"
GPT3 = "text-davinci-003"
CHATGPT = "gpt-3.5-turbo"
ENGINE = "gpt-4"

@retry_parse_fail_prone_cmd
def autofb_usmleqgen(clinical_note: str, keypoint: str, topic: str, max_attempts: int) -> str:

    # initialize all the required components
    task_init_lgc = UsmleQgenTaskInitLgc(engine=ENGINE, prompt_examples="data/prompt/usmle/init.jsonl")
    # getting feedback
    task_answer = UsmleQgenAnswer(
        engine= ENGINE,prompt_examples="data/prompt/usmle/answer.jsonl"
    )
    task_feedback_lgc = UsmleQgenFeedbackLgc(
        engine=ENGINE, prompt_examples="data/prompt/usmle/feedback.jsonl", rubrics_path="data/prompt/usmle/reasoning_rubrics.jsonl"
    )
    # iteratively improving the sentence
    task_iterate = UsmleQgenTaskIterate(
        engine=ENGINE, prompt_examples="data/prompt/usmle/iterate.jsonl"
    )

    # Initialize the task

    n_attempts = 0

    print(f"{n_attempts} INIT> {clinical_note}\n{keypoint}\n{topic}")
    content_to_fb_ret = []
    context_score,question_score,correct_answer_score,distractor_option_score, reasoning_score = '0/1','0/1','0/1','0/1','0/1'
    while n_attempts < max_attempts and check_stop(context_score,question_score,correct_answer_score,distractor_option_score,reasoning_score):
        print()

        if n_attempts == 0:
            context,question,correct_answer,distractor_options = task_init_lgc(clinical_note=clinical_note,keypoint=keypoint,topic=topic,order_enum=gen_order.step_by_step)
            attempted_answer, reasoning = task_answer(context=context,question=question, options=generate_options(distractor_options=distractor_options,correct_answer=correct_answer))
        else:

            context,question,correct_answer,distractor_options = task_iterate(clinical_note=clinical_note,keypoint=keypoint,topic=topic,content_to_fb=content_to_fb)
            attempted_answer, reasoning = task_answer(context=context,question=question,options=generate_options(distractor_options=distractor_options,correct_answer=correct_answer))

        print(f"{n_attempts} GEN> Context: {context}\nQuestion: {question}\nCorrect answer:{correct_answer}\nDistractor options:{distractor_options}")

        context_feedback, context_score, question_feedback, question_score, reasoning_feedback, reasoning_score, correct_answer_feedback, correct_answer_score, distractor_option_feedback, distractor_option_score = task_feedback_lgc(
        clinical_note=clinical_note,
        keypoint=keypoint,
        topic=topic,
        context=context,
        question=question,
        correct_answer=correct_answer,
        distractor_options=distractor_options,
        attempted_answer=attempted_answer,
        reasoning=reasoning)
        content_to_fb = [{
                "context": context,
                "question": question,
                "topic": topic,
                "keypoint" : keypoint,
                "attempted_answer" : attempted_answer,
                "reasoning" : reasoning,
                "correct_answer" : correct_answer,
                "distractor_options" : distractor_options,
                "context_feedback": context_feedback,
                "context_score":  context_score,
                "question_feedback": question_feedback,
                "question_score": question_score,
                "correct_answer_feedback" : correct_answer_feedback,
                "correct_answer_score" : correct_answer_score,
                "distractor_option_feedback": distractor_option_feedback,
                "distractor_option_score": distractor_option_score,
                "reasoning_feedback" : reasoning_feedback,
                "reasoning_score" : reasoning_score
            }]
        content_to_fb_ret.append(
            content_to_fb[0]
        )
        
        print(f"{n_attempts} Context score> {context_score} | Question score> {question_score} |  Correct answer score> {correct_answer_score} | Distractor option score> {distractor_option_score} | Reasoning score> {reasoning_score}")
        
        n_attempts += 1
    return content_to_fb_ret
def check_stop(context_score,question_score,correct_answer_score,distractor_option_score,reasoning_score):
    if get_dec_score(context_score)  >= 0.9 and get_dec_score(reasoning_score)  >= 0.9 and get_dec_score(question_score)  >= 0.9 and get_dec_score(correct_answer_score)  >= 0.9 and get_dec_score(distractor_option_score)  >= 0.9:
        print("===== Stop condition met ======\n\n")
        return False
    return True
def get_dec_score(score):
    split = score.split('/')
    num = int(re.sub("[^0-9]", "", split[0]))
    deno = int(re.sub("[^0-9]", "", split[1]))
    print(num/deno)
    return num/deno
def generate_options(distractor_options,correct_answer):
    print(f"distact : {distractor_options}")
    distractor_options = distractor_options.replace('\n','')
    distractor_options = distractor_options.replace(' :',':')
    
    ustr = ') ' if 'a)' in distractor_options.lower() else ': '
    option_key_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
    distractor_options_list = [correct_answer]
    for key in option_key_list:
        key += ustr
        try:
            opt =  re.search(re.escape(key)+r"(.*?)" + re.escape(key), distractor_options, re.IGNORECASE).group(1)
            print(opt[:-1])
            distractor_options_list.append(opt[:-1].strip())
        except:
            print(f"Except : {distractor_options}")
            opt =  re.search(re.escape(key)+r"(.*)", distractor_options,re.IGNORECASE).group(1)
            print(opt)
            distractor_options_list.append(opt.strip())
            break
    random.shuffle(distractor_options_list)
    options = ''
    for k in range(len(distractor_options_list)):
        options += option_key_list[k] +' : ' + distractor_options_list[k]
    return options
def run_cmd():
    concepts = sys.argv[2:]
    max_attempts = 5
    content_to_fb = autofb_usmleqgen(
        concepts=concepts,
        max_attempts=max_attempts,
    )

    res = []
    for s in  content_to_fb:
        sent = s["sentence"]
        fb = ";  ".join(s["concept_feedback"]) + " " + s["commonsense_feedback"]
        res.append(f"{sent} ({fb})")
    print(" -> ".join(res))


def run_iter(inputs_file_path: str, max_attempts: int = 4):
    test_df = pd.read_json(inputs_file_path, orient="records")
    is_rerun = "status" in test_df.columns
    if not is_rerun:
        test_df["content_to_fb"] = None
        test_df["content_to_fb"] = test_df["content_to_fb"].astype(object)
        test_df["status"] = None
        #this is a test comment

    else:
        print("Status column already exists! Looks like you're trying to do a re-run")
        print(test_df["status"].value_counts())
    for i, row in tqdm(test_df.iterrows(), total=len(test_df), desc="Running autofb iter"):
        if row["status"] == "success":
            continue
        content_to_fb = autofb_usmleqgen(clinical_note=row["clinical_note"],keypoint=row['keypoint'],topic=row['topic'], max_attempts=max_attempts)
            
        dict_to_write = {"clinical_note":row["clinical_note"],"keypoint":row['keypoint'],"topic":row['topic'],"content_to_fb":content_to_fb}
        output_path = inputs_file_path + (".iter.out" if not is_rerun else ".v0")
        version = 1
        output_path = output_path + f".v{version}"
        with open(output_path, 'a+') as f:
            json.dump(dict_to_write,f)
            f.write('\n')
        print(f"content to fb : {content_to_fb}")
        test_df.at[i, "content_to_fb"] = content_to_fb
        test_df.at[i, "status"] = "success"


if __name__ == "__main__":
    import sys
    import pandas as pd

    if sys.argv[1] == "cmd":
        run_cmd()

    elif sys.argv[1] == "batch-iter":
        run_iter(inputs_file_path=sys.argv[2])

    else:
        raise ValueError("Invalid mode: choose between cmd, batch-iter, batch-multi")


