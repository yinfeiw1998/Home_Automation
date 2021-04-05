#agent.py



class agent(object):
    def __init__(self, config, env):
        self.domain_name = config.domain_name
        self.task_name = config.task_name
        self.env = env

    def __repr__(self):
        return self.task_name

    def reset(self, init_arg):
        self.domain_name = init_arg.domain_name
        self.task_name = init_arg.task_name
    
    def assign_skill(self,func):
        setattr(self, func.__name__, func)
        self.__dict__[func.__name__] = Skill(self.__dict__[func.__name__])
        co_var = func.__code__.co_varnames
        if (co_var[0] == 'env') or (co_var[0] == 'self' and (co_var[1] == 'env')):
            self.__dict__[func.__name__] = partial(self.__dict__[func.__name__], self.env)
        else:
            raise Exception('env must be the first parameter of a Skill function')
        
    def assign_skillset(self, func_set):
        for func in func_set:
            self.assign_skill(func)