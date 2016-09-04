import pygame, sys
from pygame.locals import *
from Level import *

class Scene():
    def __init__(self, s):
        self.screen = s
        
        self.clock = pygame.time.Clock()
        
        self.tiles = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.tools = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        

class TextScreen():
    def __init__(self, s, text, color):
        self.screen = s
        self.text = text
        self.color = color
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                
                if event.type == KEYDOWN:
                    if event.key in [K_ESCAPE, K_RETURN]:
                        return
                    
            self.screen.fill(self.color)
            font = pygame.font.Font(None, 30)
            label = font.render(self.text, 1, (255, 255, 255))
            label_rect = label.get_rect()
            label_rect.center = ((self.screen.get_width() / 2, self.screen.get_height() / 2))
            self.screen.blit(label, label_rect)
            pygame.display.flip()
    
class Game(Scene):
    def __init__(self, s):
        Scene.__init__(self, s)
        
        level = Level(self)
        level.generate_random(self.screen.get_width() / 32, self.screen.get_height() / 32)
        
        self.trees = level.trees
        
        self.axe = Axe(self, [100, 100],self.sprites, self.tools, self.items)
        
        self.gun = Revolver(self, [200, 200], self.sprites)
        
        self.player = Player(self, [0, 0], self.sprites, self.player_group)
        
        self.finished = False
        
        self.running = False
    
    def run(self):
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT: self.quit()
           
            if self.trees == 0: #self.quit()
                self.finished = True
                
            if self.finished:
                self.sprites.empty()
                return
            
            self.screen.fill([140, 255, 115])
            self.sprites.draw(self.screen)
            self.sprites.update()
            pygame.display.flip()
            self.clock.tick(60)
                    
            
    def quit(self):
        pygame.quit()
        sys.exit(0)

class BossBattle(Scene):
    def __init__(self, s):
        Scene.__init__(self, s)
        
        self.boss = DreadMonster(self, self.sprites)
        self.gun = Revolver(self, [200, 200], self.sprites) 
        self.player = Player(self, [0, 0], self.sprites, self.player_group)
        
        self.boss_defeated = False
        
        self.axe = Axe(self, [-1000, -1000],self.sprites, self.tools, self.items)
        d = DreadBullet(self, [200, 200], self.sprites)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                    
            if self.boss_defeated:
                return
            
            self.screen.fill([255, 0, 0])
            self.sprites.draw(self.screen)
            self.sprites.update()
            pygame.display.flip()
            self.clock.tick(60)      

