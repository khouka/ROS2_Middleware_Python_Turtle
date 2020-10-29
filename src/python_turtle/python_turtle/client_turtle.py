import rclpy
from rclpy.node import Node
import turtle
from tkinter import PhotoImage
from interfaces.srv import Distance 
from sensor_msgs.msg import Image
from std_msgs.msg import Float64
import cv2
import numpy as np
from cv_bridge import CvBridge
import imutils
import random
import time 

myscreen = turtle.Screen()
myscreen.title("Turtle_Driver")
myscreen.bgcolor("silver")
myscreen.setup(1100,1000)

def Move():
    Robot.setheading(Robot.towards(Goal))        
    Robot.forward(50) 
    
def Stop():
    Robot.setheading(Robot.towards(Goal))        
    Robot.backward(25)
       
def move_goal():
    xcor = random.randint(-400,350)
    ycor = random.randint(-400,350)     
    Goal.goto(xcor,ycor)
    Robot.setheading(Robot.towards(Goal))                    
    
class Robot(turtle.Turtle):
    def __init__(self):
       turtle.Turtle.__init__(self)
       self.shape("turtle")
       self.shapesize(2)
       self.color("red")
       self.penup()
       self.goto(-350,-400)  

Robot = Robot()        
              
class Goal(turtle.Turtle):
    def __init__(self):
       turtle.Turtle.__init__(self)
       goal = PhotoImage(file="images/goal.png").zoom(1,1)          
       myscreen.addshape("goal", turtle.Shape("image", goal))
       self.shape("goal")
       self.penup()
       self.speed(0)

Goal = Goal()

class Turtle_Client(Node):
     
      def __init__(self):
          super().__init__('turtle_client')
          self.subscriber = self.create_subscription(Image, 'camera_msg', self.callback, 1000)
          self.subscriber = self.create_subscription(Float64, 'col004', self.dist_callback, 10)
          self.bridge = CvBridge()
          print("Initializing display")
          self.cli = self.create_client(Distance, 'var04') 
          self.timer = self.create_timer(1, self.send_request)
          self.req = Distance.Request()

         
      def callback(self, data): 
          sub_frames = self.bridge.imgmsg_to_cv2(data)
          cv2.namedWindow("User camera")
          cv2.imshow("User camera", sub_frames)
          key = cv2.waitKey(1) 
          if key == 27:  
            cv2.destroyAllWindows()
          hsv = cv2.cvtColor(sub_frames, cv2.COLOR_BGR2HSV)
          # red filter 
          low_red = np.array([160, 155, 84]) 
          high_red = np.array([180, 255, 255])
          red_mask = cv2.inRange(hsv, low_red, high_red)
          red_img = cv2.bitwise_and(sub_frames, sub_frames, mask = red_mask)  
          cnts_red = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   
          cnts_red = imutils.grab_contours(cnts_red)
          for r in cnts_red:
             if cv2.contourArea(r) > 1000:
                print("Red detected")
                Move()
          # Blue filter
          low_blue = np.array([94, 80, 2])
          high_blue = np.array([125, 255, 255]) 
          blue_mask = cv2.inRange(hsv, low_blue, high_blue)
          blue_img = cv2.bitwise_and(sub_frames, sub_frames, mask = blue_mask)
          cnts_blue = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
          cnts_blue = imutils.grab_contours(cnts_blue)
          for b in cnts_blue:
             if cv2.contourArea(b) > 1000:
                print("Blue detected") 
                Stop()         
         # Green filter  
          low_green = np.array([25, 50, 73])
          high_green = np.array([100, 255, 255])
          green_mask = cv2.inRange(hsv, low_green, high_green)
          green_img = cv2.bitwise_and(sub_frames, sub_frames, mask = green_mask) 
          cnts_green = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
          cnts_green = imutils.grab_contours(cnts_green)
          for g in cnts_green:
             if cv2.contourArea(g) > 1000:  
                print("Green detected") 
                move_goal()
                time.sleep(3)    
     
      def dist_callback(self, msg): 
          print('Remaining distance:', msg.data)

      def send_request(self):
          self.req.x1 = float(Robot.xcor()) 
          self.req.y1 = float(Robot.ycor())
          self.req.x2 = float(Goal.xcor())
          self.req.y2 = float(Goal.ycor())
          self.future = self.cli.call_async(self.req)  

def main():
    rclpy.init()

    node = Turtle_Client() 
    try:
       rclpy.spin(node)
    
    except KeyboardInterrupt:
       pass 

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
