import pygame
from math import sin, cos, pi
import random
from random import choice
from time import sleep

pygame.init()
game = pygame.display.set_mode((1000, 562))
pygame.display.set_caption("羽球高高手")
clock = pygame.time.Clock()

# ball obj
x_ball = 500
y_ball = 100
r_ball = 10
v_ball = 5
rad = pi / 180
ang = choice([180, 0])
angle = -ang * rad
vx_ball = cos(angle) * v_ball
vy_ball = sin(angle) * v_ball
grav = 0.1

# default settings
rad = pi / 180
iden = 20  # 擊球判定

def get_ball():
    ball = pygame.image.load('去背羽球.png')
    ball = pygame.transform.scale(ball, (40, 40))
    game.blit(ball, (int(float(x_ball)), int(float(y_ball))))


def text_score():
    pygame.font.init()
    font = pygame.font.Font("ARCADECLASSIC.TTF", 30)
    return font


def text_cele():
    font = pygame.font.Font("ARCADECLASSIC.TTF", 30)
    return font


class Player:
    def __init__(self, x, y, w, h, v, path, isJump, jumpCount):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.path = path
        self.isJump = isJump
        self.jumpCount = jumpCount

    def get_player(self): # 人物生成
        player_img = pygame.image.load(self.path)
        player_img = pygame.transform.scale(player_img, (80, 120))
        game.blit(player_img, ((self.x, self.y), (self.w, self.h)))


    def jump(self): # 人物跳
        global vx_ball
        global vy_ball
        if not self.isJump:
            if self.x - iden < x_ball < self.x + self.w + iden and y_ball > y_p1 - iden:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_z]:
                    vx_ball = cos(-10 * random.uniform(6.5, 8.0) * rad) * 6.0
                    vy_ball = sin(-10 * random.uniform(6.5, 8.0) * rad) * 6.5
                elif keys[pygame.K_x]:
                    vx_ball = cos(-10 * random.uniform(3.0, 4.5) * rad) * 4.5
                    vy_ball = sin(-10 * random.uniform(3.0, 4.5) * rad) * 5.5

        else:
            if x_ball > self.x - iden and x_ball < self.x + self.w + iden and y_ball < 400:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    vx_ball = cos(10 * random.uniform(3.0, 4.5) * rad) * 10
                    vy_ball = sin(10 * random.uniform(3.0, 4.5) * rad) * 10

    def move(self): # 人物移動
        pass

    def wiggle(self): # 人物擺動
        pass

    def drive(self): # 平抽
        pass

    def smash(self): # 殺球
        pass

    def clear(self): # 高遠球
        pass

    def score(self): # 得分
        pass

    def serve(self): # 發球
        global vx_ball
        global vy_ball
        sleep(0.5)
        self.x = 500
        self.y = 100
        angle = -0 * rad if self == p1 else -180 * rad
        vx_ball = cos(angle) * v_ball
        vy_ball = sin(angle) * v_ball

class Net:
    def __init__(self, x, y, w, h, net_img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.net_img = net_img

    def get_net(self):
        self.net_img = game.convert_alpha()  # 把中間包括背景網子的黑色長方形調為透明
        pygame.draw.rect(self.net_img, (0, 0, 0, 0), ((self.x, self.y), (self.w, self.h)))

class Ball:
    def __init__(self, x, y, r, v, ang):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.ang = ang

picture = pygame.image.load("羽球背景.jpg")
picture = pygame.transform.scale(picture, (1000, 562))
rect = picture.get_rect()
rect = rect.move((0, 0))

# 慶祝訊息
p1_cele = text_cele().render('P LAYER 1 WINS!', False, (255, 215, 0))
p2_cele = text_cele().render('P LAYER 2 WINS!', False, (255, 215, 0))

iden = 20  # 擊球判定
cnt = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    game.blit(picture, rect)

    # text
    p1_score_text = text_score().render('P layer1  ' + str(p1_score), False, (255, 215, 0))
    p2_score_text = text_score().render('P layer2  ' + str(p2_score), False, (255, 215, 0))

    game.blit(p1_score_text, (20, 0))
    game.blit(p2_score_text, (840, 0))

    keys = pygame.key.get_pressed()
    if p1_score == 3:
        game.blit(p1_cele, (200, 300))
    elif p2_score == 3:
        game.blit(p2_cele, (700, 300))
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    # p1擊球判定
    if not isJump_p1:
        if x_p1 - iden < x_ball < x_p1 + w_p1 + iden and y_ball > y_p1 - iden:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                vx_ball = cos(-10 * random.uniform(6.5, 8.0) * rad) * 6.0
                vy_ball = sin(-10 * random.uniform(6.5, 8.0) * rad) * 6.5
            elif keys[pygame.K_x]:
                vx_ball = cos(-10 * random.uniform(3.0, 4.5) * rad) * 4.5
                vy_ball = sin(-10 * random.uniform(3.0, 4.5) * rad) * 5.5
    else:
        if x_p1 - iden < x_ball < x_p1 + w_p1 + iden and y_ball < 400:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                vx_ball = cos(10 * random.uniform(3.0, 4.5) * rad) * 10
                vy_ball = sin(10 * random.uniform(3.0, 4.5) * rad) * 10
