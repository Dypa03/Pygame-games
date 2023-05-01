import pygame as pg
import random as rm
import math as mt
from pygame import mixer
# Initialize the pygame
pg.init()

# Create th screen (width, height)
screen = pg.display.set_mode((800, 600))


# Set Title and Icon
pg.display.set_caption("Space Invaders")
# Icon works not on the window but on the doc on Mac
icon = pg.image.load("free_code_camp/Python/Pygames/SpaceInvader/assets/spaceship.png")
pg.display.set_icon(icon)

def loadify(imgname):
    return pg.image.load(imgname).convert_alpha()

# Player (PlayerImg, coordinates and function)
playerImg = loadify("free_code_camp/Python/Pygames/SpaceInvader/assets/player.png")
playerX= 370
playerY = 480
playerX_change = 0
#playerY_change = 0

def player(x, y):
    # .blit function draws the player given the image and the coordinates as a tuple
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX= []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies): 
    enemyImg.append(loadify("free_code_camp/Python/Pygames/SpaceInvader/assets/alien.png"))
    enemyX.append(rm.randint(0, 800))
    enemyY.append(rm.randint(50, 100))
    enemyX_change.append(0.6)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x[i], y[i]))

# Background
background = loadify("free_code_camp/Python/Pygames/SpaceInvader/assets/background.jpg")

# Background sound
mixer.music.load("free_code_camp/Python/Pygames/SpaceInvader/sounds/p5ost-sweatshop.mp3")
mixer.music.play(-1)

# Bullet
# Ready - You can't see the bullet on screen
# Fire - You can see the bullet on screen
bulletImg = loadify("free_code_camp/Python/Pygames/SpaceInvader/assets/bullet.png")
bulletX= 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16 ,y+10))

# Collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = mt.sqrt((mt.pow(enemyX-bulletX, 2)) + (mt.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def collided(i):
    global bulletY
    bulletY = 480
    global bullet_state
    bullet_state = "ready" 
    global score_value
    score_value+= 1
    global enemyX
    enemyX[i] = rm.randint(0, 735)
    global enemyY 
    enemyY[i] = rm.randint(50, 150)

# Score
score_value = 0
font = pg.font.Font("free_code_camp/Python/Pygames/SpaceInvader/assets/Space Rave.ttf", 32)

textX = 10
textY = 10

def showScore(x,y):
    score = font.render("Score: "+ str(score_value),True, (0, 255, 0))
    screen.blit(score, (x, y))

# Game Over text
over_font = pg.font.Font("free_code_camp/Python/Pygames/SpaceInvader/assets/Space Rave.ttf", 64)
def game_over_text():
    over_text = over_font.render("GAME OVER",True, (0, 255, 0))
    screen.blit(over_text, (200, 250))
    


# Game Loop
running = True
while running:
    # Backround color
    screen.fill((20,10,120))
    #Background Image
    screen.blit(background, (0,0))
    # Quit button
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        #if keystroke is pressed the keys change the coodinates
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                playerX_change -= 0.8
            """
            if event.key == pg.K_w:
                playerY_change -= 0.3
            """
            if event.key == pg.K_d:
                playerX_change += 0.8
            """
            if event.key == pg.K_s:
                playerY_change += 0.3
            """
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("free_code_camp/Python/Pygames/SpaceInvader/sounds/gun.mp3")
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        #if keystroke is released the spaceship stops
        if event.type == pg.KEYUP:
            if event.key == pg.K_a or pg.K_d:
                playerX_change = 0
            """
            if event.key == pg.K_w or pg.K_s:
                playerY_change = 0.0
            """


    #Player Movement
    playerX += playerX_change
    #playerY += playerY_change
    # Checking for boundaries of spaceship to not go out of bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    """
    if playerY <= 0:
        playerY = 0
    elif playerY >= 540:
        playerY = 540
    """

    #Enemy Movement
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            #game_over_sound = mixer.Sound("free_code_camp/Python/Pygames/SpaceInvader/sounds/game-over.mp3")
            #game_over_sound.play()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.6
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            kill_sound = mixer.Sound("free_code_camp/Python/Pygames/SpaceInvader/sounds/kill.mp3")
            kill_sound.play()
            collided(i)
        
        enemy(enemyX, enemyY, i)

    #Bullet Movement
    if bulletY <=0:
        bulletY= 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(textX, textY)
    
    pg.display.update()