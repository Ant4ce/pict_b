import random
import numpy as np
import tensorflow as tf
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.regularizers import l1, l2
from tensorflow.keras.optimizers import Adam

def set_seeds(seed = 100):
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    
def cw(df):
    c0, c1, c2, c3, c4 = np.bincount(df["PredictionGroup"])
    w0 = (1/c0) * (len(df)) / 5
    w1 = (1/c1) * (len(df)) / 5
    w2 = (1/c2) * (len(df)) / 5
    w3 = (1/c3) * (len(df)) / 5
    w4 = (1/c4) * (len(df)) / 5

    return {0:w0, 1:w1, 2:w2, 3:w3, 4:w4 }

optimizer = Adam(lr = 0.00003)

def create_model(hl = 2, hu = 100, dropout = False, rate = 0.3, regularize = False,
                 reg = l1(0.0005), optimizer = optimizer, input_dim = None):
    if not regularize:
        reg = None
    model = Sequential()
    model.add(Dense(hu, input_dim = input_dim, activity_regularizer = reg ,activation = "relu"))
    if dropout: 
        model.add(Dropout(rate, seed = 100))
    for layer in range(hl):
        model.add(Dense(hu, activation = "relu", activity_regularizer = reg))
        if dropout:
            model.add(Dropout(rate, seed = 100))

    #model.add(Dense(1, activation = "sigmoid"))
    model.add(Dense(5, activation = "softmax"))
    model.compile(loss = "sparse_categorical_crossentropy", optimizer = optimizer, metrics = ["accuracy"])
    return model
