import json
import pathlib
import random
from tqdm import tqdm
from typing import List
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
CODEX = "code-davinci-002"
GPT3 = "text-davinci-003"
CHATGPT = "gpt-3.5-turbo"
ENGINE = "gpt-4"
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='usmle.env')

OPENAIKEY = os.getenv("OPENAIKEY")
OPENAIORG = os.getenv("OPENAIORG")
@retry_parse_fail_prone_cmd
def gen_topics(clinical_note:str,examples_path:str):
    llm = ChatOpenAI(model=ENGINE, temperature=0.7,openai_api_key=OPENAIKEY,openai_organization=OPENAIORG)
    with open(examples_path) as f:
        fs_dict = json.load(f)
    print(fs_dict)
    topic_sim_ex_prompt = PromptTemplate(
        suffix = "Clinical notes and their associated topics",
        input_variables=["clinical_note","topic_list"], 
        template="Clinical note: {clinical_note}\nTopic list: {topic_list}")
    topic_prompt = FewShotPromptTemplate(
        examples=fs_dict, 
        example_prompt=topic_sim_ex_prompt, 
        suffix="Please select five (5) topics from the provided list of USMLE topics that are closely related to the given clinical note, use the clinical topic and topic list examples as a reference. These topics should be suitable for creating USMLE context-based questions that align with the content of the clinical notes. \nClinical Note: {clinical_note}\n USMLE topics: {usmle_topics}\nTopic list:", 
        input_variables=["clinical_note","usmle_topics"])
    usmle_topics = [
    "the cause/infectious agent or predisposing factor(s)",
    "underlying processes/pathways",
    "underlying anatomic structure or physical location",
    "mechanisms, drugs",
    "knows signs/symptoms of selected disorders",
    "knows individual’s risk factors for development of condition",
    "knows what to ask to obtain pertinent additional history",
    "predicts the most likely additional physical finding",
    "select most appropriate laboratory or diagnostic study",
    "interprets laboratory or other study findings",
    "predicts the most likely laboratory or diagnostic study result",
    "most appropriate laboratory or diagnostic study after change in patient status",
    "select most likely diagnosis",
    "recognizes factors in the history, or physical or laboratory study findings",
    "interprets laboratory or other diagnostic study results and identifies current/future status of patient",
    "recognizes associated conditions of a disease",
    "recognizes characteristics of disease relating to natural history or course of disease",
    "risk factors for conditions amenable to prevention or detection",
    "identifies patient groups at risk",
    "knows common screening tests",
    "selects appropriate preventive agent or technique",
    "knows appropriate counseling regarding current and future problems",
    "educates patients",
    "selects most appropriate pharmacotherapy",
    "assesses patient adherence, recognizes techniques to increase adherence",
    "recognizes factors that alter drug requirements",
    "Knows adverse effects of various drugs or recognizes signs and symptoms of drug (and drug-drug) interactions",
    "knows contraindications of various medications",
    "knows modifications of a therapeutic regimen within the context of continuing care",
    "appropriate monitoring to evaluate effectiveness of pharmacotherapy or adverse effects",
    "most appropriate management of selected conditions",
    "immediate management or priority in management",
    "follow-up or monitoring approach regarding the management plan",
    "current/short-term management",
    "severity of patient condition in terms of need for referral for surgical treatments/procedures",
    "appropriate surgical management",
    "preoperative/postoperative",
    "Selecting Clinical Interventions (Mixed Management)",
    "indications for surveillance for recurrence or progression of disease following treatment",
    "how to monitor a chronic disease in a stable patient where a change in patient status might indicate a need to change therapy",
    "most appropriate long-term treatment"
]

    topic_chain = LLMChain(llm=llm, prompt=topic_prompt)
    topic_output = topic_chain.run({"clinical_note" : clinical_note,
        "usmle_topics" : usmle_topics})
    print(topic_output)
    return topic_output



def run_iter(inputs_file_path: str, examples_path:str, max_attempts: int = 4):
    print(inputs_file_path)
    test_df = pd.read_json(inputs_file_path, orient="records")
    print(test_df.columns)

    is_rerun = "status" in test_df.columns
    if not is_rerun:
        test_df["topic_list"] = None
        test_df["topic_list"] = test_df["topic_list"].astype(object)
        test_df["status"] = None

    else:
        print("Status column already exists! Looks like you're trying to do a re-run")
        print(test_df["status"].value_counts())
    for i, row in tqdm(test_df.iterrows(), total=len(test_df), desc="Running autofb iter"):
        if row["status"] == "success":
            continue
        topic_list = gen_topics(clinical_note=row["clinical_note"],examples_path=examples_path)
        dict_to_write = {"clinical_note":row["clinical_note"],"topic_list":topic_list}
        output_path = inputs_file_path + (".iter.out" if not is_rerun else ".v0")
        version = 1
        output_path = output_path + f".v{version}"
        with open(output_path, 'a+') as f:
            json.dump(dict_to_write,f)
            f.write('\n')
        print(f"topic_list : {topic_list}")
        test_df.at[i, "topic_list"] = topic_list
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

