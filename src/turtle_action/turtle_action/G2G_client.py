import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from interfaces2.action import Go2Goal
from action_msgs.msg import GoalStatus
import time
                   
class Turtle_Action_Client(Node):

    def __init__(self):
        super().__init__('turtle_action_client') 
        self.turtle_action = ActionClient(self, Go2Goal, 'Coor64')
        self.goalx = input("goal x coordinate:") 
        self.goaly = input("goal y coordinate:")
        self.send_goal()

    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self.turtle_action.wait_for_server()

        goal_action = Go2Goal.Goal()
        goal_action.x = int(self.goalx)
        goal_action.y = int(self.goaly)      
        self.goal_future = self.turtle_action.send_goal_async(
           goal_action, 
           feedback_callback= self.feedback_callback)

        self.goal_future.add_done_callback(self.goal_callback)
    def goal_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            print('Goal was rejected')
            return
        self.get_logger().info('Goal was accepted, will procced...')
        
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_action):
        feedback = feedback_action.feedback
        self.get_logger().info('Remaining distance for Turtle 1: {0}'.format(feedback.remaining_distance1))
        print("Turtle 1 Pose: (", feedback.turtle1_x,",", feedback.turtle1_y, ")")
        self.get_logger().info('Remaining distance for Turtle 2: {0}'.format(feedback.remaining_distance2))
        print("Turtle 2 Pose: (", feedback.turtle2_x,",", feedback.turtle2_y, ")")

    def result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            print('Goal succeeded! Duration:', result.total_time)
            print('The Winner is',result.winner)
        else:
            print('Goal could not be reached')
      
        rclpy.shutdown()
       
def main():
    rclpy.init()
    action_client = Turtle_Action_Client()
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()

