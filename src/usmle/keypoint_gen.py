import json
import pathlib
import random
from tqdm import tqdm
from typing import List
import re
import requests
from usmle.archive.task_init import UsmleQgenTaskInit
from src.usmle.task_iterate import UsmleQgenTaskIterate
from usmle.archive.feedback import UsmleQgenFeedback
from src.usmle.answer import UsmleQgenAnswer
from src.utils import retry_parse_fail_prone_cmd
import ast
from src.usmle.feedback_lgc import UsmleQgenFeedbackLgc
from src.usmle.gen_order import gen_order

from langchain import PromptTemplate,FewShotPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain,SequentialChain
from src.usmle.task_init_lgc import UsmleQgenTaskInitLgc
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='usmle.env')

OPENAIKEY = os.getenv("OPENAIKEY")
OPENAIORG = os.getenv("OPENAIORG")
COLBERT_API = os.getenv("COLBERT_API")

CODEX = "code-davinci-002"
GPT3 = "text-davinci-003"
CHATGPT = "gpt-3.5-turbo"
ENGINE = "gpt-4"

@retry_parse_fail_prone_cmd
def retrieve_sim_keypoints_colbert(content,k:int):
        p = {'query':content, 'k':k }
        r = requests.get( COLBERT_API,params=p)
        res_json = r.json()
        # print(res_json)
        qbank_topk = res_json['topk'][0]
        print(qbank_topk)
        return qbank_topk  
def gen_keypoints(clinical_note:str,topic:str,examples_path:str):
    llm = ChatOpenAI(model=ENGINE, temperature=0.7,openai_api_key=OPENAIKEY,openai_organization=OPENAIORG)
    ## Retrieving USMLE questions similar to the clinical note and topic from the qbank
    retrieved_kp = retrieve_sim_keypoints_colbert(clinical_note, 1)
    retrieved_kp_score = retrieved_kp['score']
    retrieved_keypoints = retrieved_kp['text']
    with open(examples_path) as f:
        fs_dict = json.load(f)
    print(fs_dict)
    kp_sim_ex_prompt = PromptTemplate(
        suffix = "Example keypoints for a given clinical note and based on a topic: ",
        input_variables=["clinical_note","topic","keypoint"], 
        template="Clinical note: {clinical_note}\nTopic: {topic}\nKeypoint: {keypoint}")
    keypoint_prompt = FewShotPromptTemplate(
        examples=fs_dict, 
        example_prompt=kp_sim_ex_prompt, 
        suffix="Please extract a keypoint from the provided list of USMLE concepts. These concepts are organized in a hierarchical manner, starting from the most general and progressively becoming more specific. The keypoint you extract should ideally be specific and concise, covering one or two USMLE concepts. This keypoint will be used as the central focus for generating a USMLE question based on a clinical note within the specified topic. The goal is to ensure a strong and relevant connection between the concept and the question..:\nClinical Note: {clinical_note}\nTopic: {topic}\n USMLE concepts: {usmle_concepts}\nKeypoint:", 
        input_variables=["clinical_note","topic","usmle_concepts"])
    
    keypoint_chain = LLMChain(llm=llm, prompt=keypoint_prompt)
    keypoint_output = keypoint_chain.run({"clinical_note" : clinical_note,
        "topic" : topic,
        "usmle_concepts" : retrieved_keypoints})
    print(keypoint_output)
    return retrieved_kp_score,retrieved_keypoints, keypoint_output


def run_iter(inputs_file_path: str, examples_path:str, max_attempts: int = 4):
    print(inputs_file_path)
    test_df = pd.read_json(inputs_file_path,lines=True, orient="records")
    print(test_df.columns)
    is_rerun = False
    if not is_rerun:
        test_df["keypoint_data"] = None
        test_df["keypoint_data"] = test_df["keypoint_data"].astype(object)
        test_df["status"] = None
    else:
        print("Status column already exists! Looks like you're trying to do a re-run")
        print(test_df["status"].value_counts())
    for i, row in tqdm(test_df.iterrows(), total=len(test_df), desc="Running autofb iter"):
        if row["status"] == "success":
            continue
        topic_list = ast.literal_eval(row['topic_list']) if 'topic_list' in test_df.columns else [row['topic']]
        print(topic_list)
        for topic in topic_list:
            retrieved_kp_score,retrieved_keypoints, keypoint_output = gen_keypoints(clinical_note=row["clinical_note"],topic=topic,examples_path=examples_path)
            keypoint_data = {"keypoint_data" : {"retrieved_kp_score":retrieved_kp_score,"retrieved_keypoints":retrieved_keypoints,"keypoint_gpt4_output":keypoint_output}}

            dict_to_write = {"clinical_note":row["clinical_note"],"topic":topic, "keypoint_data" : keypoint_data}
            output_path = inputs_file_path + (".iter.out" if not is_rerun else ".v0")
            version = 1
            output_path = output_path + f".v{version}"
            with open(output_path, 'a+') as f:
                json.dump(dict_to_write,f)
                f.write('\n')
            print(f"keypoint_data : {keypoint_data}")
            test_df.at[i, "keypoint_data"] = keypoint_data
            test_df.at[i, "status"] = "success"
        

    output_path = inputs_file_path + (".iter.out" if not is_rerun else ".v0")
    version = 0
    while pathlib.Path(output_path).exists():
        output_path = output_path + f".v{version}"
        version += 1

    test_df.to_json(output_path, orient="records", lines=True)



if __name__ == "__main__":
    import sys
    import pandas as pd

    run_iter(inputs_file_path=sys.argv[2],examples_path = sys.argv[3])