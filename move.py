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
p2_moving_sprites.append(pygame.image.load(str(IMG_PATH / "red_2.png")))
p2_moving_sprites.append(pygame.image.load(str(IMG_PATH / "red_run_01.png")))
p2_moving_sprites.append(pygame.image.load(str(IMG_PATH / "red_run_02.png")))



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
        self.image = pygame.transform.scale(self.image, (80, 120))

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    def wiggle(self):
        if self.is_moving_right:
            self.current += 0.3
            if self.current >= len(self.moving_sprites):
                self.current = 0
                self.is_moving_right = False
            self.image = self.moving_sprites[int(self.current)]
            self.image = pygame.transform.scale(self.image, (80, 120))
        elif self.is_moving_left:
            self.current -= 0.1
            if self.current <= 0:
                self.current = len(self.moving_sprites)
                self.is_moving_left = False
            self.image = self.moving_sprites[-int(self.current)] # It just works. Dunno why.
            self.image = pygame.transform.scale(self.image, (80, 120))

    def move_right(self):
        self.is_moving_right = True
        self.wiggle()
        self.rect.x += player_speed
        if self.rect.right >= x_net and self.rect.left <= x_net:
            self.rect.right = x_net
        elif self.rect.right >= screen_width and self.rect.left >= x_net:
            self.rect.right = screen_width

    def move_left(self):
        self.is_moving_left = True
        self.wiggle()
        self.rect.x -= player_speed
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.left <= x_net and self.rect.right > x_net:
            self.rect.left = x_net

    def jump(self): # 人物跳
        if self.is_jumping:
            self.is_moving_right = False
            self.is_moving_left = False
            self.image = pygame.image.load(str(IMG_PATH / "blue_5.png"))
            if self.jumpcount >= -10:
                self.jumpdirection = 1
                if self.jumpcount < 0:
                    self.jumpdirection = -1
                self.rect.y -= (self.jumpcount ** 2) * self.jumpdirection * 0.4
                self.jumpcount -= 0.5
            else:
                self.isjumping = False
                self.jumpcount = 10
        else:
            self.isjumping = True
    # def get_player(self): # 人物生成
    #     player_img = pygame.image.load(self.path)
    #     player_img = pygame.transform.scale(player_img, (80, 120))
    #     game.blit(player_img, ((self.x, self.y), (player_width, player_height)))


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

picture = pygame.image.load(str(IMG_PATH) + str('/') + '羽球背景.jpg')
picture = pygame.transform.scale(picture, (1000, 562))
rect = picture.get_rect()
rect = rect.move((0, 0))

p1_moves = pygame.sprite.Group()
p1 = Player(150, 412, p1_moving_sprites)
p1_moves.add(p1)

p2_moves = pygame.sprite.Group()
p2 = Player(800, 412, p2_moving_sprites)
p2_moves.add(p2)

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    game.blit(picture, (0,0))
    p1_moves.draw(game)
    if keys[pygame.K_d]:
        p1.move_right()
    elif keys[pygame.K_a]:
        p1.move_left()
    if keys[pygame.K_w]:
        p1.jump()
        
    p2_moves.draw(game)
    if keys[pygame.K_RIGHT]:
        p2.move_right()
    elif keys[pygame.K_LEFT]:
        p2.move_left()
    if keys[pygame.K_UP]:
        p2.jump()
    
    pygame.display.flip()
    clock.tick(50)
