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
    def __init__(self, path):
        # this dictonary maps object Id to functions. For example a constructor
        self.objectMapping = {
            1: go.Stone,
            2: self.registerSpawn,
            3: self.registerGoal
        }

        self.goal = None
        self.spawn = None

        # don't have to be updated every iteration
        self.passive_gameObjects = pygame.sprite.Group()
        self.leveldata = self.loadFromFile(LEVELDIR + path)
        self.build_static_level()

    #.........................................................................
    #Load all level files line wise which are located in the level folder
    def loadFromFile(self, path):
        leveldata = []
        try:
            #collect all files
            onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
            #read each file
            for file in onlyfiles:
                #try to open the file and catch an execption if thrown
                try:
                    file = open(path + file)
                except Exception as e:
                    print(e)

                #read the file linewise
                level = []
                for line in file:
                    line = list(map(int, line.rstrip().split(' ')))
                    level.append(line)

                #add the new read level to the list of available levels
                leveldata.append(level)
                file.close()
        #catch some exception if any error occures
        except Exception as e:
            print(e)
        #onyl for debuggin
        #print(leveldata)
        #return the array of levels
        return leveldata

    #.........................................................................
    #build level from read file
    def build_static_level(self):
        y_off = 0
        for line in self.leveldata[1]:
            x_off = 0
            for obj in line:
                block = None
                #try to find the obj-ID in the object map and generate a new
                #object
                if(obj in self.objectMapping.keys()):
                    block = self.objectMapping[obj](go.Position(x_off,y_off))
                #if no object can be found just add 'air'
                if block != None:
                    block.load_image()
                    self.passive_gameObjects.add(block)

                x_off = x_off + SQUARESIZE
            y_off = y_off + SQUARESIZE

    #.........................................................................
    #Create and register the spawnpoint
    def registerSpawn(self, position):
        self.spawn = go.Spawn(position)
        return self.spawn

    #.........................................................................
    #create and register the goal
    def registerGoal(self, position):
        self.goal = go.Goal(position)
        return self.goal
