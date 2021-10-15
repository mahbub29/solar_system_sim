import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse

au = 149597871
size_scalar = 1
speed_scalar = 0.01
distance_scalar = 1


class Sun:
    def __init__(self, name, centre=np.array([[0.0], [0.0]]), size=696430, size_scalar=size_scalar):
        self.name = name
        self.centre = centre
        self.size = size / au * size_scalar


class CelestialBody:
    def __init__(self, name, days_around_sun, centre, radius,
                 color='b', size=10, size_scalar=size_scalar,
                 speed_scalar=speed_scalar, distance_scalar=distance_scalar, alpha=None):
        self.name = name
        self.angular_velocity = 2*np.pi / days_around_sun * speed_scalar
        self.centre = centre
        self.radius_a, self.radius_b = 0, 0
        if type(radius) is tuple:
            self.radius_a = radius[0] * distance_scalar
            self.radius_b = radius[1] * distance_scalar
        else:
            self.radius_a = radius * distance_scalar
            self.radius_b = radius * distance_scalar
        self.position = np.array([[0.0], [self.radius_a]])
        self.color = color
        self.size = size / au * size_scalar
        self.alpha = alpha
        self.rotmat = None
        if alpha is not None:
            self.rotmat = np.array([[np.cos(alpha/180*np.pi), -np.sin(alpha/180*np.pi)],
                                    [np.sin(alpha/180*np.pi), np.cos(alpha/180*np.pi)]])

    def go(self, t):
        x = self.radius_a * np.sin(self.angular_velocity * t) + self.centre[0][0]
        y = self.radius_b * np.cos(self.angular_velocity * t) + self.centre[1][0]
        self.position[0][0], self.position[1][0] = x, y

        if self.alpha is not None:
            self.position = np.matmul(self.rotmat, self.position)


class SolarSystem:
    def __init__(self, sun, bodies):
        self.sun = sun
        self.bodies = bodies

    def go(self, show_sun=False, show_orbit=False):
        fig = plt.figure()
        ax = plt.axes(xlim=(-50*distance_scalar, 50*distance_scalar), ylim=(-50*distance_scalar, 50*distance_scalar))
        ax.set_facecolor([0,0,0])
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        ax.set_aspect(abs(x1 - x0) / abs(y1 - y0))

        points = []

        if show_sun:
            sun = plt.Circle((self.sun.centre[0][0], self.sun.centre[1][0]), self.sun.size/2, color='gold')
            points.append(sun)

        for o in self.bodies:
            celestial_body = plt.Circle((o.position[0][0], o.position[1][0]), o.size/2, color=o.color)
            points.append(celestial_body)

            if show_orbit:
                if o.radius_a == o.radius_b:
                    orbit = plt.Circle((o.centre[0][0], o.centre[1][0]), o.radius_a,
                                       color='w', linewidth=0.1, fill=False)
                    points.append(orbit)
                else:
                    orbit = Ellipse(xy=(o.centre[0][0], o.centre[1][0]),
                                    width=o.radius_a*2,
                                    height=o.radius_b*2,
                                    edgecolor='w', fc='None', lw=0.1, angle=o.alpha)
                    points.append(orbit)

        def initialize():
            u = 0
            if show_sun:
                points[0].center = (self.sun.centre[0][0], self.sun.centre[1][0])
                ax.add_patch(points[0])
                u = 1

            for j in range(int(len(points)/2-u)):
                points[2*j+u].center = (self.bodies[j].position[0][0], self.bodies[j].position[1][0])
                ax.add_patch(points[2*j+u])
                points[2*j+u+1].center = (self.bodies[j].centre[0][0], self.bodies[j].centre[1][0])
                ax.add_patch(points[2*j+u+1])

            return points,

        def update(i):
            for p in self.bodies:
                p.go(i)

            u = 0
            if show_sun:
                points[0].center = (self.sun.centre[0][0], self.sun.centre[1][0])
                u = 1

            for j in range(len(self.bodies)):
                points[2*j+u].center = (self.bodies[j].position[0][0], self.bodies[j].position[1][0])
                points[2*j+u+1].center = (self.bodies[j].centre[0][0], self.bodies[j].centre[1][0])

            return points,

        ani = FuncAnimation(fig, update, init_func=initialize, interval=1)

        plt.show()


year = 365.26

Sol = Sun("Sol")

Mercury = CelestialBody('Mercury', 87.96, Sol.centre, 0.39, 'darkorange', 4878)
Venus = CelestialBody('Venus', 224.68, Sol.centre, 0.723, 'khaki', 12104)
Earth = CelestialBody('Earth', year, Sol.centre, 1.0, 'royalblue', 12756)
Mars = CelestialBody('Mars', 686.98, Sol.centre, 1.524, 'orangered', 6787)
Jupiter = CelestialBody('Jupiter', 11.862*year, Sol.centre, 5.203, 'darkorange', 142796)
Saturn = CelestialBody('Saturn', 29.456*year, Sol.centre, 9.539, 'navajowhite', 120660)
Uranus = CelestialBody('Uranus', 84.07*year, Sol.centre, 19.18, 'lightsteelblue', 51118)
Neptune = CelestialBody('Neptune', 164.81*year, Sol.centre, 30.06, 'cornflowerblue', 48600)
Pluto = CelestialBody('Pluto', 247.7*year, Sol.centre, (29.7, 49.3), 'gray', 12104, alpha=-45)

# Earth moon
Moon = CelestialBody('Moon', 28, Earth.position, 0.1, 'w', 3475)

# Jupiter moons
Europa = CelestialBody('Europa', 3.55, Jupiter.position, 670900/au, 'goldenrod', 3140)
Ganymede = CelestialBody('Ganymede', 7.16, Jupiter.position, 1070000/au, 'beige', 5260)
Callisto = CelestialBody('Callisto', 16.69, Jupiter.position, 1883000/au, 'darkkhaki', 4800)
Io = CelestialBody('Io', 1.77, Jupiter.position, 421600/au, 'yellow', 3630)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Europa, Ganymede, Callisto, Io]

ss = SolarSystem(Sol, planets)


if __name__ == '__main__':
    ss.go(show_orbit=True, show_sun=True)
