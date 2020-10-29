import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class Webcam_cap: 
    def __init__(self): 
        self.cam = cv2.VideoCapture(0) # video capturing from the camera, default cam number is 0
        self.cam.set(3,640)
        self.cam.set(4,480)
        
    def Capture_Frame(self): 
        _, self.img = self.cam.read() # Defining our image
        return self.img 

class Campublisher(Node):
      
    def __init__(self):
       super().__init__('Cam_publisher')
       self.publisher = self.create_publisher(Image, 'camera_msg', 1000)
       self.timer = self.create_timer(0.01, self.timer_callback)
       self.obj = Webcam_cap()
       self.bridge = CvBridge()
       print("webcam running....")

    def timer_callback(self):
       pub_frames = self.obj.Capture_Frame()
       msg = self.bridge.cv2_to_imgmsg(pub_frames)       
       self.publisher.publish(msg)

def main():
    rclpy.init()
    node = Campublisher()
    try:
       rclpy.spin(node)
    except KeyboardInterrupt:
       pass 
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__': 
    main()

