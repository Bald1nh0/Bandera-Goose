import random
import os
import pygame

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1280
FONT = pygame.font.SysFont('Verdana', 20)
CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMAGE = pygame.USEREVENT + 3
IMAGE_PATH = "images/goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))
button_tmp = pygame.image.load('images/play.png').convert_alpha()
button_tmp_size = button_tmp.get_size()
play_button = pygame.Surface(button_tmp_size, pygame.SRCALPHA, 32).convert_alpha()

def create_enemy():
    enemy = pygame.image.load('images/enemy.png').convert_alpha()
    enemy_size = enemy.get_size()
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy_size[1], HEIGHT-enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move, enemy_size]

def create_bonus():
    bonus = pygame.image.load('images/bonus.png').convert_alpha()
    bonus_size = bonus.get_size()
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), -bonus_size[1], *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move, bonus_size]

def quit_game():
    pygame.quit()
    quit()

def text_objects(text, font):
    textSurface = font.render(text, True, "black")
    return textSurface, textSurface.get_rect()

def button(text, x,y,w,h,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_tmp = pygame.image.load('images/play.png').convert_alpha()
    button_tmp_size = button_tmp.get_size()
    play_button = pygame.Surface(button_tmp_size, pygame.SRCALPHA, 32).convert_alpha()
    play_button.blit(button_tmp, (0, 0))
    text_render = FONT.render(text, True, "black")
    text_size = text_render.get_rect()
    button_rect = play_button.get_rect()
    play_button.blit(text_render, (button_tmp_size[0]/2-text_size[2]/2,button_tmp_size[1]/2-text_size[3]/2))
    button_rect.center = ( (x+(w/2)), (y+(h/2)) )
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        button_rect.y -= 1
        if click[0] == 1 and action != None:
            action()         
    else:
        button_rect.y += 1
    
    main_display.blit(play_button, button_rect)


def main_menu():
    playing = True
    bg = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move = 3
    while playing:
        FPS.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        bg_X1 -= bg_move
        bg_X2 -= bg_move
        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()
        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))
        button("PLAY", WIDTH/2-button_tmp_size[0]/2,HEIGHT/2-button_tmp_size[1]/2,button_tmp_size[0],button_tmp_size[1], play_game)
        button("QUIT", WIDTH/2-button_tmp_size[0]/2,HEIGHT/2-button_tmp_size[1]/2+button_tmp_size[1],button_tmp_size[0],button_tmp_size[1], quit_game)
        pygame.display.flip()

def play_game():
    playing = True
    main_display = pygame.display.set_mode((WIDTH, HEIGHT))
    bg = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
    bg_X1 = 0
    bg_X2 = bg.get_width()
    bg_move = 3
    player = pygame.image.load('images/player.png').convert_alpha()
    player_size = player.get_size()
    player_rect = player.get_rect()
    player_rect.centery = HEIGHT // 2
    player_rect.centerx = 30 + player.get_width() // 2
    enemies = []
    bonuses = []
    score = 0
    lives = 3
    image_index = 0
    pygame.time.set_timer(CREATE_ENEMY, 1500)
    pygame.time.set_timer(CREATE_BONUS, random.randint(3000, 10000))
    pygame.time.set_timer(CHANGE_IMAGE, 200)
    while playing:
        FPS.tick(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGE:
                player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0

        bg_X1 -= bg_move
        bg_X2 -= bg_move
        if bg_X1 < -bg.get_width():
            bg_X1 = bg.get_width()
        if bg_X2 < -bg.get_width():
            bg_X2 = bg.get_width()
        main_display.blit(bg, (bg_X1, 0))
        main_display.blit(bg, (bg_X2, 0))
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and player_rect.top >= 0:
            player_rect.y -= 4
        if keys[pygame.K_s] and player_rect.bottom <= HEIGHT:
            player_rect.y += 4
        if keys[pygame.K_a] and player_rect.left >= 0:
            player_rect.x -= 4
        if keys[pygame.K_d] and player_rect.right <= WIDTH:
            player_rect.x += 4

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])
            if player_rect.colliderect(enemy[1]):
                enemies.pop(enemies.index(enemy))
                lives -= 1
                if lives == 0:
                    main_menu()

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])
            if player_rect.colliderect(bonus[1]):
                score +=1
                bonuses.pop(bonuses.index(bonus))

        main_display.blit(FONT.render(str(score), True, "Green"), (WIDTH-50, 20))
        main_display.blit(FONT.render(str(f"Lives: {lives}"), True, "red"), (WIDTH-300, 20))
        main_display.blit(player, player_rect)
        pygame.display.flip()

        for enemy in enemies:
            if enemy[1].left < -enemy[3][0]:
                enemies.pop(enemies.index(enemy))

        for bonus in bonuses:
            if bonus[1].bottom > HEIGHT+bonus[3][1]:
                bonuses.pop(bonuses.index(bonus))

main_menu()
pygame.display.quit()
pygame.quit()
