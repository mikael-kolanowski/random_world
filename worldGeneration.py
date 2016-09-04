#! /usr/bin/env python

import numpy, random, pygame, sys
from pygame.locals import *

pygame.init()

class Game():
    def __init__(self):
        #self.screen = pygame.display.set_mode([640, 640 * 3/4])
        self.screen = pygame.display.set_mode([1280, 720])
        
        self.tiles = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        
        level = Level(self)
        level.generate_random(self.screen.get_width()/32, self.screen.get_height()/32)
        
        self.running = False
    
    def run(self):
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT: self.quit()
                
            self.screen.fill([255, 255, 255])
            self.tiles.draw(self.screen)
            self.tiles.update()
            pygame.display.flip()
                    
            
    def quit(self):
        pygame.quit()
        sys.exit(0)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.image = pygame.Surface([32, 32])
        self.image.fill([50, 100, 60])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.ticks = 0
        
    def update(self):
        self.ticks += 1
        self.ticks = self.ticks % 100
        if self.ticks > 50:
            self.image.fill([30, 30, 30])
            
        if self.ticks < 50:
            self.image.fill([50, 100, 60])

class Level(object):
    def __init__(self, g):
        self.g = g

    def generate_random(self,rows, cols):
        m = numpy.zeros((rows, cols))
        
        for i in range(rows):
            for j in range(cols):
                if random.randint(1, 10) == 1:
                    m[i, j] = 1
                    t = Tile([32 * i, 32 * j], self.g.tiles)
                    
                # increase propapility if neighbour is filled
                if m[(i+1)%rows, j] == 1 or m[(i-1)%rows, j] == 1 or m[i, (j-1)%cols] == 1 or m[i, (j+1)%cols] == 1:
                    if random.randint(1, 4) == 1:
                        m[i, j] = 1
                        t = Tile([32 * i, 32 * j], self.g.tiles)
                
if __name__ == '__main__':
    g = Game()
    g.run()
