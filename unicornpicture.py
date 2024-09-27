import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 800))
def background(r, g, b, x, y, w, h):
    s = rect(screen, (r, g, b), (x, y, w, h))
    s = rect(screen, (r - 135, g + 49, b - 235), (x, y + 450, w, h - 611))

background(135, 206, 235, 0, 0, 1000, 1000)

def sun(r, g, b, x, y, w):
    a = circle(screen, (r, g, b), (x, y), w)
    
sun(255, 255, 0, 550, 75, 125)

def tree(r, g, b, x, y, w, h):
    t = rect(screen, (r, g, b), (x, y, w, h))
    t= ellipse(screen, (r - 245, g - 160, b - 199), (x-55, y-80, w + 120, h))
    t= ellipse(screen, (r - 245, g - 160, b - 199), (x-90, y-175, w + 200, h))
    t= ellipse(screen, (r - 245, g - 160, b - 199), (x-55, y-275, w + 120, h))
    t= ellipse(screen, (r-127, g - 191, b - 207), (x-65, y-80, w-20, h-90))
    t= ellipse(screen, (r-127, g - 191, b - 207), (x+75, y-120, w-20, h-90))
    t= ellipse(screen, (r-127, g - 191, b - 207), (x-25, y-200, w-20, h-90))
    
    
tree(255, 255, 255, 75, 500, 40, 120)

def unicorn(r, g, b, x, y, w, h):
    u = ellipse(screen, (r, g, b), (x, y, w, h))
    rect(screen, (r, g, b), (x+20, y+30, w-180, h+55))
    rect(screen, (r, g, b), (x+55, y+10, w-175, h+55))
    rect(screen, (r, g, b), (x+160, y+10, w-180, h+55))
    rect(screen, (r, g, b), (x+115, y+30, w-175, h+55))
    rect(screen, (r, g, b), (x+135, y-70, w-145, h))
    ellipse(screen, (r, g, b), (x+135, y- 93, w-125, h-50))
    ellipse(screen, (r, g, b), (x+160, y- 80, w-125, h-65))
    ellipse(screen, (r, g-63, b-52), (x+160, y- 80, w-180, h-90))
    ellipse(screen, (r-255, g-255, b-255), (x+168, y- 75, w-190, h-100))
    ellipse(screen, (r-255, g-255, b-255), (x+190, y- 55, w-175, h-90))
    polygon(screen, (r, g-63, b-52), [(x+175,y-170), (x+180,y-90),
                               (x+165,y-90)])
    
    
    
unicorn(255, 255, 255, 275, 575, 200, 110)












pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
