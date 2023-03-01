import pygame
import random
import math
import numpy as np

# Constants
WINDOW_SIZE = (800, 600)
PARTICLE_RADIUS = 10
PARTICLE_COUNT = 50
PARTICLE_SPEED = 0.1
BOX_THICKNESS = 5
BOX_COLOR = (0, 0, 255)
PARTICLE_COLOR = (255, 0, 0)
FPS = 30
COR = 1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2D Gas Simulation")

# Define particle class
class Particle:
    def __init__(self, x, y, radius, speed, color, mass=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.mass = mass
        self.direction = random.randint(0, 359)
        self.r = np.array([x, y])
        self.v = np.array([self.speed * round(math.cos(self.direction), 2),
                           self.speed * round(math.sin(self.direction), 2)])

    def move(self):
        radians = self.direction * (math.pi / 180.0)
        self.x += self.speed * round(math.cos(radians), 2)
        self.y -= self.speed * round(math.sin(radians), 2)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, particles):
        for p in particles:
            if p != self:
                v12 = -self.v + p.v
                r12 = self.r - p.r
                r_vers = r12 / np.linalg.norm(r12)
                v_vers = v12 / np.linalg.norm(v12)
                if np.dot(v_vers, r_vers) < 0:
                    # if particles are merged pass
                    # avoids initialization issues
                    pass
                else:
                    print("collision!")
                    # exchanged momentum q
                    # collision solved in the frame of reference of ball2
                    q = -COR * 2 * (self.mass * p.mass) / (self.mass + p.mass) * (np.dot(-v12, r_vers))
                    speed_before_self = self.speed
                    setattr(self, 'speed', speed_before_self + q / self.mass)
                    speed_before_p = p.speed
                    setattr(p, 'speed', speed_before_p -q/p.mass)
# Define box class
class Box:
    def __init__(self, x, y, width, height, thickness, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.thickness = thickness
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), self.thickness)

# Create particles and box
particles = []
for i in range(PARTICLE_COUNT):
    x = random.randint(PARTICLE_RADIUS, WINDOW_SIZE[0] - PARTICLE_RADIUS)
    y = random.randint(PARTICLE_RADIUS, WINDOW_SIZE[1] - PARTICLE_RADIUS)
    particle = Particle(x, y, PARTICLE_RADIUS, PARTICLE_SPEED, PARTICLE_COLOR)
    particles.append(particle)

box = Box(BOX_THICKNESS, BOX_THICKNESS, WINDOW_SIZE[0] - 2 * BOX_THICKNESS, WINDOW_SIZE[1] - 2 * BOX_THICKNESS, BOX_THICKNESS, BOX_COLOR)

# Run simulation
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move particles
    for particle in particles:
        particle.move()
        particle.collide(particles)

        # Bounce off walls
        if particle.x < PARTICLE_RADIUS + BOX_THICKNESS or particle.x > WINDOW_SIZE[0] - PARTICLE_RADIUS - BOX_THICKNESS:
            particle.direction = 180 - particle.direction
        if particle.y < PARTICLE_RADIUS + BOX_THICKNESS or particle.y > WINDOW_SIZE[1] - PARTICLE_RADIUS - BOX_THICKNESS:
            particle.direction = -particle.direction

    # Draw screen
    screen.fill((0, 0, 0))
    box.draw(screen)
    for particle in particles:
        particle.draw(screen)
    pygame.display.flip()

# Quit Pygame
pygame.quit()

