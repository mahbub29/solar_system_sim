from celestial_bodies import *
from celestial_system import *

# Centre
Sol = CelestialCentre("Sol")

# Circular Orbits
Mercury = CelestialBody('Mercury', 87.96, Sol.centre, 0.39, 'darkorange', 4878)
Venus = CelestialBody('Venus', 224.68, Sol.centre, 0.723, 'khaki', 12104)
Earth = CelestialBody('Earth', year, Sol.centre, 1.0, 'royalblue', 12756)
Mars = CelestialBody('Mars', 686.98, Sol.centre, 1.524, 'orangered', 6787)
Jupiter = CelestialBody('Jupiter', 11.862*year, Sol.centre, 5.203, 'darkorange', 142796)
Saturn = CelestialBody('Saturn', 29.456*year, Sol.centre, 9.539, 'navajowhite', 120660)
Uranus = CelestialBody('Uranus', 84.07*year, Sol.centre, 19.18, 'lightsteelblue', 51118)
Neptune = CelestialBody('Neptune', 164.81*year, Sol.centre, 30.06, 'cornflowerblue', 48600)

# Elliptical Orbits
pluto_orbit_a, pluto_orbit_b = 49.3, 29.7
angle = 45
Pluto = CelestialBody('Pluto', 247.7*year, Sol.centre, (pluto_orbit_a, pluto_orbit_b), 'gray', 12104, alpha=angle)

# Earth moon
Moon = CelestialBody('Moon', 28, Earth.position, 0.1, 'w', 3475)

# Jupiter moons
Europa = CelestialBody('Europa', 3.55, Jupiter.position, 670900/au, 'goldenrod', 3140)
Ganymede = CelestialBody('Ganymede', 7.16, Jupiter.position, 1070000/au, 'beige', 5260)
Callisto = CelestialBody('Callisto', 16.69, Jupiter.position, 1883000/au, 'darkkhaki', 4800)
Io = CelestialBody('Io', 1.77, Jupiter.position, 421600/au, 'yellow', 3630)

# comets
Halleys_comet = CelestialBody("Halley's comet", 75.32*year, Sol.centre, (35.08, 0.586), 'white', 20000, alpha=0)

cb = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Europa, Ganymede, Callisto, Io]

solar_system = CelestialSystem(Sol, cb)


if __name__ == '__main__':
    solar_system.go(show_orbit=True, show_sun=False)


