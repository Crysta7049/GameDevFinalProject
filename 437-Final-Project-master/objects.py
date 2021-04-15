import pygame
import sprite

playerImage = pygame.image.load('player.png')
dirtImage = pygame.image.load('dirt.png')
grassImage = pygame.image.load('grass.png')

class player(sprite.coreSprite):
    def __init__(self, scene):
        super().__init__(scene)
        image = playerImage.convert()
        self.setImage(image)
        self.setBound(self.Stop)
        self.grappleCooldown = 0
        self.isGrappled = False
        self.FacingRight = True
        self.airTimer = 0

class grapple(sprite.coreSprite):
    def __init__(self, scene):
        super().__init__(scene)
        image = pygame.Surface((5, 5))
        pygame.draw.circle(image, (255,255,255), (2,2), 2)
        self.setImage(image)
        self.setBound(self.Die)


class ground(sprite.coreSprite):
    def __init__(self, terrain, scene):
        super().__init__(scene)

        self.TERRAIN_DIRT = 0
        self.TERRAIN_GRASS = 1
        
        if terrain == self.TERRAIN_DIRT:
            image = dirtImage.convert()
        if terrain == self.TERRAIN_GRASS:
            image = grassImage.convert()

        self.setImage(image)

# sprite groups: player, grapple, ground
