# MLOps exercises

- Exercises of ML DevOps Engineer Nanodegree Udacity

## Project Description

This Project regroup exercises organised by folders corresponding to 
the different themes studied in the ML DevOps Engineer Nanodegree at 
Udacity:
  - Clean Code Principles (clean code)
  - Building a Reproducible Model Workflow (reproducible_workflow)
  - Deploying a Scalable ML Pipeline in Production (to be completed)
  - ML Model Scoring and Monitoring (to be completed)

## Requirements
packages requirements:

  - wandb~=0.12.9 
  - pandas~=1.3.5 
  - hydra~=2.5 
  - mlflow~=1.2.0 
  - requests~=2.27.1 
  - omegaconf~=2.1.1 
  - matplotlib~=3.5.1 
  - yaml~=0.2.5 
  - pyyaml~=6.0 
  - numpy~=1.22.0 
  - pillow~=8.4.0

The packages can be installed using pip or conda
```bash
pip install <package>
```
To use Weights & Biases, set up an account then type in your terminal
```bash
wandb login
```
then follow instructions on the terminal. You will also want to install the related 
CLI tool with Python.

## Exercises
Here are some details including command line instructions used for the different exercises
### Reproducible Workflow

#### Exercise 1: Versioning Data & Artifacts
Run 
```bash
upload_artifact.py --input_file zen.txt \
              --artifact_name zen_of_python \
              --artifact_type text_file \
              --artifact_description "20 aphorisms about writing good python code"
```
Modify the script use_artifact.py then run
```bash
python use_artifact.py --artifact_name exercise_1/zen_of_python:v1
```
#### Exercise 2: ML Pipeline Components in MLflow
The script can be run on its own as:
```bash
python download_data.py \
       --file_url https://raw.githubusercontent.com/scikit-learn/scikit-learn/4dfdfb4e1bb3719628753a4ece995a1b2fa5312a/sklearn/datasets/data/iris.csv \
       --artifact_name iris \
       --artifact_type raw_data \
       --artifact_description "The sklearn IRIS dataset"
```
#### Exercise 3: Linking Together the Components. Experimenting using Hydra
Run the pipeline in the directory of the main.py file using:
```bash
mlflow run .
```
Re-run the pipeline changing the name of the experiment from the command line:
```bash
mlflow run . -P hydra_options="main.experiment_name=prod"
```

#### Exercise 4: Exploratory Data Analysis
In this exercise you will perform a simple Exploratory Data Analysis in Jupyter keeping track of 
your progress with W&B.
Preliminary step
For this analysis we will use the provided genres_mod.parquet file. As a first step, you need to upload the file to
your W&B to track it:
```bash
wandb artifact put \
      --name exercise_4/genres_mod.parquet \
      --type raw_data \
      --description "A modified version of the songs dataset" genres_mod.parquet
```

#### Exercise 5: Clean and Pre-process the Data
In this exercise you will create a MLflow component that preprocess the data. It implements in a 
reusable way the steps needed for that task.
#### Exercise 6: Data Segregation
```bash
mlflow run . -P input_artifact="exercise_5/preprocessed_data.csv:latest" \
             -P artifact_root="data" \
             -P test_size=0.3 \
             -P stratify="genre"
```