"""VPython-based robot simulator and turtle graphics engine.
by Eric Farmer (erfarmer@gmail.com)

This module simulates a wheeled robot that can execute Logo-like motion
commands.  The robot has a cylindrical chassis with a hole in its center
for inserting a colored marker, which leaves a trail as the robot moves.

With just this functionality, the module may be used as a turtle
graphics engine.  The speed of animation of the robot's motion is
configurable, from "realistic" to "instantaneous."  And thanks to
VPython, users can execute commands a line at a time from the
interpreter, and slew and zoom the 3D view of the robot even while it is
moving.

Example:
>>> import vturtle
>>> robot = vturtle.Robot()
>>> robot.forward(20)
>>> robot.left(90)

In addition, the robot has a stall sensor and configurable proximity
sensors for detecting and navigating around obstacles, such as walls or
other robots.  Convenience functions, table() and maze(), are provided
for creating a simple table top with four walled edges, or a simply
connected maze, respectively.

Example:
>>> import vturtle
>>> robot = vturtle.Robot(obstacles=vturtle.table())
>>> robot.forward(200) # run into wall
>>> stalled = robot.stalled()

Many thanks to the VPython developers for providing a very cool and
useful tool!
"""

# The software is provided "as is", without warranty of any kind, express
# or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfrigement.
# In no event shall the author be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising
# from, out of or in connection with the software or the use or other
# dealings in the software.

from visual import *

__all__ = ['Robot', 'Wall', 'table', 'maze']

