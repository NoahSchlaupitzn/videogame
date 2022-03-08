import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Platforming')

# Set frame rate
clock = pygame.time.Clock()
FPS = 45

# Game Variables
gravity = .75

# Action variables
moving_left = False
moving_right = False
throw = False

# Load images
# Spear
spear_img = pygame.image.load('Pictures/weapons/spear.png').convert_alpha()
spear_size = (110, 25)
spear_img = pygame.transform.scale(spear_img, spear_size)

# Define colors
BG = (82, 122, 135, 1)
red = (0, 0, 175)


# This fill the background with bg color
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, red, (0, 500), (SCREEN_WIDTH, 500))


# This is my ghost class for create the rect/img, movement, and drawing it on the screen
class Walter(pygame.sprite.Sprite):

    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.throw_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.alive = True

        # This can probably be its own method
        self.animation_list = []
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        # Load all images for the players
        animation_types = ['idle', 'walking', 'jump', 'spearing']

        # Looping animations
        for animation in animation_types:
            # Reset temporary list
            temp_list = []
            # Count number of files in the folder
            num_of_frames = len(os.listdir(f"Pictures/{self.char_type}/{animation}"))
            # Loop through pictures in the folder
            for i in range(num_of_frames):
                img = pygame.image.load(f"Pictures/{self.char_type}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale),
                                                   int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        # Defining self.image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # Update cooldown
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

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
        if self.jump and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        dy += self.vel_y

        # Apply Gravity
        self.vel_y += gravity

        # Terminal velocity
        if self.vel_y > 8.25:
            self.vel_y = 9

        # Check collision with floor
        if self.rect.bottom + dy > 500:
            dy = 500 - self.rect.bottom
            self.in_air = False

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def throw(self):
        if self.throw_cooldown == 0 and self.ammo > 0:
            self.throw_cooldown = 20
            spear = Spear(self.rect.centerx + (.7344 * self.rect.size[0] * self.direction),
                          self.rect.centery, self.direction)
            spear_group.add(spear)
            # Reduce spears
            self.ammo -= 1

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
            # add this when I add a death animation
            #if self.action == 4:
                #self.frame_index = len(self.animation_list[self.action]) - 1
            #else:
            self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            # Add a death animation in update action
            # self.update_action()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = spear_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Move spear
        self.rect.x += (self.direction * self.speed)
        # Check if spears are off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # Check collision with characters
        if pygame.sprite.spritecollide(player, spear_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, spear_group, False):
            if enemy.alive:
                enemy.health -= 25
                print(enemy.health)
                self.kill()


# Create sprite groups
spear_group = pygame.sprite.Group()

player = Walter('walter', 400, 300, 3, 6, 1_000_000_000)
enemy = Walter('walter', 700, 300, 3, 6, 10)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.update()
    player.draw()

    enemy.update()
    enemy.draw()

    # Update and draw groups
    spear_group.update()
    spear_group.draw(screen)

    # Update player actions
    if player.alive:
        # Throw spear
        if throw:
            player.throw()
            player.update_action(3)
        elif player.in_air:
            # 2 means jump
            player.update_action(2)
        elif moving_left or moving_right:
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
            if event.key == pygame.K_a:
                throw = True

            # Leaving game
            if event.key == pygame.K_ESCAPE:
                run = False
        # Keyboard presses (up)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_a:
                throw = False

    pygame.display.update()

pygame.quit()
