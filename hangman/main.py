'''
A 30 minutes work for quick hangman for my daughter and let her practice word spelling,
reading and the use of the keyboard. So, expect a messy/quick and dirty code :)
'''

import pygame
import random

pygame.init()

# Screen initialization
display_width = 1000
display_height = 800

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('The hangman')

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (100,255,100)

# Fonts and definitions for the lines
wordfont = pygame.font.SysFont("Comic Sans MS", 60)
gameoverfont = pygame.font.SysFont("Comic Sans MS", 120)
lenght = 40
spacing = 20

# Assets: Images and sounds
image = pygame.image.load('heart.png')
loselife = pygame.mixer.Sound('SHEEPBAA.WAV')
win_sound = pygame.mixer.Sound('CrowdPart2.wav')
lose_sound = pygame.mixer.Sound('CowMoo.wav')


# Game variables 
words =['saludo', 'camara', 'galleta', 'descanso', 'globo', 'persona', 'carlos', 'margarita',
'maria', 'cabeza', 'comida', 'leche', 'tecla', 'animal', 'gato', 'perro', 'osito']
discovered_letters = []
lifes = 5


def draw_word(word, screen):
    start = 40
    end = start + lenght
    pending_letters = 0
    for i, char in enumerate(word):
        
        if i == 0 or i == len(word) - 1:

            screen.blit(wordfont.render(char.upper(), 1, BLACK), (start, 80))
        else:
            if char in discovered_letters:
                screen.blit(wordfont.render(char.upper(), 1, GREEN), (start, 80))
            else: 
                pygame.draw.line(screen, BLACK, (start, 120), (end, 120))
                pending_letters += 1
        start = end + spacing
        end = start + lenght
    
    pygame.display.update()
    return pending_letters

def draw_lifes(screen):
    x = 40
    y = 600
    distance = 100

    start = x
    if lifes >= 0:
        for life in range(lifes):
            gameDisplay.blit(image, (start,y))
            start = start + distance

def draw_gameover(screen, text):
    screen.blit(gameoverfont.render(text, 1, BLACK), (display_width/4, display_height/2))


def main():
    global lifes

    clock = pygame.time.Clock()
    word = random.sample(words,1)[0]
    done = False  # Will be used as a way to exit the main loop (the game runs until this flag changes)
    playing = True # Will be sued to allow user interaction
    pending_letters = 100  # Super high number to start with

    # The main loop finally
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if playing:
                if event.type == pygame.KEYDOWN:
                    #print(event.unicode) 
                    if event.unicode in word:
                        discovered_letters.append(event.unicode)
                    else:
                        lifes = lifes - 1
                        loselife.play()

                if pending_letters == 0:
                    win_sound.play()
                    draw_gameover(gameDisplay, "GANASTE!")
                    #time.sleep(15)
                    playing = False

                if lifes == 0:
                    lose_sound.play()
                    draw_gameover(gameDisplay, "GAME OVER")
                    playing = False

        gameDisplay.fill(WHITE)
        pending_letters = draw_word(word, gameDisplay)
        draw_lifes(gameDisplay)
            
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()