import numpy as np
from defaults import *


class CelestialCentre:
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
        X = np.matmul(self.transmat(t), np.array([[self.radius_a], [self.radius_b]]))
        if self.alpha is not None:
            X = np.matmul(self.rotmat, self.position)
        X = X + self.centre
        self.position[0][0], self.position[1][0] = X[0][0], X[1][0]

    def transmat(self, t):
        return np.array([[np.sin(self.angular_velocity*t), 0], [0, np.cos(self.angular_velocity*t)]])