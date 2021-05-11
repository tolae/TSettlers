import socket
import time
from time import sleep

import numpy as np
from messages import MessageFactory

from messages.Resource import ResourceHex

import DQN


class QEnv:
    def __init__(self):
        self._env = {}
        self._opponent_counter = 0

    def add_msg_to_env(self, msg):
        if msg.type() == MessageFactory.POSSIBILITIES:
            self._env['roads'] = msg.data().roads
            self._env['settlements'] = msg.data().settlements
            self._env['cities'] = msg.data().cities
            self._env['dev_cards'] = msg.data().dev_cards
        elif msg.type() == MessageFactory.ITEMS:
            player_num = self._opponent_counter if msg.data().player != 255 else 255
            self._opponent_counter = (self._opponent_counter + 1) % 3
            self._env['{}_longest_road_length'.format(player_num)] = msg.data().longest_road_length
            self._env['{}_knights_used'.format(player_num)] = msg.data().knights_used
        elif msg.type() == MessageFactory.RESOURCE_SET:
            self._env['Z_C'] = msg.data().clay
            self._env['Z_O'] = msg.data().ore
            self._env['Z_S'] = msg.data().sheep
            self._env['Z_T'] = msg.data().wheat
            self._env['Z_W'] = msg.data().wood
        elif msg.type() == MessageFactory.RESOURCE_PROD:
            self._env['R_C'] = msg.data().scaled[ResourceHex.CLAY]
            self._env['R_O'] = msg.data().scaled[ResourceHex.ORE]
            self._env['R_S'] = msg.data().scaled[ResourceHex.SHEEP]
            self._env['R_T'] = msg.data().scaled[ResourceHex.WHEAT]
            self._env['R_W'] = msg.data().scaled[ResourceHex.WOOD]

    def get_feature_vector(self):
        return np.array([
            self._env['roads'],
            self._env['settlements'],
            self._env['cities'],
            self._env['dev_cards'],
            self._env['Z_C'],
            self._env['Z_O'],
            self._env['Z_S'],
            self._env['Z_T'],
            self._env['Z_W'],
            self._env['R_C'],
            self._env['R_O'],
            self._env['R_S'],
            self._env['R_T'],
            self._env['R_W'],
            self._env['255_longest_road_length'],
            self._env['255_knights_used'],
            self._env['0_longest_road_length'],
            self._env['0_knights_used'],
            self._env['1_longest_road_length'],
            self._env['1_knights_used'],
            self._env['2_longest_road_length'],
            self._env['2_knights_used'],
        ])

    def reset_env(self):
        self._env.clear()
        self._opponent_counter = 0


