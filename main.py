import pandas as pd
import numpy as np
import models.naive as naive
import models.tree as tree
import models.SPN as SPN
import helper_functions
import math
from sklearn.model_selection import train_test_split
import os
import random

import warnings
warnings.filterwarnings("ignore")

def run_naive_classifiers(X_train, X_test, y_train, y_test):
    X_train = X_train.fillna(X_train.mean())

    NBC = naive.NBC()
    NBC.train(X_train, y_train)
    NBC_predictions = NBC.predict(X_test)

    NBC_acc = helper_functions.classical_accuracies(NBC_predictions, y_test)

    s = 1
    NCC = naive.NCC()
    NCC.train(X_train, y_train, s)
    NCC_predictions = NCC.predict(X_test)

    NCC_acc_interval, NCC_robust_acc = helper_functions.credal_accuracies(NCC_predictions, y_test)

    return NBC_acc, NCC_acc_interval, NCC_robust_acc

def run_tree_classifiers(X_train, X_test, y_train, y_test):
    classical_tree = tree.C45()
    classical_tree.train(X_train, y_train)
    classical_predictions = classical_tree.predict(X_test)
    classical_acc = helper_functions.classical_accuracies(classical_predictions, y_test)

    credal_tree = tree.CredalC45()
    credal_tree.train(X_train, y_train, 1)
    credal_predictions = credal_tree.predict(X_test)
    credal_acc = helper_functions.classical_accuracies(credal_predictions, y_test)

    return classical_acc, credal_acc

def run_SPN_classifiers(X_train, X_test, y_train, y_test, random_state):
    X_test_num = X_test.to_numpy()
    X_train_num = X_train.to_numpy()

    credal_predictions = SPN.CSPN(X_train_num, X_test_num, y_train, random_state)
    credal_acc_interval, credal_robust_acc = helper_functions.classical_accuracies(credal_predictions, y_test)

    X_train = X_train.fillna(X_train.mean())
    X_train_num = X_train.to_numpy()
    classical_predictions = SPN.SPN(X_train_num, X_test_num, y_train, random_state)
    classical_acc = helper_functions.classical_accuracies(classical_predictions, y_test)

    return classical_acc, credal_acc_interval, credal_robust_acc

def run_experiment1(data: pd.DataFrame, filename: str):
    missing_data = [0, 5, 10, 20, 30]
    cross_validations = 10
    y = data['classes']
    y = pd.factorize(y)[0]
    X = data.drop(['classes'], axis=1)

    reproduction_dict = dict()

    for percentage in missing_data:
        for run in range(cross_validations):
            random_state_int = random.randint(0, 20000)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=random_state_int)
            X_train, random_state_missing = helper_functions.create_missing_data(X_train, percentage)
            NBC_acc, NCC_acc_interval, NCC_robust_acc = run_naive_classifiers(X_train, X_test, y_train, y_test)
            print(NBC_acc, NCC_acc_interval, NCC_robust_acc)
            tree_acc, credal_tree_acc = run_tree_classifiers(X_train, X_test, y_train, y_test)
            print(tree_acc, credal_tree_acc)
            SPN_acc, CSPN_acc_interval, CSPN_robust_acc = run_SPN_classifiers(X_train, X_test, y_train, y_test, random_state_int)
            print(SPN_acc, CSPN_acc_interval, CSPN_robust_acc)
            exit()
            reproduction_dict[(filename, missing_data, run)] = (random_state_int, random_state_missing)

def experiment1():
    abs_path = 'C:/Users/s164389/Desktop/Afstuderen/Thesis/UCI_data/'
    col_names = helper_functions.get_names_dict()

    for filename in os.listdir(abs_path):
        data = pd.read_csv(abs_path + filename, names=col_names[filename])
        run_experiment1(data, filename)
        exit()

    exit()


# iris_data = pd.read_csv('C:/Users/s164389/Desktop/Afstuderen/Thesis/UCI_data/iris.data', names=['sepal_l', 'sepal_w', 'petal_l', 'petal_w', 'classes'])
# iris_y = iris_data['classes']
# iris_y = pd.factorize(iris_y)[0]
# iris_X = iris_data.drop(['classes'], axis=1)

# X_train, X_test, y_train, y_test = train_test_split(iris_X, iris_y, test_size=0.30, random_state=42)
# # X_train, rs = helper_functions.create_missing_data(X_train, 10)

# X_train = X_train.to_numpy()

# # change y_train
# X_test = X_test.to_numpy()

# y_pred = SPN.SPN(X_train, y_train, X_test, random_state=42)
# print(y_test)
# print(y_pred)

# exit()
experiment1()