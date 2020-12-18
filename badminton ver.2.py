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
v_ball = 5
rad = pi / 180
ang = choice([180, 0])
angle = -ang * rad
vx_ball = cos(angle) * v_ball
vy_ball = sin(angle) * v_ball
grav = 0.09


def serve(scorer):
    global x_ball
    global y_ball
    global vx_ball
    global vy_ball
    global angle
    sleep(0.5)
    x_ball = 500
    y_ball = 100
    angle = -0 * rad if scorer == 1 else -180 * rad
    vx_ball = cos(angle) * v_ball
    vy_ball = sin(angle) * v_ball


def get_ball():
    # pygame.draw.circle(game, (0, 255, 0), (int(float(x_ball)), int(float(y_ball))), r_ball, 0)
    ball = pygame.image.load('去背羽球.png')
    ball = pygame.transform.scale(ball, (40, 40))
    game.blit(ball, (int(float(x_ball)), int(float(y_ball))))


# p1 obj
x_p1 = 150
y_p1 = 412
w_p1 = 50
h_p1 = 150
v_p1 = 5


def get_p(path, x, y, w, h):
    p1 = pygame.image.load(path)
    p1 = pygame.transform.scale(p1, (80, 120))
    game.blit(p1, ((x, y), (w, h)))


# p2 obj
x_p2 = 800
y_p2 = 412
w_p2 = 50
h_p2 = 150
v_p2 = 5

# net obj # 原始數值(495, 362, 10, 200)，改過的數值調成與背景網子的範圍相同
x_net = 495
y_net = 315
w_net = 43
h_net = 400


def get_net():
    game1 = game.convert_alpha()  # 把中間包括背景網子的黑色長方形調為透明
    pygame.draw.rect(game1, (0, 0, 0, 0), ((x_net, y_net), (w_net, h_net)))


def text_score():
    pygame.font.init()
    font = pygame.font.Font("ARCADECLASSIC.TTF", 30)
    return font


def text_cele():
    font = pygame.font.Font("ARCADECLASSIC.TTF", 30)
    return font


