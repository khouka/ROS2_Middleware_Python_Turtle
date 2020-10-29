import rclpy
from rclpy.node import Node
from interfaces.msg import Setcolor

class Set_color(Node):
      
      def __init__(self):
        super().__init__('set_color')
        self.publisher = self.create_publisher(Setcolor, 'color_setting', 10)
        self.timer = self.create_timer(3, self.timer_callback)
      
      def timer_callback(self):
        msg = Setcolor()
        choice = input("Please input the color of the turtle:")
        print("Turtle's color:", choice)
        msg.color = choice
        self.publisher.publish(msg)
              
def main():
    rclpy.init()
    node = Set_color()
    try:
       rclpy.spin(node)
    except KeyboardInterrupt:
       pass 
    node.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
