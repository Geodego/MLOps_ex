"""
Used to analyse why there might be issues with hydra/launcher=joblib
"""
import yaml
from omegaconf import OmegaConf

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score, plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, FunctionTransformer
import matplotlib.pyplot as plt
import wandb
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from collections import namedtuple
from random_forest.run import get_training_inference_pipeline


def go(args, df):
    # Extract the target from the features
    X = df.copy()
    y = X.pop("genre")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    model_config = args.random_forest
    pipe = get_training_inference_pipeline(args, model_config)

    pipe.fit(X_train, y_train)
    score = roc_auc_score(
        y_val, pipe.predict_proba(X_val), average="macro", multi_class="ovo"
    )
    print(f"score: {score}")


if __name__ == '__main__':
    # Error executing job with overrides: ['random_forest_pipeline.random_forest.max_depth=10',
    # 'random_forest_pipeline.tfidf.max_features=150']
    conf = OmegaConf.to_container(OmegaConf.load('config.yaml'))
    rf = conf['random_forest_pipeline']['random_forest']
    tfidf = conf['random_forest_pipeline']['tfidf']
    rf.pop("min_impurity_split")  # need to drop it for debugging ti get things working
    Comline = namedtuple('ComLine', ['train_data', 'random_forest'])
    # having data_train saved as follow is due to the fact that run.py has already been runned
    data_path = './artifacts/data_train.csv:v0/data_train.csv'
    df = pd.read_csv(data_path, low_memory=False)
    for max_depth in [10]:#range(10, 50, 3):
        for max_features in [150]:#range(50, 200, 50):
            rf['max_depth'] = max_depth
            tfidf['max_features'] = max_features
            args = Comline(conf['data']['train_data'], conf['random_forest_pipeline'])
            msg = f"tree max_depth: {max_depth}, tfidf max_features: {max_features}"
            print(msg)
            try:
                go(args, df)
            except:
                raise Exception(f'Issue with ' + msg)
