import pygame
from settings import WIDTH, HEIGHT, TITLE, BACKGROUND_COLOUR, FPS
from world import World
from side_view import SideView

pygame.init()

world = World()

side_view = SideView()
view = "top"  # Default view is top view

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)


clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(FPS)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                view = "top"

            elif event.key == pygame.K_2:
                view = "side"

    world.update(dt)

    screen.fill(BACKGROUND_COLOUR)

    if view == "top":
        world.draw(screen)

    elif view == "side":
        side_view.draw(screen,
                       world.river, 
                       world.dam)
        

    pygame.display.flip()

pygame.quit()


