from visual import *
from visual.controls import *
import vturtle
import random
import vturtle_camera
import pygame
import time
foc = True
sb = False
def aboutMenu(b,but):
   scene2 = display(title='About Us',
   x=20, y=20, width=600, height=500,
   background=(0,0,0))
   scene2.selected = True
   ltxt = label(pos=(10000,700,0), text='                  About Us\nWe are a group of 8th grade programmers \ntaught by (name) Farmer\n We hope you enjoy Robot-MazeRunner ',font="sans",height=20)
   etxt = label(pos=(10000,600,0), text='Press x to close',font="sans",height=20,color = color.red)
   scene2.exit = False
   scene2.center = ltxt.pos
   while True:
       if scene2.kb.keys:
           s = scene2.kb.getkey()
           if s == "x":
               scene.selected = True
               b.color = color.white
               foc = True
               scene2.visible = False
               b.color = color.white
               for bb in but:
                   bb.visible = False
               tMenu()


def tMenu():
   def operation(b):
       if b.pos == startbutton.pos:
           for o in buttons:
               o.visible = False
           for l in labs:
               l.visible = False
           for ob in scene.objects:
               if isinstance(ob,box):
                   ob.visible=False
           main()
       if b.pos == aboutbutton.pos:
           foc = False
           aboutMenu(b,buttons)

       if b.pos == closebutton.pos:
           scene.visible = false
   robot = vturtle.Robot(pos = (0,0),obstacles=vturtle.maze())
   robot.hide()
   x = 0
   startbutton = box(pos=(90,140,10),height=30,length=100,width=10)
   aboutbutton = box(pos=(90,90,10),height=30,length=100,width=10)
   closebutton = box(pos=(90,40,10),height=30,length=100,width=10)
   sb = True

   lstart = label(pos=(90,140,11), text='Start',font="sans",height=20)
   labout = label(pos=(90,90,11), text='About us',font="sans",height=20)
   lclose = label(pos=(90,37,11), text='Close',font="sans",height=20,color=color.red)

   l = label(pos=(95,200,0), text='Robot-MazeRunner!',font="sans",height=20)

   buttons = [startbutton,aboutbutton,closebutton]
   labs = [lstart,labout,lclose,l]
   while foc:
       if scene.mouse.clicked:
           m = scene.mouse.getclick()
           loc = m.pos
           mx = int(loc.x)
           my = int(loc.y)
           for b in buttons:
               bloc = b.pos
               bx = int(bloc.x)
               by = int(bloc.y)
               if mx in range(bx-50,bx+50):
                   if my in range (by-25,by+25):
                       b.color = color.blue

                       operation(b)

def gameOver(robot,scene,center):
    
    import vturtle_camera
    import time
    vturtle_camera.top_pov(robot,scene,center)
    y = 175
    c = 1
    while y > 0:
        if c == 1:
            text(text='YOU WON!', pos=(30,y,50),color=color.green,height=20)
        if c == 2:
            text(text='YOU WON!', pos=(30,y,50),color=color.cyan,height=20)
        if c == 3:
            text(text='YOU WON!', pos=(30,y,50),color=color.red,height=20)
        if c == 4:
            text(text='YOU WON!', pos=(30,y,50),color=color.yellow,height=20)
        if c == 5:
            text(text='YOU WON!', pos=(30,y,50),color=color.magenta,height=20)
        if c == 6:
            text(text='YOU WON!', pos=(30,y,50),color=color.orange,height=20)
        y = y - 30
        time.sleep(.05)
        c = c + 1
    
    win.visible = True
    newgame = button(pos=(0,0), width=60, height=60, text='Play Again?', action=lambda: main()


def main():
   score = 0
   print "init"

   robot = vturtle.Robot(pos = (0,0),obstacles=vturtle.maze())
   center = scene.center
   robot.pen_up()
   robot.speed(50)
   cirle = None
   vturtle_camera.fps_pov(robot, scene)

   loc = random.randint(1,3)
   loc = 1
   iterator = 0
   cubes = []
   rint = random.randint(5,20)
   while iterator <= rint:
       x = random.randint(20,200)
       y = random.randint(20,200)
       for ob in scene.objects:
           if ob.x == x or ob.y == y:
               continue
       mycube = box(pos=(x,y,5),color=color.red,height=2,width=2,length=2)
       cubes.append(mycube)
       iterator = iterator + 1

   if loc == 1:
       circle = sphere(pos=(210,210,5), radius=5, color=color.red)
   if loc == 2:
       circle = sphere(pos=(0,215,5), radius=5, color=color.red)
   if loc == 3:
       circle = sphere(pos=(210,0,5), radius=5, color=color.red)
   time.sleep(2)
   vturtle_camera.fps_pov(robot, scene)
   robot.hide()
   fpv = True

   while True:
       rate(100)
       for c in cubes:
           x = int(robot._frame.x)
           y = int(robot._frame.y)
           if x in range(int(c.x-10),int(c.x+10)):
               if y in range(int(c.y-10),int(c.y+10)):
                   c.visible = False
                   cubes.remove(c)
                   score = score + 1

       if scene.kb.keys:
           s = scene.kb.getkey()
           robx = int(robot._frame.x)
           roby = int(robot._frame.y)

           if robx in range(int(circle.pos.x-10),int(circle.pos.x + 10)) and roby in range(int(circle.pos.y-10),int(circle.pos.y + 10)):
               x = int(robot._frame.x)
               y = int(robot._frame.y)
               z = 8
               if (loc == 1):
                  break
            
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

                   


tMenu()
