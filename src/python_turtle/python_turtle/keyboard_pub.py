import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import termios
import fcntl
import sys, os

fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

class Command(Node):
      
      def __init__(self):
        super().__init__('command')
        self.publisher = self.create_publisher(Twist, 'turtle_command', 10)
        self.timer = self.create_timer(0.01, self.timer_callback)
      
      def timer_callback(self):
        msg = Twist()
        c = sys.stdin.read()
        if  c == "\x1b[A":
          msg.linear.x= 24.0  
        elif  c == "\x1b[B":
          msg.linear.x= -24.0                    
        elif  c == "\x1b[C":
          msg.angular.z= 90.0 
        elif  c == "\x1b[D":
          msg.angular.z= -90.0 
        self.publisher.publish(msg)

              
def main():
    rclpy.init()
    node = Command()
    try:
      while True:
        try:
          rclpy.spin(node) 
        except IOError: 
          pass
        except TypeError: 
          pass 
    finally:
       termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
       fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)      
    node.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()


          

