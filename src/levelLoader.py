import os
import sys
import pygame

from os.path import isfile, join

import gameObject as go

LEVELDIR = "../levels/"
SQUARESIZE = 20



""" ----------------------------------------------------------------------------
    Class for storing level information
"""
class Level:
    objectMapping = {
        1: go.Stone,
        2: go.Spawn,
        3: go.Goal
    }

    def __init__(self, path):
        # this dictonary maps object Id to functions. For example a constructor



        self.goal = None
        self.spawn = None

        # don't have to be updated every iteration
        self.passive_gameObjects = pygame.sprite.Group()
        self.leveldata = self.loadFromFile(LEVELDIR + path)
        self.build_static_level()

    def loadFromFile(self, path):
        leveldata = []
        try:
            onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
            for file in onlyfiles:
                try:
                    file = open(path + file)
                except Exception as e:
                    print(e)

                level = []
                for line in file:
                    line = list(map(int, line.rstrip().split(' ')))
                    level.append(line)

                leveldata.append(level)
                file.close()

        except Exception as e:
            print(e)
        print(leveldata)
        return leveldata

    #build level from read file
    def build_static_level(self):
        y_off = 0
        for line in self.leveldata[1]:
            x_off = 0
            for obj in line:
                block = None

                if(obj in self.objectMapping.keys()):
                    block = self.objectMapping[obj](go.Position(x_off,y_off))

                if block != None:
                    block.load_image()
                    self.passive_gameObjects.add(block)

                x_off = x_off + SQUARESIZE
            y_off = y_off + SQUARESIZE
