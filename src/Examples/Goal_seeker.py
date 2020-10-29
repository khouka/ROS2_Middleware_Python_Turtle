import turtle
from tkinter import PhotoImage
from turtle import Turtle, Screen, Shape
import math
import random

myscreen = turtle.Screen()
myscreen.title("Turtle_Driver")
myscreen.bgcolor("silver")
myscreen.setup(1100,1000)

class Driver:
      def __init__(self):
          myscreen.tracer(0)
          self.xcor = 0
          self.ycor = 0     
          while True:
            myscreen.ontimer(self.Activity(), 300)
                                               

      def move_goal(self):          
          Goal.goto(self.xcor,self.ycor) 
       
      def robo_path_set(self):  
          Robot.setheading(Robot.towards(Goal))        
          Robot.fd(20)

      def Output(self):
          r_y = int(Robot.ycor()) 
          r_x = int(Robot.xcor())
          g_y = int(Goal.ycor()) 
          g_x = int(Goal.xcor()) 
          print ("Turtle:", int(r_x), int(r_y))
          print ("Goal:", int(g_x), int(g_y))
          self.dist = math.sqrt((g_x - r_x) **2 + (g_y - r_y) **2)
          print ("Distance left:", self.dist)  
      
      def Update_goal(self):        
          if self.dist <= 10:   
             print("checkpoint successfully reached")     
             self.xcor = random.randint(-400,350)
             self.ycor = random.randint(-400,350)
             Goal.goto(self.xcor, self.ycor)  
       
      def Activity(self):
          myscreen.update() 
          self.robo_path_set()
          self.move_goal()
          self.Output() 
          self.Update_goal()                      
    
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
       myscreen.addshape("goal", Shape("image", goal))
       self.shape("goal")
       self.penup()
       self.speed(0)

Goal = Goal()

          
                        
if __name__ == '__main__':
    Driver()
