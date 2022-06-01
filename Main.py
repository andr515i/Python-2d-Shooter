import pygame
import os

pygame.init()
# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# define player action variables
moving_left = False
moving_right = False
shoot = False

# framerate
clock = pygame.time.Clock()
fps = 60

#game variables
GRAVITY = 0.75


# load images
#bullet
bullet_img = pygame.image.load('img/Extra/Bullet.png').convert_alpha()

# background color
BG = (144, 201, 120)
RED = (255,0,0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, movespeed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.movespeed = movespeed
        self.direction = 1  # 1 is right, -1 is left
        self.flip = False
        self.vel_y = 0
        self.in_air = True
        self.jump = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump']
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)


        self.image = self.animation_list[self.action][self.frame_index]

        self.rect = self.image.get_rect()

        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # assign movement variables if moving left||right

        dx = 0
        dy = 0

        if moving_left:
            dx = -self.movespeed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.movespeed
            self.flip = False
            self.direction = 1

            #jump movement
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # invent gravity /// newton
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check for collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rect position
        self.rect.x += dx
        self.rect.y += dy



    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if new action is different to previous
        if new_action != self.action:
            self.action = new_action
            # update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.flip = False
        self.rect = self.image.get_rect()
        
        self.rect.center = (x,y)
        self.direction = direction

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed)
        #check if bullet is offscreen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


#create sprite groups
bullet_group = pygame.sprite.Group()


player = Soldier('Green', 200, 200, 3, 5)
enemy = Soldier('Red', 200, 200, 3, 5)

run = True
while run:

    clock.tick(fps)
    draw_bg()
    player.draw()
    player.update_animation()
    enemy.draw()

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)
    # update player actions
    if player.alive:
        #shoot bullets maniac
        if shoot:
            bullet = Bullet(player.rect.centerx + (0.37 * player.rect.size[0] * player.direction), player.rect.centery - 7, player.direction)
            bullet_group.add(bullet)
        if player.in_air:
            player.update_action(2)# jump
        # update player actons
        elif moving_left or moving_right:
            player.update_action(1)  # run
        else:
            player.update_action(0)  # idle

        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
            # check for key down press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # check for key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()
