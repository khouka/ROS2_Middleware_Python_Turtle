import turtle
from tkinter import PhotoImage

class TurtleMaze:

    def __init__(self):
       self.myscreen =  turtle.Screen()
       self.myscreen.title("Turtle road")
       self.myscreen.bgcolor("silver")
       self.myscreen.setup(1200,700)
       self.Turtlebot()
       self.Pen()     
       self.maze()
       self.setup_maze(self.blocks[1])
   
    def Pen(self):
       sQuare = PhotoImage(file="images/block.gif").zoom(1,1)          
       self.myscreen.addshape("sQuare", turtle.Shape("image", sQuare))
       self.pen = turtle.Turtle()
       self.pen.shape("sQuare")
       self.pen.penup()
       self.pen.speed(0)

    def Turtlebot(self):
       self.turtlebot = turtle.Turtle()
       self.turtlebot.shape("turtle")
       self.turtlebot.color("black")
       self.turtlebot.penup()
       self.turtlebot.speed(0)
       self.turtlebot.setheading(180)
    
    def maze(self):
       self.blocks = [""]
       maze_blocks = [
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
"X              X                           T X",
"X  XXXXXXXXXX  XXXXXXXXXXXXX  XXXXXXX  XXXX  X",
"X           X                 X        X     X",
"X  XXXXXXXXXX  XXXXXXXXXXXXX  XXXXXXXXXXXXX  X",
"X  X     X  X           X  X                 X",
"X  X  X  X  X  X   XXX  X  X  XXXXXXXXXXXXX  X",
"X  X  X  X  X  X  X     X  X  X  X        X  X",
"X  X  XXXX  X  XXXXXXXXXX  X  X  XXXX  X  X  X",
"X  X     X  X              X           X  X  X",
"X  XXXX  X  XXXXXXXXXXXXXXXX  XXXXXXXXXXXXX  X",
"X     X  X                    X              X",
"XXXX  X  XXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXX  X",
"X  X  X                    X     X        X  X",
"X  X  XXXX  XXXXXXXXXXXXX  X  XXXX  X  X  X  X",
"X  X  X     X     X     X  X  X     X  X  X  X",
"X  X  X     X     X     X  X  X     X     X  X",
"X  X  X  XXXXXXX  XXXX  X  X  X  XXXXXXXXXX  X",
"X                       X  X  X              X",
"XXXX  X  X  XXXXXXXXXX  X  X  X  XXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXX",
]
       self.blocks.append(maze_blocks)
       self.walls = []
    
    def setup_maze(self, block):
       for y in range(len(block)):
         for x in range(len(block[y])):
           character = block [y] [x]
           screen_x = -550 + (x * 24)
           screen_y = 250 - (y * 24)                    
           if character == "T":
                self.turtlebot.goto(screen_x, screen_y)
           if character == "X":
                self.pen.goto(screen_x, screen_y)
                self.pen.stamp() 
                self.walls.append((screen_x, screen_y))
          
TurtleMaze()
turtle.mainloop()
