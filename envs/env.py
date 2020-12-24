#env.py
from agents import hierarchy

class Action(hierarchy.Skill):
    def __init__(self, skill_func):
        super(Action, self).__init__(skill_func)

