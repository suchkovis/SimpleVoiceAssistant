import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

rect(screen, (175, 175, 175), (0, 0, 500, 500))
circle(screen, (255, 255, 0), (200, 200), 175)
circle(screen, (0, 0, 0), (200, 200), 175, 1)

circle(screen, (255, 0, 0), (125, 150), 32)
circle(screen, (0, 0, 0), (125, 150), 32, 1)
circle(screen, (0, 0, 0), (125, 150), 15)

circle(screen, (255, 0, 0), (275, 150), 28)
circle(screen, (0, 0, 0), (275, 150), 28, 1)
circle(screen, (0, 0, 0), (275, 150), 14)

rect(screen, (0, 0, 0), (125, 300, 150, 30))

rect(screen, (0, 0, 0), (125, 300, 150, 30))

polygon(screen, (0, 0, 0), [(100,100), (200,50),
                               (300,100), (100,200)], 10)






pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
