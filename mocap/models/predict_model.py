import numpy as np
import pandas as pd
from colorama import Fore, Style

from scipy import stats

from sklearn import preprocessing

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Reshape
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers import ConvLSTM2D
from keras.layers import BatchNormalization


from sklearn.model_selection import train_test_split



# 10s interval for 200 training example
time_steps = 1500
# 20 samples/second
step = 500

def create_segments_and_labels(df, time_steps, step, label):

    # x, y, z acceleration as features
    n_features = 3
    # Each generated sequence contains 200 training examples
    segments = []
    labels = []
    for i in range(0, len(df) - time_steps, step):
        xs = df['Accelerometer_x_WD'].values[i: i + time_steps]
        ys = df['Accelerometer_y_WD'].values[i: i + time_steps]
        zs = df['Accelerometer_z_WD'].values[i: i + time_steps]
        # Retrieve the most often used label in each segment
        label = stats.mode(df['Class_label'][i: i + time_steps])[0][0]
        segments.append([xs, ys, zs])
        labels.append(label)

    # Bring the segments into a better shape
    reshaped_segments = np.asarray(segments, dtype= np.float32).reshape(-1, time_steps, n_features)
    labels =np.asarray(pd.get_dummies(labels), dtype = np.float32)

    return reshaped_segments, labels


"""
X_train_res, X_test_res, y_train_res, y_test_res = train_test_split(reshaped_segments, labels, test_size=0.25, stratify=labels, random_state=911)
"""


num_classes = 7
time_steps = time_steps
input_shape = X_train_res.shape[1:]
n_neuron= n_neurons

def make_bare_dnn_model(n_neurons):
  model = Sequential()
  model.add(Reshape((time_steps, 3), input_shape=(input_shape,)))
  model.add(Dense(n_neurons, activation='relu'))
  model.add(Dense(n_neurons, activation='relu'))
  model.add(Dense(n_neurons, activation='relu'))
  model.add(Flatten())
  model.add(Dense(num_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model

lstm_neurons= lstm_neurons
dense_neurons= dense_neurons
drop_out= drop_out

def make_lstm_dense_model(lstm_neurons, dense_neurons, drop_out):
  model = Sequential()
  model.add(Reshape((time_steps, 3), input_shape=(input_shape,)))
  model.add(LSTM(lstm_neurons, input_shape=(input_shape,)))
  model.add(Dropout(drop_out))
  model.add(Dense(dense_neurons, activation='relu'))
  model.add(Dense(num_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model


def make_lstm_stack_model(lstm_neurons):
  model = Sequential()
  model.add(LSTM(lstm_neurons, return_sequences=True, stateful = True,
                 batch_input_shape=(batch_size, 200, 3)))
  model.add(LSTM(lstm_neurons, return_sequences=True, stateful = True))
  model.add(LSTM(lstm_neurons, stateful = True))
  model.add(Dense(num_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model


def make_cnn_lstm_model(lstm_neurons,dense_neurons,drop_out):
  model = Sequential()
  model.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu'),
                            input_shape=(None,n_length,n_features)))
  model.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu')))
  model.add(TimeDistributed(Dropout(drop_out)))
  model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
  model.add(TimeDistributed(Flatten()))
  model.add(LSTM(lstm_neurons))
  model.add(Dropout(drop_out))
  model.add(Dense(dense_neurons, activation='relu'))
  model.add(Dense(num_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model


def make_conv_lstm_model(dense_neurons,drop_out):
  model = Sequential()
  model.add(ConvLSTM2D(filters=64, kernel_size=(1,3), activation='relu',
                       input_shape=(n_steps, 1, n_length, n_features)))
  model.add(Dropout(drop_out))
  model.add(Flatten())
  model.add(Dense(dense_neurons, activation='relu'))
  model.add(Dense(num_classes, activation='softmax'))
  model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model



def train_model(model: Model,
                X: np.ndarray,
                y: np.ndarray,
                batch_size=16,
                patience=2,
                validation_split=0.3,
                validation_data=None) -> Tuple[Model, dict]:
    """
    Fit model and return a the tuple (fitted_model, history)
    """

    print(Fore.BLUE + "\nTrain model..." + Style.RESET_ALL)

    es = EarlyStopping(monitor="val_loss",
                       patience=patience,
                       restore_best_weights=True,
                       verbose=0)

    history = model.fit(X,
                        y,
                        validation_split=validation_split,
                        validation_data=validation_data,
                        epochs=1000,
                        batch_size=batch_size,
                        callbacks=[es],
                        verbose=0)

    print(f"\n✅ model trained ({len(X)} rows)")

    return model, history
