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

try:
    while True:
        try:
          c = sys.stdin.read()
          if  c == "\x1b[A":
            print("driving forward")  
          elif  c == "\x1b[B":
            print("driving backward")                   
          elif  c == "\x1b[C":
            print("turning right") 
          elif  c == "\x1b[D":
            print("turning left")  
          elif c == "q":
            break
        except IOError: 
          pass
        except TypeError: 
          pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
