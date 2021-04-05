#!/usr/bin/env python
from __future__ import print_function

import roslib
# roslib.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    # self.image_pub = rospy.Publisher("image_topic_2",Image)

    self.bridge = CvBridge()
    # subscribe to subscriber(topic, data type, function you want to execute every time you receive data)
    self.image_sub = rospy.Subscriber("/hsrb/arm_trajectory_controller/state",Image,self.callback)
    print(self.image_sub.get_num_connections())
  def callback(self,data):
      pass
    # try:
    #   cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    # except CvBridgeError as e:
    #   print(e)

    # (rows,cols,channels) = cv_image.shape
    # if cols > 60 and rows > 60 :
    #   cv2.circle(cv_image, (50,50), 10, 255)

    # cv2.imshow("Image window", cv_image)
    # # delay 3ms
    # cv2.waitKey(3)


    # publish image to a publisher
    # try:
    #   self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    # except CvBridgeError as e:
    #   print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    # keep program listening to the topic
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)