"""Module of functions for manipulating the VTurtle robot camera view.

Example:
>>> from visual import *
>>> import vturtle
>>> import vturtle_camera
>>> robot = vturtle.Robot(obstacles=vturtle.maze())
>>> center = vturtle_camera.fps_pov(robot, scene)
>>> robot.left(3)
>>> vturtle_camera.fps_pov(robot, scene)
"""

from visual import *

def fps_pov(robot, scene):
    """Change the camera view to look from the position of the robot.

    Returns the current camera "center."  To restore the original camera
    view, call top_pov(robot, scene, center).
    """
    center = vector(scene.center)
    robot.hide()
    scene.autoscale = False
    scene.forward = rotate((1, 0, 0), radians(robot.heading()), (0, 0, 1))
    scene.up = (0, 0, 1)
    scene.center = vector(0, 0, 8) + robot.position() + scene.forward * mag(
        scene.center - scene.mouse.camera)
    return center

def top_pov(robot, scene, center):
    """Change the camera view to look from the default top-down view.
    """
    robot.show()
    scene.autoscale = True
    scene.forward = (0, 0, -1)
    scene.up = (0, 1, 0)
    scene.center = center
