import inspect
from functools import partial

class Recorder(object):
    def __init__(self):
        self.trace = []

    def record(self, **kwargs):
        self.trace.append(kwargs)


# def Skill(skillset):

class Skill(object):
    def __init__(self, skill_func):
        self.name = skill_func.__name__
        self.skill_func = skill_func
        print(self.name)

    def __get__(self, instance, owner):
        print('get here')
        return partial(self.__call__, instance)

    def __call__(self, *args):
        print(type(self))
        cnt = [0]
        ret_name = [None]
        ret_val = [None]

        for caller in inspect.stack()[1:]:
            caller_locals = caller[0].f_locals

            if ('self' in caller_locals) and isinstance(caller_locals['self'], Skill):
                recorder = caller_locals['recorder']
                recorder.record(
                    skill_name= caller_locals['self'].name,
                    skill_arg= caller_locals['args'][1:],   ## start from the second arg because all the skills' first argument is self
                    skill_cnt= caller_locals['cnt'][0],
                    ret_name= caller_locals['ret_name'][0],
                    ret_val= caller_locals['ret_val'][0],
                    sub_name= self.name,
                    sub_arg= args[1:])  ## start from the second arg because all the skills' first argument is self

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
            return recorder.trace
            # TODO: dump recorder
        return rvals

# class C(object):
#     @Skill
#     def moveObject(self):
#         print("move Object")
#         a = [1,2,3]
#         self.moveEverything()

#     def moveEverything(self):
#         print("move Everything")
#         self.moveTable()
#         self.moveChair()
#         self.moveCups()

#     @Skill
#     def moveTable(self):
#         print("move table")

#     @Skill
#     def moveChair(self):
#         print("move chair")

#     @Skill
#     def moveCups(self):
#         print("move Cups")

class SkillSet(object):
    pass

class HierarchicalAgent(SkillSet):
    def __init__(self, env):
        SkillSet.__init__(self)
        self.env = env