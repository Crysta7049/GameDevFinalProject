import pygame, math, sys
import scene, sprite, objects

gameScene = scene.Scene()
TILE_SIZE = objects.grassImage.get_width()
GRAVITY = 0.5
JUMP_FORCE = 5
MOVE_FORCE = 1

game_map =[[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,2,2,2],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,2,2,1,1,1],
            [0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1,1,1],
            [0,0,0,0,0,2,2,1,1,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,2,2,0,0,0,0,1,1,1],
            [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,2,2,2,0,0,0,0,2,2,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,2,2,2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,2,2,1,1,1,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [2,2,2,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,1,1,1,0,0,0,0,0,0,2,2,2,2,2,2,2,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,1,1,1],
            [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [1,1,1,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,1,1,1],
            [0,0,0,0,2,2,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,2,2,1,1,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,1,1,1],
            [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,1,1,1],
            [0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,1,1,1],
            [2,2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,1,1,2,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,2,2,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
            [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,2,0,0,0,0,1,1,1,0,0,0,0,1,1,1,2,0,0,0,0,0,0,0,0,0,1,1,1],
            [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,2,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1],
            [1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,2,2,2,2,1,1,1,2,2,2,1,1,1,1,1,2,2,2,2,2,2,2,2,2,1,1,1]]

def gameUpdate(self):
    keys = pygame.key.get_pressed()
    # player is in group 0, and should be the only sprite in that group
    if not player.isGrappled:
        if keys[pygame.K_w] and player.airTimer < JUMP_FORCE:
            player.addForce(-0.5*math.pi, JUMP_FORCE - player.airTimer)
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            player.addForce(math.pi, MOVE_FORCE)
            player.facingRight = False
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            player.addForce(0, MOVE_FORCE)
            player.facingRight = True
    if player.airTimer:
        player.addForce(0.5*math.pi, GRAVITY)
    player.addForce(math.pi, 0.1*player.projectVector(player.velocity, 'x'))

    '''    for grapple in self.groups[1]:
        if player.airTimer:
            nextVel = player.addVector(player.force, player.velocity)
            relAngle = nextVel['theta'] - grapple.angleTo(player)
            if player.isGrappled and math.sin(relAngle) < 0:
                player.addForce(player.angleTo(grapple), nextVel['mag']*math.sin(relAngle))'''

def gameCollision(self):
    playerCollisions = player.collide(self.groups[2]) #group 2 is solid blocks
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    movement = player.projectVector(player.velocity)
    for block in playerCollisions:
        #check angle between centers of player and block
        #shift range to more easily divide into quarters
        theta = (player.angleTo(block.rect.center) + math.pi/4) % (2*math.pi)
        if not theta:
            theta = 2*math.pi
        if not collision_types['bottom'] and math.pi/2 <= theta <= math.pi:
            #player is above block
            collision_types['bottom'] = True
            player.rect.bottom = block.rect.top
            #cancel existing vertical velocity
            player.addForce(-.5*math.pi, movement[1])
            movement = (movement[0], 0)

        elif not collision_types['top'] and 3*math.pi/2 <= theta:
            #player is below block
            collision_types['top'] = True
            player.rect.top = block.rect.bottom
            player.addForce(-.5*math.pi, movement[1])
            movement = (movement[0], 0)

        elif not collision_types['right'] and 0 < theta < math.pi/2:
            #player is left of block
            collision_types['right'] = True
            player.rect.right = block.rect.left
            player.addForce(math.pi, movement[0])
            movement = (0, movement[1])

        elif not collision_types['left'] and math.pi < theta < 3*math.pi/2:
            #player is right of block
            collision_types['left'] = True
            player.rect.left = block.rect.right
            player.addForce(math.pi, movement[0])
            movement = (0, movement[1])
            
    if collision_types['bottom']:
        player.airTimer = 0
    else:
        player.airTimer += 1


gameScene.update = gameUpdate
gameScene.postMoveUpdate = gameCollision
player = objects.player(gameScene)
player.setPosition((50, 700))
playerGroup = gameScene.groupSprites(player)
grappleGroup = gameScene.groupSprites([])
blockGroup = gameScene.groupSprites([])
y = 0
for i in game_map:
    x = 0
    for j in i:
        
        if j:
            terrain = j - 1
            block = objects.ground(terrain, gameScene)
            block.setPosition((x*TILE_SIZE, y*TILE_SIZE))
            blockGroup.add(block)
        x += 1
    y += 1

gameScene.addGroup(playerGroup)
gameScene.addGroup(grappleGroup)
gameScene.addGroup(blockGroup)

gameScene.start()











        
