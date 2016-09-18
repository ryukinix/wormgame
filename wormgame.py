#!/usr/bin/env python
# -*- coding: 'utf-8' -*-

import sys, os, time
from random import randint as rand
from keyboard import Keyboard

keyboard = Keyboard()

class Screen:
    width = 50
    height = 20
    fps = 20
    window = [ "+" + (width - 2) *'_' +  "+",
               "|"+ (width- 2)* ' ' +"|",
               "+" + (width - 2)* '_' + "+"]

# fill the window with pipes on the borders
for i in range(Screen.height -3):
    Screen.window.insert(1, Screen.window[1])


# simple food
class Food:
    def __init__ (self, x, y, char='X'):
        self.coord = x, y
        self.char = char
    def new(self):
        self.coord = rand(1, Screen.width -1), rand(1, Screen.height - 1)

class Worm:
    
    moves = {
        'UP':(0, -1), 
        'LEFT':(-1, 0), 
        'DOWN':(0, 1), 
        'RIGHT':(1, 0)
    }
    
    control_keys = {
        'UP':ord('w'), 
        'LEFT':ord('a'), 
        'DOWN':ord('s'), 
        'RIGHT':ord('d')
    }
    
    def __init__(self, x, y, char = 'O'):
        self.x = x + 1
        self.y = y
        self.char = char
        self.cells = [(x + 1, y), (x, y)]
        self.food = Food(rand(1, Screen.width - 1), 
                         rand(1 , Screen.height - 1))
        self.move = (0, 1)


    @property
    def position(self):
        return self.x, self.y

    @property
    def tail(self):
        return self.cells[:-1]

    @property
    def head(self):
        return self.cells[-1]

    @property
    def alive(self):
        return self.head not in self.tail
    
    def draw(self):
        for j in range(Screen.height):
            for i in range(Screen.width):
                if (i, j) in self.cells:
                    sys.stdout.write(self.char)
                elif (i, j) == self.food.coord:
                    sys.stdout.write(self.food.char)
                else:
                    sys.stdout.write(Screen.window[j][i])
            sys.stdout.write('\n')

    def control(self):
        if keyboard.pressed:
            key_pressed = keyboard.key()
            if key_pressed == 27:
                print("I'm sad. Why you closed me? :(")
                quit()
            
            for a, b in [('UP', 'DOWN'), ('DOWN', 'UP'), 
                         ('LEFT', 'RIGHT'), ('RIGHT', 'LEFT')]:
                if (self.control_keys[a] == key_pressed and 
                    self.moves[b] == self.move):
                    return
            
            for direction, key in self.control_keys.items():
                if key_pressed == key:
                    self.move = self.moves[direction]
                    return

    def move_worm(self):
        dx, dy = self.move
        head = self.x, self.y
        lastcoord = head
        x, y = head
        head = x + dx, y + dy
        (self.x, self.y) = self.cells[0] = head
        for i in range(1, len(self.cells)): #body follows the head
            self.cells[i], lastcoord = lastcoord, self.cells[i]

    def screen_colision(self):
        if self.x <= 0:
            self.x = Screen.width
        elif self.x >= Screen.width:
            self.x = 1
        if self.y <= 0:
            self.y = Screen.height
        elif self.y >= Screen.height:
            self.y = 1
    
    def food_colision(self):
        for cell in self.cells:
            if cell == self.food.coord:
                self.cells.append(self.food.coord)
                self.food.new()

def main():
    clear_command = 'clear' if os.name == 'posix' else 'cls'
    
    player = Worm(1, 1)
    while True:
        os.system(clear_command)
        sys.stdout.write("Score: %02d \n" %(len(player.cells) - 2))
        player.control()
        player.move_worm()
        player.screen_colision()
        player.food_colision()
        player.draw()
        time.sleep(1/Screen.fps)
    
    print("You just is dead.")

if __name__ == '__main__':
    main()