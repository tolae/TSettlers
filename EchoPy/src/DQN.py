import os
import random
import time
from collections import deque
import numpy as np

import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.python.keras.layers import Conv1D, MaxPooling1D
from tensorflow.python.keras.optimizer_v2.adam import Adam

OBSERVATION_SPACE_SIZE = (1, 22)
ACTION_SPACE_SIZE = 5
DISCOUNT = 0.99

REPLAY_MEMORY_SIZE = 50  # How many last steps to keep for model training
MIN_REPLAY_MEMORY_SIZE = 8  # Minimum number of steps in a memory to start training
MINIBATCH_SIZE = 4  # How many steps (samples) to use for training

UPDATE_TARGET_EVERY = 4  # Terminal states (end of episodes)
MODEL_NAME = 'TSettlerPlanning'
MIN_REWARD = 0 # Minimum reward to save
AGGREGATE_STATS_EVERY = 5


class ModifiedTensorBoard(TensorBoard):
    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.create_file_writer(self.log_dir)
        self._log_write_dir = self.log_dir

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        self.model = model

        self._train_dir = self.log_dir + "\\train"
        self._train_step = model._train_counter

        self._val_dir = os.path.join(self._log_write_dir, 'validation')
        self._val_step = self.model._test_counter

        self._should_write_train_graph = False

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)

    def _write_logs(self, logs, index):
        with self.writer.as_default():
            for name, value in logs.items():
                tf.summary.scalar(name, value, step=index)
                self.step += 1
                self.writer.flush()


class DQNAgent:
    def __init__(self):
        # Main model
        self.model = self.create_model()
        self.history = None

        # Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        # An array with last n steps for training
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        # Custom tensorboard object
        self.tensorboard = ModifiedTensorBoard(log_dir="logs/{}-{}".format(MODEL_NAME, int(time.time())))

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0

        #Exploration settings
        self.epsilon = 1  # not a constant, going to be decayed
        self.EPSILON_DECAY = 0.975
        self.MIN_EPSILON = 0.001

    def create_model(self):
        model = Sequential()

        model.add(Conv1D(256, kernel_size=1, input_shape=OBSERVATION_SPACE_SIZE, batch_input_shape=(MINIBATCH_SIZE, 1, 22)))
        model.add(Activation('relu'))
        model.add(MaxPooling1D(1))
        model.add(Dropout(0.2))

        model.add(Conv1D(256, 1))
        model.add(Activation('relu'))
        model.add(MaxPooling1D(1))
        model.add(Dropout(0.2))

        model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        model.add(Dense(64))

        model.add(Dense(ACTION_SPACE_SIZE, activation='linear'))  # ACTION_SPACE_SIZE = how many choices (9)
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    # Trains main network every step during episode
    def train(self, terminal_state):

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        # Get a minibatch of random samples from memory replay table
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Get current states from minibatch, then query NN model for Q values
        current_states = np.array([transition[0] for transition in minibatch])
        current_states = np.expand_dims(current_states, axis=0)
        current_states = current_states.reshape(MINIBATCH_SIZE, 1, -1)
        current_qs_list = self.model.predict(current_states)

        # Get future states from minibatch, then query NN model for Q values
        # When using target network, query it, otherwise main network should be queried
        new_current_states = np.array([transition[3] for transition in minibatch])
        new_current_states = np.expand_dims(new_current_states, axis=0)
        new_current_states = new_current_states.reshape(MINIBATCH_SIZE, 1, -1)
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        # Now we need to enumerate our batches
        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):

            # If not a terminal state, get new q from future states, otherwise set it to 0
            # almost like with Q Learning, but we use just part of equation here
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            # Update Q value for given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            # And append to our training data
            X.append(current_state)
            y.append(current_qs)

        X = np.expand_dims(X, axis=0)
        X = X.reshape(MINIBATCH_SIZE, 1, -1)
        # Fit on all samples as one batch, log only on terminal state
        self.history = self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=2, shuffle=False,
                       callbacks=[self.tensorboard] if terminal_state else None)

        # Update target network counter every episode
        if terminal_state:
            self.target_update_counter += 1

        # If counter reaches set value, update target network with weights of main network
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    # Queries main network for Q values given current observation space (environment state)
    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape))[0]
