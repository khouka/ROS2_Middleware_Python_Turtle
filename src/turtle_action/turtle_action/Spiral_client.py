import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from interfaces2.action import SquareSpiral
from action_msgs.msg import GoalStatus
import time
                   
class Turtle_Action_Client(Node):

    def __init__(self):
        super().__init__('turtle_action_client')  
        self.turtle_action = ActionClient(self, SquareSpiral, 'Spiral64')

    def send_goal(self, loop_length):
        self.get_logger().info('Waiting for action server...')
        self.turtle_action.wait_for_server()

        goal_action = SquareSpiral.Goal()
        goal_action.loop_length = loop_length
        
        self.goal_future =  self.turtle_action.send_goal_async(
           goal_action, 
           feedback_callback= self.feedback_callback)

        self.goal_future.add_done_callback(self.goal_callback)

    def goal_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            print('Goal was rejected')
            return
        self.get_logger().info('Goal was accepted, will proceed...')
        
        self.result_future = goal_handle.get_result_async()
        self.result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_action):
        feedback = feedback_action.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.current_spiral))

    def result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            print('Goal succeeded! Total number of spirals:', result.total)
        else:
            print('Goal could not be reached')

        # Shutdown after receiving a result
        rclpy.shutdown()
       
def main():
    rclpy.init()
    action_client = Turtle_Action_Client()
    
    action_client.send_goal(61)
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()

