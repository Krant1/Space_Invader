import pygame
from math import sqrt,pow
from random import randint
from pygame import mixer
pygame.init()
mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('/Users/manojrai/Downloads/ufo.png')
pygame.display.set_icon(icon)
player = pygame.image.load('/Users/manojrai/Downloads/spaceship (1).png')
missile=pygame.image.load('/Users/manojrai/Downloads/missile.png')
background=pygame.image.load('/Users/manojrai/Downloads/wepik-2021931-14151.png')
player_x = 370
player_y = 480
player_x_change = 0

enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

missile_x = 0
missile_y = 480
missile_x_change = 0
missile_y_change = 10
missile_state='Ready'

def player_char(x,y):
    screen.blit(player, (x, y))
    
def enemy_char(x,y,i):
    screen.blit(enemy[i], (x, y))

def fire_missile(x, y):
    global missile_state
    missile_state='Fire'
    screen.blit(missile, (x + 16, y + 10))
    
def is_collision(enemy_x, enemy_y, missile_x, missile_y):
    distance = int(sqrt((pow(enemy_x - missile_x, 2)) + (pow(enemy_y - missile_y, 2))))
    if distance < 27:
        return True
    else:
        return False
def game_over():
    font = pygame.font.Font('freesansbold.ttf', 64)
    score = font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(score,(250,200))
    

x_val = 10
y_val = 10
def show_score(x, y):
    font=pygame.font.Font('freesansbold.ttf',32)
    score = font.render(f'Score : {score_value}',True,(255,255,255))
    screen.blit(score, (x_val, y_val))

mixer.music.load('/Users/manojrai/Downloads/background.wav')
mixer.music.set_volume(0.5)
mixer.music.play()   
running = True
score_value=0
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            if event.key == pygame.K_RIGHT:
                player_x_change = 2
            if event.key == pygame.K_SPACE:
                if missile_state is 'Ready':
                    missile_sound = mixer.Sound('/Users/manojrai/Downloads/dsskeatk.wav')
                    missile_sound.play()
                    missile_x=player_x
                    fire_missile(missile_x,missile_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT:
                player_x_change = 0
    
    for i in range(6):
        enemy.append(pygame.image.load('/Users/manojrai/Downloads/ufo (1).png'))
        enemy_x.append(randint(0,736))
        enemy_y.append(randint(50,100))
        enemy_x_change.append(2)
        enemy_y_change.append(40)


    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(6):
        if enemy_y[i] > 440:
            for j in range(6):
                enemy_y[j]=2000
            game_over()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i]+=enemy_y_change[i]
        if enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]
        collision=is_collision(enemy_x[i],enemy_y[i],missile_x,missile_y)
        if collision is True:
            collision_sound = mixer.Sound('/Users/manojrai/Downloads/mixkit-fast-game-explosion-1688.wav')
            collision_sound.play()
            missile_y=480
            missile_state = 'Ready'
            score_value += 1
            enemy_x[i] = randint(0, 736)
            enemy_y[i] = randint(50, 100)
            

        enemy_char(enemy_x[i], enemy_y[i],i)

    if missile_y <= 0:
        missile_y = 480
        missile_state='Ready'
        
    if missile_state is 'Fire':
        fire_missile(missile_x, missile_y)
        missile_y -= missile_y_change
    
        
    player_char(player_x, player_y)
    show_score(x_val,y_val)
    pygame.display.update()
