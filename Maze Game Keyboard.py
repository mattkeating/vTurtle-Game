# -*- coding: utf-8 -*-
from visual import *
def main():
    import vturtle
    import random
    import vturtle_camera
    import pygame
    import time
    robot = vturtle.Robot(obstacles=vturtle.maze())
    robot.pen_up()
    robot.speed(50)
    loc = random.randint(1,3)
    if loc == 1:
        ## Upper Right
        circle = sphere(pos=(210,210,1), radius=5, color=color.red)
    if loc == 2:
        ## Upper Left
        circle = sphere(pos=(0,215,1), radius=5, color=color.red)
    if loc == 3:
        ## Bottom Right
        circle = sphere(pos=(210,0,1), radius=5, color=color.red)

    time.sleep(.5)
    vturtle_camera.fps_pov(robot, scene)
    time = 0
    robot.hide() 
    fpv = True
    Cicle = None
    
    while True:
        rate(100)
        
        if scene.kb.keys:
            s = scene.kb.getkey()
            robx = int(robot._frame.x)
            roby = int(robot._frame.y)
            if robx in range(int(circle.pos.x-10),int(circle.pos.x + 10)) and roby in range(int(circle.pos.y-10),int(circle.pos.y + 10)):
                gameOver()
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
          


def gameOver():
    import vturtle
    import vturtle_camera
    robot = vturtle.Robot(obstacles=vturtle.maze())
    text(text='GAME OVER',pos=(robot._frame.x+10, robot._frame.y+10, 1), depth=-0.3, color=color.green)


main()


