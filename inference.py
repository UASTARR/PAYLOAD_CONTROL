"""Code to use the learned weights for inference."""

import numpy as np
from utils.helpers import get_weights_from_npy
from utils.tilecoder import TileCoder


class InferenceAgent():

    def __init__(self, weights_file_name='results/learned_weights.npy'):

        self.num_actions = 3
        self.actions = [-1, 0, 1]

        self.num_tilings = 4
        self.tiling_dims = [7]
        self.limits_per_dim = [[-15, 15]]

        self.tilecoder = TileCoder(
            tiling_dims=self.tiling_dims,
            limits_per_dim=self.limits_per_dim,
            num_tilings=self.num_tilings,
            style='indices'
            )
        self.num_features = self.tilecoder.n_tiles + 1

        self.weights = get_weights_from_npy(
            filename=weights_file_name,
            seed_idx=0
            )
        assert self.weights.size == self.num_features * self.num_actions

    def _get_value(self, observation, action):
        offset = self.num_features * action
        indices = np.array(observation + offset, dtype=int)
        value = np.sum(self.weights[indices])
        return value

    def choose_action(self, obs):
        observation = np.concatenate((self.tilecoder.getitem(obs), [self.num_features - 1]))
        q_s = np.array([self._get_value(observation, a) for a in range(self.num_actions)])
        action_index = np.argmax(q_s)      # can replace this with a cleverer version that matches the previous action in case of a tie
        return self.actions[action_index]


if __name__ == '__main__':
    test_agent = InferenceAgent(weights_file_name='results/test/linear_deroller_fins_initroll_0.npy')
    obs = [-2]
    action = test_agent.choose_action(obs)
    print(f'Rate of roll: {obs[0]}, Fin direction: {action}')
    obs = [0]
    action = test_agent.choose_action(obs)
    print(f'Rate of roll: {obs[0]}, Fin direction: {action}')
    obs = [2]
    action = test_agent.choose_action(obs)
    print(f'Rate of roll: {obs[0]}, Fin direction: {action}')
