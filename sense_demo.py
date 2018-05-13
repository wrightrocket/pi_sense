#!/usr/bin/env python3
''' WrightRocket Slug for Raspberry Pi
    By Keith Wright
    Created May 11, 2018
    
    This project requires the Raspberry Pi Sense Hat available from the
    same distribution channels as the Pi.

'''
from string import ascii_letters
from time import sleep
import random

from sense_hat import SenseHat

VERBOSE=True
PIX_MIN = 0 
PIX_MAX = 7
COLOR_FACTOR = 2

words = ('Keith', 'Wright', 'WrightRocket', 'cool', 'awesome', 'radical', 'sweet', 
        'nice', 'great', 'beautiful', 'wow', 'amazing', 'incredible')

pink = (255,127,127)
red = (255,0,0)
orange = (255,127,0)
yellow = (255,255,0)
green = (0,255,0)
white = (255,255,255)
purple = (0,255,255)
blue = (0,0,255)
aqua = (127,127,255)

def color():
    def c():
        return random.randint(0,255)
    return (c(), c(), c())

def pixel():
    def x():
        return random.randint(PIX_MIN, PIX_MAX)
    return x(), x(), color()

def square():
    colors = [white, pink, red, orange, yellow, green, purple, blue, aqua]
    colors_len = len(colors)
    square_loops = colors_len * COLOR_FACTOR
    for loop in range(square_loops):
        count = 0
        for pixels in range(8, 3, -1):
            c = colors[pixels]
            squares = []
            squares.extend([(x+count,7-pixels+1) for x in range(pixels-count)]) # right
            squares.extend([(pixels-1, y+count) for y in range(pixels-count)]) # top
            left = [(x+count,pixels-1) for x in range(pixels-count)] # left
            left.reverse()
            squares.extend(left) # left
            bottom = [(count, y+count) for y in range(pixels-count)] # bottom
            bottom.reverse()
            squares.extend(bottom) # bottom
            count += 1
            if VERBOSE: print('squares moving in:\n', squares)
            for pix in squares:
                sleep(0.02)
                sense.set_pixel(*pix, c)
        sleep(0.52)
        count -= 1
        for pixels in range(4, 9):
            squares = []
            left = [(count, y+count) for y in range(pixels-count)] # left
            squares.extend(left)
            bottom = [(x+count,pixels-1) for x in range(pixels-count)] # bottom
            squares.extend(bottom)
            right = [(pixels-1, y+count) for y in range(pixels-count)] # right
            right.reverse()
            squares.extend(right) 
            top = [(x+count,7-pixels+1) for x in range(pixels-count)] # top
            top.reverse()
            squares.extend(top) 
            if VERBOSE: print('squares moving out:\n', squares)
            count -= 1
            for pix in squares:
                sleep(0.02)
                sense.set_pixel(*pix, colors[count+2])
        sleep(0.52)
        if VERBOSE: print('colors last:\n', colors)
        if loop < colors_len:
            random.shuffle(colors)
        else:
            colors = [color() for tint in range(colors_len)]
        if VERBOSE: print('colors random:\n', colors)
def pixie():
    sense.clear()
    for p in range(500):
        sense.set_pixel(*pixel())
        sleep(0.01)

def get_letter():
    return random.choice(ascii_letters)

def letter():
    sense.clear()
    sense.show_letter (get_letter(), color(), color())

def message(msg=None, delay=0.09, fore_color=None, back_color=None):
    if not msg:
        msg = random.choice(words)
    if not fore_color:
        fore_color = color()
    if not back_color:
        back_color = color()
    try:
        delay = float(delay)
    except:
        delay = 0.09
    if delay < 0.01:
        delay = 0.01
    sense.show_message (msg, delay, fore_color, back_color)

    
def thing(event):
  print(event)
  if event.action == 'pressed':
      # print('You pressed me')
      if event.direction == 'up':
        #  print('Up', 'X')
          letter()
      elif event.direction == 'down':
        #  print('Down')
          square()
      elif event.direction == 'right':
          pixie()
      elif event.direction == 'left':
          message()
  elif event.action == 'released':
      pass
  elif event.action == 'held':
      exit()
      # print('You released me')

sense=SenseHat()
sense.clear()
sense.stick.direction_any = thing
#sense.stick.direction_down = pixie
#pixie()

def demo():
    random.seed()
    while True:
        message('Hold Raspberry Pi Sense Hat joybstick button to exit')
        fun = random.choice((square, message, letter, pixie, square))
        fun()
        #square()
        sleep(1)
demo()

