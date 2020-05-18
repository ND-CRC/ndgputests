#! /bin/env python3
import os
import sys
import getpass

# Add DeepSphere package from scratch365
# repository that was cloned in run_deepsphere.sh wrapper
sys.path.insert(0,'/scratch365/{user}/DeepSphere'.format(user=getpass.getuser()))

import os
import shutil

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import healpy as hp
import tensorflow as tf

from deepsphere import models, experiment_helper, plot
from deepsphere.data import LabeledDataset

plt.rcParams['figure.figsize'] = (17, 5)
EXP_NAME = 'whole_sphere'

from tensorflow.python.client import device_lib

print(device_lib.list_local_devices())

data = np.load('maps_downsampled_64.npz')
assert(len(data['class1']) == len(data['class2']))
nclass = len(data['class1'])

sample_psd_class1 = np.empty((nclass, 192))
sample_psd_class2 = np.empty((nclass, 192))

for i in range(nclass):
    sample_psd_class1[i] = experiment_helper.psd(data['class1'][i])
    sample_psd_class2[i] = experiment_helper.psd(data['class2'][i])
# Normalize and transform the data, i.e. extract features.
x_raw = np.vstack((data['class1'], data['class2']))
x_raw = x_raw / np.mean(x_raw**2) # Apply some normalization (We do not want to affect the mean)
x_psd = preprocessing.scale(np.vstack((sample_psd_class1, sample_psd_class2)))

# Create the label vector
labels = np.zeros([x_raw.shape[0]], dtype=int)
labels[nclass:] = 1

# Random train / test split
ntrain = 150
ret = train_test_split(x_raw, x_psd, labels, test_size=2*nclass-ntrain, shuffle=True)
x_raw_train, x_raw_test, x_psd_train, x_psd_test, labels_train, labels_test = ret

print('Class 1 VS class 2')
print('  Training set: {} / {}'.format(np.sum(labels_train==0), np.sum(labels_train==1)))
print('  Test set: {} / {}'.format(np.sum(labels_test==0), np.sum(labels_test==1)))
clf = SVC(kernel='rbf')
clf.fit(x_raw_train, labels_train) 

e_train = experiment_helper.model_error(clf, x_raw_train, labels_train)
e_test = experiment_helper.model_error(clf, x_raw_test, labels_test)
print('The training error is: {}%'.format(e_train*100))
print('The testing error is: {}%'.format(e_test*100))
clf = SVC(kernel='linear')
clf.fit(x_psd_train, labels_train) 

e_train = experiment_helper.model_error(clf, x_psd_train, labels_train)
e_test = experiment_helper.model_error(clf, x_psd_test, labels_test)
print('The training error is: {}%'.format(e_train*100))
print('The testing error is: {}%'.format(e_test*100))
params = dict()
params['dir_name'] = EXP_NAME

# Types of layers.
params['conv'] = 'chebyshev5'  # Graph convolution: chebyshev5 or monomials.
params['pool'] = 'max'  # Pooling: max or average.
params['activation'] = 'relu'  # Non-linearity: relu, elu, leaky_relu, softmax, tanh, etc.
params['statistics'] = None  # Statistics (for invariance): None, mean, var, meanvar, hist.

# Architecture.
architecture = 'fully_convolutional'

if architecture == 'classic_cnn':
    params['statistics'] = None
    params['nsides'] = [64, 32, 16, 16]  # Pooling: number of pixels per layer.
    params['F'] = [5, 5, 5]  # Graph convolutional layers: number of feature maps.
    params['M'] = [50, 2]  # Fully connected layers: output dimensionalities.

elif architecture == 'stat_layer':
    params['statistics'] = 'meanvar'
    params['nsides'] = [64, 32, 16, 16]  # Pooling: number of pixels per layer.
    params['F'] = [5, 5, 5]  # Graph convolutional layers: number of feature maps.
    params['M'] = [50, 2]  # Fully connected layers: output dimensionalities.

elif architecture == 'fully_convolutional':
    params['statistics'] = 'mean'
    params['nsides'] = [64, 32, 16, 8, 8]
    params['F'] = [5, 5, 5, 2]
    params['M'] = []

params['K'] = [10] * len(params['F'])  # Polynomial orders.
params['batch_norm'] = [True] * len(params['F'])  # Batch normalization.

# Regularization.
params['regularization'] = 0  # Amount of L2 regularization over the weights (will be divided by the number of weights).
params['dropout'] = 0.5  # Percentage of neurons to keep.

# Training.
params['num_epochs'] = 12  # Number of passes through the training data.
params['batch_size'] = 16  # Number of samples per training batch. Should be a power of 2 for greater speed.
params['eval_frequency'] = 15  # Frequency of model evaluations during training (influence training time).
params['scheduler'] = lambda step: 1e-1  # Constant learning rate.
params['optimizer'] = lambda lr: tf.train.GradientDescentOptimizer(lr)
#params['optimizer'] = lambda lr: tf.train.MomentumOptimizer(lr, momentum=0.5)
#params['optimizer'] = lambda lr: tf.train.AdamOptimizer(lr, beta1=0.9, beta2=0.999, epsilon=1e-8)

model = models.deepsphere(**params)

# Cleanup before running again.
shutil.rmtree('summaries/{}/'.format(EXP_NAME), ignore_errors=True)
shutil.rmtree('checkpoints/{}/'.format(EXP_NAME), ignore_errors=True)

training = LabeledDataset(x_raw_train, labels_train)
testing = LabeledDataset(x_raw_test, labels_test)
accuracy_validation, loss_validation, loss_training, t_step = model.fit(training, testing)

error_train = experiment_helper.model_error(model, x_raw_train, labels_train)
error_test = experiment_helper.model_error(model, x_raw_test, labels_test)
print('The training error is: {:.2%}'.format(error_train))
print('The testing error is: {:.2%}'.format(error_test))