class Robot:
    """Robot simulator with drawing pen and stall and proximity sensors.
    """

    def __init__(self, pos=(0, 0), sensors=[90, 0, -90], obstacles=[]):
        """Create a robot.

        Create a robot at the given (x,y) position (default at the
        origin) and facing along the positive x-axis, with a yellow pen
        for drawing a trail as the robot moves.

        Any specified sensors and obstacles are added using add_sensor()
        and add_obstacle(), respectively.
        """
        self._frame = frame(pos=pos)
        self._speed = 15 # cm/s
        self._fps = 24.0
        self._ff = 1
        self._radius = 9 # cm
        self._range = 10 # cm

        # Initialize pen and drawing trails.
        self._pen = cylinder(frame=self._frame, pos=(0,0,0), axis=(0,0,14),
                             radius=0.5, color=color.yellow)
        self._trail = curve(pos=[self._frame.pos], color=self._pen.color)
        self._trails = []

        # Create robot body.
        cylinder(frame=self._frame, pos=(0,0,2), axis=(0,0,4),
                 radius=self._radius, color=color.blue)

        # Add lights.
        sphere(frame=self._frame, pos=(6,3,6), radius=0.5, color=color.red)
        sphere(frame=self._frame, pos=(5.5,-2.5,6), radius=0.5,
               color=color.green)
        sphere(frame=self._frame, pos=(5.5,-1,6), radius=0.5, color=color.green)
        sphere(frame=self._frame, pos=(5.5,0.5,6), radius=0.5,
               color=color.green)

        # Add side wheels with tread.
        cylinder(frame=self._frame, pos=(0,7,4), axis=(0,1,0), radius=4,
                 color=color.gray(0.5))
        ring(frame=self._frame, pos=(0,7.5,4), axis=(0,1,0), radius=4,
             thickness=0.25, color=color.gray(0.25))
        cylinder(frame=self._frame, pos=(0,-7,4), axis=(0,-1,0), radius=4,
                 color=color.gray(0.5))
        ring(frame=self._frame, pos=(0,-7.5,4), axis=(0,-1,0), radius=4,
             thickness=0.25, color=color.gray(0.25))

        # Add front tricycle wheel.
        cylinder(frame=self._frame, pos=(7.5,-0.5,1.5), axis=(0,1,0),
                 radius=1.5, color=color.gray(0.5))

        # Initialize stall and proximity sensors and obstacles.
        self._stalled = False
        self._sensors = []
        for sensor in sensors:
            self.add_sensor(sensor)
        self._obstacles = []
        for obstacle in obstacles:
            self.add_obstacle(obstacle)

    def forward(self, distance):
        """Move forward the given distance (cm).

        The robot will stall if it encounters an obstacle between its
        current position and the given destination.
        """
        self.goto(self._frame.pos + distance * self._frame.axis)

    def backward(self, distance):
        """Move backward the given distance (cm).

        The robot will stall if it encounters an obstacle between its
        current position and the given destination.
        """
        self.goto(self._frame.pos - distance * self._frame.axis)

    def left(self, angle):
        """Turn left the given number of degrees.
        """
        if self._speed == Inf:
            self._frame.rotate(angle=radians(angle), axis=(0,0,1))
        else:
            psi = self.heading() + angle
            dpsi = sign(angle) * self._speed / self._fps / 7.5
            for r in arange(0, radians(angle), dpsi):
                if self._ff < Inf:
                    rate(self._fps * self._ff)
                self._frame.rotate(angle=dpsi, axis=(0,0,1))
            self._frame.rotate(angle=radians(mod(psi - self.heading() + 180,
                                                 360) - 180), axis=(0,0,1))

    def right(self, angle):
        """Turn right the given number of degrees.
        """
        self.left(-angle)

    def pen_up(self):
        """Pick up the robot's pen.

        Subsequent moves will not leave a drawing trail.
        """
        if self._trail:
            self._trails.append(self._trail)
            self._trail = False

    def pen_down(self):
        """Put down the robot's pen.

        Subsequent moves will leave a drawing trail.
        """
        if not self._trail:
            self._trail = curve(pos=[self._frame.pos], color=self._pen.color)

    def color(self, color=None, g=None, b=None):
        """Return or set the robot's pen color.

        Specify color with (red, green, blue) values in [0, 1], either
        as separate arguments or as a tuple.

        Changing the pen color while the pen is down will cause the next
        move to leave a "blended" trail from the previous drawing color
        to the new color.
        """
        if color is None:
            return self._pen.color
        if not g is None:
            color = (color, g, b)
        self._pen.color = color

    def clear(self):
        """Clear all of this robot's drawing trails.
        """
        if self._trail:
            self._trail.visible = False
        for trail in self._trails:
            trail.visible = False
        self._trail = False
        self._trails = []
        self.pen_down()

    def show(self):
        """Show the robot, making it visible.

        Visibility of the robot does not affect collisions with
        obstacles, sensor input, or whether or how the robot draws.
        """
        self._frame.visible = True

    def hide(self):
        """Hide the robot, making it invisible.

        Visibility of the robot does not affect collisions with
        obstacles, sensor input, or whether or how the robot draws.
        """
        self._frame.visible = False

    def goto(self, pos, y=None):
        """Move to the given (x,y) position without changing heading.

        Specify position either as separate (x, y) arguments or as a
        tuple.

        The robot will stall if it encounters an obstacle between its
        current position and the given destination.

        This method is an alias for position().
        """
        if self._trail:
            self._trail.append(pos=self._frame.pos, color=self._pen.color)
        if not y is None:
            pos = (pos, y)
        pos = vector(pos)
        last_pos = vector(self._frame.pos)
        dx = self._speed / self._fps
        while not self._check_stall() and abs(pos - self._frame.pos) > dx:
            if self._ff < Inf:
                rate(self._fps * self._ff)
            last_pos = vector(self._frame.pos)
            direction = norm(pos - self._frame.pos)
            self._frame.pos = self._frame.pos + direction * dx
            if self._trail:
                self._trail.pos[-1] = self._frame.pos
        if not self._stalled:
            last_pos = vector(self._frame.pos)
            self._frame.pos = pos
            self._check_stall()
        if self._stalled:
            self._frame.pos = last_pos
        if self._trail:
            self._trail.pos[-1] = self._frame.pos

    def position(self, pos=None, y=None):
        """Return or set the robot's current (x,y) position.

        Specify position either as separate (x, y) arguments or as a
        tuple.

        The robot will stall if it encounters an obstacle between its
        current position and the given destination.
        """
        if pos is None:
            return (self._frame.pos.x, self._frame.pos.y)
        self.goto(pos, y)

    def heading(self, angle=None):
        """Return or set the robot's current heading (deg).
        """
        current = mod(degrees(atan2(self._frame.axis.y, self._frame.axis.x)),
                      360)
        if angle is None:
            return current
        self.left(mod(angle - current + 180, 360) - 180)

    def distance(self, pos, y=None):
        """Return distance (cm) from this robot to the given position.

        Specify position either as separate (x, y) arguments or as a
        tuple.
        """
        if not y is None:
            pos = (pos, y)
        return mag(vector(pos) - self._frame.pos)

    def towards(self, pos, y=None):
        """Return heading (deg) from this robot to the given position.

        Specify position either as separate (x, y) arguments or as a
        tuple.
        """
        if not y is None:
            pos = (pos, y)
        v = vector(pos) - self._frame.pos
        return mod(degrees(atan2(v.y, v.x)), 360)

    def speed(self, speed=None):
        """Return or set the speed of this robot (cm/s).

        Setting speed to Inf causes the robot to move/turn
        instantaneously.

        Changing the robot's speed affects whether and how it encounters
        or detects obstacles, by changing how far the robot moves in
        each frame of animation.

        To control speed of execution when not using obstacles or
        sensors, use speed().  To control animation frame rate with
        reproducible obstacle navigation behavior, use fast_forward().
        """
        if speed is None:
            return self._speed
        self._speed = speed

    def fast_forward(self, speedup=None):
        """Return or set the animation speed of this robot.

        Specify speedup as a frame rate multiplier.  For example, 1 is
        the default normal speed, and 2 is twice normal speed.  Setting
        speedup to Inf causes the animation to move as fast as possible.

        Changing the animation speed only affects the time delay between
        frames of animation.  It does not affect whether or how the
        robot encounters or detects obstacles.

        To control speed of execution when not using obstacles or
        sensors, use speed().  To control animation frame rate with
        reproducible obstacle navigation behavior, use fast_forward().
        """
        if speedup is None:
            return self._ff
        self._ff = speedup

    def stalled(self):
        """Return current state of the robot's stall sensor.

        Return True if the robot is stalled after encountering an
        obstacle, False otherwise.
        """
        return self._stalled

    def add_sensor(self, bearing):
        """Add proximity sensor mounted at the given bearing (deg).

        The integer id of the sensor is returned, for use with sensor().
        Three sensors are available by default, with ids 0 (left),
        1 (front), and 2 (right).

        Example:
        >>> rear_id = robot.add_sensor(180)
        >>> detect = robot.sensor(rear_id)
        """
        sensor_id = len(self._sensors)
        self._sensors.append(radians(bearing))
        return sensor_id

    def sensor_range(self, distance=None):
        """Return or set the range of robot's proximity sensors (cm).

        The sensors are mounted on the circumference of the robot's
        cylindrical chassis (9 cm radius).
        """
        if distance is None:
            return self._range
        self._range = distance

    def sensor(self, sensor_id):
        """Return current state of the given proximity sensor.

        Return True if an obstacle is within range in the direction of
        the given sensor, False otherwise.
        """
        x1 = self._frame.pos
        x2 = x1 + ((self._radius + self._range) *
                   rotate(self._frame.axis, self._sensors[sensor_id]))
        for obstacle in self._obstacles:
            if obstacle._intersect_segment(x1, x2):
                return True
        return False

    def add_obstacle(self, obstacle):
        """Register obstacle (Wall or another Robot) with this robot.

        Only registered obstacles affect the robot's movement and
        sensors.
        """
        self._obstacles.append(obstacle)
        self._check_stall()

    def _check_stall(self):
        for obstacle in self._obstacles:
            self._stalled = obstacle._intersect_circle(self._frame.pos,
                                                       self._radius)
            if self._stalled:
                break
        return self._stalled

    def _intersect_circle(self, center, radius):
        radius = radius + self._radius + 0.05
        return mag2(center - self._frame.pos) <= radius * radius

    def _intersect_segment(self, x1, x2):
        v = x1 - self._frame.pos
        w = x2 - x1
        a = mag2(w)
        b = 2 * dot(v, w)
        c = mag2(v) - self._radius * self._radius
        d = b * b - 4 * a * c
        if d >= 0:
            d = sqrt(d)
            return (0 <= -b + d <= 2 * a) or (0 <= -b - d <= 2 * a)
        return False

