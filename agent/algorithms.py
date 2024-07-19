"""The learning algorithm."""

import numpy as np
from agent.base import LFAControlAgent

class CDiscQAgent(LFAControlAgent):
    """
    Implements Naik et al. (2024)'s one-step Centered Q-learning algorithm
    (CDiscQ).
    """
    def __init__(self, **agent_args):
        super().__init__(**agent_args)

        # setting eta and gamma, the two main parameters of the algorithm
        self.eta = agent_args.get('eta', 0.1)
        self.gamma = agent_args.get('gamma', 0.95)

        # initializing the reward-rate estimate
        self.avg_reward_init = agent_args.get('avg_reward_init', 0)
        self.avg_reward = self.avg_reward_init

        # initializing the step size for the reward-rate estimate
        self.beta_sequence = agent_args.get('beta_sequence', 'exponential')
        assert self.beta_sequence in ['unbiased_trick', 'exponential', '1byN']
        if self.robust_to_initialization:
            self.beta_sequence = 'unbiased_trick'
        self.beta_init = self.eta * self.alpha_init
        if self.tilecoder:
            self.beta_init *= self.num_tilings
        
        # using the TD vs conventional error for updating the reward rate
        self.conv_error = agent_args.get("conv_error", False)


    def _update_weights(self, reward, obs, term_flag):
        past_sa = self._get_representation(self.past_obs, self.past_action)
        prediction = self._get_linear_value_approximation(past_sa)
        
        # compute the target
        if not term_flag:
            q_next = self._max_action_value(obs)
            target = reward - self.avg_reward + self.gamma * q_next
        else:
            target = reward - self.avg_reward
        delta = target - prediction
        
        # update the reward-rate estimate
        avg_rew_delta = delta if not self.conv_error else (reward - self.avg_reward)
        if self.robust_to_initialization:
            old_avg_reward = self.avg_reward
            self.avg_reward += self.beta * avg_rew_delta
            updated_target = target + (old_avg_reward - self.avg_reward)
            updated_delta = updated_target - prediction
        else:
            self.avg_reward += self.beta * avg_rew_delta
            updated_delta = delta

        # update the value estimates
        if self.tilecoder:
            self.weights[past_sa] += self.alpha * updated_delta
        else:
            self.weights += self.alpha * updated_delta * past_sa

    def _initialize_step_size(self):
        """Initializes both the step sizes."""
        super()._initialize_step_size()
        if self.beta_sequence == 'unbiased_trick':
            self.o_b = self.beta_init if self.beta_init != 0 else 1
            self.beta = self.beta_init / self.o_b
        else:
            self.beta = self.beta_init

    def _update_step_size(self):
        """Updates both the step sizes per step."""
        super()._update_step_size()
        if self.beta_sequence == 'exponential':
            self.beta *= self.alpha_decay_rate
        elif self.beta_sequence == 'unbiased_trick':
            self.o_b = self.o_b + self.beta_init * (1 - self.o_b)
            self.beta = self.beta_init / self.o_b
        else:
            self.beta = self.beta_init / self.update_count if self.skip_exploratory_update else self.beta_init / self.timestep
