#dishes.py
import math
import pickle

import hierarchical
import utils
from envs.dishes import DishesEnv
import hierarchy
import pyramid

PRETRAINED = False

V = 0.07
OMEGA = math.pi / 5.

@hierarchy.Skill
def MoveObjects(task_id):
    """
    arg: [task_id]
    ret_val: after MoveObject: [success]
    """
    MoveHome()
    
    for obj_cnt in range(6):
        MoveObject(task_id, obj_cnt)
#!!check what is [success]

@hierarchy.Skill
def MoveHome():
    """
    arg: None
    ret_val: None
    """
    MoveGripper(0)
    MoveArm(0.45,0.,0.,-math.pi / 2., -math.pi / 2.)
    MoveBaseAbs(0., 0., 0., V, OMEGA)


@hierarchy.Skill
def MoveObject(task_id, obj_cnt):
    """
    arg: [task_id, obj_cnt]
    ret_val: after PickObject: [obj_class, obj_color]
    """
    if task_id == 0:
        obj_class = DishesEnv.obj_classes.index(None)
        obj_color = DishesEnv.obj_colors.index(None)
        
        obj_class, obj_color = PickObject(obj_class, obj_color)
        return False # !check it

    elif task_id == 1:
        obj_class = [DishesEnv.obj_classes.index('plate'), DishesEnv.obj_classes.index('cup')][obj_cnt % 2]
        obj_color = [
                DishesEnv.obj_colors.index('blue'),
                DishesEnv.obj_colors.index('green'),
                DishesEnv.obj_colors.index('red'),
                DishesEnv.obj_colors.index('done'),
            ][obj_cnt / 2]

        obj_class, obj_color = PickObject(obj_class, obj_color) #Do we need to reture obj_class and color?
        PlaceObject(task_id, obj_class, obj_color)
    else:
        raise NotImplementedError
    return True #!check it


@hierarchy.Skill
def PickObject(obj_class, obj_color):
    """
    arg: [obj_class, obj_color]
    ret_val: after MoveToObject: [obj_class, obj_color]; after GraspObject: [obj_class, obj_color]
    """
    obj_class, obj_color = MoveToObject(object_class, obj_color, motion_cnt = 0)

    if DishesEnv.obj_classes[obj_class] is None: #if we find nothing do this
        return obj_class, obj_color #terminate the skill
    else:
        obj_class, obj_color = MoveToObject(obj_class, obj_color, motion_cnt = 1)

    obj_class, obj_color = GraspObject(obj_class, obj_color)

    return obj_class, obj_color


@hierarchy.Skill
def PlaceObject(task_id, obj_class, obj_color):
    """
    arg: [task_id, obj_class, obj_color]
    ret_val: None
    """
    if task_id == 0:
        [x, y, z, theta] = [0.2, 0., 0.55, math.pi / 2.]
    elif task_id = 1:
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
    
    MoveBaseAbs(x, y, theta, V, OMEGA)
    MoveArm(z, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
    MoveHome()


@hierarchy.Skill
def MoveToObject(obj_class, obj_color, motion_cnt):
    """
    arg: [obj_class, obj_color, motion_cnt]
    ret_val: after LocateObject: [obj_class, obj_color, obj_pixel_x, obj_pixel_y]; after MoveToLocation: [obj_class, obj_color]
    """
    MoveHead(-math.pi / 4., 0.)
    found_obj_class, found_obj_color, obj_pixel_x, obj_pixel_y = LocateObject(motion_cnt, obj_class, obj_color)
    if DishesEnv.obj_classes[found_obj_class] is None:
        return found_obj_class, found_obj_color
    else:
        obj_class, obj_color = MoveToLocation(found_obj_class, found_obj_color, obj_pixel_x, obj_pixel_y)
    return obj_class, obj_color


@hierarchy.Skill
def GraspObject(obj_class, obj_color):
    """
    arg: [obj_class, obj_color]
    ret_val: None
    """
    z = {
        'plate': 0.35,
        'cup': 0.4,
    }[DishesEnv.obj_classes[obj_class]]
    
    MoveArm(z, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
    MoveGripper(1)
    MoveArm(0.65, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
    return obj_class, obj_color



@hierarchy.Skill
def MoveToLocation(obj_class, obj_color, obj_pixel_x, obj_pixel_y):
    """
    arg: [obj_class, obj_color, obj_pixel_x, obj_pixel_y]
    ret_val: None
    """
    if PRETRAINED:
        [x, y, theta] = MoveToLocation.teacher_model.predict(
            [utils.one_hot({1: 1, 2: 3}[obj_class], len(DishesEnv.obj_classes) + 1) + [obj_pixel_x, obj_pixel_y]])[0]
        MoveBaseRel(x, y, theta, V, OMEGA)
    else:
        Record_MoveBaseRel() # this will be demonstrated by teleoperation
    return obj_class, obj_color




