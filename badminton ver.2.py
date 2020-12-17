import pygame
from math import sin, cos, pi
import random
from random import choice
from time import sleep

pygame.init()
game = pygame.display.set_mode((1000, 562))
pygame.display.set_caption("羽球高高手")
clock = pygame.time.Clock()

# attributes
white = (255, 255, 255)
black = (0, 0, 0)

# ball obj
x_ball = 500
y_ball = 100
r_ball = 10
v_ball = 2.6
rad = pi / 180
ang = choice([180, 0])
angle = -ang * rad
vx_ball = cos(angle) * v_ball
vy_ball = sin(angle) * v_ball
grav = 0.042


def serve(scorer):
    global x_ball
    global y_ball
    global vx_ball
    global vy_ball
    global angle
    sleep(0.8)
    x_ball = 500
    y_ball = 100
    angle = -0 * rad if scorer == 1 else -180 * rad
    vx_ball = cos(angle) * v_ball
    vy_ball = sin(angle) * v_ball


def get_ball():
    pygame.draw.circle(game, (0, 255, 0), (int(float(x_ball)), int(float(y_ball))), r_ball, 0)


# p1 obj
x_p1 = 150
y_p1 = 412
w_p1 = 50
h_p1 = 150
v_p1 = 3


def get_p1():
    pygame.draw.rect(game, black, ((x_p1, y_p1), (w_p1, h_p1)))


# p2 obj
x_p2 = 800
y_p2 = 412
w_p2 = 50
h_p2 = 150
v_p2 = 3


def get_p2():
    pygame.draw.rect(game, black, ((x_p2, y_p2), (w_p2, h_p2)))


# net obj # 原始數值(495, 362, 10, 200)，改過的數值調成語背景網子的範圍相同
x_net = 495
y_net = 265
w_net = 43
h_net = 400


def get_net():
    game1 = game.convert_alpha()  # 把中間包括背景網子的黑色長方形調為透明
    pygame.draw.rect(game1, (0, 0, 0, 0), ((x_net, y_net), (w_net, h_net)))


def text():
    pygame.font.init()
    font = pygame.font.Font("ARCADECLASSIC.TTF", 30)
    return font


def text2():
    font = pygame.font.Font("ARCADECLASSIC.TTF", 30)
    return font


p1_score = 0
p2_score = 0

picture = pygame.image.load("羽球背景.jpg")
picture = pygame.transform.scale(picture, (1000, 562))
rect = picture.get_rect()
rect = rect.move((0, 0))

my_text3 = text2().render('P LAYER 1 WINS!', False, (255, 215, 0))
my_text4 = text2().render('P LAYER 2 WINS!', False, (255, 215, 0))

isJump_p1 = False  # 跳的判斷
jumpCount_p1 = 10  # 體力
isJump_p2 = False
jumpCount_p2 = 10

