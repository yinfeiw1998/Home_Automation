#pyramid.py
import math
import time

import numpy as np

import hierarchy
from envs import hsr
# from envs.pyramid import PyramidEnv

V = 0.07
OMEGA = math.pi / 5.

CUP_SPACING = 0.095
TABLE_HEIGHT = 0.375
CUP_HEIGHT = 0.06

EPSILON = 1e-6

@hierarchy.Skill
def Pyramid(height, pos):
    """
    arg: [height, pos]
    ret_val: None
    """
    print('Pyramid')
    MoveHome()
    BuildPyramid(height, pos)
    EndTask()

@hierarchy.Skill
def MoveHome():
    """
    arg: None
    ret_val: None
    """
    print(MoveHome)
    hsr.MoveGripper(0)
    hsr.MoveArm(0.45, 0., 0., -math.pi / 2., -math.pi / 2.)
    hsr.MoveHead(-math.pi / 8., 0.)

@hierarchy.Skill
def BuildPyramid(height, pos):
    """
    arg: [height, pos]
    ret_val: None
    """
    print('BuildPyramid')
    for cnt in range(height):
        BuildLevel(cnt, pos, height-cnt)

@hierarchy.Skill
def EndTask():
    """
    arg: None
    ret_val: None
    """
    print('EndTask')
    hsr.MoveArm(0., 0., 0., -math.pi / 2., 0.)

@hierarchy.Skill
def BuildLevel(level, pos, num_cups):
    """
    arg: [level, pos, num_cups]
    ret_val: None
    """
    print('BuildLevel')
    for cnt in range(num_cups):
        MoveCup(pos+cnt, level)
    
@hierarchy.Skill
def MoveCup(pos, level):
    """
    arg: [pos, level]
    ret_val: None
    """
    print('MoveCup')
    PickCup()
    PlaceCup(pos, level)


@hierarchy.Skill
def PickCup():
    """
    arg: None
    ret_val: None
    """
    print('PickCup')
    hsr.MoveBaseRel(0., 0., -math.pi / 2., V, OMEGA)
    hsr.MoveArm(0.37, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
    time.sleep(3)
    hsr.MoveGripper(1)
    hsr.MoveArm(0.45, 0., 0., -math.pi / 2., -math.pi / 2.)
    hsr.MoveBaseRel(0., 0., math.pi / 2., V, OMEGA)


@hierarchy.Skill
def PlaceCup(pos, level):
    """
    arg: [pos, level]
    ret_val: None
    """
    print('PlaceCup')
    MoveToPosition(pos, level, 0, 0)
    MoveToPosition(pos, level, 1, 0)
    PutCup(level)
    MoveToPosition(0, 0, 0, 1)


@hierarchy.Skill
def MoveToPosition(pos, level, motion_cnt, away):
    """
    arg: [pos, level, motion_cnt, away]
    ret_val: None
    """
    print('MoveToPosition')
    hsr.LocateMarkers()
    # this will be demonstrated by teleoperation
    # if away==0 and motion_cnt == 0:
    #     Record_MoveBaseRel(np.random.normal(0., 0.02), np.random.normal(0., 0.02), np.random.normal(0., math.radians(2)), V, OMEGA)
    # else:
    #     Record_MoveBaseRel(0., 0., 0., V, OMEGA)


@hierarchy.Skill
def PutCup(level):
    """
    arg: [level]
    ret_val: None
    """
    print('PutCup')
    hsr.MoveArm(TABLE_HEIGHT + CUP_HEIGHT * level, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
    hsr.MoveGripper(0)
    hsr.MoveArm(0.45, 0., 0., -math.pi / 2., -math.pi / 2.)
