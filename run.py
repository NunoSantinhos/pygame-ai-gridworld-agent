import json
import statistics as st
import os
import random
import pygame
from pygame.locals import *
from Neuralnetwork import *
from Matrix import Matrix
from genetic_algorithm import NUM_OF_GENERATIONS, create_inital_genes, generate_next_generation
import pickle
import time
lista_pop=[]
new_popp = []
layer_nodes = (4,6,4)

NUM_OF_GENES = 1500  # -> Population
NUM_OF_GENERATIONS = 50  # -> Number of generations


auto_running = True


avg_fitness_score_list = []
avg_garbage_left_list = []

genes = create_inital_genes()
print(type(genes))
print(type(genes[0]))
print(genes[0])
print("stop")

conta = -1
for generation in range(NUM_OF_GENERATIONS):
    print('Generation: ', generation, 'started')
    end_game = False
    # print("ola",len(genes))
    conta +=1
    print("geração", conta)
    for gene in genes:

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


        garbage_positions = [(random.randint(0, 4), random.randint(0, 4)) for _ in range(8)]
        m.spwanGarbage(garbage_positions)

        isLeftClicked = False
        isRightClicked = False
        isUpClicked = False
        isDownClicked = False



        for il in range(gene.moves):

            inputs = m.getadjancentes()
            #print(inputs)
            move = gene._dna.feed_forward(inputs)
            print(move)
            print(il)
            #time.sleep(1)
            screen_text = pygame.font.SysFont(pygame.font.get_default_font(), 24).render(
                f'Garbage left: {m.get_left_garbage()}', True, (0, 0, 0), (255, 255, 255))
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE] or pygame.event.peek(QUIT):
                break

            events = pygame.event.get()
            if auto_running:
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
                    gene.catch_garbage()
                    m.decrement_left_garbage()
                    if m.get_left_garbage() == 0:
                        print('You win!')
                        pygame.quit()
                        end_game = True
                        break

                else:
                    gene.bad_move()





            else:
                for event in events:
                    prev_value = None
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and not isLeftClicked:
                            prev_value = m.fillIronMatrix(m.yIron, m.xIron - 1)
                            # print(m.yIron, m.xIron)
                            isLeftClicked = True
                        if event.key == pygame.K_RIGHT and not isRightClicked:
                            prev_value = m.fillIronMatrix(m.yIron, m.xIron + 1)
                            isRightClicked = True
                        if event.key == pygame.K_UP and not isUpClicked:
                            prev_value = m.fillIronMatrix(m.yIron - 1, m.xIron)
                            isUpClicked = True
                        if event.key == pygame.K_DOWN and not isDownClicked:
                            prev_value = m.fillIronMatrix(m.yIron + 1, m.xIron)
                            isDownClicked = True

                        # verify if pass on top of garbage
                        if prev_value == 'garbage':
                            m.decrement_left_garbage()
                            if m.get_left_garbage() == 0:
                                print('You win!')
                                print()
                                pygame.quit()
                                exit(0)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT and isLeftClicked:
                            isLeftClicked = False
                        if event.key == pygame.K_RIGHT and isRightClicked:
                            isRightClicked = False
                        if event.key == pygame.K_UP and isUpClicked:
                            isUpClicked = False
                        if event.key == pygame.K_DOWN and isDownClicked:
                            isDownClicked = False

            m.drawMatrix(boardGame, _image_iron_man, _image_garbage, iconSize)
            screen.blit(boardGame, (200, 0))
            screen.blit(screen_text, (5, 5))

            pygame.display.flip()


        # if ends with garbage left, then penalize
        if m.get_left_garbage() > 0:
            gene.set_fitness_score(gene.get_fitness_score() - (2 * m.get_left_garbage()))  # tira 2
        gene.set_left_garbage(m.get_left_garbage())

        print('Score: ', gene.get_fitness_score())
        #print(gene)


    average_fitness_score = st.mean([gene.get_fitness_score() for gene in genes])
    #print('Average fitness score: ', average_fitness_score)
    avg_fitness_score_list.append(average_fitness_score)
    #print('Avarage garbage left: ', st.mean([gene.get_left_garbage() for gene in genes]))
    avg_garbage_left_list.append(st.mean([gene.get_left_garbage() for gene in genes]))
    #print('Max fitness score: ', max([gene.get_fitness_score() for gene in genes]))
    #print(genes)

    genes = generate_next_generation(genes)


    print('-' * 20)



save = {
    "last_generation_dna": [gene.get_dna() for gene in genes],
    "avg_fitness_score": avg_fitness_score_list,
    "avg_garbage_left": avg_garbage_left_list,
}

# Define the directory path
results_dir = r'C:/Users/franc/Desktop/Francisco/2ºano/AI/projeto_iron/results/'

# Create the directory if it does not exist
os.makedirs(results_dir, exist_ok=True)

# Save the data using pickle
pickle_file_path = os.path.join(results_dir, 'gen1.pk')
with open(pickle_file_path, 'wb') as pickle_file:
    pickle.dump(save, pickle_file)

# Save the data using JSON with custom encoder
json_file_path = os.path.join(results_dir, 'generation_1.json')
with open(json_file_path, 'w') as json_file:
    json.dump(save, json_file, cls=CustomEncoder)



    ##graficos
    #lina(x- numero gera, y- score)
    #lina(lina(x- numero gera, y- nºlixo)
    #tabela dos pesos e bias melhor
    #ver melhor jogo novo run
    ##numero bad moves