import itertools as itt
import sys
from Tag_16_15 import *
from steps import *

import pygame as pg
from pygame.locals import *

#The Taguchi tables are encoded with all the indices decreased by 1 to go from 0 to n-1 (easier to call)

#TODO : return all the possible graphs and display unused aliases

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nodeSize = 20

idGraph = 0
table = table16
graph = [chars[i] for i in range(len(Tgraphs[idGraph]))]
links = []
activeStep = 0
currentSol = 0
solutions = []
selected = None

window = pg.display.set_mode((1280, 720))

def tryPermut(permut) :
    pgraph = list(permut)
    usedInters = Tgraphs[idGraph].copy()
    for link in links :
        interraction = set((Tgraphs[idGraph][pgraph.index(link[0])], Tgraphs[idGraph][pgraph.index(link[1])]))
        interraction = table[min(interraction), max(interraction)]
        if interraction not in usedInters :
            usedInters.append(interraction)
        else :
            break
    else :
        return pgraph

def process() :
    solutions = []
    for permut in itt.permutations(graph, len(graph)) :
        sol = tryPermut(permut)
        if sol is not None :
            solutions.append(sol)
    return solutions

def display() :
    window.fill((100, 100, 100))
    steps[activeStep].display(window)
    
    if steps[activeStep].name == 'step0' :
        Tgraph = pg.image.load(f'Tgraph_{idGraph}.png')
        window.blit(Tgraph, (390, 50))
    
    if steps[activeStep].name == 'step1' :

        #Drawing links
        for link in links :
            np = nodePos[idGraph]
            start = np[graph.index(link[0])]
            start = (start[0]+10, start[1]+10)
            end = np[graph.index(link[1])]
            end = (end[0]+10, end[1]+10)
            pg.draw.line(window, (0, 0, 0), start, end)

        #Drawing nodes
        for i in range(len(nodePos[idGraph])) :
            node = nodePos[idGraph][i]
            if selected == i :
                rect = pg.Rect((node[0]-2, node[1]-2), (24, 24))
                pg.draw.rect(window, (180, 0, 0), rect)
            rect = pg.Rect(node, (20, 20))
            pg.draw.rect(window, (180, 180, 180), rect)

            text = font.render(graph[i], True, (0, 0, 0))
            window.blit(text, (node[0]+(20-text.get_width())//2, node[1]+(20-text.get_height())//2))
    
    if steps[activeStep].name == 'step2' :

        sol = solutions[currentSol]

        #Drawing links
        for link in links :
            np = nodePos[idGraph]
            start = np[sol.index(link[0])]
            start = (start[0]+10, start[1]+10)
            end = np[sol.index(link[1])]
            end = (end[0]+10, end[1]+10)
            pg.draw.line(window, (0, 0, 0), start, end)

        #Drawing nodes
        for i in range(len(nodePos[idGraph])) :
            node = nodePos[idGraph][i]
            if selected == i :
                rect = pg.Rect((node[0]-2, node[1]-2), (24, 24))
                pg.draw.rect(window, (180, 0, 0), rect)
            rect = pg.Rect(node, (20, 20))
            pg.draw.rect(window, (180, 180, 180), rect)

            text = font.render(sol[i], True, (0, 0, 0))
            window.blit(text, (node[0]+(20-text.get_width())//2, node[1]+(20-text.get_height())//2))
        
        text = font.render(f'{currentSol+1}/{len(solutions)}', True, (0, 0, 0))
        window.blit(text, ((1280-text.get_width())//2, 680))

    pg.display.flip()
    


while True :
    for event in pg.event.get() :
        if event.type == QUIT :
            pg.quit()
            sys.exit()
        
        elif event.type == MOUSEBUTTONDOWN and event.button == 1 :
            x, y = event.pos
            action = steps[activeStep].click(x ,y)

            if action == 'nextStep' and activeStep != len(steps)-1 :
                activeStep += 1
            elif action == 'prevStep' and activeStep != 0 :
                activeStep -= 1

            elif action == 'nextgraphtype' :
                idGraph = (idGraph+1)%7
                #Changing the graph size :
                graph = [chars[i] for i in range(len(Tgraphs[idGraph]))]
                #Just keeping the table type up to date :
                if idGraph == 0 :
                    table = table8
                else :
                    table = table16

            elif action == 'process' :
                solutions = process()
                if len(solutions) == 0 :
                    print('No solution')
                else :
                    activeStep += 1
                    # print('Solutions for this graph :')
                    # for sol in solutions :
                    #     print(sol)
            
            elif action == 'prevSol' :
                currentSol = (currentSol-1)%len(solutions)
            elif action == 'nextSol' :
                currentSol = (currentSol+1)%len(solutions)

            else :
                for i in range(len(nodePos[idGraph])) :
                    nx, ny = nodePos[idGraph][i]
                    if nx <= x <= nx+20 and ny <= y <= ny+20 :
                        if selected is None :
                            selected = i
                        else :
                            if selected != i :
                                link = graph[selected]+graph[i]
                                rev_link = graph[i]+graph[selected]
                                if link in links :
                                    links.remove(link)
                                elif rev_link in links :
                                    links.remove(rev_link)
                                else :
                                    links.append(link)
                            selected = None
    if steps[activeStep].name == 'step0' :
        selected = None
        links = []
    
    if steps[activeStep].name != 'step2' :
        currentSol = 0
            
    display()