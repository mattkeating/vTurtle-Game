from visual import *
import vturtle
import pygame
import vturtle_camera
robot = vturtle.Robot(obstacles=vturtle.maze())
robot.pen_up()
robot.speed(50)
pygame.init()
circle = sphere(pos=(0,30,5), radius=5, color=color.red)
time = 0
robot.hide()
##vturtle_camera.fps_pov(robot, scene)
print pygame.joystick.get_count()
stick = pygame.joystick.Joystick(0)
stick.init()
fpv = True

while True:

    if robot.pos() == sphere.pos():
        print "GAME WON!"
    
    pygame.event.get()
    x = stick.get_axis(0)
    y = stick.get_axis(1)
    a = stick.get_button(11)
    xbutton = stick.get_button(13)
    if y > .8:
        robot.backward(10)
        if fpv == True:    
            vturtle_camera.fps_pov(robot, scene)
    if y < -.8:
        robot.forward(10)
        if fpv == True:
            vturtle_camera.fps_pov(robot, scene)
    if x > .8:
        robot.right(10)
        if fpv == True:
            vturtle_camera.fps_pov(robot, scene)
    if x < -.8:
        robot.left(10)
        if fpv == True:
            vturtle_camera.fps_pov(robot, scene)
    if xbutton > 0:
        robot.pen_down()

        ## A - button 11
        ## B - button 12
        ## Y - button 14
        ## X - button 13
