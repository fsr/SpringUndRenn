import pygame


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

    def setText(self, text):
        self._text = text

    def update(self, mousePos, clickEvent):
        if (self._x + self._width > mousePos[0] > self._x  and
            self._y + self._height > mousePos[1] > self._y ):
            self._color = self._colorHover
            if clickEvent[0] == 1:
                return True
        else:
            self._color = self._colorBase

    def setColors(self, baseColor, hoverColor):
        self._colorBase = baseColor
        self._colorHover= hoverColor

    def draw(self):
        pygame.draw.rect(self._display, self._color, (self._x, self._y, self._width, self._height))
        textSurf = self._font.render(self._text, True, (0, 0, 0))
        textRect = textSurf.get_rect()
        textRect.center = (self._x + self._width / 2, self._y + self._height / 2)
        self._display.blit(textSurf, textRect)


class Ui:
    def __init__(self, display, window):
        self._display = display
        self._window = window
        self._runAction = None
        self.clock = pygame.time.Clock()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            midWidth = self._window.width/2
            midHeight = self._window.height/2
            self._display.fill((255, 255, 255))
            largeText = pygame.font.Font('freesansbold.ttf', 115)
            TextSurf, TextRect = self.text_objects('Spring und Renn!', largeText)
            TextRect.center = ((midWidth),(midHeight - 100))
            self._display.blit(TextSurf, TextRect)

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            exitButtom = Buttom(self._display, midWidth -100, midHeight + 150, 200, 50)
            exitButtom.setText("Exit!")
            exitButtom.setColors((255, 0, 0), (255, 100, 0))
            if (exitButtom.update(mouse, click)):
                intro = False
            exitButtom.draw()

            goButtom = Buttom(self._display, midWidth -100, midHeight + 50, 200, 50)
            goButtom.setText("Go!")
            goButtom.setColors((0, 255, 128), (0, 255, 180))
            if (goButtom.update(mouse, click)):
                self._runAction()
            goButtom.draw()

            pygame.display.update()
            self.clock.tick(15)

    def setRunAction(self, action):
        self._runAction = action
