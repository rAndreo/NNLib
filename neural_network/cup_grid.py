from grid_search import GridSearch
import numpy as np
import sys


train_set = np.genfromtxt("../cup/ML-CUP18-TR.csv", delimiter=",")[:, 1:-2]
train_targets = np.genfromtxt("../cup/ML-CUP18-TR.csv", delimiter=",")[:, -2:]

n_units = int(sys.argv[1])
layers = [(n_units, n_units, 2), (n_units, 2*n_units, 2)]
param_grid = {
    'layers': layers,
    'activation': ['sigmoid'],
    'lr': [0.001, 0.0005, 0.0001],
    'l2_lambda': [None],
    'epoch': [5000],
    'patience': [200],
    'test_size': [0.3],
    'batch_size': [64, 128],
    'momentum': [0.9],
    'dropout': [[0.5, 0.5, 0.5]],
    'nesterov': [False, True],
    'lr_sched': [(1, 1), (0.7, 50), (0.9, 100)]
}

gs = GridSearch(task='Regression', tuning_params=param_grid, restarts=10)
gs.fit(train_set, train_targets, checkpoints='../cup/'+str(n_units)+'units_cup_results_dropout')
