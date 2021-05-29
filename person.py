import random
from math import *
import numpy as np
import tkinter as tk

class Person:
    '''Class describing a person that is either suceptible to
    a disease, infected, recovered or dead.
    '''
    

    def __init__(self, master, settings, is_infected = False):
        '''Constructor giving initial direction, speed and status'''
        self.settings = settings
        self.master = master
        self.infected_time = 0
        self.is_dead = False
        area = [self.master.winfo_width(), self.master.winfo_height()]
        # To initiate time taking from the start.
        self.is_immune = False
        self.setState(is_infected)
        # Using angle as direction
        self.angle = 2*pi*random.random()
        self.direction = np.array([cos(self.angle), sin(self.angle)])*self.settings.speed*random.random()
        self.position = np.array([area[0]*random.random(), area[1]*random.random()])
        # Storing the available space
        self.limits = [[0, area[0]],[0, area[1]]]

        self.radius = 10
        

    def getDir(self):
        return self.direction

    def isSick(self):
        return self.is_infected

    def getPos(self):
        return self.position

    def isImmune(self):
        return self.is_immune

    def updateDirection(self):
        self.angle += (-1 + 2*random.random())*(2*pi/10)
        # If it overlaps
        self.angle %= 2*pi
        self.direction[0], self.direction[1] = cos(self.angle), sin(self.angle)
        self.direction *= random.random()*self.settings.speed

    def setState(self, state):
        if state and not self.is_immune:
            self.is_infected = state
        elif not state and not self.is_immune:
            self.is_infected = state
        # Record infected time
        if self.is_infected:
            self.infected_time = 0

    def updateLocation(self):
        if self.is_dead:
            # Stay in place if dead.
            return
        self.position += self.direction
        # Kollar om vi hamnar utanför, gör i så fall om förändringen
        logic_check = [0 if x > limit[0] and x < limit[1] else 1\
            for x, limit in zip(self.position, self.limits)]
        if sum(logic_check) != 0:
            # Send them back twice the distance in the previous direction.
            self.position -= 3*self.direction
            self.angle += pi
        self.updateDirection()

    def updateTime(self):
        if self.is_infected:
            self.infected_time += 1


    def drawPerson(self):
        x0, y0 = self.position[0] - self.radius, self.position[1] - self.radius
        x1, y1 = x0 + 2*self.radius, y0 + 2*self.radius

        if self.is_infected:
            color = 'red'
        elif self.is_dead:
            color = 'grey'
        else:
            color = 'green'
        

        self.master.create_oval(x0, y0, x1, y1, fill = color)

    def inContact(self, otherPerson):
        distVec = self.position - otherPerson.getPos()
        if np.linalg.norm(distVec) < self.radius:
            return True
        return False

    def check_state(self):
        if self.infected_time*self.settings.delay/1000 > self.settings.recovery_time and not self.is_immune:
            # Determine death or recovery
            if self.settings.death_rate > random.random():
                self.setState(False)
                self.is_dead = True
            else:
                self.setState(False)

            self.is_immune = True
            self.infected_time = 0

    def update(self):
        self.updateLocation()
        self.updateTime()
        self.check_state()
        