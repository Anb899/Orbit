# Anuj Brahmania

# Importing module's that we will need, and initialize pygame.
import pygame
import math

pygame.init()

# Set up a window size
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Colors that we will be using, and font/size of text
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (190, 40, 50)
GREY = (44, 44, 44)

FONT = pygame.font.SysFont("comiscans", 18)


class Planet:
    # Distance from sun, km to meters (AU = distance from earth to sun approximately )
    AU = (149.6e6 * 1000)
    # Gravitational force
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 2000 * 24  # Represents 1 day, speed at which planets orbit the sun


    # Setting up initialization values
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        # Draw in the center of the screen
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # list of updated points which are x and y coordinates to scale
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)  # draw lines between the points

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # Creating text object that will display distance from sun to each planet
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            # draw text and shift over so number appear bottom left for each planet
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    # Calculate force of attraction between another object and current object
    def attraction(self, other):
        # distance between the 2 objects
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        # If object is the sun, store the distance
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2  # Straight line force
        theta = math.atan2(distance_y, distance_x)  # calculate the angle
        force_x = math.cos(theta) * force  # x force
        force_y = math.sin(theta) * force  # y force
        return force_x, force_y

    def update_position(self, planets):
        # Total forces exerted on this planet that is not the planet itself
        total_fx = total_fy = 0
        # For every planet calculate the force x and force y occurring
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # use these forces to calculate the velocity of the planet's
        # increasing velocity by the acceleration multiplied by the TIMESTEP
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # update the x and y position using the velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))  # appending the x and y position we are currently at


def main():
    run = True
    # regulate the frame rate
    clock = pygame.time.Clock()
    # creating planets (and sun)
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    # making sure the sun is being orbited
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000  # km/s converted to meters

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, 3.30 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    # Need a loop to keep the program running
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
