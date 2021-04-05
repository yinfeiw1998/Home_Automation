import rospy
from gazebo_msgs.msg import ModelStates
import sys
from utils import DictTree
import math
import genpy
import struct

class Gz_getPos:

    def __init__(self):
        self.pos_lib = DictTree()
        # rospy.init_node('Gz_getPos', anonymous=True)  #uncomment this when there is no ROS master node
        self.getmessage()


    def getmessage(self):
        data = rospy.wait_for_message("/gazebo/model_states", ModelStates)
        name_list = data.name
        # print(name_list)
        '''pose is geometry_msgs/Pose. It has compact message geometry_msgs/Point position and 
        geometry_msgs/Quaternion orientation. For message position, it has message x, y, z, all in float64 form '''
        # print(type(data.pose[1].position.x))
        # print("count time is: {:.0f}".format(self.count))
        for model_name in name_list:
            # Model name are the model name in the Gazebo Simulation.
            self.pos_lib[model_name] = data.pose[name_list.index(model_name)].position
        # Quaternion to Euler angle
        X = data.pose[name_list.index('hsrb')].orientation.x
        Y = data.pose[name_list.index('hsrb')].orientation.y
        Z = data.pose[name_list.index('hsrb')].orientation.z
        W = data.pose[name_list.index('hsrb')].orientation.w
        t3 = +2.0 * (W * Z + X * Y)
        t4 = +1.0 - 2.0 * (Y * Y + Z * Z)
        theta = math.atan2(t3, t4)
        self.pos_lib['hsrb'].z = theta

    def IsOnTable(self, model_name):
        # modelkey = '{}_{}'.format(color, modeltype)
        if self.pos_lib[model_name].y >= 1.6:
            return True
        else:
            return False

    # def IsFull(self, model_name):
    #     return self.pos_lib[model_name].isfull


def main(args):
    rospy.init_node('Gz_getPos', anonymous=True)
    samplesub = Gz_getPos()
    samplesub.getmessage()
    print(samplesub.pos_lib['hsrb'].x)
    print(samplesub.pos_lib['hsrb'].y)
    print(samplesub.pos_lib['hsrb'].z)
    samplesub = Gz_getPos()
    samplesub.getmessage()
    print(samplesub.pos_lib['hsrb'].x)
    print(samplesub.pos_lib['hsrb'].y)
    print(samplesub.pos_lib['hsrb'].z)
    # print(samplesub.pos_lib["red_plate"])
    # print("IKEA")
    # print(samplesub.pos_lib["IKEAtable"])
    # print("blue plate")
    # print(samplesub.pos_lib["blue_plate"])
    # print("green cup")
    # print(samplesub.pos_lib["green_cup"])
    # print("red cup")
    # print(samplesub.pos_lib["red_cup"])
    # print(samplesub.IsOnTable('red', 'plate'))



if __name__=="__main__":
    main(sys.argv)





# name = data.name
# ['ground_plane', 'IKEAtable', 'blue_plate', 'red_plate', 'green_plate', 'blue_cup', 'red_cup', 'green_cup', 'hsrb']