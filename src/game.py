import pygame
import math

from pygame.locals import *

from time import sleep

import levelLoader
import gameObject as go
import ui

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class App:
    def __init__(self):
        self._running = True
        self._display = None
        self.window = Window(1000, 740)
        # list to keep track of alle the objects, which have to be updated
        self.active_gameObjects = pygame.sprite.Group()

    def on_init(self):
        #TODO remove: just to test the leveldata
        pygame.init()
        self._display = pygame.display.set_mode((self.window.width,self.window.height),pygame.HWSURFACE)
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

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    #show the intro screen
    def game_intro(self):
        if self.on_init() == False:
            self._running = False

        self.ui.setRunAction(self.startGame)
        self.ui.game_intro()

        self.on_cleanup()

    def startGame(self):
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

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    # additional action which occurs each loop
    def on_loop(self):
        # colission detection
        # make hitboxes as large as the whole area covered by a move
        permitMove = True
        collideBot = False

        if(self.level.goal != None):
            if(self.player.change.colliderect(self.level.goal.rect)):
                self._running = False
                print("You won! Time needed", self.player.time, "time units")

        for sprite in self.level.passive_gameObjects:
            if(sprite.blocking):
                hitbox = self.player.change.copy()
                hitbox.y += self.player.gravity
                if hitbox.colliderect(sprite.rect):
                    collideBot = True
                    self.player.jumpingHeight = 0

                elif  self.player.change.colliderect(sprite.rect):
                    permitMove = False

        self.player.jumpingAllowed = collideBot and permitMove

        if(not permitMove):
            self.player.cancelMove()

        if(not collideBot):
            self.player.applyGravity()

        # update all active objects
        self.active_gameObjects.update()

        self.player.time += 1

    # rendering the frame
    def on_render(self):
        self._display.fill((0,0,0))

        self.active_gameObjects.draw(self._display)
        self.level.passive_gameObjects.draw(self._display)

        pygame.display.flip()
        self.clock.tick(30)

    # actions on shutting the program down
    def on_cleanup(self):
        pygame.quit()

    def move_player(self):
        keys = pygame.key.get_pressed()
        direction = 0
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
        self.player.move(direction)

    def on_execute(self):
        while(self._running):
            pygame.event.pump()
            self.move_player()
            self.on_loop()
            self.on_render()



if __name__ == "__main__":
    app = App()
    app.game_intro()
