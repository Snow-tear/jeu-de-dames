import pygame
pygame.init()
window=pygame.display.set_mode((1024,768))
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:break

pygame.quit()