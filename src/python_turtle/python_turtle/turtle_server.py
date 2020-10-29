import rclpy
from rclpy.node import Node
import math
import time
from interfaces.srv import Distance 
from std_msgs.msg import Float64


class Turtle_Service(Node):
    def __init__(self):
        super().__init__('turtle_service')
        self.srv = self.create_service(Distance, 'var04', self.Find_Distance) 
        self.publisher = self.create_publisher(Float64, 'col004', 10)
        self.timer = self.create_timer(1, self.timer_callback)
        self.res = 0.0
    def Find_Distance(self, request, response):
        response.dist = math.sqrt((request.x2 - request.x1) **2 + (request.y2 - request.y1) **2) 
        self.res = response.dist
        print('Turtle:', request.x1, request.y1 )
        print('Goal:' , request.x2, request.y2 ) 
        return response
     
    def timer_callback(self):
        msg = Float64()        
        msg.data = self.res
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args) 
    turtle_service = Turtle_Service() 
    try:
       rclpy.spin(turtle_service)
    except KeyboardInterrupt:
       pass 
    rclpy.shutdown()

if __name__ == '__main__':
    main()
