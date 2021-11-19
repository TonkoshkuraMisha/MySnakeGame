import math
import pygame, sys
from pygame.locals import *
pygame.init()
(windows_width, windows_height, windows_title) = (600, 400, "Simple Anim")
screen = pygame.display.set_mode((windows_width,windows_height),0,32)
pygame.display.set_caption(windows_title)
windows_bgcolor = (255,255,255)
mainLoop = True
clock = pygame.time.Clock()
milli = seconds = 0.0
#initial data here
rect = Rect(0,0,100,100)
rect_color = (0,0,255)
speed_by_second = 50
while mainLoop:
    for event in pygame.event.get():
        if event.type == QUIT:
            mainLoop = False
    screen.fill(windows_bgcolor)
    milli = clock.tick(40)
    seconds = milli / 1000.0
    dm = speed_by_second * seconds
    rect.x += dm
    if rect.x > 600:
        rect.x = - rect.width
    pygame.draw.rect(screen,rect_color,rect)
    #create frame here
    pygame.display.update()
pygame.quit()
#destroy data here