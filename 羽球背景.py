import pygame

screen = pygame.display.set_mode((1000, 562))
pygame.display.set_caption("羽球高高手")

picture = pygame.image.load("羽球背景.jpg")
picture = pygame.transform.scale(picture,(1000, 562))

rect = picture.get_rect()

rect = rect.move((0, 0))
screen.blit(picture, rect)

pygame.display.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
