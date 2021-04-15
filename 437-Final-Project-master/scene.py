import pygame, sys

class Scene(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 800), 0, 32)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((146, 244, 255))

        self.groups = []
        self.frameRate = 30

    def groupSprites(self, sprites):
        return pygame.sprite.OrderedUpdates(sprites)

    def addGroup(self, group):
        self.groups.append(group)

    def setFrameRate(self, rate):
        self.frameRate = rate

    def setTitle(self, title):
        pygame.display.set_caption(title)

    def start(self):
        #create initial sprites before starting
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.active = True
        while self.active:
            self.__gameLoop()

    def stop(self):
        self.active = False

    def getMouse(self):
        return pygame.mouse.get_pos()

    def handleEvent(self, event):
        #overwrite
        pass

    def update(self):
        #overwrite
        #use pygame.key.get_pressed here to handle keyboard input
        pass

    def postMoveUpdate(self):
        pass

    def __gameLoop(self):
        self.clock.tick(self.frameRate)
        for event in pygame.event.get():

            #don't assume event handler handles quit event
            if event.type == pygame.QUIT:
                self.stop()
                pygame.quit()
                sys.exit()
            else:
                self.handleEvent(event)

        self.update(self)

        for group in self.groups:
            group.clear(self.screen, self.background)
            group.update()
        self.postMoveUpdate(self)
        for group in self.groups:
            group.draw(self.screen)

        pygame.display.flip()
