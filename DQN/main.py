
import matplotlib.pyplot as plt
import gym
import numpy as np


import csv
import datetime as dt

from environment import Environment
from agent import Agent
from randomAgent import RandomAgent


def get_rand_agent_memory(env, actionsCount):
    randAgent = RandomAgent(actionsCount)
    while randAgent.memory.is_full():
        env.run(randAgent)

    return randAgent.memory


def init_CartPole():
    CartPoleProb = "CartPole-v1"
    env = Environment(CartPoleProb, normalize=False, render=False)

    stateDataCount = env.env.observation_space.shape[0]
    actionsCount = env.env.action_space.n

    print("\nState Data Count:", stateDataCount)
    print("Action Count:", actionsCount)

    agent = Agent(stateDataCount, actionsCount, min_eps=0.01)
    agent.memory = get_rand_agent_memory(env, actionsCount)

    return agent, env


#def run_alg(stateDataCount, actionsCount):


def init_MountainCar():
    MountainProb ="MountainCarContinuous-v0"
    env = Environment(MountainProb, normalize=True, render=True)

    stateDataCount = env.env.observation_space.shape[0]
    actionsCount = env.env.action_space.shape[0]

    print("\nState Data Count:", stateDataCount)
    print("Action Count:", actionsCount)

    agent = Agent(stateDataCount, actionsCount, min_eps=0.1)
    agent.memory = get_rand_agent_memory(env, actionsCount)

    return agent, env


def main():
    agent, env = init_CartPole()

    print("\nStart")

    # initialize the csv 
    folder = 'results/'
    nameResult = env.name + '-' + dt.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    fileNetPath = folder + nameResult + '.h5'
    fileCsvPath = folder + nameResult + '.csv'

    with open(fileCsvPath, 'w', newline='') as csvfile:
        fieldnames = ['episode', 'reward', 'q-value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        try:
            results = []

            for episode in range(5000):


                q_results = agent.get_and_reinit_q_results()
                results.append({
                    fieldnames[0]: episode + 1,
                    fieldnames[1]: env.run(agent),
                    fieldnames[2]: np.mean(q_results)
                })

                if episode % 250 == 0:
                    writer.writerows(results)
                    results = []

        finally:
            writer.writerows(results)
            agent.brain.model.save(fileNetPath)

    print("End\n")

if __name__ == "__main__":
    main()