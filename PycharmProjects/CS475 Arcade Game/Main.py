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

#set up pyGame
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((650, 850))
interval = 1
songList = ["sound/Song1.wav", "sound/Song2.wav", "sound/Song3.wav"]
isPlaying = True

#play the theme song while on the main menu
themeSong = pygame.mixer.Sound("sound/Theme.wav")
channel1 = themeSong.play()
gameStart = False
gameEnd = False

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
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
isPlaying = True

#game controls
while gameEnd == False:
    for event in pygame.event.get():
        #give player option to quit the game at any time
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

        #player input checks
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: #move up
                print("u")
            if event.key == pygame.K_a: #move left
                print("l")
            if event.key == pygame.K_s: #move down
                print("d")
            if event.key == pygame.K_d: #move right
                print("r")
            if event.key == pygame.K_SPACE: #shoot
                print("s")
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: #hyperdrive (movement speed increase)
                print("p")
            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS: #volume down
                if channel1.get_volume() > 0:
                    channel1.set_volume(channel1.get_volume() - .1)
            if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS: #volume up
                if channel1.get_volume() < 1:
                    channel1.set_volume(channel1.get_volume() + .1)
            if event.key == pygame.K_m:
                if isPlaying:
                    isPlaying = False
                    channel1.pause()
                else:
                    isPlaying = True
                    channel1.unpause()



