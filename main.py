import sys
import time
import pygame
import pygame_menu
from pygame_menu import sound
import project_colors
import random
from database import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
bg_image = pygame.image.load('images/wallpaper.png')

SIZE_BLOCK = 24
MARGIN = 1
COUNT_BLOCKS = 30
HEADER_MARGIN = (SIZE_BLOCK + MARGIN) * 4
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
FRAME_COLOR = project_colors.BACKGROUND

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()

# MyFont = pygame.font.Font('fonts/open-sans/ttf/OpenSans-Bold.ttf', 24)
MyFont = pygame.font.SysFont('Verdana', 24)
BEST_USERS = get_best()


def draw_top_users():
    font_result = pygame.font.SysFont('Verdana', 24)
    font_user = pygame.font.SysFont('Verdana', 20)
    text_header = font_result.render('Best scores:', True, project_colors.WHITE)
    screen.blit(text_header, (23 * (SIZE_BLOCK + MARGIN), 0))
    for index, user in enumerate(BEST_USERS):
        user_name, user_score = user
        s = f"{index + 1}. {user_name}: {user_score}"
        text_user = font_user.render(s, True, project_colors.WHITE)
        screen.blit(text_user, (23 * (SIZE_BLOCK + MARGIN), 23 * (index + 1)+2))
        print(index, user_name, user_score)


class SnakeBlock():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * (SIZE_BLOCK + MARGIN),
                                     HEADER_MARGIN + SIZE_BLOCK + row * (SIZE_BLOCK + MARGIN),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])



def start_the_game():
    pygame.mixer.music.load("sounds/Chiptronical.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mouse.set_visible(False)
    sound_eating = pygame.mixer.Sound("sounds/mixkit-arcade-bonus-alert-767.wav")
    crash_sound = pygame.mixer.Sound("sounds/mixkit-retro-arcade-game-over-470.wav")

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(random.randint(12, 20), random.randint(12, 20))]
    apple = get_random_empty_block()

    d_row = buf_row = 0
    d_col = buf_col = 1
    global score
    score = 0
    speed = 1
    delta1 = random.randint(2, 21)
    delta2 = random.randint(2, 7)

    flPause = False
    vol = 0.1
    pygame.mixer.music.set_volume(vol)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                time.sleep(1)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = +1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = +1
                elif event.key == pygame.K_SPACE:
                    flPause = not flPause
                    if flPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_z:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                    print(pygame.mixer.music.get_volume())
                elif event.key == pygame.K_a:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
                    print(pygame.mixer.music.get_volume())
            elif event.type == pygame.K_UP:
                pass
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, project_colors.LIGHT_BLUE, [0, 0, size[0], HEADER_MARGIN])

        draw_top_users()
        text_user = MyFont.render(f"User: {USER_NAME.get_value()}", 0, project_colors.WHITE)
        text_total = MyFont.render(f"Score: {score}", 0, project_colors.WHITE)
        text_speed = MyFont.render(f"Speed: {speed}", 0, project_colors.WHITE)
        screen.blit(text_user, (SIZE_BLOCK, 0))
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK + 7))
        screen.blit(text_speed, (SIZE_BLOCK, 2 * SIZE_BLOCK + 14))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row * column) % delta1 == delta2:
                    draw_block(project_colors.LIGHT_GREEN, row, column)
                else:
                    draw_block(project_colors.DARK_GREEN, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            pygame.mixer.music.stop()
            crash_sound.play()
            time.sleep(1)
            insert_result(USER_NAME.get_value(), score)
            break

        if random.randint(1, 2) % 2 == True:
            draw_block(project_colors.LIGHT_RED, apple.x, apple.y)
        else:
            draw_block(project_colors.DARK_RED, apple.x, apple.y)

        for block in snake_blocks:
            if block == head:
                draw_block(project_colors.LIGHT_YELLOW, block.x, block.y)
            else:
                draw_block(project_colors.DARK_YELLOW, block.x, block.y)

        pygame.display.flip()
        if apple == head:
            sound_eating.set_volume(0.2)
            sound_eating.play()
            score += 1
            speed = score // 5 + 1
            snake_blocks.insert(0, apple)
            apple = get_random_empty_block()

        d_row = buf_row
        d_col = buf_col
        head = snake_blocks[-1]
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            pygame.mixer.music.stop()
            crash_sound.play()
            time.sleep(1)
            insert_result(USER_NAME.get_value(), score)
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(speed + 2)

# Menu options
main_theme = pygame_menu.themes.THEME_MY_SNAKE.copy()
main_theme.set_background_color_opacity(0.6)

engine = sound.Sound()
engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'sounds/mixkit-arcade-bonus-229.wav')

menu = pygame_menu.Menu('Welcome', 450, 250, theme=main_theme)
menu.set_sound(engine, recursive=True)
USER_NAME = menu.add.text_input('Name: ', default='User', maxchar=17)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

while True:
    screen.blit(bg_image, (-5, 0))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()


    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()