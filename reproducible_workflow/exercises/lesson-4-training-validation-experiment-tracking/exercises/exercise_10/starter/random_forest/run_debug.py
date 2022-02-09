"""
This is used to debug run.py

author: Geoffroy de Gournay
date: February 9, 2022
"""
from collections import namedtuple
import os
import run

if __name__ == "__main__":
    args = namedtuple('Inputs', ['train_data', 'model_config'])
    args.train_data = "exercise_6/data_train.csv:latest"
    model_config = os.path.join(os.path.dirname(os.getcwd()), 'outputs', '2022-02-08', '20-20-22',
                                "random_forest_config.json")
    args.model_config = model_config

    run.go(args)