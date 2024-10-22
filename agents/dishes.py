#dishes.py
import math
import pickle

from agents.hierarchy import Skill
from agents.hierarchy import SkillSet
from agents.hierarchy import HierarchicalAgent
# import utils
from envs.dishes import DishesEnv
from agents import pyramid
# from envs import hsr

PRETRAINED = False

V = 0.07
OMEGA = math.pi / 5.

class DishesAgent(HierarchicalAgent):
    def __init__(self, domain, task, data, teacher, env):
        HierarchicalAgent.__init__(self, domain, task, data, teacher, env)
        self.default_model_name = "log_poly2"
        

    #TODO: what if more than one skillset for skill in a class
    @Skill(arg_in_len=1, sub_skill_names=['MoveHome', "MoveObject"], ret_out_len=0)
    def MoveObjects(skillset, task_id):  #root skill define in this class(with env) MoveObjects
        """
        arg: [task_id]
        ret_val: after MoveObject: [success]
        """
        # print("MoveObjects")
        skillset.MoveHome()
        
        for obj_cnt in range(6):
            skillset.MoveObject(task_id, obj_cnt)

    root_skill = MoveObjects

    @Skill(arg_in_len=0, sub_skill_names=["MoveGripper", "MoveArm", "MoveBaseAbs"], ret_out_len=0)
    def MoveHome(skillset):
        """
        arg: None
        ret_val: None
        """
        print("MoveHome")
        skillset.env.MoveGripper(0)
        skillset.env.MoveArm(0.45,0.,0.,-math.pi / 2., -math.pi / 2.)
        skillset.env.MoveBaseAbs(0., 0., 0., V, OMEGA)

    @Skill(model_name='table|log_poly2', arg_in_len=2, max_cnt=3, sub_skill_names=["PickOBject", "PlaceObject"], ret_out_len=1)
    def MoveObject(skillset, task_id, obj_cnt):
        """
        arg: [task_id, obj_cnt]
        ret_val: after PickObject: [obj_class, obj_color]
        """
        print("MoveObject")
        if task_id == 0:
            obj_class = DishesEnv.obj_classes.index(None)
            obj_color = DishesEnv.obj_colors.index(None)
            
            obj_class, obj_color = skillset.PickObject(obj_class, obj_color)
            if DishesEnv.obj_classes[obj_class] is None:
                return False
            else:
                skillset.PlaceObject(task_id, obj_class, obj_color)
                return True

        elif task_id == 1:
            obj_class = [DishesEnv.obj_classes.index('plate'), DishesEnv.obj_classes.index('cup')][obj_cnt % 2]
            obj_color = [
                    DishesEnv.obj_colors.index('blue'),
                    DishesEnv.obj_colors.index('green'),
                    DishesEnv.obj_colors.index('red'),
                    DishesEnv.obj_colors.index('done'),
                ][obj_cnt / 2]

            obj_class, obj_color = skillset.PickObject(obj_class, obj_color)
            if DishesEnv.obj_classes[obj_class] is None:
                return False
            else:
                skillset.PlaceObject(task_id, obj_class, obj_color)
                return True
        else:
            raise NotImplementedError

    @Skill(arg_in_len=2, sub_skill_names=["MoveToObject", "GraspOBject"], ret_out_len=2)
    def PickObject(skillset, obj_class, obj_color):
        """
        arg: [obj_class, obj_color]
        ret_val: after MoveToObject: [obj_class, obj_color]; after GraspObject: [obj_class, obj_color]
        """
        print("PickObject")
        obj_class, obj_color = skillset.MoveToObject(obj_class, obj_color, 0) # Motioncnt = 0

        if DishesEnv.obj_classes[obj_class] is None: #if we find nothing, do this
            return obj_class, obj_color #terminate the skill
        else:
            obj_class, obj_color = skillset.MoveToObject(obj_class, obj_color, 1) # Motioncnt = 1

        obj_class, obj_color = skillset.GraspObject(obj_class, obj_color)

        return obj_class, obj_color

    @Skill(arg_in_len=3, sub_skill_names=["MoveBaseAbs", "MoveArm", "MoveHome"], ret_out_len=0)
    def PlaceObject(skillset, task_id, obj_class, obj_color):
        """
        arg: [task_id, obj_class, obj_color]
        ret_val: None
        """
        print("PlaceObject")
        # print(obj_color)
        if task_id == 0:
            [x, y, z, theta] = [0.2, 0., 0.55, math.pi / 2.]
        elif task_id == 1:
            [x, y] = [
                None,
                [0., 0.2],
                [0.3, 0.2],
                [0.15, 0.],
            ][obj_color]
            y += {
                'plate': 0.,
                'cup': 0.06,
            }[DishesEnv.obj_classes[obj_class]]
            z = {
                'plate': 0.36,
                'cup': 0.41,
            }[DishesEnv.obj_classes[obj_class]]
            theta = math.pi / 2.
        else:
            raise NotImplementedError
        
        skillset.env.MoveBaseAbs(x, y, theta, V, OMEGA)
        skillset.env.MoveArm(z, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
        skillset.MoveHome()

    @Skill(model_name="t_log_poly2", arg_in_len=3, max_cnt=4, sub_skill_names=["MoveHead", "LocateObject", "MoveToLocation"], ret_out_len=2)
    def MoveToObject(skillset, obj_class, obj_color, motion_cnt):
        """
        arg: [obj_class, obj_color, motion_cnt]
        ret_val: after LocateObject: [obj_class, obj_color, obj_pixel_x, obj_pixel_y]; after MoveToLocation: [obj_class, obj_color]
        """
        print("MoveToObject")
        skillset.env.MoveHead(-math.pi / 4., 0.)
        # print("MoveHead")
        found_obj_class, found_obj_color, obj_pixel_x, obj_pixel_y = skillset.env.LocateObject(motion_cnt, obj_class, obj_color)
        if DishesEnv.obj_classes[found_obj_class] is None:
            return found_obj_class, found_obj_color
        else:
            obj_class, obj_color = skillset.MoveToLocation(found_obj_class, found_obj_color, obj_pixel_x, obj_pixel_y)
            return obj_class, obj_color

    @Skill(arg_in_len=2, sub_skill_names=["MoveArm", "MoveGripper"], ret_out_len=2)
    def GraspObject(skillset, obj_class, obj_color):
        """
        arg: [obj_class, obj_color]
        ret_val: None
        """
        print('GraspObject')
        z = {
            'plate': 0.35,
            'cup': 0.4,
        }[DishesEnv.obj_classes[obj_class]]
        
        skillset.env.MoveArm(z, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
        skillset.env.MoveGripper(1)
        skillset.env.MoveArm(0.65, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
        return obj_class, obj_color


    @Skill(arg_in_len=4, sub_skill_names=['MoveBaseRel'], ret_out_len=2)
    def MoveToLocation(skillset, obj_class, obj_color, obj_pixel_x, obj_pixel_y):
        """
        arg: [obj_class, obj_color, obj_pixel_x, obj_pixel_y]
        ret_val: None
        """
        print("MoveToLocation")
        # if PRETRAINED:
        #     [x, y, theta] = MoveToLocation.teacher_model.predict(
        #         [utils.one_hot({1: 1, 2: 3}[obj_class], len(DishesEnv.obj_classes) + 1) + [obj_pixel_x, obj_pixel_y]])[0]
        #     MoveBaseRel(x, y, theta, V, OMEGA)
        # else:
        #     Record_MoveBaseRel() # this will be demonstrated by teleoperation
        return obj_class, obj_color




