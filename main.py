import pygame

FRAME_COLOR = (155, 188, 15)
size = [600, 800]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill(FRAME_COLOR)
    pygame.display.flip()