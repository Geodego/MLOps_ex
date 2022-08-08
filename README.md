[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
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
Inspection shows that there are nan in column 'loundness' even if not specified in instructions
we replace nans wth the average loudness in the dataset.
To execute the code and save the pre-processed data we run:
```bash
mlflow run . -P input_artifact="exercise_4/genres_mod.parquet:latest" \
             -P artifact_name="preprocessed_data.csv" \
             -P artifact_type="clean_data" \
             -P artifact_description="Data after preprocessing"
```
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
Experiment 4: sweep on multiple parameters
```bash
mlflow run . -P hydra_options="-m random_forest_pipeline.random_forest.max_depth=range(10,50,3) random_forest_pipeline.tfidf.max_features=range(50,200,50) hydra/launcher=joblib"
```
Note: We had to do some modifications to the code to get things to work with hydra/launcher:
It seems that mlflow.run can fail randomly when used with hydra-launcher. When run again with exactly the same 
parameters it ends up working after a few trials, so we added a while loop to catch mlflow exceptions and run things 
again until they work.
#### Exercise 12: Validation and choice of the best performing model
In this exercise you will export a model using the parameters we have found in the previous exercise during 
the experimentation phase.
```bash
mlflow run . 
```

#### Exercise 13: Test the final model
In this exercise you will build a component that fetches a model and test it on the test dataset.
Then, you will mark that model as "production ready".
````bash
mlflow run . \
-P model_export="exercise_12/model_export:latest" \
-P test_data="exercise_6/data_test.csv:latest"
````

#### lesson 5: Final pipeline release and deploy

#### Exercise 14: Write an End-to-End Machine Learning Pipeline
The purpose of the exercise is to build a pipeline for learning the genre of the songs using a random
forest classifier. The objective is to make the pipeline reproducible. For that purpose a specific repository 
is set-up and can be accessed  [here](https://github.com/Geodego/genre_classification.git)

#### Exercise 15: Release your pipeline
In this exercise you will release your final pipeline as a versioned code artifact on GitHub.
Steps:
- Go to the repository we created in Exercise 14. 
- Make a release with version 1.0.0
- Now anybody can use your pipeline at version 1.0.0 with mlflow and w&b:
````bash
mlflow run -v 1.0.0 [URL of your Github repo]
````
Note: they need to be logged in to wandb (wandb login)

#### Exercise 16: Deploy with MLflow
In this exercise we experiment with different ways of deploying an exported model for online and offline inference.
First we need to fetch the production model. We are going to save it into the model directory:
````bash
wandb artifact get genre_classification_prod/model_export:prod --root model
````
Offline (batch) inference:
Let's run inference on the test set.

Use the W&B CLI to download the genre_classification_prod/data_test.csv:latest artifact locally
````bash
wandb artifact get genre_classification_prod/data_test.csv:latest
````
Now we can run the model on that file:
````bash
mlflow models predict \
                -t csv \
                -i ./artifacts/data_test.csv:v0/data_test.csv \
                -m model
````

Online inference:
We first need to start the REST API for our model:
````bash
mlflow models serve -m model &
````
We open Jupyter in another terminal, and in a notebook use the ``requests`` library
   to interrogate the API and do inference on the provided ``data_sample.json``:
   ```python
   import requests
   import json
   
   with open("data_sample.json") as fp:
       data = json.load(fp)
   
   results = requests.post("http://localhost:5000/invocations", json=data)
   
   print(results.json())
   ```

Bonus: docker deployment
You can also use docker to build an image and then deploy to a Cloud provider 
(AWS, GCP, Azure...). Expose port 5000 of that machine to the world, and you will be able to
use your model from whenever as a simple API call.

1. Create the docker image:
   ```bash
   mlflow models build-docker -m model -n "genre_classification"
   ```
   This will take a few minutes (of course, you need docker installed)

2. Follow the procedure for your Cloud provider of choice to deploy a Docker image

3. Open port 5000 on the machine hosting the image

4. Use requests to interrogate that machine, by using the snippet we used earlier and substituting
   ``http://localhost:5000/invocations`` with ``[url to the deployed machine]:5000/invocations``

### Scalable pipeline

#### Exercise: write a model card

#### Exercise: Aequitas
In this exercise, you will use Aequitas to investigate the potential bias in a model/data set.

- We'll use the Car Evaluation Data Set from the UCI Machine Learning Repository, a notebook that trains a logistic 
regression model to determine the car's acceptability is provided.
- Using Aequitas, determine if the model contains bias. For simplicity, from Aequitas' Fairness class obtain the results 
of the get_overall_fairness method which returns a dictionary with Yes/No result for "Unsupervised Fairness", 
"Supervised Fairness" and "Overall Fairness".
- Lastly, use the aequitas.plotting.Plot module and compute the summary on fpr, fnr, and for with a 1.25 
fairness_threshold.
- You can draw inspiration from examples present here: https://github.com/dssg/aequitas/blob/master/docs/source/examples/compas_demo.ipynb

### Monitoring

#### Exercise1: API configuration
As a data scientist or ML engineer, you should have mastery over your own code, and a clear sense of the accuracy of 
your models. However, you may work with colleagues and stakeholders who aren't as familiar with your models as you are. 
Building ML monitoring and reporting API's can enable a broader audience to access crucial information about your 
deployed models.

In this exercise, you'll accomplish the basics of API configuration. This will prepare you to create a full-scale API 
that can provide monitoring and reporting about your data and models to a broad audience.

#### Exercise2: Endpoint Scripting
Configuring an API is only the first step to having a useful API. After configuration, you need to write scripts for 
endpoints that can provide useful information to you and other users of the API.

In this exercise, you'll write scripts for API endpoints so they can provide useful information about data.

- Instructions: Function for Reading Data  
The first thing you need to add to your app2.py script is a function for reading data.
You can call your function readpandas(). It should take a filename string as its input. It should use a pandas method 
to read a CSV whose filename is given by the function input. It should return the DataFrame that it read.

- Instructions: Size Endpoint  
Next, you can write a "size" endpoint that enables users to check the size of a dataset.
Your "size" endpoint needs to start with a line that specifies the app route (the route should be called '/size').
Your endpoint needs a function, that you can call size(). This function should read a query string from the API user 
called "filename". Then, your function should call the readpandas() function you created previously, passing the 
filename as the argument to this function. This will enable you to get the Dataframe specified by the filename.
Finally, you need to add a return statement to your size() function.

- Instructions - Summary Endpoint
Next, you can write a "summary" endpoint that enables users to check the summary statistics - in this case the mean of 
each column of a dataset. Your "summary" endpoint needs to start with a line that specifies the app route 
(the route should be called '/summary'). Your endpoint needs a function, that you can call summary(). This function 
should read a query string from the API user called "filename". Then, your function should call the readpandas() 
function you created previously, passing the filename as the argument to this function. This will enable you to get the 
Dataframe specified by the filename. You need to add a return statement to your summary() function. It should return 
the mean of the column of the pandas DataFrame the function read. Finally, you should test your summary() function. 
There's a dataset in the /L5 directory of your workspace called testdata.csv. You can pass the name 'testdata.csv' to 
your summary() function, and check the column means of the file. . You can also test your size() function by passing 
the testdata.csv filename to it, and checking that it's working correctly, and returning the correct size.
- Check API:
   ```bash
   curl 'http://192.168.1.17:8000/size?filename=testdata.csv'
   ```
  and
   ```bash
   curl 'http://192.168.1.17:8000/summary?filename=testdata.csv'
   ```

#### Exercise3: Calling API Endpoints
The API's you've set up in the previous exercises are capable of returning data about ML models to whoever calls them. 
However, every API is different and calling API's correctly is not always easy. Writing scripts that correctly call 
API's is especially important since many of your API users may be non-technical people who have never called an API in 
their lives. Writing scripts that correctly and efficiently call API's and monitor their outputs can help you and 
others keep your ML models and projects up-to-date and effective.

In this exercise, you'll write a script that will call API endpoints in two different ways:

- by accessing the command line of your workspace
- by using the Python module called requests

It will be useful to understand two different ways to call API endpoints, because in some cases, one or the other method may be impossible. For example, you might have to work in an environment in which the requests module is not available. Or, you might have to work in an environment in which the command line has restrictions on it. In either case, you'll be unable to use one of the methods for calling API's, and it will be useful to know the other one.
