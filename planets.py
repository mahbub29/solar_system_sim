import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

au = 149597871
size_scalar = 10000
speed_scalar = 30
distance_scalar = 1


class Sun:
    def __init__(self, name, centre=np.array([[0.0], [0.0]]), size=696430, size_scalar=size_scalar):
        self.name = name
        self.centre = centre
        self.size = size / au * size_scalar


class Planet:
    def __init__(self, name, days_around_sun, centre, radius, color='b', size=10, size_scalar=size_scalar, speed_scalar=speed_scalar, distance_scalar=distance_scalar):
        self.name = name
        self.angular_velocity = 2*np.pi / days_around_sun * speed_scalar
        self.centre = centre
        self.position = np.array([[0.0], [radius]])
        self.radius = radius * distance_scalar
        self.color = color
        self.size = size / au * size_scalar

    def go(self, t):
        x = self.radius * np.sin(self.angular_velocity * t) + self.centre[0][0]
        y = self.radius * np.cos(self.angular_velocity * t) + self.centre[1][0]
        self.position[0][0], self.position[1][0] = x, y


class SolarSystem:
    def __init__(self, sun, planets, show_sun=False):
        self.sun = sun
        self.planets = planets
        self.show_sun = show_sun

    def go(self):
        fig = plt.figure()
        ax = plt.axes(xlim=(-40*distance_scalar, 40*distance_scalar), ylim=(-40*distance_scalar, 40*distance_scalar))
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        ax.set_aspect(abs(x1 - x0) / abs(y1 - y0))

        points = []

        if self.show_sun:
            sun, = ax.plot([], [], 'o', color='gold', markersize=self.sun.size)
            points.append(sun)

        for o in self.planets:
            planet, = ax.plot([], [], 'o', color=o.color, markersize=o.size)
            points.append(planet)
            orbit = plt.Circle((o.centre[0][0], o.centre[1][0]), o.radius, color='k', linewidth=0.05, fill=False)
            ax.add_patch(orbit)

        def initialize():
            for o in points:
                o.set_data([], [])

        def update(i):
            for p in self.planets:
                p.go(i)
            # print([(p.name, p.position.T) for p in self.planets])

            u = 0
            if self.show_sun:
                points[0].set_data(self.sun.centre[0][0], self.sun.centre[1][0])
                u = 1

            for j in range(len(self.planets)):
                points[j+u].set_data(self.planets[j].position[0][0],
                                   self.planets[j].position[1][0])

            return points,

        ani = FuncAnimation(fig, update, init_func=initialize, interval=1)

        plt.show()


year = 365.26

Sol = Sun("Sol")

Mercury = Planet('Mercury', 87.96, Sol.centre, 0.39, 'darkorange', 4878)
Venus = Planet('Venus', 224.68, Sol.centre, 0.723, 'khaki', 12104)
Earth = Planet('Earth', year, Sol.centre, 1.0, 'royalblue', 12756)
Mars = Planet('Mars', 686.98, Sol.centre, 1.524, 'orangered', 6787)
Jupiter = Planet('Jupiter', 11.862*year, Sol.centre, 5.203, 'darkorange', 142796)
Saturn = Planet('Saturn', 29.456*year, Sol.centre, 9.539, 'navajowhite', 120660)
Uranus = Planet('Uranus', 84.07*year, Sol.centre, 19.18, 'lightsteelblue', 51118)
Neptune = Planet('Neptune', 164.81*year, Sol.centre, 30.06, 'cornflowerblue', 48600)

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

ss = SolarSystem(Sol, planets)


if __name__ == '__main__':
    ss.go()
