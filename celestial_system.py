from defaults import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse


class CelestialSystem:
    def __init__(self, sun, bodies):
        self.sun = sun
        self.bodies = bodies

    def go(self, show_sun=False, show_orbit=False):
        fig = plt.figure()
        ax = plt.axes(xlim=(-side*distance_scalar, side*distance_scalar), ylim=(-side*distance_scalar, side*distance_scalar))
        ax.set_facecolor([0,0,0])
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        ax.set_aspect(abs(x1 - x0) / abs(y1 - y0))

        yr_count = ax.text(-40, -40, '0 years', size=12, color='w')

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
                    if o.alpha is not None:
                        orbit = Ellipse(xy=(o.centre[0][0], o.centre[1][0]),
                                        width=o.radius_a*2,
                                        height=o.radius_b*2,
                                        edgecolor='w', fc='None', lw=0.1, angle=o.alpha)
                    else:
                        orbit = Ellipse(xy=(o.centre[0][0], o.centre[1][0]),
                                        width=o.radius_a * 2,
                                        height=o.radius_b * 2,
                                        edgecolor='w', fc='None', lw=0.1)
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

            return [[points], yr_count]

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

            yr_count.set_text(str(round(speed_scalar*i/365, 2)) + ' years')

            return [[points], yr_count]

        ani = FuncAnimation(fig, update, init_func=initialize, interval=1)

        plt.show()