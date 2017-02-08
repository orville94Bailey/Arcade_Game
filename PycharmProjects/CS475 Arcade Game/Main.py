#
# Programmer: Michael Cantley
# CS475 @ WVU
# Date last edited: Feb 7, 2017
#
# Arcade Game: Beat Pilot
# Description: A mix of a rhythm game and a top-down shooter akin to Galactica

#imports
import pygame
import sys
from Sprite import Sprite

#set up pyGame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

#set up the screen
screenW = 650
screenH = 850
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("Rhythm Pilot")

#some song variables
interval = 0
songList = ["sound/Song1.wav", "sound/Song2.wav", "sound/Song3.wav"]
isPlaying = True

#play the theme song while on the main menu
themeSong = pygame.mixer.Sound("sound/Theme.wav")
channel1 = themeSong.play()
themeSong.set_volume(.5)
gameStart = False #boolean to check if player has started the game
gameEnd = False #boolean to check if player has reached the win condition

#setup player sprite
spriteList = pygame.sprite.Group()
player = Sprite("sprite/PlayerShip.png", .5 * screenW - 40, .75 * screenH, 80, 80)

#setup other sprites
background = pygame.image.load("sprite/Background.png")

# make object pools of player bullets and enemies
bulletPool = []
enemyPool = []
bulletCounter = 0
enemyCounter = 0
bulletCooldown = 500
for index in range(0, 10):
    spr = Sprite("sprite/EnergyBall1.png", 0, 0, 20, 20)
    spr.destructable = True
    bulletPool.append(spr)
for index in range(0, 20):
    spr = Sprite("sprite/EnergyBall2.png", 0, 0, 50, 50)
    spr.destructable = True
    enemyPool.append(spr)

#menu controls
while gameStart == False:
    for event in pygame.event.get():
        #give player option to quit game before it begins
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()
        #press enter to start the game
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
            gameStart = True
            break
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS):  # volume down
            if channel1.get_volume() > 0:
                channel1.set_volume(channel1.get_volume() - .1)
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS):  # volume up
            if channel1.get_volume() < 1:
                channel1.set_volume(channel1.get_volume() + .1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m: #mute
            if isPlaying:
                isPlaying = False
                channel1.pause()
            else:
                isPlaying = True
                channel1.unpause()
#
#set up the game
#

#set the first song
channel1.stop() #stop the theme song
currentSong = pygame.mixer.Sound(songList[interval])
channel1 = currentSong.play()
currentSong.set_volume(.5)
isPlaying = True

#add appropriate sprites to the list
spriteList.add(player)

#The game!
while gameEnd == False:
    while interval < 4:
        #game controls
        for event in pygame.event.get():
            #give player option to quit the game at any time
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

            #player input checks
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: #move up
                    player.uSpeed = -player.speed
                if event.key == pygame.K_a: #move left
                    player.lSpeed = -player.speed
                if event.key == pygame.K_s: #move down
                    player.dSpeed = player.speed
                if event.key == pygame.K_d: #move right
                    player.rSpeed = player.speed
                if event.key == pygame.K_SPACE: #shoot
                    #create a bullet if able
                    if bulletCooldown >= 50:
                        bulletCounter = bulletCounter + 1
                        if bulletCounter > len(bulletPool) - 1: #if at the end of pool, reset the index
                            bulletCounter = 0
                        bullet = bulletPool[bulletCounter]
                        bullet.speed = 15 # set it's speed and location
                        bullet.uSpeed = -bullet.speed
                        bullet.rect.x = player.rect.centerx
                        bullet.rect.y = player.rect.centery
                        spriteList.add(bullet)
                        bulletCooldown = 0
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: #hyperdrive (movement speed increase)
                    player.uSpeed = player.uSpeed * 2
                    player.lSpeed = player.lSpeed * 2
                    player.dSpeed = player.dSpeed * 2
                    player.rSpeed = player.rSpeed * 2
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS: #volume down
                    if channel1.get_volume() > 0:
                        channel1.set_volume(channel1.get_volume() - .1)
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS: #volume up
                    if channel1.get_volume() < 1:
                        channel1.set_volume(channel1.get_volume() + .1)
                if event.key == pygame.K_m: #mute
                    if isPlaying:
                        isPlaying = False
                        channel1.pause()
                    else:
                        isPlaying = True
                        channel1.unpause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:  # move up
                    player.uSpeed = 0
                if event.key == pygame.K_a:  # move left
                    player.lSpeed = 0
                if event.key == pygame.K_s:  # move down
                    player.dSpeed = 0
                if event.key == pygame.K_d:  # move right
                    player.rSpeed = 0
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # hyperdrive (movement speed increase)
                    player.speed = 5

        bulletCooldown = bulletCooldown + 1

        spritesToModify = spriteList.sprites()

        for sprite in spritesToModify:
            #update positions (using pixel-perfect movement)
            if sprite.rect.bottom < screenH and sprite.rect.top > 0 and sprite.rect.right < screenW and sprite.rect.left > 0:
                sprite.rect.y = sprite.rect.y + sprite.uSpeed + sprite.dSpeed
                sprite.rect.x = sprite.rect.x + sprite.lSpeed + sprite.rSpeed

            #player position adjustments
            while (sprite.rect.bottom >= screenH):
                if sprite.destructable == True:  # if the obj is destructible and it hits a wall, get rid of it
                    spriteList.remove(sprite)
                sprite.rect.y = sprite.rect.y - 1
            while (sprite.rect.top <= 0):
                if sprite.destructable == True:  # if the obj is destructible and it hits a wall, get rid of it
                    spriteList.remove(sprite)
                sprite.rect.y = sprite.rect.y + 1
            while (sprite.rect.right >= screenW):
                if sprite.destructable == True:  # if the obj is destructible and it hits a wall, get rid of it
                    spriteList.remove(sprite)
                sprite.rect.x = sprite.rect.x - 1
            while (sprite.rect.left <= 0):
                if sprite.destructable == True:  # if the obj is destructible and it hits a wall, get rid of it
                    spriteList.remove(sprite)
                sprite.rect.x = sprite.rect.x + 1

        #update screen
        spriteList.update()
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        spriteList.draw(screen)

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)


