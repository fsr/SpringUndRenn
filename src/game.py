import pygame
import math

from pygame.locals import *

from time import sleep

import levelLoader
import gameObject as go

#TODO look into the relative paths, from where the applicaiton is launched
MAXVELOCITY = 40

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class App:
    def __init__(self):
        self._running = True
        self._display = None
        self.window = Window(1000, 900)
        # list to keep track of alle the objects, which have to be updated
        self.active_gameObjects = pygame.sprite.Group()

    def on_init(self):
        #TODO remove: just to test the leveldata
        pygame.init()
        self._display = pygame.display.set_mode((self.window.width,self.window.height),pygame.HWSURFACE)
        pygame.display.set_caption('SpringUndRenn')
        self.level = levelLoader.Level('level1/')

        # create the player
        self.player = go.Player(go.Position(60,  20))
        self.player.load_image() # remove this later
        self.active_gameObjects.add(self.player)

        self.clock = pygame.time.Clock()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    def game_intro(self):
        if self.on_init() == False:
            self._running = False

        intro = True
        while intro:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            midWidth = self.window.width/2
            midHeigt = self.window.height/2
            self._display.fill((255, 255, 255))
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects('Spring und Renn!', largeText)
            TextRect.center = ((midWidth),(midHeigt - 100))
            self._display.blit(TextSurf, TextRect)

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            action = app.on_execute
            #print(mouse)

            if midWidth + 100 > mouse[0] > midWidth - 100 and midHeigt + 100 > mouse[1] > midHeigt + 50:
                pygame.draw.rect(self._display, (0, 255, 128), (midWidth - 100, midHeigt + 50, 200, 50))
                if click[0] == 1 and action != None:
                    print('Entering game')
                    action()
            else:
                pygame.draw.rect(self._display, (0, 255, 180), (midWidth - 100, midHeigt + 50, 200, 50))

            if midWidth + 100 > mouse[0] > midWidth - 100 and midHeigt + 200 > mouse[1] > midHeigt + 150:
                pygame.draw.rect(self._display, (255, 0, 0), (midWidth - 100, midHeigt + 150, 200, 50))
                if click[0] == 1 and action != None:
                    print('Entering game')
                    intro = False

            else:
                pygame.draw.rect(self._display, (255, 100, 0), (midWidth - 100, midHeigt + 150, 200, 50))

            smallText = pygame.font.Font("freesansbold.ttf", 20)
            textSurf, textRect = self.text_objects("GO!", smallText)
            textRect.center = (midWidth, midHeigt + 75)

            textSurfQuit, textRectQuit = self.text_objects("Quit!", smallText)
            textRectQuit.center = (midWidth, midHeigt + 175)

            self._display.blit(textSurf, textRect)
            self._display.blit(textSurfQuit, textRectQuit)

            pygame.display.update()
            self.clock.tick(15)

        self.on_cleanup()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    # additional action which occurs each loop
    def on_loop(self):
        # colission detection
        # make hitboxes as large as the whole area covered by a move
        permitMove = True
        collideBot = False
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