class Wall:
    """Wall obstacle.
    """

    def __init__(self, x1, x2, **args):
        """Create a wall between (x,y) positions x1 and x2.

        A wall is a VPython box 1 cm wide, 15 cm tall, with optional
        additional box() arguments specifying material properties.  For
        example:

        >>> from visual import *
        >>> wall = vturtle.Wall((50, -50), (50, 50), material=materials.wood)
        """
        height = 15.0
        x1 = vector(x1)
        x2 = vector(x2)
        x1.z = height / 2
        x2.z = x1.z
        self._wall = box(pos=((x1 + x2) / 2), axis=(x2 - x1),
                         height=1, width=height, **args)
        x1.z = 0
        x2.z = 0
        self._x1 = x1
        self._x2 = x2
        self._a = mag2(self._wall.axis)

    def _intersect_circle(self, center, radius):
        radius = radius + 0.55
        v = self._x1 - center
        b = 2 * dot(v, self._wall.axis)
        c = mag2(v) - radius * radius
        d = b * b - 4 * self._a * c
        if d >= 0:
            d = sqrt(d)
            return (0 <= -b + d <= 2 * self._a) or (0 <= -b - d <= 2 * self._a)
        return False

    def _intersect_segment(self, x1, x2):
        return ((self._ccw(self._x1, x1, x2) != self._ccw(self._x2, x1, x2)) and
                (self._ccw(self._x1, self._x2, x1) !=
                 self._ccw(self._x1, self._x2, x2)))

    def _ccw(self, a, b, c):
        return (b.x - a.x) * (c.y - a.y) > (c.x - a.x) * (b.y - a.y)

