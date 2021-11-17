import sys
import pygame
import project_colors
import random

SIZE_BLOCK = 24
MARGIN = 1
COUNT_BLOCKS = 30


HEADER_MARGIN = (SIZE_BLOCK+MARGIN)*4

size = [SIZE_BLOCK*COUNT_BLOCKS + 2*SIZE_BLOCK + MARGIN*COUNT_BLOCKS,
        SIZE_BLOCK*COUNT_BLOCKS + 2*SIZE_BLOCK + MARGIN*COUNT_BLOCKS + HEADER_MARGIN]
print(size)
FRAME_COLOR = project_colors.BACKGROUND


screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()


class SnakeBlock():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def get_random_empty_block():
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
        empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
    return empty_block


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column*(SIZE_BLOCK + MARGIN),
                                     HEADER_MARGIN + SIZE_BLOCK + row*(SIZE_BLOCK + MARGIN),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


snake_blocks = [SnakeBlock(9, 8),
                SnakeBlock(9, 9),
                SnakeBlock(9, 10)]
apple = get_random_empty_block()

d_row = 0
d_col = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('exit')
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_col != 0:
                d_row = -1
                d_col = 0
            elif event.key == pygame.K_DOWN and d_col != 0:
                d_row = +1
                d_col = 0
            elif event.key == pygame.K_LEFT and d_row != 0:
                d_row = 0
                d_col = -1
            elif event.key == pygame.K_RIGHT and d_row != 0:
                d_row = 0
                d_col = +1

    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, project_colors.LIGHT_BLUE, [0, 0, size[0], HEADER_MARGIN])

    for row in range(COUNT_BLOCKS):
        for column in range(COUNT_BLOCKS):
            draw_block(project_colors.DARK_GREEN, row, column)

    head = snake_blocks[-1]
    if not head.is_inside():
        print('crush')
        pygame.quit()
        sys.exit()

    draw_block(project_colors.LIGHT_RED, apple.x, apple.y)

    for block in snake_blocks:
        draw_block(project_colors.DARK_YELLOW, block.x, block.y)


    if apple == head:
        apple = get_random_empty_block()

    head = snake_blocks[-1]
    new_head = SnakeBlock(head.x + d_row, head.y + d_col)
    snake_blocks.append(new_head)
    snake_blocks.pop(0)

    pygame.display.flip()
    timer.tick(5)
