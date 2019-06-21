import pygame

IMAGEDIR = "../images/"

""" ----------------------------------------------------------------------------
    Class for storing position information
"""
class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

""" ----------------------------------------------------------------------------
    Base class for all game objects
"""
class GameObject(pygame.sprite.Sprite):
    def __init__(self, path, pos = Position(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.imagepath = IMAGEDIR + path
        self.load_image()
        self.time = 0
        #set the initial position of the object
        self.rect = self.image.get_rect()
        self.set_position(pos)

    #.........................................................................
    def load_image(self):
        # if you want animated pictures, load a list of images and iterate
        # through them each frame you call the update method of an object which
        # derived from this class.
        self.image = pygame.image.load(self.imagepath).convert()

    #.........................................................................
    # set the position of the object
    def set_position(self, pos):
        self.rect.x = pos.x
        self.rect.y = pos.y

    #.........................................................................
    def set_size(self, size):
        self.Size = size

""" ----------------------------------------------------------------------------
    Class for static objects
"""
class staticObject(GameObject):
    def __init__(self, path, blocking,  pos = Position(0, 0)):
        GameObject.__init__(self, path, pos)
        self.blocking = blocking

""" ----------------------------------------------------------------------------
    Class for static stone like object which bloch movement
"""
class Stone(staticObject):
    def __init__(self, pos = Position(0, 0)):
        staticObject.__init__(self, "stone.png", True, pos)

""" ----------------------------------------------------------------------------
    Class for spawn point
"""
class Spawn(staticObject):
    def __init__(self, pos = Position(0, 0)):
        staticObject.__init__(self, "spawn.png", False, pos)

""" ----------------------------------------------------------------------------
    Class for goal
"""
class Goal(staticObject):
    def __init__(self, pos = Position(0, 0)):
        staticObject.__init__(self, "goal.png", False, pos)

""" ----------------------------------------------------------------------------
    Class for player data
"""
class Player(GameObject):
    def __init__(self, startpos, speed=10, velocity=0.95, gravity=20):
        GameObject.__init__(self, "jumper.png")
        self.rect = pygame.Rect((startpos.x, startpos.y),(20,20))
        self.change = self.rect.copy()
        self.speed = speed

        self.velocity = velocity
        self.jumpingHeight = 0
        self.gravity = gravity

        self.jumpingAllowed = False

    #.........................................................................
    # This function updates the position
    def move (self, delta_x):
        self.change.x +=  delta_x * self.speed
        self.change.y -=  self.jumpingHeight
        self.jumpingHeight = round(self.jumpingHeight * self.velocity)
        if(self.jumpingHeight <= 10):
            self.jumpingHeight = 0

    #.........................................................................
    def applyGravity(self):
        self.change.y +=  self.gravity

    #.........................................................................
    # Revert move so no ch
    def cancelMove (self):
        self.change.x =  self.rect.x
        self.change.y =  self.rect.y
        self.jumpingHeight /= self.velocity

    #.........................................................................
    # activates jumping
    def jump (self):
        if(self.jumpingAllowed ):
         self.jumpingHeight = 40
         self.jumpingAllowed = False

    #.........................................................................
    #update the rect by writing the new data to it
    def update(self):
        self.rect.x = self.change.x
        self.rect.y = self.change.y