iden = 20  # 擊球判定

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    game.blit(picture, rect)

    # text
    my_text = text().render('P layer1  ' + str(p1_score), False, (255, 215, 0))
    my_text2 = text().render('P layer2  ' + str(p2_score), False, (255, 215, 0))

    game.blit(my_text, (20, 0))
    game.blit(my_text2, (840, 0))

    keys = pygame.key.get_pressed()
    if p1_score == 3:
        game.blit(my_text3, (200, 300))
    elif p2_score == 3:
        game.blit(my_text4, (700, 300))
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    if x_p1 - iden < x_ball < x_p1 + w_p1 + iden and y_ball > y_p1 - iden:
        keys = pygame.key.get_pressed()
        # if x_ball > x_p1 and x_ball < x_p1+20:
        #    vx_ball = cos(-80*rad)*7
        #    vy_ball = sin(-80*rad)*7
        if keys[pygame.K_LCTRL]:
            vx_ball = cos(-10 * random.uniform(6.5, 8.0) * rad) * 6.0
            vy_ball = sin(-10 * random.uniform(6.5, 8.0) * rad) * 6.5
        # elif x_ball > x_p1+40 and x_ball < x_p1+60:
        #    vx_ball = cos(-45 * rad) * 5.5
        #    vy_ball = sin(-45 * rad) * 5.5
        elif keys[pygame.K_LSHIFT]:
            vx_ball = cos(-10 * random.uniform(3.0, 4.5) * rad) * 4.5
            vy_ball = sin(-10 * random.uniform(3.0, 4.5) * rad) * 5.5
        # elif x_ball > x_p1+80 and x_ball < x_p1+100:
        #    vx_ball = cos(-18 * rad) * 5.3
        #    vy_ball = sin(-18 * rad) * 5.3

    if x_p2 - iden < x_ball < x_p2 + w_p2 + iden and y_ball > y_p2 - iden:
        keys = pygame.key.get_pressed()
        # if x_ball > x_p2 and x_ball < x_p2 + 20:
        #    vx_ball = cos(-162 * rad) * 5.3
        #    vy_ball = sin(-162 * rad) * 5.3
        if keys[pygame.K_l]:
            vx_ball = cos(-10 * random.uniform(15.0, 16.2) * rad) * 4.5
            vy_ball = sin(-10 * random.uniform(15.0, 16.2) * rad) * 5.5
        # elif x_ball > x_p2 + 40 and x_ball < x_p2 + 60:
        #    vx_ball = cos(-135 * rad) * 5.5
        #    vy_ball = sin(-135 * rad) * 5.5
        elif keys[pygame.K_k]:
            vx_ball = cos(-10 * random.uniform(11.5, 13.5) * rad) * 6.0
            vy_ball = sin(-10 * random.uniform(11.5, 13.5) * rad) * 6.5
        # elif x_ball > x_p2 + 80 and x_ball < x_p2 + 100:
        #    vx_ball = cos(-100 * rad) * 7
        #    vy_ball = sin(-100 * rad) * 7

    # if x_ball > x_p1 - iden and x_ball < x_p1 + w_p1 + iden and y_ball < 400:
    #    keys = pygame.key.get_pressed()
    #    if keys[pygame.K_c]:
    #        y_p1 = y_p1 - 300
    #        vx_ball = cos(10 * random.uniform(3.0,4.5) * rad) * 6.5
    #        vy_ball = sin(10 * random.uniform(3.0,4.5) * rad) * 6.5
    #        y_p1 = y_p1 + 300

    if x_net < x_ball < x_net + w_net and y_net < y_ball <= y_net + h_net:
        if x_ball > x_net and y_ball > y_net:
            p2_score += 1
            serve(2)
        elif x_ball < x_net + w_net and y_ball > y_net:
            p1_score += 1
            serve(1)

        # sleep(0.8)
        # x_ball = 500
        # y_ball = 100
        # angle = -ang * rad
        # vx_ball = cos(angle) * v_ball
        # vy_ball = sin(angle) * v_ball

    if y_ball > 562 or x_ball > 1000 or x_ball < 0:
        if (0 < x_ball < x_net and y_ball > 562) or (x_ball > 1000):
            p2_score += 1
            serve(2)
        elif (x_net + w_net < x_ball < 1000 and y_ball > 562) or (x_ball < 0):
            p1_score += 1
            serve(1)

        # sleep(0.8)
        # x_ball = 500
        # y_ball = 100
        # angle = -ang * rad
        # vx_ball = cos(angle) * v_ball
        # vy_ball = sin(angle) * v_ball

    # p1
    get_p1()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x_p1 -= v_p1
        if x_p1 <= 0:
            x_p1 = 0
    elif keys[pygame.K_d]:
        x_p1 += v_p1
        if x_p1 + w_p1 >= 495:
            x_p1 = 495 - w_p1

    if not isJump_p1:  # 跳起來啦
        if keys[pygame.K_w]:
            isJump_p1 = True
    else:
        if jumpCount_p1 >= -10:
            neg_p1 = 1
            if jumpCount_p1 < 0:
                neg_p1 = -1
            y_p1 -= (jumpCount_p1 ** 2) * neg_p1 * 0.75
            jumpCount_p1 -= 1
        else:
            isJump_p1 = False
            jumpCount_p1 = 10

    # p2
    get_p2()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_p2 -= v_p2
        if x_p2 <= 495 + w_net:
            x_p2 = 495 + w_net
    elif keys[pygame.K_RIGHT]:
        x_p2 += v_p2
        if x_p2 + w_p2 >= 1000:
            x_p2 = 1000 - w_p2

    if not isJump_p2:  # 跳起來啦
        if keys[pygame.K_UP]:
            isJump_p2 = True
    else:
        if jumpCount_p2 >= -10:
            neg_p2 = 1
            if jumpCount_p2 < 0:
                neg_p2 = -1
            y_p2 -= (jumpCount_p2 ** 2) * neg_p2 * 0.75
            jumpCount_p2 -= 1
        else:
            isJump_p2 = False
            jumpCount_p2 = 10

    # net
    get_net()

    # ball
    get_ball()
    vy_ball += grav
    x_ball += vx_ball
    y_ball += vy_ball

    pygame.display.flip()
    clock.tick(250)
