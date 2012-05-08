from visual import *
import vturtle
import vturtle_camera
robot = vturtle.Robot()
vturtle_camera.fps_pov(robot,scene)
text(text='GAME OVER',pos=(robot._frame.x, robot._frame.y, 10), color=color.green,axis=(1,0,0))
