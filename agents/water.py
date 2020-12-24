# water.py

import math
import pickle
import gazebo_getpos
import hierarchical
import utils

from envs import hsr

# Think about what model for each skill.
DEBUG = False
PRETRAINED = True
V = 0.07
OMEGA = math.pi / 5.
STATION_POSITION = [0.75, -2]
FAKE_WATER_LEVEL = 2
ARM_STAND_BY = [0, -0.6, -1.57, -1.57, 0.6]


""" Upper Level Skills"""

@hierarchical.Skill
def ServeTables(consta):
    """
    arg: [consta]
    ret_val:
    """
    MoveGripper(1.57)
    MoveArm(0, -0, -1.57, -1.57, 1.02)
    ServeTable()


@hierarchy.Skill
def ServeTable():
    """
    arg: None
    ret_val: region_list
    """
    region_list = [0] * 16
    region_list = InspectTable()
    region_list = GoStandBy(region_list)
    region_list = FillCups(region_list)
    FillCups(region_list)


@hierarchy.Skill
def GoStandBy(region_list)
    """
    arg: region_list
    ret_val: region_list
    """
    region_list[0:8] = [1] + [0] * 7
    hsr.MoveBaseAbs(0, -1.2, 1.57, V, OMEGA)
    hsr.MoveBaseAbs(0.375, -1.2, 1.57, V, OMEGA)
    return region_list

#not really sure
@hierarchy.Skill
def InspectTable():
    """
    arg:
    ret_val: region_list from LookAtTable, Move_succeed from GoToTable
    """
    region_list = [0] * 16
    motion_cnt = 1
    motion_cnt, region_list = GoToTable(motion_cnt, region_list)
    motion_cnt, region_list = LookAtTable(motion_cnt, region_list)
    motion_cnt += 1
    motino_cnt, region_list = GoToTable(motion_cnt, region_list)
    return region_list

#not really sure
@hierarchy.Skill
def FillCups(region_list):
    """
    arg:region list
    ret_val:
    """
    region_list = ReturnRegionList(region_list)
    while(sum(region_listp[8:16])!=0):
        region_list = FillCupsWrapper(region_list)
        region_list = FillCup(region_list)      ###not sure the return value
        region_list = ScanTable(region_list)



@hierarchy.Skill
def FillCupsWrapper(region_list):
    """
    arg: region_list
    ret_val:
    """
    #region_list = arg[0:16]

    water_level, is_refilled = EnsureWaterAmount(region_list[0:8])
    destin_region, water_level, is_refilled = SelectNextRegionWrapper(region_list, water_level, is_refilled)
    curr_region = region_list[0:8]
    #changes: in original file, return value has to arguments and comment shows only one of them
    water_level, destin_region = MoveNextRegion(curr_region, destin_region, water_level, is_refilled)
    region_list[0:8] = destin_region
    return region_list, water_level

@hierarchy.Skill
def SelectNextRegionWrapper(region_list, water_level, is_refilled)
    """
    arg: region_list = arg (current region: arg[0:8], region cup number: arg[8:16], [water_level, is_refilled])
    ret_val: destination region in one hot representation
    """
    curr_region = region_list[0:8]
    region_cup_num = region_list[8:16]
    #for here, the function passed in 4 arguments, water_level and is_refilled is missing
    destin_region = SelectNextRegion(curr_region, region_cup_num)
    return destin_region, water_level, is_refilled


@hierarchy.Skill
def SelectNextRegion(curr_region, region_cup_num):
    """
    arg: region_list = arg (current region: arg[0:8], region cup number: arg[8:16], [water_level, is_refilled])
    ret_val: destination region in one hot representation
    """
    update_region = CheckRegion(curr_region, region_cup_num)
    check, update_region = CheckRegion(update_region, region_cup_num)
    while(not check):
        update_region = ShiftRegion(update_region)
        check, update_region = CheckRegion(update_region, region_cup_num)

    return update_region


@hierarchy.Skill
def ShiftRegion(prev_region):
    """
    arg: previous region: arg[0:8]
    ret_val: selected region in one hot representation
    """
    index = sum([i*prev_region[i] for i in range(8)])
    prev_region[index] = 0
    prev_region[(index+1)%8] = 1
    return prev_region


@hierarchy.Skill
def CheckRegion(sele_region, region_cup_num)
    """
    arg: region_list = arg, current region: arg[0:8], region cup number: arg[8:16]
    ret_val: destination region in one hot representation
    """
    index = sum([i*sele_region[i] for i in range(8)])
    return region_cup_num[index], sele_region


@hierarchy.Skill
def MoveNextRegion(curr_region, destin_region, water_level, is_refilled):
    """
    arg: [curr_region, destin_region, water_level, is_refilled]
    ret_val: [water_level]
    """
    