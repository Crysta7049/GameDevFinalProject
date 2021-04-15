import pygame, math

class coreSprite(pygame.sprite.Sprite):
    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen

        self.image = pygame.Surface((10, 10))
        self.image = self.image.convert_alpha()
        self.masterImage = self.image
        # current angle: imgAngle. Next angle: imgAngle + rotAngle.
        self.imgAngle = 0.0
        self.rotAngle = 0.0

        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.rotCenter = self.rect.center

        # storing vectors as dictionaries because I don't trust myself
        self.velocity = {'mag': 0.0, 'theta': 0.0}
        self.force = {'mag': 0.0, 'theta': 0.0}

        self.Die = 0
        self.Stop = 1 #can still move parallel to boundary
        self.FullStop = 2 #stop entirely at boundary
        self.Bounce = 3
        self.Wrap = 4
        self.Continue = 5

        self.bound = self.Stop

    # Setters: use for initial properties

    def setImage(self, image):
        self.image = image
        self.image = self.image.convert_alpha()
        self.masterImage = self.image

    def setImgAngle(self, angle): 
        self.imgAngle = angle % 2*math.pi

        self.rect = self.rect.move(pos)
        self.__translate()

    def setVelocity(self, angle, speed):
        self.velocity = {'theta': angle, 'mag': speed}

    def setBound(self, bound):
        self.bound = bound

    def setPosition(self, pos):
        self.rect.center = pos
        self.__translate()
        #Control functions: use to move or rotate the sprite

    def addForce(self, angle, power):
        # accumulates forces into a single vector
        # self.force is zeroed each frame
        if power < 0:
            angle = angle + math.pi
            power *= -1
        newForce = {'theta': angle, 'mag': power}
        self.force = self.addVector(self.force, newForce)

    def rotateSprite(self, angle):
        # sums effects of multiple rotations in a single frame
        # rotAngle is zeroed each frame
        self.rotAngle += angle 
        self.rotAngle = self.rotAngle % (2*math.pi)

    # Vector operations: used by control and behavior methods

    def addVector(self, v1, v2):
        #add two vectors using the parallelogram method
        mag1 = v1['mag'] #P
        mag2 = v2['mag'] #Q
        theta = v2['theta'] - v1['theta'] #angle of Q relative to P
        magSquared = abs(mag1**2 + mag2**2 + 2*mag1*mag2*math.cos(theta))
        magSum = math.sqrt(magSquared)
        dirSum = v1['theta'] + math.atan2(mag2*math.sin(theta), (mag1 + mag2*math.cos(theta)))
        return {'mag': magSum, 'theta': dirSum}

    def projectVector(self, vector, direction = None):
        xval = vector['mag']*math.cos(vector['theta'])
        yval = vector['mag']*math.sin(vector['theta'])
        if direction == 'x':
            return xval
        elif direction == 'y':
            return yval
        else:
            return xval, yval

    # Behavior methods: Apply force/rotation, move sprite, check boundary

    def update(self):
        self.__applyForce()
        self.__rotate()
        self.__translate() #boundary checking occurs in here

    def __applyForce(self): #add force vector to velocity
        newVelocity = self.addVector(self.velocity, self.force)
        self.velocity = newVelocity
        self.force['mag'] = 0

    def __rotate(self):
        self.rotCenter = self.rect.center
        self.imgAngle += self.rotAngle
        self.imgAngle = self.imgAngle % (2*math.pi)
        self.image = pygame.transform.rotate(self.masterImage, math.degrees(self.imgAngle*-1))
        self.rect = self.image.get_rect()
        self.rect.center = self.rotCenter
        self.rotAngle = 0

    def __translate(self):
        dx, dy = self.projectVector(self.velocity)
        self.rect = self.rect.move(dx, dy)
        self.boundCheck()
        self.rotCenter = self.rect.center

    def shift(self, x, y):
        self.rect = self.rect.move(x, y)

    def boundCheck(self):
        # Ensure object is not out of bounds
        # If it is, pass distance OoB to boundAction
        boundary = self.screen.get_size()
        boundBreach = [0, 0] #store distance out of bounds
        if self.rect.centerx < 0:
            boundBreach[0] = self.rect.center[0]
        elif self.rect.centerx > boundary[0]:
            boundBreach[0] = self.rect.center[0] - boundary[0]
        if self.rect.centery < 0:
            boundBreach[1] = self.rect.center[1]
        elif self.rect.centery > boundary[1]:
            boundBreach[1] = self.rect.center[1] - boundary[1]
        if boundBreach != [0, 0]:
            self.boundAction(boundBreach)

    def boundAction(self, breach):
        if self.bound == self.Die:
            self.kill()

        elif self.bound == self.Stop:
            #set position to boundary, stop further motion in that direction
            if breach[0]:
                self.rect.centerx -= breach[0]
                self.velocity['mag'] = self.projectVector(self.velocity, 'y')
                self.velocity['theta'] = math.pi/2
            if breach[1]:
                self.rect.centery -= breach[1]
                self.velocity['mag'] = self.projectVector(self.velocity, 'x')
                self.velocity['theta'] = 0

        elif self.bound == self.FullStop:
            #set position to boundary, stop all motion
            self.rect.centerx -= breach[0]
            self.rect.centery -= breach[1]
            self.velocity['mag'] = 0

        elif self.bound == self.Bounce:
            #reflect position and velocity across boundary
            if breach[0]:
                self.rect.centerx -= (2*breach[0])
                self.velocity['theta'] = math.pi - self.velocity['theta']
            if breach[1]:
                self.rect.centery -= (2*breach[1])
                self.velocity['theta'] = self.velocity['theta'] * -1

        elif self.bound == self.Wrap:
            #add/subtract screen width/height, depending on which side it breached
            if breach[0]:
                self.rect.centerx -= (math.copysign(1, breach[0]) * self.screen.get_width())
            if breach[1]:
                self.rect.centery -= (math.copysign(1, breach[1]) * self.screen.get_height())

        #else self.bound = self.Continue
            #ride off into the sunset
        
    def draw(self):
        self.image.draw()

    # Collision methods

    def collide(self, group):
        collisions = pygame.sprite.spritecollide(self, group, False)
        return collisions

    def anyCollide(self, group):
        collision = pygame.sprite.spritecollideany(self, group)
        return collision

    # Spatial methods: use to determine relative position

    def distanceTo(self, point):
        distance = math.hypot(point[0]-self.rect.centerx, point[1] - self.rect.centery)
        return distance

    def angleTo(self, point):
        angle = math.atan2(point[1] - self.rect.centery, point[0]-self.rect.centerx)
        return angle
