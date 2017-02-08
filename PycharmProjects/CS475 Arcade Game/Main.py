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

speed = 5 #player speed
xSpeed = 0
ySpeed = 0

#setup other sprites
background = Sprite("sprite/GameBackground.jpg", 0, 0, screenW, screenH)

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
spriteList.add(background)
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
                    ySpeed = -speed
                if event.key == pygame.K_a: #move left
                    xSpeed = -speed
                if event.key == pygame.K_s: #move down
                    ySpeed = speed
                if event.key == pygame.K_d: #move right
                    xSpeed = speed
                if event.key == pygame.K_SPACE: #shoot
                    print("sd")
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: #hyperdrive (movement speed increase)
                    speed = speed * 2
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
                    ySpeed = 0
                if event.key == pygame.K_a:  # move left
                    xSpeed = 0
                if event.key == pygame.K_s:  # move down
                    ySpeed = 0
                if event.key == pygame.K_d:  # move right
                    xSpeed = 0
                if event.key == pygame.K_SPACE:  # shoot
                    print("su")
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:  # hyperdrive (movement speed increase)
                    speed = 5

        #update positions (using pixel-perfect movement)
        if player.rect.bottom < screenH and player.rect.top > 0:
            player.rect.y = player.rect.y + ySpeed
        if player.rect.right < screenW and player.rect.left > 0:
            player.rect.x = player.rect.x + xSpeed

        #player position adjustments
        while (player.rect.bottom >= screenH):
            player.rect.y = player.rect.y - 1
        while (player.rect.top <= 0):
            player.rect.y = player.rect.y + 1
        while (player.rect.right >= screenW):
            player.rect.x = player.rect.x - 1
        while (player.rect.left <= 0):
            player.rect.x = player.rect.x + 1

        #update screen
        spriteList.update()

        screen.fill((0, 0, 0))
        spriteList.draw(screen)

        # Refresh Screen
        pygame.display.flip()
        clock.tick(60)


