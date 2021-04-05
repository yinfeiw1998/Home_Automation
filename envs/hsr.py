#hsr.py
import math

import numpy as np

# import vision
from utils import DictTree

# try:
# import ar_markers
#############################################################################
# import control_msgs.msg as ctrl_msg
# import cv2
# import cv_bridge
# import rospy
# import sensor_msgs.msg as sens_msg
# import tmc_control_msgs.msg as tmc_msg
# import trajectory_msgs.msg as traj_msg

# from agents import gazebo_getpos # modification: LocateObject will use Gz_getPos
#############################################################################
import os, pickle, time

DEBUG = 0

# except ImportError as e:
#     print(e)

from envs import env
# from envs.dishes import DishesEnv

V = 0.07
OMEGA = math.pi / 5.

# I delete all hsr parameter for all Action decorated function, Add it to the first one when you need it
class HSREnv(object):
    def __init__(self):
        pass
        self.default_model_name = "log_poly2"
        self.actions = [i for i in dir(self) if (not i.startswith("__")) or i!="record"]
        #############################################################################
        # rospy.init_node('main', anonymous=True)
        # self.subscribers = {
        #     'base_pose': rospy.Subscriber('/hsrb/omni_base_controller/state', ctrl_msg.JointTrajectoryControllerState, PoseCallback(), queue_size=1),
        #     'head_cam': rospy.Subscriber('/hsrb/head_r_stereo_camera/image_rect_color', sens_msg.Image, ImageCallback(), queue_size=1),
        #     'arm_pose': rospy.Subscriber('/hsrb/arm_trajectory_controller/state', ctrl_msg.JointTrajectoryControllerState, PoseCallback(), queue_size=1),
        # }
        # self.publishers = {
        #     'arm': rospy.Publisher('/hsrb/arm_trajectory_controller/follow_joint_trajectory/goal', ctrl_msg.FollowJointTrajectoryActionGoal, queue_size=1),
        #     'base': rospy.Publisher('/hsrb/omni_base_controller/follow_joint_trajectory/goal', ctrl_msg.FollowJointTrajectoryActionGoal, queue_size=1),
        #     'grip': rospy.Publisher('/hsrb/gripper_controller/grasp/goal', tmc_msg.GripperApplyEffortActionGoal, queue_size=1),
        #     'head': rospy.Publisher('/hsrb/head_trajectory_controller/follow_joint_trajectory/goal', ctrl_msg.FollowJointTrajectoryActionGoal, queue_size=1),
        # }

        # try:
        #     while (any(publisher.get_num_connections() == 0 for publisher in self.publishers.values())
        #            or any(subscriber.get_num_connections() == 0 or subscriber.callback.data is None for subscriber in self.subscribers.values())):
        #         if rospy.is_shutdown():
        #             raise ValueError()
                
        #         print('Waiting for: {}'.format(
        #             [name for name, publisher in self.publishers.items() if publisher.get_num_connections() == 0] +
        #             [name for name, subscriber in self.subscribers.items() if subscriber.get_num_connections() == 0 or subscriber.callback.data is None]))
        #         rospy.sleep(0.1)
        # except KeyboardInterrupt:
        #     rospy.loginfo(KeyboardInterrupt)
        #     raise
        #############################################################################
        # self.vision = vision.Yolo()
        # self.obs = None  ## useless anymore

    # def record(self):
    #     return [
    #         self.subscribers['arm_pose'].callback.data,
    #         self.subscribers['base_pose'].callback.data,
    #     ]

    @env.Action(arg_in_len=5, ret_out_len=0)
    def MoveArm(self, arm_lift, arm_flex, arm_roll, wrist_flex, wrist_roll):
        print("MoveArm")
        # point = traj_msg.JointTrajectoryPoint()
        # point.positions = [arm_lift, arm_flex, arm_roll, wrist_flex, wrist_roll]
        # point.velocities = [0] * 5
        # point.time_from_start = rospy.Time(0.5)
        # traj = ctrl_msg.FollowJointTrajectoryActionGoal()
        # traj.goal.trajectory.joint_names = ['arm_lift_joint', 'arm_flex_joint', 'arm_roll_joint', 'wrist_flex_joint', 'wrist_roll_joint']
        # traj.goal.trajectory.points = [point]
        # self.publishers['arm'].publish(traj)
        # rospy.sleep(1.)
        # while True:
        #     error = self.subscribers['arm_pose'].callback.data['error']
        #     if all(abs(x) <= 1e-2 for x in error):
        #         break
        #     rospy.sleep(0.1)

    @env.Action(arg_in_len=5, ret_out_len=0)
    def MoveBaseAbs(self, x, y, theta, v, omega):
        print("MoveBaseAbs")
        # x0, y0, theta0 = self.subscribers['base_pose'].callback.data['actual']
        # print(self.subscribers['base_pose'].callback.data)
        # dx = ((x - x0) ** 2 + (y - y0) ** 2) ** .5
        # dtheta = abs(theta - theta0)
        # t = max(dx / v, dtheta / omega)
        # acceleration = 0.05
        # point = traj_msg.JointTrajectoryPoint()
        # point.positions = [x, y, theta]
        # point.accelerations = [acceleration] * 3
        # point.effort = [1]
        # point.time_from_start = rospy.Time(t)
        # traj = ctrl_msg.FollowJointTrajectoryActionGoal()
        # traj.goal.trajectory.joint_names = ['odom_x', 'odom_y', 'odom_t']
        # traj.goal.trajectory.points = [point]
        # self.publishers['base'].publish(traj)
        # rospy.sleep(1.)
        # # while True:
        # error = self.subscribers['base_pose'].callback.data['error']
        # print(error)
        # # if abs(error[0])<=0.001 and abs(error[1])<=0.021 and abs(error[2])<=0.02:
        # #     break 
        # # if all(abs(x) <= 1e-6 for x in error):
        # #     break
        # rospy.sleep(2)


    @env.Action(arg_in_len=5, ret_out_len=0)
    def MoveBaseRel(self, x, y, theta, v, omega):
        print("MoveBaseRel")
        # x0, y0, theta0 = self.subscribers['base_pose'].callback.data['actual']
        # x, y, theta = (
        #     x * math.cos(theta0) - y * math.sin(theta0) + x0,
        #     x * math.sin(theta0) + y * math.cos(theta0) + y0,
        #     theta + theta0)
        # self.MoveBaseAbs(x, y, theta, v, omega)


    @env.Action(arg_in_len=1, ret_out_len=0)
    def MoveGripper(self, close):
        print("MoveGripper")
        # if close:
        #     rospy.sleep(1.)
        # grip = tmc_msg.GripperApplyEffortActionGoal()
        # grip.goal.effort = -0.1 if close > 0.5 else 0.1
        # self.publishers['grip'].publish(grip)
        # rospy.sleep(1.)


    @env.Action(arg_in_len=2, ret_out_len=0)
    def MoveHead(self, tilt, pan):
        print("MoveHead")
        # point = traj_msg.JointTrajectoryPoint()
        # point.positions = [tilt, pan]
        # point.velocities = [0] * 2
        # point.time_from_start = rospy.Time(0.5)
        # traj = ctrl_msg.FollowJointTrajectoryActionGoal()
        # traj.goal.trajectory.joint_names = ['head_tilt_joint', 'head_pan_joint']
        # traj.goal.trajectory.points = [point]
        # self.publishers['head'].publish(traj)
        # rospy.sleep(2.)


    @env.Action(arg_in_len=3, ret_out_len=4)
    def LocateObject(self, motion_cnt, obj_class, obj_color):
        print('LocateObject')
        # img = self.subscribers['head_cam'].callback.data
        # objs = self.vision.get_objs(img, 0.1)
        # objs = list(sorted((obj for obj in objs if obj['class'] in DishesEnv.obj_classes_filter), key=lambda o: o['bottom'], reverse=True))
        # detected_obj_class = DishesEnv.obj_classify([[motion_cnt, obj['left'], obj['top'], obj['right'], obj['bottom']] for obj in objs])
        # for i, obj in enumerate(objs):
        #     obj['class_idx'] = detected_obj_class[i]
        #     obj['mean_color'] = img[obj['top']:obj['bottom'], obj['left']:obj['right'], :].mean(0).mean(0) - img.mean(0).mean(0)
        #     obj['color_idx'] = 1 + np.argmax(obj['mean_color'])
        # for i, obj in enumerate(objs):
        #     box_color = (255, 0, 0)
        #     cv2.rectangle(img, (obj['left'], obj['top']), (obj['right'], obj['bottom']), box_color, 4)
        #     cv2.putText(
        #         img, "{} {}".format(DishesEnv.obj_colors[obj['color_idx']], DishesEnv.obj_classes[obj['class_idx']]),
        #         (obj['left'], obj['top']), cv2.FONT_HERSHEY_PLAIN, 2, box_color, 1, 8)
        # cv2.imshow('head', img)
        # cv2.waitKey(3)
        # if abs(obj_class - DishesEnv.obj_classes.index(None)) > 0.5:
        #     objs = [obj for obj in objs if abs(obj['class_idx'] - obj_class) < 0.5]
        # if abs(obj_color - DishesEnv.obj_colors.index(None)) > 0.5:
        #     objs = [obj for obj in objs if abs(obj['color_idx'] - obj_color) < 0.5]
        # if len(objs) > 0:
        #     obj = objs[0]
        #     box_color = (0, 255, 0)
        #     cv2.rectangle(img, (obj['left'], obj['top']), (obj['right'], obj['bottom']), box_color, 4)
        #     cv2.putText(
        #         img, "{} {}".format(DishesEnv.obj_colors[obj['color_idx']], DishesEnv.obj_classes[obj['class_idx']]),
        #         (obj['left'], obj['top']), cv2.FONT_HERSHEY_PLAIN, 2, box_color, 1, 8)
        #     return [obj['class_idx'], obj['color_idx'], (obj['left'] + obj['right']) / 2, (obj['top'] + obj['bottom']) / 2]
        # else:
        #     return [0, 0, 0, 0]
        #############################################################################
        # if DEBUG:
        #     return [True, 0,0,0]
        # # region_list = arg[1:17]

        # # initialize the getpos class
        # gzpos = gazebo_getpos.Gz_getPos()
        # pos_dict = gzpos.pos_lib

        # if motion_cnt == 0:
        #     # calculate robot's current region
        #     curr_region = (int)(pos_dict['hsrb'].x // 0.375 + 1)
        #     if curr_region > 4:
        #         curr_region = 4
        #     elif curr_region < 1:
        #         curr_region = 1
        #     if pos_dict['hsrb'].y > 2:
        #         curr_region = 8-curr_region+1
        #     print('Locate_Object: hsrb region: ', curr_region, 'x', pos_dict['hsrb'].x, 'y: ', pos_dict['hsrb'].y)

        #     # construct region that robot could 'see'
        #     lcurr_region = curr_region-1
        #     rcurr_region = curr_region+1
        #     if curr_region == 1 or curr_region == 5:
        #         lcurr_region = curr_region
        #     if curr_region == 4 or curr_region == 8:
        #         rcurr_region = curr_region
        #     curr_list = []
        #     lcurr_list = []
        #     rcurr_list = []

        #     cup_selected = False
        #     cup_region = None
        #     if os.path.exists('watered_cup.pkl'):
        #         input = open('watered_cup.pkl')
        #         watered_cups = pickle.load(input)
        #     else:
        #         watered_cups = []
        #     for mname in pos_dict.allkeys():
        #         model_name = mname[0]
        #         # object in gazebo that isn't cups
        #         if model_name == 'hsrb' or model_name == 'ground_plane' or model_name == 'IKEAtable' or model_name == 'Pitcher' or model_name == 'station' or model_name in watered_cups:
        #             continue

        #         # calculate cup region
        #         # Table is at (0, 1.6) (1.6, 2.4)
        #         cup_region = (int)(pos_dict[mname].x//0.375+1)
        #         if (pos_dict[mname].y-1.6)//0.4 == 1:
        #             cup_region = 8-cup_region+1

        #         if curr_region == cup_region:
        #             curr_list.append(model_name)
        #         elif lcurr_region == cup_region:
        #             lcurr_list.append(model_name)
        #         elif rcurr_region == cup_region:
        #             rcurr_list.append(model_name)
        #     print(curr_region, lcurr_list, curr_list, rcurr_list)
        #     if len(lcurr_list) > 0:
        #         item_name = lcurr_list[0]
        #         cup_region = lcurr_region
        #     elif len(curr_list)>0:
        #         item_name = curr_list[0]
        #         cup_region = curr_region
        #     elif len(rcurr_list) > 0:
        #         item_name = rcurr_list[0]
        #         cup_region = rcurr_region
        #     else:
        #         # terminated
        #         return [False, 0, 0, 0]
        #     watered_cups.append(item_name)
        #     output = open('watered_cup.pkl', 'wb')
        #     pickle.dump(watered_cups, output)
        #     output.close()
        #     output = open('target_cup.pkl', 'wb')
        #     pickle.dump([item_name, cup_region], output)
        #     output.close()
        # else:
        #     # motion_cnt == 1
        #     iput = open('target_cup.pkl')
        #     [item_name, cup_region] = pickle.load(iput)
        #     iput.close()

        # armlength = 0.55
        # y_adjust = 0.1

        # # only works when hsrb face the direction of +y axi.
        # if (0 < cup_region < 5):  # TODO change to 0-7
        #     # In this case, x for hsrb is +y in gazebo, y for hsrb is -x in gazebo
        #     theta_0 = 1.55
        #     theta = theta_0 - pos_dict['hsrb'].z
        #     if abs(theta) < 0.01:
        #         theta = 0
        #     y = -(pos_dict[item_name].x - pos_dict["hsrb"].x) + y_adjust
        #     x = pos_dict[item_name].y - armlength - pos_dict["hsrb"].y
        # else:
        #     theta_0 = -1.55
        #     theta = theta_0 - pos_dict['hsrb'].z
        #     if abs(theta) < 0.01:
        #         theta = 0
        #     y = (pos_dict[item_name].x - pos_dict["hsrb"].x) + 0.075
        #     x = -(pos_dict[item_name].y + armlength - pos_dict["hsrb"].y)


        # ret_val = [True, x, y, theta]
        # return ret_val
        #############################################################################
        return [0, 0, 0, 0]


    @env.Action(arg_in_len=0, ret_out_len=16)
    def LocateMarkers(self):
        print('LocateMarkers')
        # while True:
        #     rospy.sleep(5.)
        #     img = self.subscribers['head_cam'].callback.data
        #     _, img = cv2.threshold(img, 32, 255, cv2.THRESH_BINARY)
        #     markers = {marker.id: marker for marker in ar_markers.detect_markers(img)}.values()
        #     for marker in markers:
        #         marker.draw_contour(img)
        #     cv2.imshow('head', img)
        #     cv2.waitKey(3)
        #     if len(markers) == 2:
        #         return sort_markers(sum([list(marker.contours.flat) for marker in markers], []))
        #     else:
        #         print('found {} markers'.format(len(markers)))
        #         rospy.sleep(1.)

