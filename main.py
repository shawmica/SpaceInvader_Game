import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, (800, 600))

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('arcade-game.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_alive = []
num_of_enemies = 6

def reset_enemies():
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    enemyX_change.clear()
    enemyY_change.clear()
    enemy_alive.clear()
    for _ in range(num_of_enemies):
        img = pygame.image.load('enemy.png')
        img = pygame.transform.scale(img, (64, 64))
        enemyImg.append(img)
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.3)
        enemyY_change.append(40)
        enemy_alive.append(True)

reset_enemies()

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (8, 24))
bulletX = 0
bulletY = 480
bulletY_change = 1
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font(None, 32)
textX = 10
textY = 10

# Fonts
over_font = pygame.font.Font(None, 64)
button_font = pygame.font.Font(None, 40)

# Game State
game_over = False

# Functions
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def draw_button(text, x, y, w, h, base_color, hover_color=(200, 200, 200), text_color=(0, 0, 0)):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    is_hovered = x < mouse[0] < x + w and y < mouse[1] < y + h
    button_color = hover_color if is_hovered else base_color

    pygame.draw.rect(screen, (50, 50, 50), (x + 3, y + 3, w, h), border_radius=10)
    pygame.draw.rect(screen, button_color, (x, y, w, h), border_radius=10)

    label = button_font.render(text, True, text_color)
    label_rect = label.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(label, label_rect)

    if is_hovered and click[0] == 1:
        pygame.time.delay(150)
        return True
    return False

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    over_rect = over_text.get_rect(center=(400, 250))
    screen.blit(over_text, over_rect)
    final_score = font.render("Final Score: " + str(score_value), True, (255, 255, 255))
    final_rect = final_score.get_rect(center=(400, 300))
    screen.blit(final_score, final_rect)

def you_win_text():
    win_text = over_font.render("YOU WIN!", True, (255, 255, 0))
    win_rect = win_text.get_rect(center=(400, 250))
    screen.blit(win_text, win_rect)
    final_score = font.render("Final Score: " + str(score_value), True, (255, 255, 255))
    final_rect = final_score.get_rect(center=(400, 300))
    screen.blit(final_score, final_rect)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 28, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27

def reset_game():
    global playerX, bullet_state, bulletY, score_value, game_over
    playerX = 370
    bullet_state = "ready"
    bulletY = 480
    score_value = 0
    game_over = False
    reset_enemies()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.3
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.3
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    playerX_change = 0

    if not game_over:
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        all_dead = True
        for i in range(num_of_enemies):
            if not enemy_alive[i]:
                continue
            all_dead = False

            if enemyY[i] > 440:
                game_over = True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.3
                enemyY[i] += enemyY_change[i]

            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemy_alive[i] = False

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

        if all_dead:
            game_over = True
            win = True
        else:
            win = False

    else:
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        if all(enemy_alive[i] == False for i in range(num_of_enemies)):
            you_win_text()
        else:
            game_over_text()

        if draw_button("Restart", 300, 360, 200, 50, (0, 200, 0), hover_color=(0, 255, 0)):
            reset_game()
        if draw_button("Exit", 300, 430, 200, 50, (200, 0, 0), hover_color=(255, 0, 0)):
            pygame.quit()
            exit()

    pygame.display.update()
