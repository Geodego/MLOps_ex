[![Python 3.6](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
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
  - pytest~=6.2.5 
  - scipy~=1.7.3 
  - scikit-learn~=1.0.2
  - torch~=1.4.0
  - torchvision~=0.5.0

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

#### lesson 1: Machine Learning Pipelines

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
#### lesson 2: Data Exploration and Preparation

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

#### lesson 3: Data Validation

#### Exercise 7: Deterministic Tests
In this exercise you will apply deterministic tests to the cleaned dataset from exercise 5.
Since we do not have a new training dataset, we will compare the test dataset against the train dataset. 
This is a useful trick when obtaining a new training dataset right away is not possible. 
The thresholds can be adjusted using K-fold cross validation.
We use the Kolmogorov-Smirnov test in this exercise.

To run the code there is no parameter to specify:
```bash
mlflow run . 
```

#### Exercise 8: Non-deterministic Tests
In this exercise you will apply non-deterministic tests to the cleaned dataset from exercise 5. We use the artifacts 
created in exercise_6 to get the train dataset and the test dataset.
To run the code there is no parameter to specify:
```bash
mlflow run . 
```

#### Exercise 9: Parameters in pytest
n this exercise we will modify the non-deterministic test we prepared in the previous exercise, by allowing it to 
accept the reference dataset, the new dataset as well as the threshold for the statistical test from the command line. 
This is fundamental for configurability and reusability.
To run the code there are 3 parameters to specify:
```bash
mlflow run . \
-P reference_artifact="exercise_6/data_train.csv:latest" \
-P sample_artifact="exercise_6/data_test.csv:latest" \
-P ks_alpha=0.05
```

#### lesson 4: Training, Validation and Experiment Tracking

#### demo/sklearn_pipeline:
We use the ColumnTransformer to apply different preprocessing steps to numerical, textual and categorical columns

#### demo/pytorch
Example of how we define an inference pipeline using pytorch for a image classification task.

#### demo/wandb_tracking
jupyter notebook illustrating tracking with W&B.

#### Exercise 10: Write a Training/Inference Sub-Pipeline
This exercise use the artifact "exercise_6/data_train.csv:latest". 
To run the code there is no parameter to specify, the configuration is done using Hydra:
```bash
mlflow run . 
```
#### Exercise 11: Validation and choice of the best performing model
In this exercise we will perform experiments using a slightly improved version of the pipeline we developed in 
exercise 10, using the Hydra configuration management system.
Experiment 1: override max_depth parameter
```bash
mlflow run . -P hydra_options="random_forest_pipeline.random_forest.max_depth=5"
```
#### Exercise 12: Validation and choice of the best performing model
In this exercise you will export a model using the parameters we have found in the previous exercise during 
the experimentation phase.
