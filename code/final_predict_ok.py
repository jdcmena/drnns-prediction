## Loads best checkpointed model and makes prediciton on test set

from __future__ import print_function
import sys
import math
import numpy as np
from itertools import product
import cPickle as pkl

from keras import backend as K
from keras.utils.visualize_util import plot, model_to_dot
from keras.models import Sequential
from keras.layers import GRU, Dense, Masking, Dropout, Activation
from keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
from keras.optimizers import RMSprop

from utils import set_trace, plot_ROC

# Load saved data

print('Load saved test data')

X_test = pkl.load(open('data/X_test.np', 'rb'))

y_test = pkl.load(open('data/y_test.np', 'rb'))

# Define network structure

nb_timesteps = 1 
nb_classes = 2
nb_features = X_test.shape[1]
output_dim = 1

# Define cross-validated model parameters

batch_size = 13
dropout = 0.5
activation = 'sigmoid'
nb_hidden = 128
initialization = 'glorot_normal'

# # Reshape X to three dimensions
# # Should have shape (batch_size, nb_timesteps, nb_features)

X_test = np.resize(X_test, (X_test.shape[0], nb_timesteps, X_test.shape[1]))

print('X_test shape:', X_test.shape)

# Reshape y to two dimensions
# Should have shape (batch_size, output_dim)

y_test = np.resize(y_test, (X_test.shape[0], output_dim))

print('y_test shape:', y_test.shape)

# Initiate sequential model

print('Initializing model')

model = Sequential()

# Stack layers
# expected input batch shape: (batch_size, nb_timesteps, nb_features)
# note that we have to provide the full batch_input_shape since the network is stateful.
# the sample of index i in batch k is the follow-up for the sample i in batch k-1.
model.add(Masking(mask_value=0., batch_input_shape=(batch_size, nb_timesteps, nb_features))) # embedding for variable input lengths
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization,
               batch_input_shape=(batch_size, nb_timesteps, nb_features)))
model.add(Dropout(dropout))  
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout))
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout)) 
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout)) 
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout)) 
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout))
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout))
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout))
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout))
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout))
model.add(GRU(nb_hidden, return_sequences=True, stateful=True, init=initialization))  
model.add(Dropout(dropout))
model.add(GRU(nb_hidden, stateful=True, init=initialization))  
model.add(Dropout(dropout)) 
model.add(Dense(output_dim, activation=activation))

# Visualize model

plot(model, to_file='results/final_model.png', # Plot graph of model
  show_shapes = True,
  show_layer_names = False)

model_to_dot(model,show_shapes=True,show_layer_names = False).write('results/final_model.dot', format='raw', prog='dot') # write to dot file

# Load weights
model.load_weights(sys.argv[-1])

# Configure learning process

model.compile(optimizer='rmsprop',
              loss='mean_absolute_error',
              metrics=['mean_absolute_error'])

print("Created model and loaded weights from file")

# Evaluation 

print('Generate predictions on test data')

y_pred = model.predict(X_test, batch_size=batch_size, verbose=1) # generate output predictions for test samples, batch-by-batch

np.savetxt("gini-test-pred.csv", y_pred, delimiter=",")