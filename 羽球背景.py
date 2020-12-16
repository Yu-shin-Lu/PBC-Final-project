import pygame
pygame.font.init()

screen = pygame.display.set_mode((1000, 562))
pygame.display.set_caption("羽球高高手")

picture = pygame.image.load("羽球背景.jpg")
picture = pygame.transform.scale(picture,(1000, 562))

rect = picture.get_rect()

rect = rect.move((0, 0))

screen.blit(picture, rect)


myfont1 = pygame.font.Font("ARCADECLASSIC.TTF", 60)  # player1(左邊)的分數
textsurface1 = myfont1.render("Score 0", True, (255,215,0))  
screen.blit(textsurface1, (20, 0))

myfont2 = pygame.font.Font("ARCADECLASSIC.TTF", 60)  # player2(右邊)的分數
textsurface2 = myfont2.render("Score 0", True, (255,215,0))
screen.blit(textsurface2, (780, 0))

pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
pygame.quit()
