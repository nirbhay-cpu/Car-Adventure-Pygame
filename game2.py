# Import libraries
import math
import time
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 550))

# Background image
road = icon = pygame.image.load("road2.png")

# Baackground music
mixer.music.load("bg-music.wav")
# -1 used for play music in loop
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Car Adventure")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Player
sound = "False"
playerImg = pygame.image.load("my_car.png")
playerX = 370
playerY = 480
playerX_change = 0

# Opponent
a, b = 0, 0
opponentImg = []
opponentX = []
opponentY = []
opponentY_change = 2
num_of_opponents = 4
for i in range(num_of_opponents):
    opponentImg.append(pygame.image.load("opponents.png"))
    opponentX.append(random.randint(320, 480))
    opponentY.append(0)


# Score
highscore=0
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
highscore_font=pygame.font.Font("freesansbold.ttf", 22)
textX = 10
textY = 10

# Game Over text
display = "False"
over_font = pygame.font.Font("freesansbold.ttf", 56)

#intro_page font
intro_font = pygame.font.Font("freesansbold.ttf", 64)
start_font = pygame.font.Font("freesansbold.ttf", 20)

# pause text
pause_font=pygame.font.Font("freesansbold.ttf", 15)

# Levels texts
head = pygame.font.Font("freesansbold.ttf", 29)
level = pygame.font.Font("freesansbold.ttf", 25)

def show_pause_text():
    pause_text=pause_font.render("Press SPACE to pause",True,(255,255,255))
    screen.blit(pause_text,(10,500))

def show_levels():
    head_text= head.render("Levels :-",True,(0,0,255))
    level1 = level.render("Level 1 : 10" , True, (255, 255, 255))
    level2 = level.render("Level 2 : 30" , True, (255, 255, 255))
    level3 = level.render("Level 3 : 50" , True, (255, 255, 255))
    screen.blit(head_text,(600,250))
    screen.blit(level1, (600, 290))
    screen.blit(level2, (600, 315))
    screen.blit(level3, (600, 340))


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 0,0))
    screen.blit(score, (x, y))
    highscore_text = highscore_font.render("HIGH SCORE :" + str(highscore), True, (255,255,255))
    screen.blit(highscore_text, (605,10))


def game_over():
    global  to
    over_text = over_font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(over_text, (251, 250))
    if (time.time()-to)>=5:
        restart()

def pause():
    pause=True
    while pause:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (9, 9, 149, 35))
        screen.blit(road, (250, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause=False
        show_score(textX,textY)
        show_levels()
        show_pause_text()
        pause_text = over_font.render("PAUSE", True, (255, 255, 0))
        screen.blit(pause_text, (335, 250))

        pygame.display.update()

def game_intro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro=False
        screen.fill((0,0,0))
        intro_text = intro_font.render("CAR ADVENTURE", True, (255,0, 0))
        screen.blit(intro_text, (130, 200))
        start_text = start_font.render("Press ENTER to start", True, (255, 0, 0))
        screen.blit(start_text, (270, 350))
        player(465,330)

        pygame.display.update()

def restart():
    global num_of_opponents, opponentY, display, sound, score_value,opponentX,a,b,opponentY_change,playerX,playerY
    display = "False"
    sound = "False"
    playerX=370
    playerY=480
    score_value = 0
    a,b=0,0
    opponentY_change=2
    for i in range(num_of_opponents):
        opponentY[i] = 0

def player(x, y):
    screen.blit(playerImg, (x, y))


def opponent(x, y, i):
    screen.blit(opponentImg[i], (x, y))


def iscollision(playerX, playerY, opponentX, opponentY):
    distance = math.sqrt((math.pow(playerX - opponentX, 2)) + (math.pow(playerY - opponentY, 2)))
    if distance < 35:
        return True
    return False


game_intro()

# Game Loop
running = True
while running:

    # RGB - Red, Green ,Blue
    screen.fill((0, 0, 0))

    # Score BgColor
    pygame.draw.rect(screen, (255, 255, 255), (9, 9, 149, 35))

    # Background image
    screen.blit(road, (250, 0))

    for event in pygame.event.get():

        # for "x" button on window
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 2
            if event.key == pygame.K_RIGHT:
                playerX_change += 2
            if event.key== pygame.K_SPACE:
                pause()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Setting boundaries for player
    if playerX <= 300:
        playerX = 300
    elif playerX >= 491:
        playerX = 491

    # Roadside Clash
    if sound == "False" and display=="False":
        if playerX >= 487 or playerX <= 305:
            collision_sound = mixer.Sound("car_crash.wav")
            collision_sound.play()
            to=time.time()
            sound = "True"
            display = "True"

    if display == "False":

        # Opponent movement
        i = 0
        opponent(opponentX[i], opponentY[i], i)
        opponentY[i] += opponentY_change
        if opponentY[i] == 252:
            a = opponentY[i]
        if a == 252:
            opponent(opponentX[i + 1], opponentY[i + 1], i + 1)
            opponentY[i + 1] += opponentY_change
            if opponentY[i + 1] == 252:
                b = opponentY[i + 1]
        if b == 252:
            opponent(opponentX[i + 2], opponentY[i + 2], i + 2)
            opponentY[i + 2] += opponentY_change
        if opponentY[i] > 560:
            opponentX[i] = random.randint(320, 480)
            opponentY[i] = 0
        if opponentY[i + 1] > 560:
            opponentX[i + 1] = random.randint(320, 480)
            opponentY[i + 1] = 0
        if opponentY[i + 2] > 560:
            opponentX[i + 2] = random.randint(320, 480)
            opponentY[i + 2] = 0
        for i in range(num_of_opponents):
            if  opponentY[i]==552 or opponentY[i]==555:
                score_value += 1
                if score_value == 10 or score_value==30 or score_value==50  :
                    opponentY_change += 1
                if score_value>=highscore:
                    highscore=score_value

            # Collision
            collision = iscollision(playerX, playerY, opponentX[i], opponentY[i])
            if collision:
                opponentY[i] = 2000
                collision_sound = mixer.Sound("car_crash.wav")
                collision_sound.play()
                to = time.time()
                display = "True"
    else:
        game_over()

    player(playerX, playerY)
    show_score(textX, textY)
    show_levels()
    show_pause_text()
    pygame.display.update()
pygame.quit()
quit()
