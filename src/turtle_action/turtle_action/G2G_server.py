import rclpy
from rclpy.node import Node
from interfaces2.action import Go2Goal
from rclpy.action import ActionServer, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
import turtle 
from turtle import *
import random
import math
import time
import os

# Screen Setup
myscreen = turtle.Screen()
myscreen.title("Turtle_Action")
myscreen.setup(600,600)
myscreen.bgcolor("bisque")
myscreen.tracer(0)
    
class Turtle1(turtle.Turtle):
    def __init__(self):
       turtle.Turtle.__init__(self)
       self.shape("turtle")
       self.color("blue")
       self.penup()
       self.goto(-220,-220)

T1 = Turtle1() 

class Turtle2(turtle.Turtle):
    def __init__(self):
       turtle.Turtle.__init__(self)
       self.shape("turtle")
       self.color("red")
       self.penup()
       self.goto(-220,-250)

T2 = Turtle2()

class Goal(turtle.Turtle):
    def __init__(self):
       turtle.Turtle.__init__(self)
       self.shape("circle")
       self.shapesize(1)
       self.penup()
       self.hideturtle()
       self.color("green")

Goal = Goal()

def Race():
   myscreen.update()
   T1.setheading(T1.towards(Goal)) 
   T2.setheading(T2.towards(Goal)) 
   pixel1 = random.randint(0,20)
   pixel2 = random.randint(0,20)
   T1.fd(pixel1)
   T2.fd(pixel2)

class Turtle_Action_Server(Node):

    def __init__(self):
        super().__init__('turtle_action_server')
        self.action_server = ActionServer(self,Go2Goal, 'Coor64', 
             execute_callback = self.execute_callback,
             callback_group = ReentrantCallbackGroup(),
             goal_callback = self.goal_callback)

    def goal_callback(self, goal_request):
        self.get_logger().info('The goal request was received')
        return GoalResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Initializing goal execution....')
        start = time.time()
        feedback_msg = Go2Goal.Feedback() 
        Goal.goto(goal_handle.request.x, goal_handle.request.y)
        Goal.showturtle()
        feedback_msg.remaining_distance1 = int(math.sqrt((goal_handle.request.x - T1.xcor()) **2 + (goal_handle.request.y - T1.ycor()) **2))  
        feedback_msg.remaining_distance2 = int(math.sqrt((goal_handle.request.x - T2.xcor()) **2 + (goal_handle.request.y - T2.ycor()) **2)) 
        while (feedback_msg.remaining_distance1 > 10) and (feedback_msg.remaining_distance1 > 10):
            feedback_msg.remaining_distance1 = int(math.sqrt((goal_handle.request.x - T1.xcor()) **2 + (goal_handle.request.y - T1.ycor()) **2))  
            feedback_msg.remaining_distance2 = int(math.sqrt((goal_handle.request.x - T2.xcor()) **2 + (goal_handle.request.y - T2.ycor()) **2)) 
            feedback_msg.turtle1_x = int(T1.xcor())
            feedback_msg.turtle1_y = int(T1.ycor())
            feedback_msg.turtle2_x = int(T2.xcor())
            feedback_msg.turtle2_y = int(T2.ycor())
            self.get_logger().info('Publishing Turtle 1 Remaining distance: {0}'.format(feedback_msg.remaining_distance1))
            self.get_logger().info('Publishing: Turtle 1 Pose')
            self.get_logger().info('Publishing Turtle 2 Remaining distance: {0}'.format(feedback_msg.remaining_distance2))
            self.get_logger().info('Publishing: Turtle 2 Pose')
            goal_handle.publish_feedback(feedback_msg)
            myscreen.ontimer(Race(), 100)
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal was canceled')
                return Go2Goal.Result()
        else: 
           T1.fd(0)
           T2.fd(0)
           goal_handle.succeed()
           result = Go2Goal.Result()
           end = time.time()        
           result.total_time = float(end - start) 
           if (feedback_msg.remaining_distance1 < feedback_msg.remaining_distance2):
              result.winner = "Turtle 1"
           if (feedback_msg.remaining_distance2 < feedback_msg.remaining_distance1):
              result.winner = "Turtle 2"
           self.get_logger().info('Returning result: {0}'.format(result.total_time))
           self.get_logger().info('Publishing winner: {0}'.format(result.winner))
        return result

def main():
    rclpy.init()
def main():
    rclpy.init()
    action_server = Turtle_Action_Server()

    try:
       rclpy.spin(action_server)
    except KeyboardInterrupt:
       pass 

    rclpy.shutdown()


if __name__ == '__main__':
    main()
