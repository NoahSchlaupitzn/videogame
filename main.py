import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platforming')

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Game Variables
gravity = .75

# Left and right variables
moving_left = False
moving_right = False

# Define colors
BG = (100, 100, 100)


# This fill the background with bg color
def draw_bg():
    screen.fill(BG)


# This is my ghost class for create the rect/img, movement, and drawing it on the screen
class Walter(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.alive = True

        # This can probably be its own method
        self.animation_list = []
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Range is 3 because it's looping through the first 3 images
        # Idle animation
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f"Pictures/{self.char_type}/idle/walter{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale),
                                               int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Walking animation

        temp_list = []
        for i in range(6):
            img = pygame.image.load(f"Pictures/{self.char_type}/walking/walter{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * scale),
                                               int(img.get_height() * scale)))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Defining self.image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def movement(self, moving_left, moving_right):
        # Reset movement variables
        dx = 0
        dy = 0

        # Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump:
            self.vel_y = -11
            self.jump = False
        dy += self.vel_y

        # Apply Gravity
        self.vel_y += gravity

        # Terminal velocity
        if self.vel_y > 8.25:
            self.vel_y = 9

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        animation_cooldown = 100
        # Update image base on current frame
        self.image = self.animation_list[self.action][self.frame_index]

        # Check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # If the animation ends, restart it
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Walter('walter', 400, 300, 3, 6)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()

    # Update player actions
    if player.alive:
        if moving_left or moving_right:
            # 1 means run
            player.update_action(1)
        else:
            # 0 means idle
            player.update_action(0)
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
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
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
