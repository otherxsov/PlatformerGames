from .character import Character
from ..map import map
import pygame
from ..settings import screen
from .hero import hero



class FlyEnemy(Character):
    def __init__(self, width, height, x, y, speed, finish_x):
        Character.__init__(self, width, height, "enemy1/fly/0.png", x, y, speed)
        self.FLYING_IMAGE = self.create_animation_list(folder_name = "enemy1/fly", count_image = 2)
        self.FLYING_IMAGE_LEFT = self.create_animation_list(folder_name = "enemy1/fly", count_image= 2,flip_x = True)
        
        self.FINISH_X = finish_x
        self.START_POINT = x
        self.ATACK_COUNTER = 0
        self.IS_EXPLOSION = False
        self.BARREL = Character(width = 50, height = 50, image_name = "barrel/0.png", x = 0, y = 0, speed = 0)
        self.BARREL.LIST_EXPLOSION = self.BARREL.create_animation_list(folder_name = "barrel", count_image = 8)
        self.ENEMY_DEATH_LIST = self.create_animation_list("enemy1/death", 5, False)

    def flying(self):
        if self.DIRECTION == "right":
            self.X += self.SPEED
            if self.X >= self.FINISH_X:
                self.DIRECTION = "left"
        else:
            self.X -= self.SPEED
            if self.X <= self.START_POINT:
                self.DIRECTION = "right"
        self.play_animation(15, 29, self.FLYING_IMAGE, self.FLYING_IMAGE_LEFT)

    def animation(self):
        if self.ENEMY_DEATH:
            self.play_animation(time= 10, max_count= 39, list_image=self.ENEMY_DEATH_LIST)
            self.Y += 4
            if self.Y >= 500:
                map.ENEMY_LIST.remove(self)
        else:
            self.flying()
            self.attack()
    
    def attack(self):
        coll_rect = pygame.Rect(self.X + self.WIDTH / 2 - 1, self.Y + self.HEIGTH * 0.75 , 2,700)
        # pygame.draw.rect(screen, "magenta", coll_rect)
        if hero.RECT_HERO.colliderect(coll_rect) and self.ATACK_COUNTER == 0:
            self.BARREL.X = self.X + 45
            self.BARREL.Y = self.Y + self.HEIGTH * 0.75
            self.ATACK_COUNTER = 150
        self.barrel_motion()
        if self.ATACK_COUNTER < 0:
            self.ATACK_COUNTER += 1
        if self.IS_EXPLOSION == True:
            self.BARREL.show_image()
            if self.BARREL.IMAGE_COUNTER == 38:
                self.IS_EXPLOSION = False
            self.BARREL.play_animation(time= 5, max_count= 39, list_image= self.BARREL.LIST_EXPLOSION)
    
    def barrel_motion(self):
        if self.ATACK_COUNTER > 0:
            self.ATACK_COUNTER -= 1
            self.BARREL.Y += 4
            self.BARREL.show_image()
            self.BAREEL_RECT = pygame.Rect(self.BARREL.X, self.BARREL.Y, self.BARREL.WIDTH, self.BARREL.HEIGTH)
            if hero.RECT_HERO.colliderect(self.BAREEL_RECT):
                if hero.PROTECT == True:
                    hero.PROTECT = False
                else:
                    hero.HEART -= 1
                self.IS_EXPLOSION = True
                self.ATACK_COUNTER = -40
            for block in map.LIST_COLLISION:
                block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
                # pygame.draw.rect(screen,'RED',block_rect)
                if block_rect.colliderect(self.BAREEL_RECT):
                    self.ATACK_COUNTER = -40
                    self.IS_EXPLOSION = True
                    break
                


fly_enemy1 = FlyEnemy(140, 120, 300, 100, 3, 1000)
map.ENEMY_LIST.append(fly_enemy1)
