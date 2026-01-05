import json
import time

import pygame
from pygame.locals import *

from Matrix import Matrix

auto_running = True

avg_fitness_score_list = []
avg_garbage_left_list = []

with open(r'C:/Users/franc/Desktop/Francisco/2ºano/AI/projeto_iron/results/generation_1.json') as json_file:
    last_generation = json.load(json_file)

end_game = False
for gene in last_generation['last_generation_dna']:
    # print('Gene size: ', len(gene.get_dna()))
    iconSize = (100, 100)  # (y, x)
    totalWidthAndHeight = 5
    windowWidth = iconSize[0] * totalWidthAndHeight
    windowHeight = iconSize[0] * totalWidthAndHeight

    pygame.init()
    screen = pygame.display.set_mode((windowWidth + 200, windowHeight), pygame.HWSURFACE)
    screen.fill((255, 255, 255))
    boardGame = pygame.Surface((windowWidth, windowHeight))
    screen_text = pygame.Surface((200, windowWidth))
    screen_text.fill((255, 255, 255))

    pygame.display.set_caption('Iron Garbage')

    _image_iron_man = pygame.image.load("/Users/franc/Desktop/Francisco/2ºano/AI/projeto_iron/textures/iron-man.png").convert_alpha()
    _image_iron_man = pygame.transform.scale(_image_iron_man, (iconSize[0], iconSize[1]))

    _image_garbage = pygame.image.load("/Users/franc/Desktop/Francisco/2ºano/AI/projeto_iron/textures/garbage.jpg").convert_alpha()
    _image_garbage = pygame.transform.scale(_image_garbage, (iconSize[0], iconSize[1]))

    m = Matrix(windowHeight, windowWidth, iconSize)
    m.fillIronMatrix(0, 0)

    totalSquares = totalWidthAndHeight * totalWidthAndHeight

    # garbagePercentage = int(0.3 * totalSquares)
    # m.spwanGarbageRandom(garbagePercentage)

    # Had to fix the garbage for genetic algorithms
    garbage_positions = [(0, 3), (1, 1), (1, 4), (2, 2), (3, 1), (3, 3), (4, 4)]
    m.spwanGarbage(garbage_positions)

    while True:

        for move in gene:
            # print(move)
            time.sleep(2)
            screen_text = pygame.font.SysFont(pygame.font.get_default_font(), 24).render(
                f'Garbage left: {m.get_left_garbage()}', True, (0, 0, 0), (255, 255, 255))
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE] or pygame.event.peek(QUIT):
                break

            prev_value = None

            if move == 'left':
                prev_value = m.fillIronMatrix(m.yIron, m.xIron - 1)
            if move == 'right':
                prev_value = m.fillIronMatrix(m.yIron, m.xIron + 1)
            if move == 'up':
                prev_value = m.fillIronMatrix(m.yIron - 1, m.xIron)
            if move == 'down':
                prev_value = m.fillIronMatrix(m.yIron + 1, m.xIron)

            # verify if pass on top of garbage
            if prev_value == 'garbage':
                m.decrement_left_garbage()
                if m.get_left_garbage() == 0:
                    # print('You win!')
                    pygame.quit()
                    end_game = True
                    break

            m.drawMatrix(boardGame, _image_iron_man, _image_garbage, iconSize)
            screen.blit(boardGame, (200, 0))
            screen.blit(screen_text, (5, 5))

            pygame.display.flip()

        if end_game:
            break
