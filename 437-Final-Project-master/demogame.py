import pygame, random, math, sys
import scene, sprite

class playerSprite(sprite.coreSprite):
    def __init__(self, scene):
        super().__init__(scene)
        image = pygame.Surface((25, 25))
        pygame.draw.polygon(image, (255,255,255, 0), ((0,0),(5,12),(0,24),(24,12)))
        self.setImage(image)
        self.setBound(self.Stop)
        self.cooldown = 0

class bulletSprite(sprite.coreSprite):
    def __init__(self, scene):
        super().__init__(scene)
        image = pygame.Surface((5, 5))
        pygame.draw.circle(image, (255,255,255), (2,2), 2)
        self.setImage(image)
        self.setBound(self.Die)

class enemySprite(sprite.coreSprite):
    def __init__(self, scene, enemyType):
        super().__init__(scene)
        self.colors = ((0,255,0),(0,0,255),(255,0,255),(255,0,0))
        self.bounds = (self.Wrap, self.Bounce, self.Continue, self.FullStop)
        self.type = enemyType
        
        image = pygame.Surface((25, 25))
        pygame.draw.circle(image, self.colors[self.type], (12,12), 12)
        self.setImage(image)
        self.setBound(self.bounds[self.type])

def gameUpdate(self):
    keys = pygame.key.get_pressed()
    for player in self.groups[0]:
        player.addForce(player.velocity['theta'], (player.velocity['mag']/-20))
        if player.anyCollide(self.groups[2]):
            player.kill()
            self.stop()
        if keys[pygame.K_w]:
            player.addForce(player.imgAngle, 1)
        if keys[pygame.K_s]:
            player.addForce(player.imgAngle, -1)
        if keys[pygame.K_a]:
            player.rotateSprite(-0.1)
        if keys[pygame.K_d]:
            player.rotateSprite(0.1)
        if player.cooldown:
            player.cooldown -= 1
        if keys[pygame.K_SPACE] and not player.cooldown:
            newShot = bulletSprite(demoScene)
            newShot.setPosition(player.rect.center)
            newShot.setVelocity(player.imgAngle, 25)
            self.groups[1].add(newShot)
            player.cooldown = 10
    
    collisions = pygame.sprite.groupcollide(self.groups[1], self.groups[2], True, True)
    for sprite in self.groups[2]:
        if sprite.type == 2:
            sprite.addForce(sprite.angleTo(player.rect.center), 0.1)
        if sprite.type == 3:
            sprite.addForce(sprite.angleTo(player.rect.center), (sprite.distanceTo(player.rect.center)-320) *0.005)
    self.counter = (self.counter+1) % (2*self.frameRate)
    if not self.counter:
        enemyType = random.choices([0,1,2,3], weights=(3,3,3,1))
        newEnemy = enemySprite(self, enemyType[0])
        border = random.choice(('left', 'right', 'top', 'bottom'))
        if border == 'left':
            newEnemy.setPosition((0, random.random() * self.screen.get_height()))
            newEnemy.setVelocity((random.random() * math.pi) - math.pi/2, 2)
        if border == 'right':
            newEnemy.setPosition((self.screen.get_width()-1, random.random() * self.screen.get_height()))
            newEnemy.setVelocity((random.random() * math.pi) + math.pi/2, 2)
        if border == 'top':
            newEnemy.setPosition((random.random() * self.screen.get_width(), 0))
            newEnemy.setVelocity((random.random() * math.pi), 2)
        if border == 'bottom':
            newEnemy.setPosition((random.random() * self.screen.get_width(), self.screen.get_height()))
            newEnemy.setVelocity((random.random() * math.pi) + math.pi, 2)
        self.groups[2].add(newEnemy)


demoScene = scene.Scene()
demoScene.counter = 0
demoScene.update = gameUpdate
demoScene.setTitle("Game Engine Demo")
player = playerSprite(demoScene)
player.setPosition((demoScene.screen.get_width()*0.5, demoScene.screen.get_height()*0.5))
playerGroup = demoScene.groupSprites(player)
bulletGroup = demoScene.groupSprites([])
enemyGroup = demoScene.groupSprites([])
demoScene.addGroup(playerGroup)
demoScene.addGroup(bulletGroup)
demoScene.addGroup(enemyGroup)
demoScene.start()
