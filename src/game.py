import pygame
import math

from pygame.locals import *

from time import sleep

import levelLoader
import gameObject as go
import ui

""" ----------------------------------------------------------------------------
    Container class for resolution information
"""
class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

""" ----------------------------------------------------------------------------
    Class for player data
"""
class App:
    def __init__(self):
        #initialize the application
        self._running = True
        self._display = None
        self.window = Window(1000, 740)
        # list to keep track of alle the objects, which have to be updated
        self.active_gameObjects = pygame.sprite.Group()

    #.........................................................................
    def on_init(self):
        #inti the engine
        #TODO remove: just to test the leveldata
        pygame.init()
        self._display = pygame.display.set_mode((self.window.width,
                                                 self.window.height),
                                                pygame.HWSURFACE)
        pygame.display.set_caption('SpringUndRenn')
        self.level = levelLoader.Level('level1/')

        # create the player
        if(self.level.spawn != None):
            #set the spawn if any
            spawnRect = self.level.spawn.rect
            self.player = go.Player(go.Position(spawnRect.x, spawnRect.y))
        else:
            self.player = go.Player(go.Position(60,  20))

        #self.player.load_image() # remove this later
        self.active_gameObjects.add(self.player)
        self.ui = ui.Ui(self._display, self.window)
        self.clock = pygame.time.Clock()

    #.........................................................................
    #show the menue screen
    def game_intro(self):
        if self.on_init() == False:
            self._running = False

        #make the game callable by the menue
        self.ui.setRunAction(self.startGame)
        #call the menue
        self.ui.game_intro()
        #after menue terminates, terminate the application
        self.on_cleanup()

    #.........................................................................
    def startGame(self):
        #start/restart the game and reset the player
        if(self.level.spawn != None):
            spawnRect = self.level.spawn.rect
            self.player.change.x = spawnRect.x
            self.player.change.y = spawnRect.y
        else:
            self.player.change.x, self.player.change.y = (60, 20)
        self.player.time = 0
        self.player.update()

        self._running = True
        self.on_execute()

    #.........................................................................
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    #.........................................................................
    # additional action which occurs each loop
    def on_loop(self):
        # colission detection
        # make hitboxes as large as the whole area covered by a move
        permitMove = True
        collideBot = False

        #check if the player reached the goal
        if(self.level.goal != None):
            if(self.player.change.colliderect(self.level.goal.rect)):
                self._running = False
                print("You won! Time needed", self.player.time, "time units")

        #check for each sprite of blocking objects if it collides with the
        #player
        for sprite in self.level.passive_gameObjects:
            if(sprite.blocking):
                hitbox = self.player.change.copy()
                hitbox.y += self.player.gravity
                if hitbox.colliderect(sprite.rect):
                    #if there is ground under the player, than save this info
                    collideBot = True
                    self.player.jumpingHeight = 0

                elif self.player.change.colliderect(sprite.rect):
                    #if the player collides and it's not ground, cancel player
                    #move
                    permitMove = False

        #the player is only allowed to jump if he stands on ground and will not
        #collide with other objects (TODO: works not that good...)
        self.player.jumpingAllowed = collideBot and permitMove

        #if the move did not fullfill all conditions for a valid move, cancel
        if(not permitMove):
            self.player.cancelMove()

        #if there is nothing under us, we will fall, and fall, and fall..
        if(not collideBot):
            self.player.applyGravity()

        # update all active objects
        self.active_gameObjects.update()

        #increase the time the player has played
        self.player.time += 1

    #.........................................................................
    # rendering the frame
    def on_render(self):
        #fill the display with a nice black
        self._display.fill((0,0,0))

        #draw all game objects
        self.active_gameObjects.draw(self._display)
        self.level.passive_gameObjects.draw(self._display)

        #redraw whole display content
        pygame.display.flip()
        self.clock.tick(30)

    #.........................................................................
    # actions on shutting the program down
    def on_cleanup(self):
        pygame.quit()

    #.........................................................................
    def move_player(self):
        keys = pygame.key.get_pressed()
        direction = 0
        #horizantal moves
        if (keys[K_d]):
            direction = 1
        if (keys[K_a]):
            direction = -1
        # if (keys[K_w]):
        #     self.player.move_up()
        # if (keys[K_s]):
        #     self.player.move_down()
        if (keys[K_SPACE]):
            self.player.jump()
        if (keys[K_ESCAPE]):
            self._running = False
        #execute the move
        self.player.move(direction)

    #.........................................................................
    def on_execute(self):
        #game loop
        while(self._running):
            pygame.event.pump()
            self.move_player()
            self.on_loop()
            self.on_render()


""" ----------------------------------------------------------------------------
    Main function and entry point of the programm
"""
if __name__ == "__main__":
    #create the application
    app = App()
    #call the menu screen
    app.game_intro()
