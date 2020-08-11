class Recorder(object):
    def record(self, skill_name, skill_arg, skill_cnt, ret_name, ret_val, sub_name, sub_arg):
        # TODO: append to trace
        pass


class Skill(object):
    def __init__(self, f):
        self.name = f.__name__
        self.f = f

    def __call__(self, *args):
        cnt = 0
        for caller in call_stack:
            if isinstance(caller, Skill):
                self.recorder = caller.recorder
                self.recorder.record(
                    skill_name=caller.name,
                    skill_arg=caller.args,
                    skill_cnt=caller.cnt,
                    ret_name=caller.ret_name,
                    ret_val=caller.ret_val,
                    sub_name=self.name,
                    sub_arg=args)
                caller.cnt += 1
                break
        else:
            # root skill
            caller = None
            self.recorder = Recorder()
        rvals = self.f(*args)
        if caller is not None:
            caller.ret_name = self.name
            caller.ret_val = rvals
        else:
            # TODO: dump recorder
            pass
        return rvals


class Action(Skill):
    pass

# def skill(f):
#     @functools.wraps(f)
#     def wrapper(agent, *args):
#         rvals = f(*args)
#         agent.record(f, args, rvals)
#         return rvals
#
#     return wrapper
