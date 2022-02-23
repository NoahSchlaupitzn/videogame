import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platforming')

# Set frame rate
clock = pygame.time.Clock()


moving_left = False
moving_right = False


class Ghost(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load("Pictures/ghost.jpg")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale),
                                           int(img.get_height() * scale)))
        self.rect = img.get_rect()
        self.rect.center = (x, y)

    def movement(self, moving_left, moving_right):
        # Reset movement variables
        dx = 0
        dy = 0

        # Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(self.image, self.rect)


player = Ghost(400, 300, .25, 1)

run = True
while run:

    player.draw()
    player.movement(moving_left, moving_right)

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            run = False
        # Keyboard presses (down)
            # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            # Leaving game
            if event.key == pygame.K_ESCAPE:
                run = False
        # Keyboard presses (up)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    pygame.display.update()

pygame.quit()

