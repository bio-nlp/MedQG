# MedQG
USMLE Style Question Generation Conditional on Clinical Notes

This repository contains the source code for generating USMLE style questions using clinical notes, and human/machine generated topics and keypoints. The main file is run.py and can be used to generate USMLE questions using iterative feedback and refinement steps. The code used GPT-4 and the openai key can be updated in the usmle.env file for starting generation. 

It also contains code to generate topics and keypoints using GPT-4 using appropriate USMLE official content.

Use the following command to generate from a file having clinical notes, topics and keypoints. 


`python3 src/usmle/run.py batch-iter <data_path>`
