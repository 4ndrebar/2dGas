import pygame
import random
import math
# Constants
WINDOW_SIZE = (800, 600)
PARTICLE_RADIUS = 5
PARTICLE_COUNT = 50
PARTICLE_SPEED = 5
BOX_THICKNESS = 5
BOX_COLOR = (0, 0, 41)
PARTICLE_COLOR = (255, 0, 0)
FPS = 30

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("2D Gas Simulation")

# Define particle class
class Particle:
    def __init__(self, x, y, radius, speed, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.direction = random.randint(0, 359)

    def move(self):
        radians = self.direction * (3.14159265358979323846 / 180.0)
        self.x += self.speed * round(math.cos(radians), 2)
        self.y -= self.speed * round(math.sin(radians), 2)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, particles):
        for p in particles:
            if p != self:
                distance = math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)
                if distance <= self.radius + p.radius:
                    angle = math.atan2(self.y - p.y, self.x - p.x)
                    self.direction = 2 * angle - self.direction
                    p.direction = 2 * angle - p.direction

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
        if particle.y < PARTICLE_RADIUS + BOX_THICKNESS or particle.y >             WINDOW_SIZE[1] - PARTICLE_RADIUS - BOX_THICKNESS:
            particle.direction = -particle.direction

    # Draw screen
    screen.fill((0, 0, 0))
    box.draw(screen)
    for particle in particles:
        particle.draw(screen)
    pygame.display.flip()

# Quit Pygame
pygame.quit()

