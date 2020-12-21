import pygame, sys
from math import sin, cos, pi
import random
from time import sleep
from pathlib import Path

pygame.init()
screen_width = 1000
screen_height = 562
game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("羽球高高手")
clock = pygame.time.Clock()

# ball obj
x_ball = 500
y_ball = 100
r_ball = 10
v_ball = 5
rad = pi / 180
ang = random.choice([180, 0])
angle = -ang * rad
vx_ball = cos(angle) * v_ball
vy_ball = sin(angle) * v_ball
grav = 0.1

# net obj # 原始數值(495, 362, 10, 200)，改過的數值調成與背景網子的範圍相同
x_net = 495
y_net = 315
w_net = 43
h_net = 400

# default settings
rad = pi / 180
IDEN = 20  # 擊球判定
player_width = 50
player_height = 150
IMG_PATH = Path(__file__).resolve().parent / '圖檔'
MUSIC_PATH = Path(__file__).resolve().parent / '音效'
p1_score = 0
p2_score = 0
player_speed = 5

p1_moving_sprites = []
p1_moving_sprites.append(pygame.image.load(str(IMG_PATH / "blue_4.png")))
p1_moving_sprites.append(pygame.image.load(str(IMG_PATH / "blue_run_01.png")))
p1_moving_sprites.append(pygame.image.load(str(IMG_PATH / "blue_run_02.png")))

p2_moving_sprites = [] # 跟p1方向相反



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, moving_sprites_list):
        super().__init__()
        self.x, self.y = pos_x, pos_y
        self.moving_sprites = []
        self.jumping_sprites = []
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_jumping = False
        self.jumpcount = 0
        self.jumpdirection = 0
        self.moving_sprites = moving_sprites_list
        self.current = 0
        self.image = self.moving_sprites[self.current]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        
    def wiggle(self):
        if self.is_moving_right:
            self.current += 0.3
            if self.current >= len(self.moving_sprites):
                self.current = 0
                self.is_moving_right = False
            self.image = self.moving_sprites[int(self.current)]
        elif self.is_moving_left:
            self.current -= 0.3
            if self.current >= len(self.moving_sprites):
                self.current = 0
                self.is_moving_left = False
            self.image = self.moving_sprites[int(self.current)]


    def move_right(self):
        self.is_moving_right = True
        self.x += player_speed
        if self.rect.right >= x_net or self.rect.right >= screen_width:
            self.x = self.rect.centerx


    def move_left(self):
        self.is_moving_left = True
        self.x -= player_speed
        if self.rect.left <= 0 or self.rect.left <= x_net:
            self.x = self.rect.centerx

    # def get_player(self): # 人物生成
    #     player_img = pygame.image.load(self.path)
    #     player_img = pygame.transform.scale(player_img, (80, 120))
    #     game.blit(player_img, ((self.x, self.y), (player_width, player_height)))


    def jump(self): # 人物跳
        if self.is_jumping:
            self.is_moving_right = False
            self.is_moving_left = False
            self.image = pygame.image.load(str(IMG_PATH / "blue_5.png"))
            if self.jumpcount >= -10:
                self.jumpdirection = 1
                if self.jumpcount < 0:
                    self.jumpdirection = -1
                self.y -= (self.jumpcount ** 2) * self.jumpdirection * 0.4
                self.jumpcount -= 0.5
            else:
                self.isjumping = False
                self.jumpcount = 10


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


def check_if_win():
    if p1_score == 3:
        p1_cele = text_cele().render('P LAYER 1 WINS!', False, (255, 215, 0))
        game.blit(p1_cele, (200, 300))
    elif p2_score == 3:
        p2_cele = text_cele().render('P LAYER 2 WINS!', False, (255, 215, 0))
        game.blit(p2_cele, (700, 300))
    if keys[pygame.K_ESCAPE]:
        pygame.quit()


IDEN = 20  # 擊球判定
cnt = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    check_if_win()

    # p1擊球判定
    if not self.isjumping:
        if x_p1 - IDEN < x_ball < x_p1 + w_p1 + IDEN and y_ball > y_p1 - IDEN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                vx_ball = cos(-10 * random.uniform(6.5, 8.0) * rad) * 6.0
                vy_ball = sin(-10 * random.uniform(6.5, 8.0) * rad) * 6.5
            elif keys[pygame.K_x]:
                vx_ball = cos(-10 * random.uniform(3.0, 4.5) * rad) * 4.5
                vy_ball = sin(-10 * random.uniform(3.0, 4.5) * rad) * 5.5
    else:
        if x_p1 - IDEN < x_ball < x_p1 + w_p1 + IDEN and y_ball < 400:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                vx_ball = cos(10 * random.uniform(3.0, 4.5) * rad) * 10
                vy_ball = sin(10 * random.uniform(3.0, 4.5) * rad) * 10

    game.blit(picture, (0,0))