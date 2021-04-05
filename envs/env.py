#env.py
from agents import hierarchy

class Action(hierarchy.Skill):
    def __init__(self, model_name=None, arg_in_len=0, max_cnt=None, sub_skill_names=[], 
                    ret_out_len=0, min_valid_data=None, sub_arg_accuracy=None):
        super(Action, self).__init__(model_name=None, arg_in_len=0, max_cnt=None, sub_skill_names=[], 
                    ret_out_len=0, min_valid_data=None, sub_arg_accuracy=None)

# def Action(model_name=None, arg_in_len=0, max_cnt=None, sub_skill_names=[], 
#                     ret_out_len=0, min_valid_data=None, sub_arg_accuracy=None):
#     return hierarchy.Skill(model_name=model_name, arg_in_len=arg_in_len, max_cnt=max_cnt, sub_skill_names=sub_skill_names, 
#                     ret_out_len=ret_out_len, min_valid_data=min_valid_data, sub_arg_accuracy=sub_arg_accuracy)

