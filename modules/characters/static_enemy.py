from .character import Character
from ..map import map
import pygame
from ..settings import screen
from .hero import hero


class StaticEnemy(Character):
    def __init__(self, width, height, x, y, direction):
        Character.__init__(self, width, height, "enemy2/atack/0.png",x, y, 0, direction)
        self.DIRECTION = direction
        self.IMAGE_ATACK = self.create_animation_list("enemy2/atack",6)
        self.IMAGE_ATACK_LEFT = self.create_animation_list("enemy2/atack",6, True)
        if self.DIRECTION == "right":
            self.IMAGE = self.IMAGE_ATACK[0]
        else:
            self.IMAGE = self.IMAGE_ATACK_LEFT[0]
        self.ENEMY_DEATH_LIST = self.create_animation_list("enemy2/death", 6, False)
        self.ENEMY_DEATH_LIST_LEFT = self.create_animation_list("enemy2/death", 6, True)
    def attack(self):
        if self.DIRECTION == "right":
            enemy_rect = pygame.Rect(self.X + self.WIDTH / 2, self.Y, self.WIDTH * 0.75, self.HEIGTH)
        else:
            enemy_rect = pygame.Rect(self.X - self.WIDTH / 2, self.Y, self.WIDTH * 0.75, self.HEIGTH)
        # pygame.draw.rect(screen, "red", enemy_rect)
        if hero.RECT_HERO.colliderect(enemy_rect) and self.IMAGE_COUNTER == 0:
            self.IMAGE_COUNTER = 1
        if hero.RECT_HERO.colliderect(enemy_rect) and self.IMAGE_COUNTER == 58:
            if hero.PROTECT == True:
                hero.PROTECT = False
            else:
                hero.HEART -= 1
            
    def animation(self):
        if self.ENEMY_DEATH:
            self.play_animation(time=10, max_count= 60, list_image= self.ENEMY_DEATH_LIST, list_image_left= self.ENEMY_DEATH_LIST_LEFT)
            if self.IMAGE_COUNTER == 59:
                map.ENEMY_LIST.remove(self)
        else:
            self.attack()
            if self.IMAGE_COUNTER > 0:
                self.play_animation(10, 59, self.IMAGE_ATACK, self.IMAGE_ATACK_LEFT)
            
static_enemy = StaticEnemy(width= 80, height=80, x=730, y= 370, direction= "right")
map.ENEMY_LIST.append(static_enemy)
static_enemy2 = StaticEnemy(width=80, height=80, x=180, y=570, direction="left")
map.ENEMY_LIST.append(static_enemy2)