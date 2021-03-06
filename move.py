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

# shuttle obj
x_shuttle = 500
y_shuttle = 100
r_shuttle = 10
v_shuttle = 3
rad = pi / 180
ang = random.choice([180])
angle = -ang * rad
vx_shuttle = cos(angle) * v_shuttle
vy_shuttle = sin(angle) * v_shuttle
grav = 0.09

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

shuttle_moving_sprites = []
shuttle_moving_sprites.append(pygame.image.load(str(IMG_PATH / "去背羽球_球頭向右下.png")))
shuttle_moving_sprites.append(pygame.image.load(str(IMG_PATH / "去背羽球_球頭向左上.png")))
shuttle_moving_sprites.append(pygame.image.load(str(IMG_PATH / "去背羽球_球頭向左下.png")))
shuttle_moving_sprites.append(pygame.image.load(str(IMG_PATH / "去背羽球_球頭向右上.png")))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, moving_sprites_list):
        super().__init__()
        self.x, self.y = pos_x, pos_y
        self.is_moving_right = False
        self.is_moving_left = False
        self.is_jumping = False
        self.jumpcount = 10
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
            self.current -= 0.3
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
        elif self.rect.left <= x_net + w_net and self.rect.right > x_net:
            self.rect.left = x_net + w_net

    def check_if_jump(self, path): # 人物跳
        if not self.is_jumping:
            if self == p1:
                if keys[pygame.K_w]:
                    self.image = pygame.image.load(str(IMG_PATH / path))
                    self.image = pygame.transform.scale(self.image, (80, 120))
                    self.is_jumping = True
            elif self == p2:
                if keys[pygame.K_UP]:
                    self.image = pygame.image.load(str(IMG_PATH / path))
                    self.image = pygame.transform.scale(self.image, (80, 120))
                    self.is_jumping = True

        else:
            self.is_moving_right = False
            self.is_moving_left = False
            self.image = pygame.image.load(str(IMG_PATH / path))
            self.image = pygame.transform.scale(self.image, (80, 120))
            if self.jumpcount >= -10:
                self.jumpdirection = 1
                if self.jumpcount < 0:
                    self.jumpdirection = -1
                self.rect.y -= (self.jumpcount ** 2) * self.jumpdirection
                self.jumpcount -= 1
            else:
                self.is_jumping = False
                self.jumpcount = 10


    def lift(self, shuttle): # 挑球
        if self.rect.colliderect(shuttle):
            shuttle.vx = cos(-10 * random.uniform(6.5, 8.0) * rad) * 9
            shuttle.vy = sin(-10 * random.uniform(6.5, 8.0) * rad) * 10
            shuttle.update()

    def short(self, shuttle): # 小球
        if self.rect.colliderect(shuttle):
            shuttle.vx = cos(-10 * random.uniform(6.5, 8.0) * rad) * 7
            shuttle.vy = sin(-10 * random.uniform(6.5, 8.0) * rad) * 8
            shuttle.update()

    def drive(self, shuttle): # 平抽
        if self.rect.colliderect(shuttle):
            shuttle.vx = cos(-10 * random.uniform(4.0, 4.5) * rad) * 7.0
            shuttle.vy = sin(-10 * random.uniform(4.0, 4.5) * rad) * 7.5
            shuttle.update()

    def low_drive(self, shuttle): # 平抽(更平)
        if self.rect.colliderect(shuttle):
            shuttle.vx = cos(-10 * random.uniform(4.0, 4.5) * rad) * 6.5
            shuttle.vy = sin(-10 * random.uniform(4.0, 4.5) * rad) * 5.5
            shuttle.update()

    def hit(self, shuttle): # 平抽(更平)
        if self.rect.colliderect(shuttle):
            shuttle.vx = cos(-10 * random.uniform(6.5, 7.5) * rad) * 5.5
            shuttle.vy = sin(-10 * random.uniform(6.5, 7.5) * rad) * 5.5
            shuttle.update()


