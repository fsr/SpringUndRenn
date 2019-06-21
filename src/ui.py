import pygame

""" ----------------------------------------------------------------------------
    Class for displaying buttoms
"""
class Buttom:
    def __init__(self, display, x, y, width, height):
        self._display = display
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._text = ""
        self._font = pygame.font.Font('freesansbold.ttf', 20)
        self._color = (0, 0, 0)
        self._colorHover = (255, 255, 255)
        self._colorBase = (0, 0, 0)

    #.........................................................................
    def setText(self, text):
        self._text = text

    #.........................................................................
    def update(self, mousePos, clickEvent):
        #check if the mouse hovers over the buttom and perfrom an update of
        #the colors
        if (self._x + self._width > mousePos[0] > self._x  and
            self._y + self._height > mousePos[1] > self._y ):
            self._color = self._colorHover
            #if the mouse is clicked while hovering, singal this by returning
            #true
            if clickEvent[0] == 1:
                return True
        else:
            self._color = self._colorBase
        #return false if no clicking was registered
        return False

    #.........................................................................
    # sets the colors for hover animation. First is base color, second is color
    # when hovered
    def setColors(self, baseColor, hoverColor):
        self._colorBase = baseColor
        self._colorHover= hoverColor

    #.........................................................................
    def draw(self):
        #draw the reactagle of the buttom
        pygame.draw.rect(self._display, self._color, (self._x, self._y,
                                                      self._width,
                                                      self._height)
                        )
        #render the buttom text
        textSurf = self._font.render(self._text, True, (0, 0, 0))
        #get the rectangle of the text, which discribes it's position
        textRect = textSurf.get_rect()
        #set the text rectangles position
        textRect.center = (self._x + self._width / 2,
                           self._y + self._height / 2)
        #move the buttom and the text to the right place on the display
        self._display.blit(textSurf, textRect)

""" ----------------------------------------------------------------------------
    Class which displays ar primitve ui
"""
class Ui:
    def __init__(self, display, window):
        self._display = display
        self._window = window
        self._runAction = None
        self._clock = pygame.time.Clock()

    #.........................................................................
    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    #.........................................................................
    def game_intro(self):
        #condition on which the loop will run
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #save values for shorter lines and preventing from recalculating
            midWidth = self._window.width/2
            midHeight = self._window.height/2
            #fill the dsiplay with white
            self._display.fill((255, 255, 255))
            #create some text
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects('Spring und Renn!',
                                                   largeText)
            #move the text to the right place
            TextRect.center = ((midWidth),(midHeight - 100))
            self._display.blit(TextSurf, TextRect)

            #read mouse information
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            #create the exit buttom
            exitButtom = Buttom(self._display, midWidth -100,
                                midHeight + 150, 200, 50)
            exitButtom.setText("Exit!")
            exitButtom.setColors((255, 0, 0), (255, 100, 0))
            # stop the loop which will terminate the menue
            if (exitButtom.update(mouse, click)):
                intro = False
            exitButtom.draw()

            # create the start buttom
            goButtom = Buttom(self._display, midWidth -100, midHeight + 50,
                              200, 50)
            goButtom.setText("Go!")
            goButtom.setColors((0, 255, 128), (0, 255, 180))
            # start the game on click
            if (goButtom.update(mouse, click)):
                self._runAction()
            goButtom.draw()

            #update the screen
            pygame.display.update()
            #wait for 15ms before rerunning the loop
            self._clock.tick(15)

    #.........................................................................
    #sets the action which is performed when the game should be run
    def setRunAction(self, action):
        self._runAction = action