def table(center=(0,0), length=200, width=200):
    """Create a table with walled edges.

    This is a convenience function for creating a standard "tabletop"
    with Wall() edge obstacles for use with add_obstacle().  The list of
    walls is returned.
    """
    c = vector(center)
    dx = vector(length / 2.0, 0, 0)
    dy = vector(0, width / 2.0, 0)
    box(pos=(c.x, c.y, -1.1), length=length, height=width, width=2,
        color=color.gray(0.25), material=materials.emissive)
    walls = []
    walls.append(Wall(c - dx + dy, c + dx + dy, material=materials.rough))
    walls.append(Wall(c - dx - dy, c + dx - dy, material=materials.rough))
    walls.append(Wall(c + dx - dy, c + dx + dy, material=materials.rough))
    walls.append(Wall(c - dx - dy, c - dx + dy, material=materials.rough))
    return walls

def maze(pos=(0,0), rows=8, columns=8, cell_size=30):
    """Create a maze on a table with walled edges.

    This is a convenience function for creating a simply connected
    binary tree maze with Wall() edge obstacles for use with
    add_obstacle().  The list of walls is returned.

    The given (x,y) position specifies the location of the center of the
    lower left cell of the maze.  The autocenter flag of the current
    display is temporarily enabled to center the maze within the viewing
    window.
    """
    flag = display.get_selected().autocenter
    display.get_selected().autocenter = True
    dx = vector(cell_size, 0, 0)
    dy = vector(0, cell_size, 0)
    pos = vector(pos) + (dx + dy) / 2
    walls = table(center=pos + dx * (columns / 2.0 - 1) + dy * (rows / 2.0 - 1),
                  length=columns * cell_size, width=rows * cell_size)
    for row in range(rows - 1):
        for col in range(columns - 1):
            c = pos + dx * col + dy * row
            if random.randint(2) == 0:
                walls.append(Wall(c, c - dy))
            else:
                walls.append(Wall(c - dx, c))
    display.get_selected().autocenter = flag
    return walls

if __name__ == "__main__":
    robot = Robot(obstacles=table())
