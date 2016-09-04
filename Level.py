import pygame, numpy, random

from Entities import *

class Level(object):
    def __init__(self, g):
        self.g = g
        self.trees = 0

    def generate_random(self,rows, cols):
        m = numpy.zeros((rows, cols))
        
        
        # Generate water
        for i in range(rows):
            for j in range(cols):
                if random.randint(1, 10) == 1:
                    m[i, j] = 1
                    w = Water([32 * i, 32 * j], self.g.water, self.g.sprites)
                    
                # increase probability if neighbour is filled
                if m[(i+1)%rows, j] == 1 or m[(i-1)%rows, j] == 1 or m[i, (j-1)%cols] == 1 or m[i, (j+1)%cols] == 1:
                    if random.randint(1, 4) == 1:
                        m[i, j] = 1
                        w = Water([32 * i, 32 * j], self.g.water, self.g.sprites)
        
        # Generate trees
        for i in range(rows):
            for j in range(cols):
                if m[i, j] != 1:
                        if random.randint(1, 90) == 1:
                            t = Tree(self.g, [32*i, 32*j], self.g.trees, self.g.sprites)
                            m[i, j] = 1
                            print("{0}: {1}").format(32*i, 32*j)
                            self.trees += 1