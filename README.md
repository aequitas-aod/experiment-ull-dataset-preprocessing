# Unfair Inequality in Education: A Benchmark for AI-Fairness Research

This is the repository for the code and dataset of the paper intitled "Unfair Inequality in Education: A Benchmark for AI-Fairness Research" submitted to the DEMO track of the 27TH European Conference on Artificial Intelligence (ECAI).

## Abstract

This paper proposes a novel benchmark specifically designed for AI fairness research in education.
It can be used for challenging tasks aimed at improving students' performance and reducing dropout rates which are also discussed in the paper to emphasize significant research directions.
By prioritizing fairness,  this benchmark aims to foster the development of bias-free AI solutions, promoting equal educational access and outcomes for all students.

## Structure

```benchmark```
contains:
- the proposed dataset (```dataset.csv```), and
- the mask for dealing with missing values (```missing_mask.csv```).

```raw_data``` includes:
- the original dataset (```original.csv```), and
- the intermediate stages of the pre-processing pipeline (```split``` and ```pre_processed```).

```res``` contains the documentation, including:
- the transformation mapping each column of the original dataset to the proposed one, along with missingness category and original text (```meta_data_mapping.csv```), and
- the value type and domains of each column of the original, intermediate-stage, and proposed datasets (rispectively, ```meta_data_original.json``` and ```meta_data_merged.json``` and ```meta_data_final.json```).

```src``` contains the source code for running the pre-processing and corresponding analysis:
- ```pre_processing``` and ```stats```contain the code for the two corresponding tasks, and
- ```pre_processing.py``` and ```split.py``` are two entry points.

Finally, ```Dockerfile``` and ```requirements.txt``` set up the environment for running the applications across multiple platforms and with Python, respectively.