import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platforming')

x = 200
y = 200
img = pygame.image.load("Pictures/ghost.jpg")

run = True
while run:
    for event in pygame.event.get():
        #Quit game
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