class QServer:
    def __init__(self, host, port, use_learned=False):
        self.socket = None
        self.conn = None
        self.host = host
        self.port = port

        self.env = QEnv()
        self.agent = DQN.DQNAgent()
        self.prev_vector = None
        self.prev_action = None

        self.ep_rewards = []
        self.curr_episode = 0
        self.standing_log = "logs/agent_standings.csv"
        self.standing_results = [0, 0, 0, 0]

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            self.socket.bind((self.host, self.port))
            print("Bound and listening...")
            self.socket.listen()
            self.conn, addr = self.socket.accept()
            with self.conn:
                print('Connected by', addr)
                sleep(3)
                while True:
                    length = int.from_bytes(self.conn.recv(2), byteorder='big', signed=False)
                    message = MessageFactory.build({'length': length,
                                                    'type': int.from_bytes(
                                                        self.conn.recv(1),
                                                        byteorder='big',
                                                        signed=False
                                                    ),
                                                    'data': self.conn.recv(length)
                                                    })
                    print("Received: " + message.__str__())
                    self._handle_msg(message)

    def _handle_msg(self, msg):
        if msg.type() == MessageFactory.KEEP_ALIVE:
            pass  # TODO: Keep track of keep alive intervals for death
        elif msg.type() == MessageFactory.END_OF_GAME:
            self.end_of_game(msg)
        elif msg.type() == MessageFactory.UNKNOWN:
            print("Warning: Unknown message received! Ignoring...")
        elif msg.type() == MessageFactory.RESOURCE_SET:
            self.env.add_msg_to_env(msg)
        elif msg.type() == MessageFactory.RESOURCE_PROD:
            self.env.add_msg_to_env(msg)
        elif msg.type() == MessageFactory.ITEMS:
            self.env.add_msg_to_env(msg)
        elif msg.type() == MessageFactory.POSSIBILITIES:
            self.env.add_msg_to_env(msg)
        elif msg.type() == MessageFactory.PLAN:
            self.get_planned_action(msg)

    def get_planned_action(self, msg):
        feat_vector = self.env.get_feature_vector()
        if self.prev_vector is not None:
            self.agent.update_replay_memory((self.prev_vector, self.prev_action, 0, feat_vector, False))
            self.agent.train(False)
        else:
            print("First step. Ignoring training...")

        action = self.get_action(feat_vector)
        self.prev_vector = feat_vector
        self.prev_action = action

        package = {
            'type': msg.type(),
            'length': msg.length(),
            'data': action
        }

        msg_to_send = MessageFactory.build(package)
        self.conn.sendall(MessageFactory.to_bytearray(msg_to_send))

    def end_of_game(self, msg):
        reward = QServer._reward_func(msg.data()['VP'], msg.data()['Z'], msg.data()['Position'])
        self.write_result(msg.data()['Position'])
        print("Finished game with reward of: {}".format(reward))
        feat_vector = [0 for _ in self.prev_vector]
        self.agent.update_replay_memory((self.prev_vector, self.prev_action, reward, feat_vector, True))
        self.agent.train(True)

        self.prev_vector = None
        self.prev_action = None

        self.ep_rewards.append(reward)
        if not self.curr_episode % DQN.AGGREGATE_STATS_EVERY or self.curr_episode == 1:
            average_reward = sum(self.ep_rewards[-DQN.AGGREGATE_STATS_EVERY:])/len(self.ep_rewards[-DQN.AGGREGATE_STATS_EVERY:])
            min_reward = min(self.ep_rewards[-DQN.AGGREGATE_STATS_EVERY:])
            max_reward = max(self.ep_rewards[-DQN.AGGREGATE_STATS_EVERY:])
            loss = self.agent.history.history["loss"][0]
            accuracy = self.agent.history.history["accuracy"][0]
            self.agent.tensorboard.update_stats(loss=loss, accuracy=accuracy, reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward, epsilon=self.agent.epsilon)
            self.curr_episode += 1
            # Save model
            if(min_reward >= DQN.MIN_REWARD):
                self.agent.model.save(f'models/{DQN.MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')
        else:
            self.curr_episode += 1

        if self.agent.epsilon > self.agent.MIN_EPSILON:
            self.agent.epsilon *= self.agent.EPSILON_DECAY
            self.agent.epsilon = max(self.agent.MIN_EPSILON, self.agent.epsilon)

        self.env.reset_env()

    def get_action(self, state):
        state = np.array(state)
        state = state.reshape((1, 22))
        if np.random.random() > self.agent.epsilon:
            action = np.argmax(self.agent.get_qs(state))
        else:
            possible_actions = [4]
            if state[0, 0] > 0:
                possible_actions.append(0)
            if state[0, 1] > 0:
                possible_actions.append(1)
            if state[0, 2] > 0:
                possible_actions.append(2)
            if state[0, 3] > 0:
                possible_actions.append(3)
            action = np.random.choice(possible_actions)
        return action

    def write_result(self, place):
        self.standing_results[place-1] += 1
        with open(self.standing_log, "w+") as f:
            for res in self.standing_results:
                f.write(str(res) + '\n')

    @staticmethod
    def _reward_func(vp, z, position):
        earned_vp = vp - 2
        avg_z_per_vp = 9
        position_reward = {1: 5, 2: 0, 3: 0, 4: -5}
        reward = (earned_vp * avg_z_per_vp) / z + position_reward[position] - 1
        return reward
