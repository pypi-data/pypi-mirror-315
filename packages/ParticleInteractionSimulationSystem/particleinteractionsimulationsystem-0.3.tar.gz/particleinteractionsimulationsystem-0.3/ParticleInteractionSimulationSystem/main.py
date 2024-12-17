import pygame
import random

# Constants
BLOOD_COLOR = (255, 0, 0)
BLOOD_COUNT = 100
PARTICLE_LIFETIME = 60  # Frames
GRAVITY = 0.1           # Gravity effect
SMOKE_COLOR = (192, 192, 192)  # Light gray for smoke
SMOKE_COUNT = 50
SMOKE_LIFETIME = 100  # Longer lifetime for smoke
EXPLOSION_COLOR = (255, 215, 0)  # Gold color for explosion
EXPLOSION_COUNT = 80
EXPLOSION_LIFETIME = 40  # Shorter lifetime for explosion ParticleInteractionSimulationSystem
DUST_WIDTH = 6  
DUST_HEIGHT = 3  # Set a height to give it a rectangular shape  
DUST_COLOR = (150, 100, 63)  # Dark gray for dust  
DUST_COUNT = 50  
DUST_LIFETIME = 40  # Short lifetime for dust particles
JUMP_PARTICLE_COLOR = (255, 255, 224)  # Light yellow for jump particles  
JUMP_PARTICLE_COUNT = 30  
JUMP_PARTICLE_LIFETIME = 20  # Short lifetime for jump particles

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = PARTICLE_LIFETIME
        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(1, 2)  # Initial downward motion
        self.alpha = 255  # Full opacity

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y + GRAVITY
        self.lifetime -= 1
        self.alpha = max(0, self.alpha - (255 // PARTICLE_LIFETIME))

    def is_alive(self):
        return self.lifetime > 0

    def draw(self, surface):
        if self.alpha > 0:
            particle_surface = pygame.Surface((5, 5))  # Small square particle
            particle_surface.fill(BLOOD_COLOR)
            particle_surface.set_alpha(self.alpha)  # Set transparency
            surface.blit(particle_surface, (self.x, self.y))

class BloodParticleSystem:
    def __init__(self):
        self.particles = []

    def create_particles(self, x, y):
        for _ in range(BLOOD_COUNT):
            self.particles.append(Particle(x, y))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
######################################################################################

class SmokeParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity_y = random.uniform(-1, -3)  # Initial upward motion
        self.alpha = 200  # Semi-transparent

    def update(self):
        super().update()
        self.velocity_y += 0.02  # Slow upward drift as it "rises"

    def draw(self, surface):
        if self.alpha > 0:
            particle_surface = pygame.Surface((10, 10), pygame.SRCALPHA)  # Semi-transparent particle
            pygame.draw.circle(particle_surface, SMOKE_COLOR, (5, 5), 5)  # Circle shape for smoke
            particle_surface.set_alpha(self.alpha)  # Set transparency
            surface.blit(particle_surface, (self.x, self.y))

class SmokeParticleSystem:
    def __init__(self):
        self.particles = []

    def create_particles(self, x, y):
        for _ in range(SMOKE_COUNT):
            self.particles.append(SmokeParticle(x, y))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

#############################################################################################

class ExplosionParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity_x = random.uniform(-3, 3)  # Explode outward
        self.velocity_y = random.uniform(-3, 0)  # Initial upward motion
        self.alpha = 255  # Full opacity

    def update(self):
        super().update()
        # Explode outward and then fall down
        self.velocity_y += 0.1  # Add gravity effect over time
        self.velocity_x *= 0.98  # Slow down horizontal motion

    def draw(self, surface):
        if self.alpha > 0:
            particle_surface = pygame.Surface((10, 10), pygame.SRCALPHA)  # Use SRCALPHA for transparency
            pygame.draw.circle(particle_surface, EXPLOSION_COLOR, (5, 5), 5)  # Circular shape
            particle_surface.set_alpha(self.alpha)  # Set transparency
            surface.blit(particle_surface, (self.x, self.y))

class ExplosionParticleSystem:
    def __init__(self):
        self.particles = []

    def create_particles(self, x, y):
        for _ in range(EXPLOSION_COUNT):
            self.particles.append(ExplosionParticle(x, y))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


#######################################################################################

class DustParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity_x = random.uniform(-1, 1)  # Slight horizontal spread  
        self.velocity_y = random.uniform(-1, 0)  # Slightly negative vertical velocity  
        self.alpha = 180  # Semi-transparent

    def update(self):
        super().update()
        self.velocity_y += 0.05  # Slow downward drift

    def draw(self, surface):
        if self.alpha > 0:
            particle_surface = pygame.Surface((DUST_WIDTH, DUST_HEIGHT), pygame.SRCALPHA)  # Rectangular particle  
            particle_surface.fill((0, 0, 0, 0))  # Fill with transparent color  
            pygame.draw.rect(particle_surface, DUST_COLOR, (0, 0, DUST_WIDTH, DUST_HEIGHT))  # Draw rectangle  
            particle_surface.set_alpha(self.alpha)  # Set transparency  
            surface.blit(particle_surface, (self.x, self.y))

class DustParticleSystem:
    def __init__(self):
        self.particles = []

    def create_particles(self, x, y):
        for _ in range(DUST_COUNT):
            self.particles.append(DustParticle(x, y))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

#######################################################################################
class JumpParticle(Particle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity_x = random.uniform(-1, 1)  # Slight horizontal spread  
        self.velocity_y = random.uniform(-3, -1)  # Initial upward velocity  
        self.alpha = 255  # Full opacity

    def update(self):
        super().update()
        self.velocity_y += 0.1  # Add gravity to simulate falling  
        self.alpha = max(0, self.alpha - (255 // JUMP_PARTICLE_LIFETIME))  # Gradually fade out

    def draw(self, surface):
        if self.alpha > 0:
            particle_surface = pygame.Surface((5, 5), pygame.SRCALPHA)  # Small, semi-transparent particle  
            pygame.draw.circle(particle_surface, JUMP_PARTICLE_COLOR, (2, 2), 2)  # Circle shape for jump particles  
            particle_surface.set_alpha(self.alpha)  # Set transparency  
            surface.blit(particle_surface, (self.x, self.y))

class JumpParticleSystem:
    def __init__(self):
        self.particles = []

    def create_particles(self, x, y):
        for _ in range(JUMP_PARTICLE_COUNT):
            self.particles.append(JumpParticle(x, y))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
