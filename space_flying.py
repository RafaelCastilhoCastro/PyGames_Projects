import random
import time
import sys
import pygame
import pygame.time
from pygame.locals import *

pygame.init()

FPS = pygame.time.Clock()

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(128, 128, 128)
blue = pygame.Color(0, 0, 135)

pygame.display.set_caption("Space flying")

screen_width = 800
screen_height = 600
display_surf = pygame.display.set_mode((screen_width, screen_height))
speed = 1
score = 0
fps_max = 60

font = pygame.font.SysFont("Verdana", 100)
font_small = pygame.font.SysFont("Verdana", 30)
game_over = font.render("Game Over", True, white)
game_over_w, game_over_h = font.size('Game Over')


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/red_dot2.png")
        self.size = random.randint(15, 55)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.surf = pygame.Surface((self.size, self.size))
        self.rect = self.surf.get_rect()
        self.rect.x = screen_width + self.surf.get_width() + random.randint(0, 300)
        self.rect.y = random.randint(0, screen_height/2) + random.randint(0, screen_height/2)
        self.x_spd = random.randint(1, 5) * random.randint(1, 3)
        self.y_spd = 0
        self.type = random.randint(1, 3)        # Type 0 horizontal. Type 1 ascending. Type 2 descending.

    def move(self):
        self.rect.move_ip(((self.x_spd * speed)/2) * -1, 0)

        if self.type == 1:
            if self.y_spd == 0:     # Softens the Y decrease
                self.y_spd = -1
            else:
                self.y_spd = 0
        elif self.type == 2:
            if self.y_spd == 0:     # Softens the Y increase
                self.y_spd = 1
            else:
                self.y_spd = 0

        self.rect.move_ip(0, self.y_spd)

        if self.rect.right < 0:
            self.x_spd = random.randint(1, 5) * random.randint(1, 3)
            self.rect.center = (screen_width + self.surf.get_width(), (random.randint(0, screen_height)))

        if self.rect.bottom < 0:
            self.x_spd = random.randint(1, 5) * random.randint(1, 3)
            self.rect.center = (screen_width + self.surf.get_width(), (random.randint(0, screen_height)))

        if self.rect.top > screen_height:
            self.x_spd = random.randint(1, 5) * random.randint(1, 3)
            self.rect.center = (screen_width + self.surf.get_width(), (random.randint(0, screen_height)))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/player_pose0.png")
        self.surf = pygame.Surface((90, 40))
        self.rect = self.surf.get_rect(center=(self.surf.get_width()/2, screen_height/2))
        self.spin = 0

    """
    # KEYBOARD-BASED PLAYER MOVEMENT & ANIMATION
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] and self.rect.top >= 0:
            self.rect.move_ip(0, -5)
            if self.spin > -3:
                self.spin -= 0.3
        elif pressed_keys[K_DOWN] and self.rect.bottom <= 600:
            self.rect.move_ip(0, 5)
            if self.spin < 3:
                self.spin += 0.3
        elif pressed_keys[K_LEFT] and self.rect.left >= 0:
            self.rect.move_ip(-5, 0)
        elif pressed_keys[K_RIGHT] and self.rect.right <= 800:
            self.rect.move_ip(5, 0)

        player_pose = "images/player_pose{}.png".format(str(int(self.spin)))
        self.image = pygame.image.load(player_pose)
    """


class Background():
    def __init__(self):
        self.bg_img = pygame.image.load("images/stars_bg1.png")
        self.bg_rect = self.bg_img.get_rect()

        self.bg1_y = 0
        self.bg1_x = 0

        self.bg2_y = 0
        self.bg2_x = self.bg_rect.width

        self.bg_spd = 1

    def move(self):
        self.bg1_x -= self.bg_spd
        self.bg2_x -= self.bg_spd
        if self.bg1_x <= -self.bg_rect.width:
            self.bg1_x = self.bg_rect.width
        if self.bg2_x <= -self.bg_rect.width:
            self.bg2_x = self.bg_rect.width

    def render(self):
        display_surf.blit(self.bg_img, (self.bg1_x, self.bg1_y))
        display_surf.blit(self.bg_img, (self.bg2_x, self.bg2_y))


P1 = Player()
E1 = Enemy()
E2 = Enemy()
E3 = Enemy()
E4 = Enemy()
E5 = Enemy()
E6 = Enemy()
E7 = Enemy()
E8 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
enemies.add(E3)
enemies.add(E4)
enemies.add(E5)
enemies.add(E6)
enemies.add(E7)
enemies.add(E8)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)
all_sprites.add(E3)
all_sprites.add(E4)
all_sprites.add(E5)
all_sprites.add(E6)
all_sprites.add(E7)
all_sprites.add(E8)

bg_obj = Background()


# INCREASE GAME SPEED & SCORE
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

while True:
    for event in pygame.event.get():
        if event.type == inc_speed:
            speed += 0.01
            score += 1

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        # MOUSE-BASED PLAYER MOVEMENT & ANIMATION
        if event.type == MOUSEMOTION:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)
            P1.rect.center = (event.pos[0], event.pos[1])
            mouse_y_pos = pygame.mouse.get_rel()[1]
            if mouse_y_pos < 0:
                if P1.spin > -3:
                    P1.spin -= 0.08
            elif mouse_y_pos > 0:
                if P1.spin < 3:
                    P1.spin += 0.08

            player_pose = "images/player_pose{}.png".format(str(int(P1.spin)))
            P1.image = pygame.image.load(player_pose)

    bg_obj.move()
    bg_obj.render()

    # DRAW SCORE
    scores_text = font_small.render(str(score), True, white)
    display_surf.blit(scores_text, (10, 10))

    # DRAWS AND MOVES SPRITES
    display_surf.blit(P1.image, P1.rect)
    # P1.move()     # ENABLE FOR KEYBOARD-BASED PLAYER MOVEMENT
    for entity in enemies:
        display_surf.blit(entity.image, entity.rect)
        entity.move()

    # COLLISION CHECK
    if pygame.sprite.spritecollideany(P1, enemies):
        # pygame.mixer.Sound('crash.wav').play()
        display_surf.blit(game_over, (screen_width/2 - game_over_w/2, screen_height/2 - game_over_h/2))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FPS.tick(fps_max)

"""

Multiple lives or health bar

Add audio
    ambient
    player moves


collision between enemies


Done:


"""