#############################################################################
# def sort_markers(markers, sort_between_markers=True):
#     assert len(markers) == 16
#     markers = [int(x) for x in markers]
#     res = []
#     for marker in [markers[i:i + 8] for i in range(0, 16, 8)]:
#         # sort 4 points from left to right
#         points_xy = sorted(marker[i:i + 2] for i in range(0, 8, 2))
#         # sort each pair of points from top to bottom, and flatten
#         res.append(sum(sum((sorted(points_xy[i:i + 2], key=lambda xy: xy[1]) for i in range(0, 4, 2)), []), []))
#     if sort_between_markers:
#         return sum(sorted(res), [])
#     else:
#         return sum(res, [])


# class DataCallback(object):
#     def __init__(self, sleep=0.1):
#         self.data = None
#         self.sleep = sleep

#     def __call__(self, data):
#         self.data = data
#         rospy.sleep(self.sleep)


# class ImageCallback(DataCallback):
#     def __init__(self, sleep=0.1):
#         super(ImageCallback, self).__init__(sleep)
#         self.bridge = cv_bridge.CvBridge()

#     def __call__(self, img):
#         img = self.bridge.imgmsg_to_cv2(img, 'bgr8')
#         img = cv2.resize(img, (920, 690), interpolation=cv2.INTER_CUBIC)
#         super(ImageCallback, self).__call__(img)


# class PoseCallback(DataCallback):
#     def __call__(self, data):
#         pose = DictTree(
#             actual=data.actual.positions,
#             error=data.error.positions,
#         )
#         super(PoseCallback, self).__call__(pose)
#############################################################################