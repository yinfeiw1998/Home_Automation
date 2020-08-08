import functools


class HierarchicalAgent(object):
    def record(self, skill, args, rvals):
        # TODO: append to trace
        pass


def skill(f):
    @functools.wraps(f)
    def wrapper(agent, *args):
        rvals = f(*args)
        agent.record(f, args, rvals)
        return rvals

    return wrapper