# p1圖片左右移動轉換
def move(cnt, img1, img2, img3):
    if (cnt // 6) % 3 == 0:
        get_p(img1, x_p1, y_p1, w_p1, h_p1)
        cnt += 1
    elif (cnt // 6) % 3 == 1:
        get_p(img2, x_p1, y_p1, w_p1, h_p1)
        cnt += 1
    else:
        get_p(img3, x_p1, y_p1, w_p1, h_p1)
        cnt += 1
    return cnt


def jump(img1):
    get_p(img1, x_p1, y_p1, w_p1, h_p1)


# 解除殘影
def return_background():
    game.blit(picture, (0, 0))
    game.blit(p1_score_text, (20, 0))
    game.blit(p2_score_text, (840, 0))
    if p1_win and not p2_win:
        game.blit(p1_win_text, (200, 300))
    elif p2_win and not p1_win:
        game.blit(p2_win_text, (700, 300))


p1_score = 0
p2_score = 0

picture = pygame.image.load("羽球背景.jpg")
picture = pygame.transform.scale(picture, (1000, 562))
rect = picture.get_rect()
rect = rect.move((0, 0))

p1_win_text = text_cele().render('P LAYER 1 WINS!', False, (255, 215, 0))
p2_win_text = text_cele().render('P LAYER 2 WINS!', False, (255, 215, 0))

isJump_p1 = False  # 跳的判斷
jumpCount_p1 = 10  # 體力
isJump_p2 = False
jumpCount_p2 = 10

iden = 20  # 擊球判定

isHit_p1 = False

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

    # 慶祝訊息
    p1_win = False
    p2_win = False
    if p1_score == 3:
        p1_win = True
        game.blit(p1_win_text, (200, 300))
    elif p2_score == 3:
        p2_win = True
        game.blit(p2_win_text, (700, 300))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    # p1擊球判定
    if not isHit_p1:
        if not isJump_p1:
            if x_p1 - iden < x_ball < x_p1 + w_p1 + iden and y_ball > y_p1 - iden:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_z]:
                    vx_ball = cos(-10 * random.uniform(6.5, 8.0) * rad) * 5
                    vy_ball = sin(-10 * random.uniform(6.5, 8.0) * rad) * 5
                    isHit_p1 = True
                elif keys[pygame.K_x]:
                    vx_ball = cos(-10 * random.uniform(3.0, 4.5) * rad) * 9
                    vy_ball = sin(-10 * random.uniform(3.0, 4.5) * rad) * 9
                    isHit_p1 = True
        else:
            if x_p1 - iden < x_ball < x_p1 + w_p1 + iden and y_ball < 400:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_c]:
                    vx_ball = cos(10 * random.uniform(3.0, 4.5) * rad) * 40
                    vy_ball = sin(10 * random.uniform(3.0, 4.5) * rad) * 30
                    isHit_p1 = True
    else:
        if x_ball >= 500:
            isHit_p1 = False

    # p2擊球判定
    if not isJump_p2:
        if x_p2 - iden < x_ball < x_p2 + w_p2 + iden and y_ball > y_p2 - iden:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_l]:
                vx_ball = cos(-10 * random.uniform(15.0, 16.2) * rad) * 9
                vy_ball = sin(-10 * random.uniform(15.0, 16.2) * rad) * 10
            elif keys[pygame.K_k]:
                vx_ball = cos(-10 * random.uniform(11.5, 13.5) * rad) * 9
                vy_ball = sin(-10 * random.uniform(11.5, 13.5) * rad) * 9.5
    else:
        if x_p2 - iden < x_ball < x_p2 + w_p2 + iden and y_ball < 400:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SEMICOLON]:
                vx_ball = cos(-10 * random.uniform(18.5, 20.0) * rad) * 10
                vy_ball = sin(-10 * random.uniform(18.5, 20.0) * rad) * 25

    # 觸網
    if x_net < x_ball < x_net + w_net and y_net < y_ball <= y_net + h_net:
        # if x_ball > x_net and y_ball > y_net:
        if vx_ball > 0:
            p2_score += 1
            serve(2)
        # if x_ball < x_net + w_net and y_ball > y_net:
        else:
            p1_score += 1
            serve(1)

    # 落地和出界
    if y_ball > 562 or x_ball > 1000 or x_ball < 0:
        if (0 < x_ball < x_net and y_ball > 562) or (x_ball > 1000):
            p2_score += 1
            serve(2)
        elif (x_net + w_net < x_ball < 1000 and y_ball > 562) or (x_ball < 0):
            p1_score += 1
            serve(1)

    # p1 movement
    get_p("blue_4.png", x_p1, y_p1, w_p1, h_p1)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        return_background()
        x_p1 -= v_p1
        cnt = move(cnt, "blue_4.png", "blue_run_01.png", "blue_run_02.png")
        if x_p1 <= 0:
            x_p1 = 0
    elif keys[pygame.K_d]:
        return_background()
        x_p1 += v_p1
        cnt = move(cnt, "blue_4.png", "blue_run_01.png", "blue_run_02.png")
        if x_p1 + w_p1 >= 495:
            x_p1 = 495 - w_p1

    if not isJump_p1:
        if keys[pygame.K_w]:
            return_background()
            jump('blue_5.png')
            isJump_p1 = True
    else:
        return_background()
        jump('blue_5.png')
        if jumpCount_p1 >= -10:
            neg_p1 = 1
            if jumpCount_p1 < 0:
                neg_p1 = -1
            y_p1 -= (jumpCount_p1 ** 2) * neg_p1 * 0.4
            jumpCount_p1 -= 0.5
        else:
            isJump_p1 = False
            jumpCount_p1 = 10

    # p2 movement
    get_p("red_2.png", x_p2, y_p2, w_p2, h_p2)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x_p2 -= v_p2
        if x_p2 <= 495 + w_net:
            x_p2 = 495 + w_net
    elif keys[pygame.K_RIGHT]:
        x_p2 += v_p2
        if x_p2 + w_p2 >= 1000:
            x_p2 = 1000 - w_p2

    if not isJump_p2:
        if keys[pygame.K_UP]:
            isJump_p2 = True
    else:
        if jumpCount_p2 >= -10:
            neg_p2 = 1
            if jumpCount_p2 < 0:
                neg_p2 = -1
            y_p2 -= (jumpCount_p2 ** 2) * neg_p2 * 0.4  # 用參數調整起跳與落地速度
            jumpCount_p2 -= 0.5
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
    clock.tick(75)

# 二碰
# 球的角度和速度需調整
# 殺球(角度、速度、gravity要調整)(是否要和跳起來整合成一個按鍵)
# 太靠近網子時怎麼處理
