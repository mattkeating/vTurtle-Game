from visual import *
def main():
       import vturtle
       import random
       import vturtle_camera
       import pygame
       import time
      # import WinMenu
       robot = vturtle.Robot(obstacles=vturtle.maze())
       robot.pen_up()
       robot.speed(50)
       cirle = None
       ## TO DO:
       ## Distance detection from sphere
       ## Image overlay sphere?

       loc = random.randint(1,3)
       if loc == 1:
           ## Upper Right
           circle = sphere(pos=(210,210,5), radius=5, color=color.red)
       if loc == 2:
           ## Upper Left
           circle = sphere(pos=(0,215,5), radius=5, color=color.red)
       if loc == 3:
           ## Bottom Right
           circle = sphere(pos=(210,0,5), radius=5, color=color.red)

       time.sleep(.5)
       vturtle_camera.fps_pov(robot, scene)
       time = 0
       robot.hide() 
       fpv = True
       #print loc
       #print circle.pos
       while True:
           rate(100)
           
           if scene.kb.keys:
               s = scene.kb.getkey()
               robx = int(robot._frame.x)
               roby = int(robot._frame.y)
               #print "x ",robx
               #print "y ",roby
               
               
               #print robot.position
               if robx in range(int(circle.pos.x-10),int(circle.pos.x + 10)) and roby in range(int(circle.pos.y-10),int(circle.pos.y + 10)):
                   #root = Tk()
                   #WinMenu(root)
                   print "Hi"
                   break
               """
               if loc == 1:
                   if robx in range(200,210):
                                    if roby in range(200,210):
                                        print "Winner"
                                        break;
               if loc == 2:
                   if robx == 0:
                       if roby in range(205,215):
                           print "Winner"
                           break;
               if loc == 3:
                   if robx in range(200,210):
                       if roby == 0:
                           print "Winner"
                           break;
               """


               if s == 'down':
                   robot.backward(10)
                   if fpv == True:    
                       vturtle_camera.fps_pov(robot, scene)
               if s == 'up':
                   robot.forward(10)
                   if fpv == True:
                       vturtle_camera.fps_pov(robot, scene)
               if s == 'right':
                   robot.right(10)
                   if fpv == True:
                       vturtle_camera.fps_pov(robot, scene)
               if s == 'left':
                   robot.left(10)
                   if fpv == True:
                       vturtle_camera.fps_pov(robot, scene)
main()
