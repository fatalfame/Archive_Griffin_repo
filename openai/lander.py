import time
import numpy as np
import random
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import NotFittedError
from IPython.display import clear_output
from functools import lru_cache
import itertools

import gym

env = gym.make('LunarLander-v2')

model = MLPRegressor((40, 80, 40, 40), learning_rate='adaptive')


def bin_a(a):
    a_bool = np.zeros(env.action_space.n)
    a_bool[a] = 1
    return a_bool


def q(s, a):
    try:
        return model.predict(np.hstack([s, bin_a(a)]).reshape(1, 12))[0]
    except NotFittedError:
        return 0


def best_move(s, actions):
    return max(actions, key=lambda a: q(s, a))


def mc(observed_sar, discount=0.99, learning_rate=0.99):
    mc_sav = []
    for i in range(len(observed_sar)):
        s, a, _r, _d = observed_sar[i]
        qsa = q(s, a)
        g = 0
        for j in range(len(observed_sar) - i):
            g += (discount ** j) * observed_sar[i + j][2]
            if observed_sar[i + j][3]:
                break
        mc_value = qsa + learning_rate * (g - qsa)
        mc_sav.append((s, a, mc_value))
    assert len(mc_sav) == len(observed_sar)
    return mc_sav


def update_model(mc_sav):
    model.partial_fit(
        np.vstack([np.hstack([s, bin_a(a)]).reshape(1, 12) for s, a, _v in mc_sav]),
        np.vstack([v for _s, _a, v in mc_sav]),
    )


def avg(iterable):
    return sum(iterable) / len(iterable)


actions = list(range(env.action_space.n))

episode_rewards = [0]
episode_rewards_limit = 200
episode_lengths = [0]
deltas = [0]
past_observed_sar = []
obs_limit = 0


def episode(explore=0.1, render=True):
    random.shuffle(actions)
    current_state = env.reset()
    observed_sar = []
    for step in itertools.count(1):
        a = best_move(current_state, actions)
        if random.random() < explore:
            a = random.choice(actions)
        new_state, reward, done, info = env.step(a)
        if render:
            env.render()
        observed_sar.append((current_state, a, reward, done))

        if done:
            return observed_sar
        current_state = new_state


try:
    for episode_n in itertools.count(0):
        clear_output(True)
        print(episode_n, len(past_observed_sar))
        a = avg(episode_lengths[:int(episode_rewards_limit / 2)])
        b = avg(episode_rewards[:int(episode_rewards_limit / 2)])
        c = avg(episode_lengths[-int(episode_rewards_limit / 2):])
        d = avg(episode_rewards[-int(episode_rewards_limit / 2):])
        if episode_n < 10:
            max_d = -999999999
        max_d = max(max_d, d)
        deltas.append(abs(b - d))
        deltas = deltas[-int(episode_rewards_limit):]
        if avg(deltas) == 0:
            explore = 0
        else:
            explore = max((b - d) / avg(deltas) / 10, 0)
        print('Oldest rewards:',
              '{:.2f}'.format(a),
              '{:.2f}'.format(b),
              )
        print('Newest rewards:',
              '{:.2f}'.format(c),
              '{:.2f}'.format(d),
              '{:.2f}'.format(max_d),
              )
        print('Explore:', '{:.2f}'.format(explore), '{:.2f}'.format(avg(deltas)))
        print('Learning rate:', model.learning_rate_init)
        render = episode_n % 25 == 0
        observed_sar = episode(explore=1 - episode_n / 500, render=episode_n % 10 == 0 or max_d > 0)
        past_observed_sar.extend(observed_sar)
        obs_limit += len(observed_sar) / 5
        past_observed_sar = past_observed_sar[-int(round(obs_limit)):]
        last_max_d = max_d
        episode_rewards.append(sum(i[2] for i in observed_sar))
        episode_lengths.append(len(observed_sar))
        episode_rewards = episode_rewards[-int(episode_rewards_limit):]
        episode_lengths = episode_lengths[-int(episode_rewards_limit):]
        update_model(mc(past_observed_sar))
finally:
    env.close()