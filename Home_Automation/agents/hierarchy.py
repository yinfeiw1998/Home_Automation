import inspect

class Recorder(object):
    def __init__(self):
        self.trace = []

    def record(self, **kwargs):
        self.trace.append(kwargs)


class Skill(object):
    def __init__(self, skill_func):
        self.name = skill_func.__name__
        self.skill_func = skill_func

    def __call__(self, *args):
        cnt = [0]
        ret_name = [None]
        ret_val = [None]

        for caller in inspect.stack()[1:]:
            caller_locals = caller[0].f_locals

            if ('self' in caller_locals) and isinstance(caller_locals['self'], Skill):
                recorder = caller_locals['recorder']
                recorder.record(
                    skill_name= caller_locals['self'].name,
                    skill_arg= caller_locals['args'],
                    skill_cnt= caller_locals['cnt'][0],
                    ret_name= caller_locals['ret_name'][0],
                    ret_val= caller_locals['ret_val'][0],
                    sub_name= self.name,
                    sub_arg= args)

                caller_locals['cnt'][0] += 1
                break
        else:
            # root skill 
            caller_locals = None
            recorder = Recorder()

        rvals = self.skill_func(*args)

        if caller_locals is not None: 

            caller[0].f_locals['ret_name'][0] = self.name
            caller[0].f_locals['ret_val'][0] = rvals
        else:
            print(recorder.trace)
            # TODO: dump recorder
        return rvals


