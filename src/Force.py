import pygame
from abstract import Updateable

'''
A force object is one that acts on an Entity
and interacts with its movement. They can have lifecycles.
'''
class Force(Updateable):
    def __init__(self, vector: pygame.math.Vector2, duration=100):
        Updateable.__init__(self, lifetime=duration)
        self.vector = vector
    
    @Updateable._contingent_update
    def update(self):
        pass

    @property
    def x(self):
        return self.vector.x
        
    @property
    def y(self):
        return self.vector.y