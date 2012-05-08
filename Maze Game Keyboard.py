from visual import *
from visual.controls import *
win = controls(title='Play Again?',x=60, y=90, width=300, height=300, range=50)
def main():
    win.visible = False
    import sys
    import vturtle
    import random
    import vturtle_camera
    import pygame
    import time
    robot = vturtle.Robot(obstacles=vturtle.maze())
    robot.pen_up()
    center = vturtle_camera.fps_pov(robot,scene)
    robot.speed(50)
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

    vturtle_camera.fps_pov(robot, scene)
    time = 0
    fpv = True

    while True:
        rate(100)
        if scene.kb.keys:
            s = scene.kb.getkey()
            robx = int(robot._frame.x)
            roby = int(robot._frame.y)
            if robx in range(int(circle.pos.x-10),int(circle.pos.x + 10)) and roby in range(int(circle.pos.y-10),int(circle.pos.y + 10)):
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
    gameOver(robot,scene,center)
    
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
    newgame = button(pos=(0,0), width=60, height=60, text='Play Again?', action=lambda: main())
    

main()

