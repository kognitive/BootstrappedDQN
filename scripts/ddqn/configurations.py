import tensorflow as tf
from environments.GeneralOpenAIEnvironment import GeneralOpenAIEnvironment
from policies.impl.EpsilonGreedyPolicy import EpsilonGreedyPolicy

import util.extensions.tensorflow_extensions as tfh
from agents.impl.DDQNAgent import DDQNAgent
from memory.ExperienceReplayMemory import ExperienceReplayMemory
from policies.impl.GreedyPolicy import GreedyPolicy


def ddqn_general_ddqn_eps_config(env_name, max_timesteps, num_models):

        # Replay memory
        replay_size = 65000
        sample_size = 64

        # DQN
        structure = [256, 256]
        agent_config = {
                'discount': 0.99,
                'learning_rate': 0.00075,
                'target_offset': 2000,
        }

        # Exploration reduction
        exp_rate_begin = 1.0
        exp_rate_end = 0.1
        decay_lambda = 0.1

        env = GeneralOpenAIEnvironment(env_name, num_models)
        memories = [ExperienceReplayMemory(replay_size, sample_size, env) for _ in range(num_models)]
        agents = [DDQNAgent(env, structure, agent_config) for _ in range(num_models)]

        # obtain an exploration strategy
        exploration_parameters = [tfh.linear_decay(int(decay_lambda * 100000),
                                                 exp_rate_begin, exp_rate_end, agents[k].global_step) for k in range(num_models)]

        exploration_strategies = [EpsilonGreedyPolicy(env.action_space, exploration_parameters[k]) for k in range(num_models)]
        return [env, agents, memories, exploration_strategies, exploration_parameters], agent_config


def ddqn_general_ddqn_greedy_config(env_name, max_timesteps, num_models):

        # Replay memory
        replay_size = 50000
        sample_size = 64

        # DQN
        structure = [128, 128]
        agent_config = {
            'discount': 0.99,
            'learning_rate': 0.00025,
            'target_offset': 500,
        }

        env = GeneralOpenAIEnvironment(env_name, num_models)
        memories = [ExperienceReplayMemory(replay_size, sample_size, env) for _ in range(num_models)]
        agents = [DDQNAgent(env, structure, agent_config) for _ in range(num_models)]

        exploration_strategy = [GreedyPolicy() for k in range(num_models)]
        return [env, agents, memories, exploration_strategy, [tf.constant(0.0)]], agent_config