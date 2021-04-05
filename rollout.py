#roll_out.py
import agents
import envs
from utils import DictTree

import argparse
import os
import pickle
import time

action_name = ['MoveArm', "MoveBaseAbs", "MoveBaseRel", "MoveGripper", "MoveHead", 'LocateObject', 'LocateMarkers']

def update_trace(trace):
    output = []
    steps = []
    for i in trace:
        steps.append(DictTree(i))
        print(i.keys())
        print(i['sub_name'])
        if i['sub_name'] in action_name:
            info = DictTree({
                'steps': steps
            })
            dt = DictTree({
                'info': info,
                'act_name': i['sub_name'],
                'act_arg': i['sub_arg']
            })
            output.append(dt)

            #reset
            steps = []
    return output

def rollout(config):
    print(0)
    env = envs.catalog(config.domain)
    agent = agents.catalog(config.domain, config.task, config.data, config.teacher, env)
    init_arg = env.init_arg(config.task)

    trace = agent.root_skill(*init_arg)
    
    trace = update_trace(trace)
    print(trace)

    try:
        os.makedirs("{}/{}".format(config.data, config.domain))
    except OSError:
        pass
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    pickle.dump(trace, open("{}/{}/{}.{}.pkl".format(config.data, config.domain, config.task, time_stamp), 'wb'), protocol=2)
    print("=== trace saved ===")
    input("Press Enter to continue...")

if __name__ == '__main__':
    # model = pickle.load(open("model/dishes/ClearTable/MoveObject.pkl", 'rb'))
    # print(model)
    # print(update_trace(model))


    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', required=True)
    parser.add_argument('--task', required=True)
    parser.add_argument('--data')
    parser.add_argument('--teacher', action='store_true')
    args = parser.parse_args()
    print(args.teacher, type(args.teacher))
    rollout(args)

