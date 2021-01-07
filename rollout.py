#roll_out.py
import agents
import envs
from utils import DictTree

import argparse
import os
import pickle
import time

def rollout(config):
    env = envs.catalog(config.domain)
    agent = agents.catalog(config.domain, env)
    init_arg = env.init_arg(config.task)

    trace = agent.root_skill(*init_arg)
    
    try:
        os.makedirs("{}/{}".format(config.data, config.domain))
    except OSError:
        pass
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    pickle.dump(trace, open("{}/{}/{}.{}.pkl".format(config.data, config.domain, config.task, time_stamp), 'wb'), protocol=2)
    print("=== trace saved ===")
    raw_input("Press Enter to continue...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', required=True)
    parser.add_argument('--task', required=True)
    # parser.add_argument('--model')
    parser.add_argument('--data')
    # parser.add_argument('--teacher', action='store_true')
    args = parser.parse_args()
    rollout(args)
