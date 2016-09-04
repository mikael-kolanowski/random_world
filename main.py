#! /usr/bin/env python

import numpy, random, pygame, sys
from pygame.locals import *

from Entities import *
from Level import *
from Scenes import *

pygame.init()

screen = pygame.display.set_mode([1280, 720])
                        
if __name__ == '__main__':
    intro = TextScreen(screen, "The world is filled with evil trees. You must destroy them!", [140, 255, 115])
    intro.run()
    
    g = Game(screen)
    g.run()
    
    bossIntro = TextScreen(screen, "You have defeated all the trees! Now you must vanquish the terrible Dread Monster!", [140, 255, 115])
    bossIntro.run()
    
    b = BossBattle(screen)
    b.run()
    
    testE = TextScreen(screen, "The dreadlock monster turned out to be a pacifist! The victory is yours!", [140, 255, 115])
    testE.run()
