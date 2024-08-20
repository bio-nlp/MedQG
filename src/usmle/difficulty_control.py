#!/usr/bin/env python
# coding: utf-8

# In[6]:


import openai
import json
import pandas as pd
openai.api_key = "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"




def prompt(sample_question):
    instruction = """
  You are a medical expert who is preparing questions for the USMLE-step 2-CK exam.
  """
  


    prompt0 =''' There are 5 difficulty levels for the questions: Very Easy, Easy, Medium, Hard, Very Hard. These are the characteristics of a particular difficulty level, along with an example for each difficulty level:

Very Easy
{"question": "A 53-year-old man comes to the emergency department for severe left knee pain for the past 8 hours. He describes it as an unbearable, burning pain that woke him up from his sleep. He has been unable to walk since. He has not had any trauma to the knee. Ten months ago, he had an episode of acute pain and swelling of the right big toe that improved with analgesics. He has hypertension, type 2 diabetes mellitus, psoriasis, and hyperlipidemia. Current medications include topical betamethasone, metformin, glipizide, losartan, and simvastatin. Two weeks ago, hydrochlorothiazide was added to his medication regimen to improve blood pressure control. He drinks 1–2 beers daily. He is 170 cm (5 ft 7 in) tall and weighs 110 kg (242 lb); BMI is 38 kg/m2. His temperature is 38.4°C (101.1°F). Examination shows multiple scaly plaques over his palms and soles. The left knee is erythematous, swollen, and tender; range of motion is limited by pain. In addition to administering analgesics, which of the following is the most appropriate next step in management?",
  "options": [{"A": "Obtain blood cultures"}, {"B": "Measure serum uric acid levels"} , {"C": "Perform arthrocentesis of the knee"}, {"D": "Measure serum anticitrullinated peptide antibodies"}, {"E": "Obtain x-ray of the knee"}], 
  "answer": "Perform arthrocentesis of the knee",
  "answer_idx": "C"
}

The question is considered level Very Easy due to several factors:
1. Clear Clinical Picture: The patient's symptoms, history, and physical examination findings clearly point towards a common condition, gout, which is a part of the basic medical curriculum. The patient's history of podagra, multiple risk factors for gout, and the acute presentation of severe knee pain, swelling, and fever are classic for an acute gout flare.
2. Basic Diagnostic Approach: The question asks for the next appropriate step in management, which is a basic concept in clinical decision-making. The correct answer, performing an arthrocentesis of the knee, is a standard procedure to confirm the diagnosis of gout and rule out other conditions like septic arthritis or pseudogout.
3. Common Distractors: The distractors in the options are common considerations in the differential diagnosis of acute knee pain but can be easily ruled out based on the patient's history and presentation.
4. Basic Medical Knowledge: The knowledge required to answer this question correctly is fundamental and typically covered early in medical education. Understanding the presentation and management of gout does not require advanced or specialized knowledge.
5. High Clinical Prevalence: Gout is a common condition encountered in general practice, making it more likely that a test-taker would be familiar with its presentation and management.

Summarized list of characteristics:
1. Clear Presentation: The question provides a clear clinical presentation of a patient with a specific condition.
2. Common Condition: The condition is well-known and often taught in medical school.
3. Straightforward Answer Choices: The answer choices are distinct medical conditions that do not overlap significantly in their presentations.
4. Basic Knowledge: The knowledge required to answer this question is fundamental and would be expected of anyone who has completed a basic medical school curriculum.
5. Obviously incorrect options: Some options are clearly incorrect, making it easier to choose the correct answer.


Easy
{"question": "An 11-year-old boy is brought to the physician by his parents because of a 2-month history of progressive swelling of his right upper arm. He has otherwise been healthy. Medical history is unremarkable and he takes no medications. Immunizations are up-to-date. He appears well-nourished and well-developed. He is at the 60th percentile for height and weight. Vital signs are within normal limits. Physical examination shows an immobile mass on the right proximal humerus that is nontender to palpation. Erythrocyte sedimentation rate is 10 mm/h and alkaline phosphatase is 35 U/L. An x-ray shows a 3-cm sessile bony protrusion with a cartilage cap on the proximal metaphysis of the right humerus. Which of the following is the most likely diagnosis?",
  "options": [{"A": "Chondrosarcoma"}, {"B": "Osteoid osteoma"}, {"C": "Ewing sarcoma"}, {"D": "Osteosarcoma"}, {"E": "Osteochondroma"}, {"F": "Chondroblastoma"}], 
  "correct_answer": "Osteochondroma",
  "answer_idx": "E"
}

The question is considered level Easy due to several factors:
1. Clear Presentation: The patient's symptoms and the physical examination findings are clearly presented. The question provides a detailed description of the patient's condition, including the location and nature of the mass, the patient's age, and the results of the x-ray, which all point towards a specific diagnosis.
2. Basic Knowledge: The question tests basic knowledge about common bone tumors in children. It requires the test taker to differentiate between various types of bone tumors based on the patient's age, symptoms, and radiographic findings. This is a fundamental skill in orthopedics and pediatrics, and is typically covered early in medical education.
3. Straightforward Radiographic Findings: The x-ray findings described in the question (a sessile bony protrusion with a cartilage cap) are characteristic of a specific type of bone tumor (osteochondroma), making the diagnosis relatively straightforward for those familiar with this condition.
4. Limited Differential Diagnosis: The differential diagnosis for a painless bone mass in a child is relatively limited, and the question provides clear clues (e.g., the patient's age, the location of the mass, the absence of pain, and the x-ray findings) that help to narrow down the possibilities.
5. Absence of Complex Decision-Making: The question does not require complex decision-making or the application of advanced clinical reasoning skills. It simply asks for the most likely diagnosis based on the information provided.

Summarized list of characteristics:
1. Clear Presentation: The question presents a clear clinical scenario with a well-defined patient history and physical examination findings.
2. Specific Findings: The question provides specific imaging findings that are characteristic of a particular diagnosis.
3. Limited Differential: The differential diagnosis for the condition is relatively limited.
4. Basic Knowledge: The question tests basic knowledge about a common condition or disease.
5. Straightforward Answer Choices: The answer choices are straightforward and each one is clearly different from the others.
6. Direct Question: The question directly asks for the most likely diagnosis.


Medium
{"question": "A 70-year-old man comes to the physician for a follow-up evaluation. Eight months ago, he presented with a 6-month history of increased urinary frequency, difficulty to initiate urination, and straining to maintain the urinary stream. Digital rectal examination showed a symmetrically enlarged, nontender prostate with a rubbery texture. Laboratory studies showed a prostate-specific antigen level of 2.1 ng/mL. Abdominal ultrasound showed a post-void residual urine volume of 250 mL and bladder wall thickening. The patient received appropriate treatment. His vital signs are within normal limits. Laboratory studies today show a PSA level of 0.9 ng/mL. Which of the following medications was most likely used to treat this patient?",
  "options": [{"A": "Oxybutynin"}, {"B": "Dutasteride"}, {"C": "Terazosin"}, {"D": "Flutamide"}, {"E": "Tadalafil"}], 
  "correct_answer": "Dutasteride",
  "answer_idx": "B"
}

The question is considered level Medium due to several factors:
1. Clinical Scenario: The question presents a complex clinical scenario involving a patient with benign prostatic hyperplasia (BPH). The student must understand the pathophysiology of BPH, the clinical presentation, and the diagnostic findings to correctly identify the condition.
2. Interpretation of Laboratory Results: The question requires the student to interpret laboratory results, specifically the prostate-specific antigen (PSA) levels, and understand how they relate to the patient's condition and treatment.
3. Knowledge of Pharmacotherapy: The student must have a good understanding of the pharmacological treatment options for BPH, including their mechanisms of action, indications, and effects on laboratory values. This involves knowledge of several different classes of drugs.
4. Critical Thinking: The student must use critical thinking to integrate the clinical findings, laboratory results, and knowledge of pharmacotherapy to identify the most likely treatment the patient received.
5. Misleading Options: The options provided include several plausible treatments for BPH, making it more challenging to select the correct answer. The student must not only know what each drug does but also how it affects the PSA levels.

Summarized list of characteristics:
1. Clinical Scenario: The question presents a complex clinical scenario.
2. Interpretation of Lab results: The question requires the student to interpret laboratory results.
3. Knowledge of Pharmacology: The student must have a good understanding of the pharmacological treatment options for the condition.
4. Application of Knowledge: The student must apply their knowledge to identify the most likely medication used in this case.
5. Distractor and Misleading Options: The options provided include several medications used in the management of the condition or related conditions, which can be misleading.


Hard
{"question": "Two days after delivery, a 4300-g (9-lb 8-oz) male newborn has difficulty feeding and has become increasingly lethargic. His cry has become weak. He was born at term. His mother has a history of intravenous drug use. His temperature is 36.4°C (97.5°F), pulse is 170/min, respirations are 62/min, and blood pressure is 70/48 mm Hg. Examination shows midfacial hypoplasia, diaphoresis, and tremor of the lower extremities. Macroglossia is present. There are folds in the posterior auricular cartilage. The left lower extremity is larger than the right lower extremity. Abdominal examination shows an umbilical hernia. The liver is palpated 4 cm below the right costal margin. Neurologic examination shows decreased tone in all extremities. Administration of which of the following is the most appropriate intervention?", 
  "options": [{"A": "Calcium gluconate"}, {"B": "Thyroxine"}, {"C": "3% saline"}, {"D": "Glucose"}, {"E": "Ampicillin and gentamicin"}, {"F": "Naloxone"}], 
  "correct_answer": "Glucose",
  "answer_idx": "D"
}

The question is considered level Hard due to several factors:
1. Clinical Complexity: The question presents a complex clinical scenario involving a newborn with multiple symptoms and physical findings. The student must be able to recognize and interpret these findings correctly to arrive at the correct diagnosis.
2. Knowledge Required: The question requires a deep understanding of neonatology, genetics, and metabolic disorders. The student must be familiar with Beckwith-Wiedemann syndrome, a rare genetic disorder, and its associated features and complications.
3. Differential Diagnosis: The question provides several plausible options for intervention, each associated with different conditions. The student must be able to rule out these conditions based on the information provided in the question stem.
4. Critical Thinking: The question requires the student to integrate clinical findings with their knowledge of pathophysiology to identify the most appropriate intervention. This involves a high level of critical thinking and clinical reasoning skills.
5. Application of Knowledge: The question requires the application of knowledge in a clinical context, which is generally more challenging than questions that test recall of facts.

Summarized list of characteristics:
1. Complexity of the case: The question presents a complex clinical scenario involving a patient with multiple symptoms and physical findings.
2. Need for advanced knowledge: The question requires knowledge of a relatively rare genetic syndrome and its associated features.
3. Interpretation of clinical findings: The examinee must correctly interpret a variety of clinical findings and understand their significance in the context of the case.
4. Decision-making skills: The examinee must choose the most appropriate intervention from several plausible options.
5. Misleading and distractor options: Some of the answer choices could be plausible explanations for some of the symptoms, making the question more challenging.


Very Hard
{"question": "A 27-year-old man is brought to a mountain base camp at 4000 m (13,100 ft) above sea level because he has had a 2-hour history of confusion, difficulties walking, and decreased responsiveness. He has been participating in a 5-day hiking trip in which the group has ascended 1500 m (4900 ft) from the base camp in 2 days. This morning, the third day of the trip, the patient was found in his tent unable to respond to simple questions and having wet himself. The night before, he reported headaches, dizziness, and nausea. He appears lethargic. Temperature is 37.5°C (99.5°F), pulse is 85/min, respirations are 20/min, and blood pressure is 135/85 mm Hg. Pulse oximetry on room air shows an oxygen saturation of 89%. Neurological examination shows slurred speech and an ataxic gait. Kernig sign is absent. Further diagnostic studies cannot be performed due to limited medical equipment. The most appropriate initial step in management is the administration of which of the following?",
  "options": [{"A": "Nifedipine"}, {"B": "Haloperidol"}, {"C": "Mannitol"}, {"D": "Acetazolamide"}, {"E": "Dexamethasone"}], 
  "correct_answer": "Dexamethasone",
  "answer_idx": "E"
}

The question is considered level Very Hard due to several factors:
1. Clinical Scenario Complexity: The question presents a complex clinical scenario involving a patient with symptoms of high-altitude cerebral edema (HACE), a life-threatening condition that requires immediate intervention. The symptoms are not straightforward and require a deep understanding of the pathophysiology of altitude sickness and its complications.
2. Knowledge Required: The question requires a deep understanding of the pathophysiology of acute mountain sickness (AMS) and its complications, including HACE. It also requires knowledge of the pharmacological management of these conditions, including the use of dexamethasone, a rescue medication for HACE.
3. Diagnostic Difficulty: The question requires the examinee to differentiate between different conditions that can present with similar symptoms at high altitudes, such as AMS, HACE, and high altitude pulmonary edema (HAPE). This requires a high level of clinical reasoning and diagnostic skills.
4. Management Decision: The question requires the examinee to make a critical management decision in a life-threatening situation with limited resources, which adds to the difficulty level.
5. Limited Information: The question scenario also mentions that further diagnostic studies cannot be performed due to limited medical equipment, which adds another layer of complexity to the question. The examinee must make a diagnosis and treatment decision based on the limited information available.

Summarized list of characteristics:
1. Clinical Scenario Complexity: The question presents a complex clinical scenario involving a patient with symptoms of a relatively rare and life-threatening condition.
2. Diagnostic Challenge: The question requires the test taker to differentiate between several possible diagnoses based on the patient's symptoms and history.
3. Treatment Knowledge: The correct answer involves knowing the appropriate initial treatment for the condition.
4. Limited Resources: The question scenario involves a situation with limited medical equipment, adding an additional layer of complexity to the decision-making process.
5. Critical Decision Making: The question requires critical decision-making skills as the patient's condition is life-threatening and requires immediate intervention.
6. Application of Clinical Guidelines: The question may require the application of clinical guidelines to the scenario.
7. Understanding of Research Data: The question may require the interpretation of research data.
8. Interpretation of Pharmaceutical Advertisement: The question may require the interpretation of pharmaceutical advertisements.

For the below USMLE-step 2 question, revise the below question to generate five new USMLE Step 2 CK questions.
You have various strategies for adjusting the difficulty of a question, such as manipulating the amount of information within the context. This information could be crucial clues or interference information, so you can modify the difficulty by adding or removing certain pieces of information from the context. Besides, the specific focus of the question and the options provided can also be altered. With the same context, you can ask about common or uncommon points to change the difficulty, or you can use more challenging distractors to increase the difficulty.
Please using this json format: 
{"Very easy": {question, options, answer, answer_idx}, 
 "Easy": {question, options, answer, answer_idx},
 "Medium": {question, options, answer, answer_idx}
 "Hard": {question, options, answer, answer_idx}
 "Very Hard": {question, options, answer, answer_idx}
}
Please output strictly according to the format and do not output any other content.
Make sure the generated questions are different from each other and satisfy the level of difficulty.
'''

    print('working...')
    input_titles = prompt0 + "\n" + sample_question
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
          {"role": "system", "content": instruction},
          {"role": "user", "content": input_titles},
      ],
      temperature=0
  )
    return json.loads(response["choices"][0]["message"]["content"])
  

# In[4]:

if __name__ == "__main__":
    df = pd.read_csv('data/inputs/gpt4_usmle_q_hum_kp.csv', index_col=None)


    i=2
    final_data = []
    for i in range(len(df)):
        question = json.dumps({
        "question": df.iloc[i]['question'],
        "options": df.iloc[i]['options'], 
        "correct_answer": df.iloc[i]['answer'],
        "answer_idx": df.iloc[i]['answer_idx']
        })

        data = prompt(question)
        output_path = "data/inputs/gpt4_dc_usmle_q_hum_kp.jsonl"
        with open(output_path, 'a+') as f:
            json.dump(data,f)
            f.write('\n')
        print(data)
        final_data.append(data)
    






