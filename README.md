Here’s the updated README with information on setting the `COLBERT_API` environment variable:

```markdown
# USMLE-Style Question Generation Conditional on Clinical Notes

This repository contains the source code for generating USMLE-style multiple-choice questions from clinical notes, using **topics** and **test points** as key components. The generated questions follow the USMLE format, including the following elements:

- **Context**
- **Question**
- **Correct Answer**
- **Distractors** (incorrect answer options)
- **Test Points** (key takeaways or objectives of the question)
- **Topics** (specific medical areas or themes)

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

## Detailed Usage

Each component in the generation pipeline is powered by iterative feedback and refinement using **GPT-4**. Specify the initial prompt and exemplar set, and the model will generate and refine questions based on the input clinical data.

- **Input JSON Format**  
  Each record in the input file `<data_path>` should follow this structure:

  ```json
  {
    "clinical_note": "Clinical note text here.",
    "topic": "Topic description",
    "test_point": "Key objectives"
  }
  ```

  - `clinical_note`: The main text of the clinical note.
  - `topic`: Medical topic for question alignment.
  - `test_point`: The question's intended test objective.

- **Generated Output**
  - Contextualized USMLE-style question components will be saved to the specified output directory.

## Customization and Updates

To use different models, specify the desired GPT model version in the `.env` file, and modify `run.py` to adjust the retrieval and generation settings.

- **Model API Key**: Update the `OPENAI_API_KEY` in `usmle.env`.
- **ColBERT API Endpoint**: Update the `COLBERT_API` variable in `usmle.env` with the ColBERT API endpoint URL.
- **Few-shot Examples**: Add or modify few-shot examples in `./data/prompt/usmle/` for different components.

## Example Outputs

*Examples of generated question formats can be added here, demonstrating the typical structure and variety produced by the pipeline.*

---

Feel free to add further details, such as contact information, license terms, or links to relevant research papers. This format should make the README easier to navigate and understand!
```

This README now includes instructions for setting up the `COLBERT_API` environment variable. Let me know if you'd like any further modifications.