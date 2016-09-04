import pygame

from pygame.locals import *

import random

class Water(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.image = pygame.Surface([32, 32])
        self.image.fill([20,75, 230])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.ticks = 0
        
    def update(self):
        self.ticks += 1
        self.ticks = self.ticks % 100
        if self.ticks > 50:
            self.image.fill([2, 125, 210])
            
        if self.ticks < 50:
            self.image.fill([20,75, 230])
            
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, color, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.image = pygame.Surface([32, 32])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.ticks = 0
        
    def update(self):
        pass
    
class Wall(Tile):
    def __init__(self, pos, *groups):
        Tile.__init__(self, pos, color=[70,70,70], *groups)
        
    def update(self):
        pass

class Tree(pygame.sprite.Sprite):
    def __init__(self,g, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.g = g
        
        #self.image = pygame.Surface([32, 32])
        #self.image.fill([11, 94, 4])
        self.image = pygame.image.load("tree.jpeg")
        #self.image = pygame.image.load("jew.png")
        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.health = 100
    
    def update(self):
        if self.health <= 0:
            self.kill()
            self.g.trees -= 1
            
        if pygame.sprite.spritecollide(self, self.g.tools, False) and self.g.axe.attacking:
            self.health -= 50
            
        if pygame.sprite.spritecollide(self, self.g.bullets, True):
            self.health -= 20
            
class Axe(pygame.sprite.Sprite):
    def __init__(self,g, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.g = g
        
        self.image = pygame.image.load("axe.png")
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.held = False
        self.attacking = False
        self.ticks = 0
        self.cooldown = 5
        self.extended = False
    
    def update(self):
        if pygame.sprite.spritecollide(self, self.g.player_group, False):
            self.held = True
            
        if self.held and not self.extended:
            self.rect.x = self.g.player.rect.right - 10
            self.rect.y = self.g.player.rect.centery + 5
            
        if self.held and self.extended:
            self.rect.x = self.g.player.rect.right + 5
            self.rect.y = self.g.player.rect.centery + 5
            
            if self.ticks > self.cooldown:
                self.extended = False
                self.attacking = False
            
        self.ticks += 1
    
    def attack(self):
        if self.ticks < self.cooldown:
            pass
            
        if self.ticks > self.cooldown:
            self.extended = True
            self.attacking = True
            self.ticks = 0
        
class Revolver(pygame.sprite.Sprite):
    def __init__(self, g, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.image = pygame.image.load("gun1.jpg")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.g = g
        
        self.held = False
        self.cooldown = 10
        self.ticks = 0
    
    def update(self):
        if pygame.sprite.spritecollide(self, self.g.player_group, False):
            self.held = True
        
        if self.held:
            self.rect.x = self.g.player.rect.x + 20
            #self.rect.y = self.g.player.rect.y
            self.rect.y = self.g.player.rect.centery - 10
            
            self.ticks += 1
        
    def fire(self):
        if self.ticks > self.cooldown:
            b = Bullet(self.g, [self.rect.x, self.rect.y], self.g.player.facing, self.g.sprites, self.g.bullets)
            self.ticks = 0
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, g, pos, d, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.image = pygame.Surface([5, 5])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.direction = d
        
    def update(self):
        v = 8
        
        if self.direction == "left":
            self.rect.x -= v
            
        elif self.direction == "right":
            self.rect.x += v
        
        elif self.direction == "up" or self.direction == "down":
            self.rect.x += v
    
class DreadMonster(pygame.sprite.Sprite):
    def __init__(self, g, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.image = pygame.image.load("dread_monster.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = 5
        
        self.health = 100
        self.direction = "down"
        
        self.g = g
        
    def update(self):
        v = 1.4
        
        if self.direction == "down":
            self.rect.y += v
            if self.rect.bottom >= self.g.screen.get_height():
                self.direction = "up"
                self.attack()
                
        if self.direction == "up":
            self.rect.y -= v
            if self.rect.y <= 0:
                self.direction = "down"
                self.attack()
                
        if random.randint(1, 10) == 1:
            self.attack()
            
        if pygame.sprite.spritecollide(self, self.g.bullets, True):
            self.health -= 10
            
        if self.health <= 0:
            self.g.boss_defeated = True
            self.kill()
    
    def attack(self):
        d = DreadBullet(self.g, [self.rect.x, self.rect.y], self.g.sprites)
        #self.g.sprites.add(d)
        print("attacking!")
    
class DreadBullet(pygame.sprite.Sprite):
    def __init__(self,g ,pos, *groups):
        #self.image = pygame.image.load("shampoo_projectile.jpg")
        self.image = pygame.Surface([10, 10])
        self.image.fill([30, 40, 50])
        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.health = 100
        
        self.g = g
        
    def update(self):
        v = 1
        self.rect.x -= v
        print(self.rect.x)
        
        if pygame.sprite.spritecollide(self, self.g.bullets, False):
            self.health -= 10
            
        if self.health < 0:
            self.kill()
    
    
class Player(pygame.sprite.Sprite):
    def __init__(self, g, pos, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        
        self.g = g
        
        #self.image = pygame.Surface([32, 32])
        #self.image.fill([100, 100, 100])
        self.image = pygame.image.load("Adolf_Hitler_portrait.jpg")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        
        self.ticks = 0
        
        
        self.attack_cooldown = 20
        #self.extended_cooldown = 10
        self.ticks = 0
        
        self.facing = "right"
        
    def update(self):
        pressed = pygame.key.get_pressed()
        v = 1.5
        self.ticks += 1
        self.g.axe.attacking = False
        
        if pygame.sprite.spritecollide(self, self.g.water, False):
            pass
            #v = 0.4
        
        if pressed[K_a]:
            self.rect.x -= v
            self.facing = "left"
            
        if pressed[K_d]:
            self.rect.x += v
            self.facing = "right"
            
        if pressed[K_w]:
            self.rect.y -= v
            self.facing = "up"
            
        if pressed[K_s]:
            self.rect.y += v
            self.facing = "down"
            
        if pressed[K_SPACE] and self.g.axe.held:
            #self.g.axe.attacking = True
            #self.g.axe.rect.x = self.rect.x + 25
            self.g.axe.attack()
            
        if pressed[K_SPACE] and self.g.gun.held:
            self.g.gun.fire()
        
        #if pressed[K_SPACE] and self.g.axe.held and self.ticks > self.cooldown:
         #   self.
            
            
        