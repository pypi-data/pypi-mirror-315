# Particle Interaction Simulation System
Introducing the new, lightweight, pygame-based 2D game particle system that you need for your next game!

The Particle Interaction Simulation System creates beautiful, interactive particles that spice up any game. 

Enemy deaths not satisfying enough? Add a blood simulation! 
Jumps feel empty and fake? Bang on some dust particles when you land!
Weapons not packing enough punch? A massive explosion is exactly what you need!

Our revolutionary system is lag-free, lightweight, and easy to use! With multi-threading support and implementation in just one line (plus three to setup and render), the Particle Interaction Simulation System is the simplest and quickest solution. 

## Features

 - Blood
 - Smoke
 - Explosion
 - Dust (jump landing)
 - Dirt (jump)

With many more released every week or two!

**Install for free today with** 
```console
pip install Particle Interaction Simulation System
```

## TL;DR Implementation
```python
# Imports
import pygame  
from ParticleInteractionSimulationSystem import ExplosionParticleSystem

# Put this outside your main loop
explosion_system = ExplosionParticleSystem()

# Call this when you need a particle
explosion_system.create_particles(x, y)

# Put this in your update loop
explosion_system.update()

# Put this in the draw section of your update loop
explosion_system.draw(screen)
```

## Example Usage
```python
import pygame    
from ParticleInteractionSimulationSystem import BloodParticleSystem, SmokeParticleSystem, ExplosionParticleSystem  # Importing all systems  
  
WIDTH, HEIGHT = 800, 600  
  
def main():  
    pygame.init()  
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  
    clock = pygame.time.Clock()  
    blood_system = BloodParticleSystem()  
  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                pygame.quit()  
            if event.type == pygame.MOUSEBUTTONDOWN:  
                x, y = event.pos    
                blood_system.create_particles(x, y)    
  
  
        blood_system.update()    
  
        screen.fill((255, 255, 255))  # White background    
 blood_system.draw(screen)    
         
        pygame.display.flip()    
        clock.tick(60)  
  
if __name__ == '__main__':  
    main()
```

## Advanced Demo Program
```python
import pygame  
from ParticleInteractionSimulationSystem import JumpParticleSystem, SmokeParticleSystem, ExplosionParticleSystem  
  
# Initialize Pygame  
pygame.init()  
  
# Constants  
WIDTH, HEIGHT = 800, 600  
BACKGROUND_COLOR = (0, 0, 0)  
SQUARE_SIZE = 100  
  
# Create the screen  
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Particle System Demo")  
  
# Create particle systems  
jump_system = JumpParticleSystem()  
smoke_system = SmokeParticleSystem()  
explosion_system = ExplosionParticleSystem()  
  
# Define square positions  
squares = {  
    "jump": (100, 100),  
    "Smoke": (350, 100),  
    "Explosion": (600, 100)  
}  
  
clock = pygame.time.Clock()  
  
# Main loop  
running = True  
while running:  
    clock.tick (60)  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
 elif event.type == pygame.MOUSEBUTTONDOWN:  
            mouse_x, mouse_y = event.pos  
            for label, (x, y) in squares.items():  
                if x <= mouse_x <= x + SQUARE_SIZE and y <= mouse_y <= y + SQUARE_SIZE:  
                    if label == "jump":  
                        jump_system.create_particles(mouse_x, mouse_y)  
                    elif label == "Smoke":  
                        smoke_system.create_particles(mouse_x, mouse_y)  
                    elif label == "Explosion":  
                        explosion_system.create_particles(mouse_x, mouse_y)  
  
    # Update particle systems  
  jump_system.update()  
    smoke_system.update()  
    explosion_system.update()  
  
    # Draw everything  
  screen.fill(BACKGROUND_COLOR)  
  
    # Draw squares and labels  
  for label, (x, y) in squares.items():  
        pygame.draw.rect(screen, (255, 255, 255), (x, y, SQUARE_SIZE, SQUARE_SIZE))  
        font = pygame.font.Font(None, 20)  
        text = font.render(label, True, (0, 0, 0))  
        screen.blit(text, (x + 10, y + 10))  
  
    # Draw particles  
  jump_system.draw(screen)  
    smoke_system.draw(screen)  
    explosion_system.draw(screen)  
  
    # Update the display  
  pygame.display.flip()  
  
# Quit Pygame  
pygame.quit()
```

## Changelog
- v0.1: Release
- v0.2: Added dust and dirt
- v0.3: Added README.md description