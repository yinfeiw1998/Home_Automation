#pyramid.py
import math
import time

import numpy as np

from hierarchy import SkillSet
from hierarchy import HierarchicalAgent
import hierarchy
from envs import hsr
# from envs.pyramid import PyramidEnv

V = 0.07
OMEGA = math.pi / 5.

CUP_SPACING = 0.095
TABLE_HEIGHT = 0.375
CUP_HEIGHT = 0.06

EPSILON = 1e-6


class PyramidAgent(HierarchicalAgent):
    ##change skill name to lowercase
    @hierarchy.Skill
    def Pyramid(skillset, height, pos):  #root skill: Pyramid  
        """
        arg: [height, pos]
        ret_val: None
        """
        print('Pyramid')
        skillset.MoveHome()
        skillset.BuildPyramid(height, pos)
        skillset.EndTask()

    root_skill = Pyramid  ##check it later

    @hierarchy.Skill
    def MoveHome(skillset):
        """
        arg: None
        ret_val: None
        """
        print(MoveHome)
        skillset.env.MoveGripper(0)
        skillset.env.MoveArm(0.45, 0., 0., -math.pi / 2., -math.pi / 2.)
        skillset.env.MoveHead(-math.pi / 8., 0.)

    @hierarchy.Skill
    def BuildPyramid(skillset, height, pos):
        """
        arg: [height, pos]
        ret_val: None
        """
        print('BuildPyramid')
        for cnt in range(height):
            skillset.BuildLevel(cnt, pos, height-cnt)

    @hierarchy.Skill
    def EndTask(skillset):
        """
        arg: None
        ret_val: None
        """
        print('EndTask')
        skillset.env.MoveArm(0., 0., 0., -math.pi / 2., 0.)

    @hierarchy.Skill
    def BuildLevel(skillset, level, pos, num_cups):
        """
        arg: [level, pos, num_cups]
        ret_val: None
        """
        print('BuildLevel')
        for cnt in range(num_cups):
            skillset.MoveCup(pos+cnt, level)
        
    @hierarchy.Skill
    def MoveCup(skillset, pos, level):
        """
        arg: [pos, level]
        ret_val: None
        """
        print('MoveCup')
        skillset.PickCup()
        skillset.PlaceCup(pos, level)


    @hierarchy.Skill
    def PickCup(skillset):
        """
        arg: None
        ret_val: None
        """
        print('PickCup')
        skillset.env.MoveBaseRel(0., 0., -math.pi / 2., V, OMEGA)
        hsr.MoveArm(0.37, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
        skillset.env.sleep(3)
        skillset.env.MoveGripper(1)
        skillset.env.MoveArm(0.45, 0., 0., -math.pi / 2., -math.pi / 2.)
        skillset.env.MoveBaseRel(0., 0., math.pi / 2., V, OMEGA)


    @hierarchy.Skill
    def PlaceCup(skillset, pos, level):
        """
        arg: [pos, level]
        ret_val: None
        """
        print('PlaceCup')
        skillset.MoveToPosition(pos, level, 0, 0)
        skillset.MoveToPosition(pos, level, 1, 0)
        skillset.PutCup(level)
        skillset.MoveToPosition(0, 0, 0, 1)


    @hierarchy.Skill
    def MoveToPosition(skillset, pos, level, motion_cnt, away):
        """
        arg: [pos, level, motion_cnt, away]
        ret_val: None
        """
        print('MoveToPosition')
        skillset.env.LocateMarkers()
        # this will be demonstrated by teleoperation
        # if away==0 and motion_cnt == 0:
        #     Record_MoveBaseRel(np.random.normal(0., 0.02), np.random.normal(0., 0.02), np.random.normal(0., math.radians(2)), V, OMEGA)
        # else:
        #     Record_MoveBaseRel(0., 0., 0., V, OMEGA)


    @hierarchy.Skill
    def PutCup(skillset, level):
        """
        arg: [level]
        ret_val: None
        """
        print('PutCup')
        skillset.env.MoveArm(TABLE_HEIGHT + CUP_HEIGHT * level, -math.pi / 2., 0., -math.pi / 2., -math.pi / 2.)
        skillset.env.MoveGripper(0)
        skillset.env.MoveArm(0.45, 0., 0., -math.pi / 2., -math.pi / 2.)
