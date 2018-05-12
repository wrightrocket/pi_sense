''' WrightRocket Slug for Raspberry Pi
    By Keith Wright
    Created May 11, 2018
    
    This project requires the Raspberry Pi Sense Hat available from the
    same distribution channels as the Pi.

'''
from sense_hat import SenseHat
from time import sleep
import random
import string

words = ('keith', 'wright', 'wrightrocket', 'cool', 'awesome', 'radical', 'sweet', 'nice', 'great', 'beautiful', 'wow', 'amazing', 'incredible')

def color():
    def c():
        return random.randint(0,255)
    return (c(), c(), c())

def pixel():
    def x():
        return random.randint(0,7)
    return x(), x(), color()

def square():
    sense.clear()
##    sleep(1)
##    blue=(0,0,255)
##    red=(255,0,0)
##    green=(0,255,0)
##    white=(255,255,255)
    
    #for pixels in range(random.randint(1,7)):
    count = 0
    for pixels in range(8, -1, -1):
        c = color()  
        squares = []
        squares.extend([(x+count,pixels-1) for x in range(pixels-count)]) # bottom
        squares.extend([(x+count,7-pixels+1) for x in range(pixels-count)]) # top
        squares.extend([(pixels-1, y+count) for y in range(pixels-count)]) # right
        squares.extend([(count, y+count) for y in range(pixels-count)]) # 
        count += 1
        for pix in squares[::-1]:
            sleep(0.02)
            sense.set_pixel(*pix, c)


def pixie():
    sense.clear()
    for p in range(500):
        #xyc = pixel()
        sense.set_pixel(*pixel())
        sleep(0.01)

def get_letter():
    return random.choice(string.ascii_letters)

def letter():
    sense.clear()
    sense.show_letter (get_letter(), color(), color())

def message():
    sense.clear()
    sense.show_message (random.choice(words),
                              0.05, color(), color())

    
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
      pass
      # print('You released me')

sense=SenseHat()
sense.clear()
#sense.stick.direction_any = thing
#sense.stick.direction_down = pixie
#pixie()

def demo():
    while True:
        fun = random.choice((message, letter, pixie, square))
        fun()
        #square()
        sleep(1)
demo()

