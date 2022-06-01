import pygame

pygame.init()
#screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#define player action variables
moving_left = False
moving_right = False

#framerate
clock = pygame.time.Clock()
fps = 90


#background color
BG = (144, 201, 120)

def draw_bg():
    screen.fill(BG)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, movespeed):
        pygame.sprite.Sprite.__init__(self)
        self.movespeed = movespeed
        self.direction = 1  # 1 is right, -1 is left
        self.flip = False
        img = pygame.image.load('art/CHARACTER_SPRITES/Black/Gunner_Black_Idle.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        #assign movement variables if moving left||right

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
        #update rect position
        self.rect.x += dx
        self.rect.y += dy



    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



player = Soldier(200, 200, 3, 5)

run = True
while run:

    clock.tick(fps)
    draw_bg()
    player.draw()
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
            if event.key == pygame.K_ESCAPE:
                run = False

        #check for key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False


    pygame.display.update()

pygame.quit()