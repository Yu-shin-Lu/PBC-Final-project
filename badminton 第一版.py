import pygame
from math import sin, cos, pi
import random
from random import choice
from time import sleep

pygame.init()
game = pygame.display.set_mode((1000,562))
clock = pygame.time.Clock()

#attributes
white = ((255,255,255))
black = ((0, 0, 0))

#ball obj
x_ball = 500
y_ball = 100
r_ball = 6
v_ball = 2.6
rad = pi/180
ang = choice([180, 0])
angle = -ang*rad
vx_ball = cos(angle)*v_ball
vy_ball = sin(angle)*v_ball
grav = 0.042
def get_ball():
    pygame.draw.circle(game, (0, 255, 0), (int(float(x_ball)), int(float(y_ball))), r_ball, 0)

#p1 obj
x_p1 = 150
y_p1 = 412
w_p1 = 50
h_p1 = 150
v_p1 = 3
def get_p1():
    pygame.draw.rect(game, black, ((x_p1,y_p1),(w_p1,h_p1)))

#p2 obj
x_p2 = 800
y_p2 = 412
w_p2 = 50
h_p2 = 150
v_p2 = 3
def get_p2():
    pygame.draw.rect(game, black, ((x_p2,y_p2),(w_p2,h_p2)))

#net obj
x_net = 495
y_net = 362
w_net = 10
h_net = 200
def get_net():
    pygame.draw.rect(game, black, ((x_net,y_net),(w_net,h_net)))

def text():
    pygame.font.init()
    font = pygame.font.SysFont('Lucida Console', 15)
    return font

def text2():
    font = pygame.font.SysFont('Lucida Console', 70)
    return font

p1_score = 0
p2_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    game.fill(white)

    #text
    my_text = text().render('P1: ' + str(p1_score), False, black)
    my_text2 = text().render('P2: ' + str(p2_score), False, black)
    my_text3 = text2().render('PLAYER 1 WINS!', False, black)
    my_text4 = text2().render('PLAYER 2 WINS!', False, black)

    game.blit(my_text, (1,1))
    game.blit(my_text2, (940, 1))

    keys = pygame.key.get_pressed()
    if p1_score == 12:
        game.blit(my_text3, (200,300))
    elif p2_score == 12:
        game.blit(my_text4, (200,300))
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    iden = 20
    if x_ball > x_p1 - iden and x_ball < x_p1 + w_p1 + iden and y_ball > y_p1 - iden:
        keys = pygame.key.get_pressed()
        #if x_ball > x_p1 and x_ball < x_p1+20:
        #    vx_ball = cos(-80*rad)*7
        #    vy_ball = sin(-80*rad)*7
        if keys[pygame.K_z]:
            vx_ball = cos(-10 * random.uniform(6.5,8.0) * rad) * 6.5
            vy_ball = sin(-10 * random.uniform(6.5,8.0) * rad) * 6.5
        #elif x_ball > x_p1+40 and x_ball < x_p1+60:
        #    vx_ball = cos(-45 * rad) * 5.5
        #    vy_ball = sin(-45 * rad) * 5.5
        elif keys[pygame.K_x]:
            vx_ball = cos(-10 * random.uniform(3.0,4.5) * rad) * 5.5
            vy_ball = sin(-10 * random.uniform(3.0,4.5) * rad) * 5.5
        #elif x_ball > x_p1+80 and x_ball < x_p1+100:
        #    vx_ball = cos(-18 * rad) * 5.3
        #    vy_ball = sin(-18 * rad) * 5.3

    if x_ball > x_p2 - iden and x_ball < x_p2 + w_p2 + iden and y_ball > y_p2 - iden:
        keys = pygame.key.get_pressed()
        #if x_ball > x_p2 and x_ball < x_p2 + 20:
        #    vx_ball = cos(-162 * rad) * 5.3
        #    vy_ball = sin(-162 * rad) * 5.3
        if keys[pygame.K_l]:
            vx_ball = cos(-150 * rad) * 5.5
            vy_ball = sin(-150 * rad) * 5.5
        #elif x_ball > x_p2 + 40 and x_ball < x_p2 + 60:
        #    vx_ball = cos(-135 * rad) * 5.5
        #    vy_ball = sin(-135 * rad) * 5.5
        elif keys[pygame.K_k]:
            vx_ball = cos(-115 * rad) * 6
            vy_ball = sin(-115 * rad) * 6
        #elif x_ball > x_p2 + 80 and x_ball < x_p2 + 100:
        #    vx_ball = cos(-100 * rad) * 7
        #    vy_ball = sin(-100 * rad) * 7

    if x_ball > x_net and x_ball < x_net + w_net and y_ball > y_net and y_ball <= y_net + h_net:
        if x_ball > x_net and y_ball > y_net:
            p2_score += 1
        elif x_ball < x_net + w_net and y_ball > y_net:
            p1_score += 1

        sleep(0.8)
        x_ball = 500
        y_ball = 100
        angle = -ang * rad
        vx_ball = cos(angle) * v_ball
        vy_ball = sin(angle) * v_ball

    if y_ball > 562 or x_ball > 1000 or x_ball < 0:
        if (x_ball > 0 and x_ball < x_net and y_ball > 562) or (x_ball > 1000):
            p2_score += 1
        elif (x_ball > x_net + w_net and x_ball < 1000 and y_ball > 562) or (x_ball < 0):
            p1_score += 1

        sleep(0.8)
        x_ball = 500
        y_ball = 100
        angle = -ang * rad
        vx_ball = cos(angle) * v_ball
        vy_ball = sin(angle) * v_ball

    #p1
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

    #p2
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

    #net
    get_net()

    #ball
    get_ball()
    vy_ball += grav
    x_ball += vx_ball
    y_ball += vy_ball

    pygame.display.flip()
    clock.tick(150)