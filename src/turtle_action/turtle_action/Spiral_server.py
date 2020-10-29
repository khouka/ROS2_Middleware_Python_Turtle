import rclpy
from rclpy.node import Node
from interfaces2.action import SquareSpiral
from rclpy.action import ActionServer, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
import turtle 
from turtle import *
import time

def screen_setup():
     myscreen = turtle.Screen()
     myscreen.title("Turtle_Action")
     myscreen.setup(600,600)
     myscreen.bgcolor("black")

screen_setup()
     
class Robot(turtle.Turtle):
    def __init__(self):
       turtle.Turtle.__init__(self)
       self.shape("classic")
       self.speed(8)
       self.pensize(3)
       self.color("white")
Robot = Robot()   

class Turtle_Action_Server(Node):

    def __init__(self):
        super().__init__('turtle_action_server')
        self.action_server = ActionServer(self, SquareSpiral, 'Spiral64', 
             execute_callback= self.execute_callback,
             callback_group= ReentrantCallbackGroup(),
             goal_callback= self.goal_callback,)

    def goal_callback(self, goal_request):
        self.get_logger().info('The goal request was received')
        return GoalResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Initializing goal execution....')
        feedback_msg = SquareSpiral.Feedback()
        feedback_msg.current_spiral = 0
        for i in range(1, goal_handle.request.loop_length):
            Robot.right(90)
            Robot.forward(4*i)
            if i % 4 == 0:
               feedback_msg.current_spiral = i
               self.get_logger().info('Publishing feedback: {0}'.format(feedback_msg.current_spiral))
               goal_handle.publish_feedback(feedback_msg)
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal was canceled')
                return SquareSpiral.Result()
        goal_handle.succeed()
        result = SquareSpiral.Result()
        result.total = int(feedback_msg.current_spiral /4)
        self.get_logger().info('Returning result: {0}'.format(result.total))

        return result

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
