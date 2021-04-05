import inspect
from functools import partial
import utils
from utils import DictTree
import pickle

class Recorder(object):
    def __init__(self):
        self.trace = []

    def record(self, **kwargs):
        self.trace.append(kwargs)


class Skill(object):
    def __init__(self, model_name=None, arg_in_len=0, max_cnt=None, sub_skill_names=[], 
                    ret_out_len=0, min_valid_data=None, sub_arg_accuracy=None):
        self.model_name = model_name
        self.arg_in_len = arg_in_len
        self.max_cnt = max_cnt
        self.sub_skill_names = sub_skill_names
        self.ret_out_len = ret_out_len
        self.min_valid_data = min_valid_data
        self.sub_arg_accuracy = sub_arg_accuracy

        # self.name = skill_func.__name__
        # self.skill_func = skill_func

        # print(self.name)

    def __get__(self, instance, owner):

        # print('get here')
        output = partial(self.__call__, instance)
        # setattr(output, "__name__", self.name)
        return output

    def __call__(self, func):  
        # print("classnfunc", func)
        self.name = func.__name__
        self.func = func
        # classIns = classnfunc[0] if len(classnfunc)==2 else None
        # print(dir(args[0]))
        def wrapper(*args):
            print("name", func.__name__)
            save_arg_in_len = self.arg_in_len
            save_ret_out_len = self.ret_out_len

            classIns = args[0]

            cnt = [0]
            ret_name = [None]
            ret_val = [None]

            for caller in inspect.stack()[1:]:
                caller_locals = caller[0].f_locals
                # print("caller_locals:",caller_locals)
                if ('self' in caller_locals) and isinstance(caller_locals['self'], Skill):
                    # do I need to do it here or do it after calling the function,, we need obs(return value of current function)
                    # sub_name, sub_arg = self.skillset[top.name].step(top.arg, top.cnt, ret_name, ret_val, obs)

                    recorder = caller_locals['recorder']
                    recorder.record(
                        name= caller_locals['self'].name,
                        arg= caller_locals['args'][1:],   ## start from the second arg because all the skills' first argument is self
                        cnt= caller_locals['cnt'][0],
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

            ####################################
            ### start preparing for training ###
            ####################################
            ###For here, it did not support function method
            # print(classIns)
            print("classIns", dir(classIns))
            skill = classIns.skillset[self.name] if hasattr(classIns, 'skillset') else 0 # get the trained function
            if skill!=0 and skill.step!=0:#if in training stage
                trained_function = skill.step
                # if hasattr(classIns, 'skillset'):
                #     print(classIns.skillset[self.name])
                skill.model_name = self.model_name if self.model_name!=None else classIns.default_model_name
                skill.arg_in_len = self.arg_in_len
                skill.max_cnt = self.max_cnt
                skill.sub_skill_names = self.sub_skill_names
                skill.ret_out_len = self.ret_out_len
                skill.min_valid_data = self.min_valid_data
                skill.sub_arg_accuracy = self.sub_arg_accuracy

                ### ret_in_len arg_out_len
                # print("checkcheck", self.sub_skill_names[0])
                # print("checkglobals", getattr(classIns, self.sub_skill_names[0]).skill.arg_in_len)
                if [subSkill for subSkill in self.sub_skill_names if hasattr(classIns, subSkill)]:
                    skill.ret_in_len = max([getattr(classIns, subSkill).skill.arg_in_len for subSkill in self.sub_skill_names if hasattr(classIns, subSkill)])
                    skill.arg_out_len = max([getattr(classIns, subSkill).skill.ret_out_len for subSkill in self.sub_skill_names if hasattr(classIns, subSkill)])
                else:
                    skill.ret_in_len = 0
                    skill.arg_out_len = 0
     
                sub_name = None
                sub_args = None
                rvals = None
                # print(arg[0].)

                if caller_locals == None:  # if root skill
                    sub_name = self.func
                    sub_args = args
                else:
                    # print("caller_locals: ", caller_locals)
                    # print(caller_locals['args'], 
                    #     caller_locals['cnt'], caller_locals['ret_name'], 
                    #     caller_locals['ret_val'], None, skill)
                    print(self.name)
                    print("input: ",caller_locals['args'][1:], 
                        caller_locals['cnt'], caller_locals['ret_name'][0], 
                        caller_locals['ret_val'][0], [0], skill)
                    sub_name, sub_args = trained_function(caller_locals['args'][1:], 
                        caller_locals['cnt'], caller_locals['ret_name'][0], 
                        caller_locals['ret_val'][0], [0], skill)
                    sub_name = getattr(classIns, sub_name)
                rvals = sub_name(*sub_args)
            else: #if in predicting stage
                #we did not handle the situation if it is function skill
                rvals = self.func(*args)

            if caller_locals is not None: 
                caller[0].f_locals['ret_name'][0] = self.name
                caller[0].f_locals['ret_val'][0] = rvals
            else:
                return recorder.trace
                # TODO: dump recorder
            return rvals
        wrapper.skill = self
        return wrapper


# def Skill(model_name=None, arg_in_len=0, max_cnt=None, sub_skill_names=[], 
#                     ret_out_len=0, min_valid_data=None, sub_arg_accuracy=None):
#     # if function:
#     #     return _Skill(function)
#     # else:
#     # print(function)
#     def wrapper(function):
#         return _Skill(function, model_name=model_name, arg_in_len=arg_in_len, max_cnt=max_cnt, sub_skill_names=sub_skill_names, 
#                 ret_out_len=ret_out_len, min_valid_data=min_valid_data, sub_arg_accuracy=sub_arg_accuracy)
#     return wrapper

class SkillSet(object):
    pass

class HierarchicalAgent(SkillSet):
    default_model_name = "log_poly2"
    def __init__(self, domain, task, data, teacher, env):
        self.default_model_name = "log_poly2"
        SkillSet.__init__(self)
        # self.default_model_name = "log_poly2"
        self.skills = [i for i in dir(self)[:dir(self).index("__class__")]]  ##use raise error here
        # print(self.skills)
        # print("teacher:", teacher)
        self.skillset = dict({skill : DictTree(step= load_skill(domain, task, data, skill) if teacher else 0)
        for skill in (self.skills)})
        # print(self.skillset)
        # for skill in (self.skills + env.actions)})

        self.task_name = task
        self.domain_name = domain

        self.env = env


def load_skill(domain, task, data, skill_name):
    model = pickle.load(open("{}/{}/{}/{}.pkl".format(data, domain, task, skill_name), 'rb'))

    def step(arg, cnt, ret_name, ret_val, obs, skill):  ## we dont need obs here for now
        if arg is not None:
            print(arg)
            print(arg[skill.arg_in_len:])
            assert not any(arg[skill.arg_in_len:])
            arg = arg[:skill.arg_in_len]
        if ret_val is not None:
            assert not any(ret_val[skill.ret_in_len:])
            ret_val = ret_val[:skill.ret_in_len]
        sub_skill_names = [None] + skill.sub_skill_names
        iput = (list(utils.pad(arg, skill.arg_in_len)) + [cnt]
                + utils.one_hot(sub_skill_names.index(ret_name), len(sub_skill_names))
                + utils.pad(ret_val, skill.ret_in_len)
                + obs)
        print(iput)
        oput = model.predict([iput])
        sub_name = sub_skill_names[oput.sub[0]]
        sub_arg = list(oput.arg[0])
        if sub_name is None:
            return None, sub_arg
        else:
            assert not any(sub_arg[skill.arg_out_len:])
            sub_arg = sub_arg[:skill.arg_out_len]
            return sub_name, sub_arg

    return step




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
