import pygame
from .settings import screen
from .image import object
from .map import map
from .characters.hero import hero
from .characters.fly_enemy import fly_enemy1
from .characters.friendly_bot import friendly_bot
from .characters.static_enemy import static_enemy
from .characters.enemy import enemy1
from .settings import font
from .items import items
def start():
    run = True
    fps = pygame.time.Clock()
    finish_rect = pygame.Rect(1450, 600, 50, 50)
    
    win_text = font.render("Ви вийграли", True, "white")
    loose_text = font.render("Ви програли", True, "white")
    win = False
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    hero.IS_HOLD_BLASTER = not hero.IS_HOLD_BLASTER
        screen.fill((0, 0, 0))
        
        # for rect in map.LIST_COLLISION:
        #     pygame.draw.rect(screen, "green", rect)
        # pygame.draw.rect(screen,"magenta",finish_rect)
        
        fps.tick(60)
        if hero.HEART > 0 and win == False:
            object.show_image()
            
            map.show_map()
            hero.show_states()
            hero.show_image()
            hero.move()
            # pygame.draw.rect(screen, "red", hero.RECT_HERO)
            for enemy in map.ENEMY_LIST:
                enemy.animation()
                enemy.show_image()
                
            for item in items:
                item.show_image()
                item.collect()
            if hero.RECT_HERO.colliderect(finish_rect) and hero.HAS_KEY == True:
                win = True
        elif win == True:
            screen.blit(win_text, (520, 330))
        elif hero.HEART <= 0:
            screen.blit(loose_text, (520, 330))

        pygame.display.flip() 
