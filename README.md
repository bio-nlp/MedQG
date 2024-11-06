# MCQG-SRefine: Multiple Choice Question Generation and Evaluation with Iterative Self-Critique, Correction, and Comparison Feedback
This repository contains the source code for our paper on generating USMLE-style multiple-choice questions from clinical notes, leveraging **topics** and **test points** as key components to create high-quality exam questions tailored to medical training. The model integrates contextual understanding and medical relevance to generate questions with essential USMLE-style elements, including:

- **Context**
- **Question**
- **Correct Answer**
- **Distractors** (incorrect answer options)

The approach combines iterative feedback and refinement, aimed at aligning with clinical education standards. The full research paper, detailing the methodology and findings, is available [here on arXiv](https://arxiv.org/abs/2410.13191).

The code is compatible with **GPT-3.5** and **GPT-4** chat completion APIs from OpenAI and employs a retriever model to enhance context-specificity. 

## Quick Start

**Requirements:**  
Ensure that you have a GPT-3 or GPT-4 API key from OpenAI. The API key should be added to a `.env` file (see **Environment Setup**).

### 1. **Environment Setup**

- Place your OpenAI API key in a `.env` file:

  ```bash
  echo "OPENAI_API_KEY=<Your_OpenAI_API_Key>" > usmle.env
  ```

- Set up the **ColBERT API** endpoint by adding it as another environment variable in the `.env` file. This is required for retrieving similar exemplars to improve context relevance.

  ```bash
  echo "COLBERT_API=<Your_ColBERT_API_Endpoint>" >> usmle.env
  ```

- Ensure all dependencies are installed:

  ```bash
  pip install -r requirements.txt
  ```

### 2. **Retrieval Model Setup**

To retrieve similar exemplars, we use **ColBERT** (Colbert Late Interaction over BERT). This repository assumes access to a **ColBERT API endpoint** (set up internally). ColBERT helps identify the closest clinical note exemplars to enhance question relevance. Ensure that the **ColBERT API path** is updated in the `COLBERT_API` environment variable.

- **ColBERT Model API:** [ColBERT GitHub Repository](https://github.com/stanford-futuredata/ColBERT)

## Components

### 1. **Topic Generation**

Generate topics relevant to a clinical note.

```bash
python3 src/usmle/topic_gen.py batch-iter <path_to_clinical_notes> ./data/prompt/usmle/topic_fewshot.jsonl
```

- `<path_to_clinical_notes>`: Path to the file containing clinical notes.
- `./data/prompt/usmle/topic_fewshot.jsonl`: A JSONL file containing few-shot examples.

### 2. **Test Point Generation**

Generate key test points from a clinical note.

```bash
python3 src/usmle/keypoint_gen.py batch-iter <path_to_clinical_notes> ./data/prompt/usmle/keypoint_fewshot.jsonl
```

- `<path_to_clinical_notes>`: Path to the file containing clinical notes.
- `./data/prompt/usmle/keypoint_fewshot.jsonl`: A JSONL file containing few-shot examples.

### 3. **USMLE Question Generation**

To generate USMLE-style questions based on clinical notes, topics, and test points:

```bash
python3 src/usmle/run.py batch-iter <data_path>
```

- `<data_path>`: Path to a JSON file containing clinical notes, topics, and test points.


## Customization and Updates

To use different models, specify the desired GPT model version in the `.env` file, and modify `run.py` to adjust the retrieval and generation settings.

- **Model API Key**: Update the `OPENAI_API_KEY` in `usmle.env`.
- **ColBERT API Endpoint**: Update the `COLBERT_API` variable in `usmle.env` with the ColBERT API endpoint URL.
- **Few-shot Examples**: Add or modify few-shot examples in `./data/prompt/usmle/` for different components.