class Net(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.image = pygame.draw.rect(self.net_img, (0, 0, 0, 0), ((self.x, self.y), (self.w, self.h)))


    def get_net(self):
        self.net_img = game.convert_alpha()  # 把中間包括背景網子的黑色長方形調為透明
        pygame.draw.rect(self.net_img, (0, 0, 0, 0), ((self.x, self.y), (self.w, self.h)))

class Shuttle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x, self.y = x_shuttle, y_shuttle
        self.vx, self.vy = vx_shuttle, vy_shuttle
        self.is_hit_by_p1 = False
        self.is_hit_by_p2 = False
        self.moving_sprites = shuttle_moving_sprites
        self.current = 0
        self.image = self.moving_sprites[self.current]
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def dropping(self):
        self.vy += grav
        self.rect.x += self.vx
        self.rect.y += self.vy

    def update(self):
        if self.is_hit_by_p1:
            self.current += 1
            if self.current >= len(self.moving_sprites):
                self.current = 0
                self.is_moving_right = False
            self.image = self.moving_sprites[int(self.current)]
            self.image = pygame.transform.scale(self.image, (40, 40))
        elif self.is_hit_by_p2:
            self.current -= 1
            if self.current <= 0:
                self.current = len(self.moving_sprites)
                self.is_moving_left = False
            self.image = self.moving_sprites[-int(self.current)] # It just works. Dunno why.
            self.image = pygame.transform.scale(self.image, (40, 40))



# music_path = MUSIC_PATH / "背景音-選項3.mp3"
# pygame.mixer.music.load(str(music_path))
# pygame.mixer.music.play(loops = 0, start = 0.0)

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

shuttle_moves = pygame.sprite.Group()
shuttle = Shuttle()
shuttle_moves.add(shuttle)

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

    if keys[pygame.K_z] and 0 <= p1.rect.x <= 250:
        p1.lift(shuttle)
        shuttle.is_hit_by_p1 = True
    elif keys[pygame.K_z] and 250 < p1.rect.x <= 500:
        p1.short(shuttle)
        shuttle.is_hit_by_p1 = True
    elif keys[pygame.K_x] and 0 <= p1.rect.x <= 250:
        p1.drive(shuttle)
        shuttle.is_hit_by_p1 = True
    elif keys[pygame.K_x] and 250 < p1.rect.x <= 375:
        p1.low_drive(shuttle)
        shuttle.is_hit_by_p1 = True
    elif keys[pygame.K_x] and 375 < p1.rect.x <= 500:
        p1.hit(shuttle)
        shuttle.is_hit_by_p1 = True


    p1.check_if_jump('blue_5.png')
    # if not p1.is_jumping:
    #     p1.jump('blue_5.png')
    # else:
    #     p1.jump('blue_5.png')
        
    p2_moves.draw(game)
    if keys[pygame.K_RIGHT]:
        p2.move_right()
    elif keys[pygame.K_LEFT]:
        p2.move_left()

    if keys[pygame.K_k] and 0 <= p2.rect.x <= 250:
        p2.lift(shuttle)
        shuttle.is_hit_by_p2 = True
    elif keys[pygame.K_k] and 250 < p2.rect.x <= 500:
        p2.short(shuttle)
        shuttle.is_hit_by_p2 = True
    elif keys[pygame.K_l] and 0 <= p2.rect.x <= 250:
        p2.drive(shuttle)
        shuttle.is_hit_by_p2 = True
    elif keys[pygame.K_l] and 250 < p2.rect.x <= 375:
        p2.low_drive(shuttle)
        shuttle.is_hit_by_p2 = True
    elif keys[pygame.K_l] and 375 < p2.rect.x <= 500:
        p2.hit(shuttle)
        shuttle.is_hit_by_p2 = True
    p2.check_if_jump('red_6.png')
    # if not p2.is_jumping:
    #     p2.jump()
    # else:
    #     p2.jump('red_6.png')

    shuttle_moves.draw(game)
    shuttle.dropping()
    
    pygame.display.flip()
    clock.tick(50)
