"""
Slicing exercise.
"""

import pandas as pd
import os


def get_iris_data():
    file_adress = "./data/iris.csv"
    df = pd.read_csv(file_adress)
    return df


def slice_iris(df):
    """
    outputs the descriptive stats for each numeric feature while the categorical variable is held fixed.
    """
    average = {}
    var = {}
    # in the iris dataset the last column hold the classes
    features = df.columns[:-1]
    groups = df.groupby('class')
    average = groups.mean()
    std_dev = groups.std()
    return average, std_dev


if __name__ == "__main__":
    df = get_iris_data()
    average, std_dev = slice_iris(df)
    print(f'average: {average}')
    print(f'var: {std_dev}')
