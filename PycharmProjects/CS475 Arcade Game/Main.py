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
import json
from Sprite import Sprite

#grab the data from the song text files (want to front-load this)
f = open('sound/Song1.txt', 'r')
THING = f.read()
parsed_json = json.loads(THING)
f.close()

#set up pyGame
pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()

#set up the screen
screenW = 650
screenH = 850
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("Rhythm Pilot")

#some variables
isHyper = False

#some song variables
interval = 0
songList = ["sound/Song1.mp3", "sound/Song2.mp3", "sound/Song3.mp3"]
isPlaying = True

#play the theme song while on the main menu
pygame.mixer.music.load("sound/Theme.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(.5)
gameStart = False #boolean to check if player has started the game
gameEnd = False #boolean to check if player has reached the win condition

#setup player sprite
spriteList = pygame.sprite.Group()
player = Sprite("sprite/PlayerShip.png", .5 * screenW - 40, .75 * screenH, 80, 80)

#setup enemy sprite
enemy = Sprite("sprite/EnemyShip.png", .5 * screenW - ((screenW)/2), 0, screenW, 250)

#setup other sprites
background = Sprite("sprite/Background.png", 0, 0, screenW, screenH)
menuBackground = Sprite("sprite/MainMenu.png", 0, 0, screenW, screenH)

#fonts
gameFont = pygame.font.Font("font/space.ttf", 40) #cool title font!
insFont = pygame.font.Font("font/space2.ttf", 18) #easier to read font for instructions.
p2Font = pygame.font.Font("font/space2.ttf", 14) #font for further clarification.

titleText = "Rhythm Pilot"
title = gameFont.render(titleText, True, (255, 255, 255))

gameInsP1 = "Use W,A,S,D to move. You can also shoot with SPACE."
gameInsP2 = "You can increase your movement speed with SHIFT."
gameInsP3 = "Use + or - to control volume. M will mute the music."
gameInsP4 = "Press ENTER or RETURN to begin."
gameInsP4p2 = "(Use the first few seconds to get use to the controls)"

ins1 = insFont.render(gameInsP1, True, (255, 255, 255))
ins2 = insFont.render(gameInsP2, True, (255, 255, 255))
ins3 = insFont.render(gameInsP3, True, (255, 255, 255))
ins4 = insFont.render(gameInsP4, True, (255, 255, 255))
ins4p2 = p2Font.render(gameInsP4p2, True, (255, 255, 255))

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
            if pygame.mixer.music.get_volume() > 0:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - .1)
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS):  # volume up
            if pygame.mixer.music.get_volume() < 1:
                pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + .1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m: #mute
            if isPlaying:
                isPlaying = False
                pygame.mixer.music.pause()
            else:
                isPlaying = True
                pygame.mixer.music.unpause()

    # update screen
    screen.fill((0, 0, 0))
    screen.blit(menuBackground.image, menuBackground.rect)
    screen.blit(title, (.5 * screenW - (gameFont.size(titleText)[0] / 2), 10))
    screen.blit(ins1, (.5 * screenW - (insFont.size(gameInsP1)[0] / 2), 50))
    screen.blit(ins2, (.5 * screenW - (insFont.size(gameInsP2)[0] / 2), 50 + gameFont.size(gameInsP1)[1] * .7))
    screen.blit(ins3, (.5 * screenW - (insFont.size(gameInsP3)[0] / 2), 50 + gameFont.size(gameInsP1)[1] * 1.4))
    screen.blit(ins4, (.5 * screenW - (insFont.size(gameInsP4)[0] / 2), screenH - 100))
    screen.blit(ins4p2, (.5 * screenW - (p2Font.size(gameInsP4p2)[0] / 2), screenH - 50))
    # Refresh Screen
    pygame.display.flip()
    clock.tick(60)
#
#set up the game
#

#set the first song
pygame.mixer.music.stop() #stop the theme song
pygame.mixer.music.load(songList[interval])
pygame.mixer.music.play() #no looping
pygame.mixer.music.set_volume(.5)
isPlaying = True

#add appropriate sprites to the list
spriteList.add(player)
spriteList.add(enemy)

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
                    if bulletCooldown >= 30:
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
                    isHyper = True
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS: #volume down
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - .1)
                if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS: #volume up
                    if pygame.mixer.music.get_volume() < 1:
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + .1)
                if event.key == pygame.K_m: #mute
                    if isPlaying:
                        isPlaying = False
                        pygame.mixer.music.pause()
                    else:
                        isPlaying = True
                        pygame.mixer.music.unpause()

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
                    isHyper = False

        bulletCooldown = bulletCooldown + 1

        spritesToModify = spriteList.sprites()

        for sprite in spritesToModify:
            #update positions (using pixel-perfect movement)
            if sprite.rect.bottom < screenH and sprite.rect.top > 0 and sprite.rect.right < screenW and sprite.rect.left > 0:
                if isHyper == False:
                    sprite.rect.y = sprite.rect.y + sprite.uSpeed + sprite.dSpeed
                    sprite.rect.x = sprite.rect.x + sprite.lSpeed + sprite.rSpeed
                else:
                    sprite.rect.y = sprite.rect.y + ((sprite.uSpeed + sprite.dSpeed)*2)
                    sprite.rect.x = sprite.rect.x + ((sprite.lSpeed + sprite.rSpeed)*2)

            #position adjustments
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

        if pygame.mixer.music.get_busy() == False:
            interval = interval + 1

            if interval < 4:
                pygame.mixer.music.load(songList[interval])
                pygame.mixer.music.play()  # no looping
                pygame.mixer.music.set_volume(.5)

        #update screen
        spriteList.update()
        screen.fill((0, 0, 0))
        screen.blit(background.image, background.rect)
        spriteList.draw(screen)

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)


