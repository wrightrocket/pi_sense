''' WrightRocket Slug for Raspberry Pi
    By Keith Wright
    Created May 11, 2018
    
    This project requires the Raspberry Pi Sense Hat available from the
    same distribution channels as the Pi.

    This project is an based upon some of the concepts from
    https://projects.raspberrypi.org/en/projects/slug.
    
'''
from sense_hat import SenseHat
from time import sleep
import random

UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'
STOP = 'stop'
PRESS = 'pressed'
HELD = 'held'

MSG_END = 'Game Over :D'
MSG_START = 'Go!'
MSG_SCORE = 'Score:'
MSG_VEGIES = '!!!'
MSG_LIVES = 'Only'
MSG_LIFE = 'LAST LIFE LEFT...'
MSG_LEFT = 'lives left...'
MSG_WIN = 'Leveling up...'
MSG_RAT = 'Rats!!!'
MSG_SPEED = 0.05

FRUIT_DELAY = 0.1    
DELAY = 1.0
WHITE = (255,255,255)
BLACK = (0,0,0) 
RED = (255,0,0)
YELLOW = (255, 255, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CHANCE = 5
WINNER = random.randint(1, CHANCE)
PIXMAX = 7
PIXMIN = 0
FRUITMAX = 2
VEGMAX = 4
RATMAX = 2
LIVES = 3
VERBOSE = False

def coord(z):
    if z < PIXMIN:
        return PIXMAX
    elif z > PIXMAX:
         return PIXMIN
    else:
        return z

def pixel():
    return (random.randint(PIXMIN,PIXMAX), random.randint(PIXMIN,PIXMAX))

class Slug():
    ''' Class Objects '''
    
    def left(self):
        x = coord(self.slug[-1][0] - 1)
        self.slug.append((x, self.slug[-1][1]))
        if VERBOSE: print('left slug', self.slug)

    def right(self):
        x = coord(self.slug[-1][0] + 1)
        self.slug.append((x, self.slug[-1][1]))
        if VERBOSE: print('right slug', self.slug)
                    
    def up(self):
        y = coord(self.slug[-1][1] - 1)
        self.slug.append((self.slug[-1][0], y))
        if VERBOSE: print('up_slug', self.slug)

    def down(self):
        y = coord(self.slug[-1][1] + 1)
        self.slug.append((self.slug[-1][0], y))
        if VERBOSE: print('down_slug', self.slug)

    def message(self, msg, color=WHITE):
            self.hat.show_message(msg, MSG_SPEED, color)
            
    def stop(self):
        if VERBOSE: print('lives', self.lives)
        msg =' '.join((MSG_SCORE, str(self.score)))
        if not self.winner:
            self.lives -= 1
   
        
        if not self.lives:
            self.message(msg, YELLOW)
            self.message(MSG_END, RED)
            exit()
        else:
            if self.winner and self.lives > 1:
                self.message(msg, BLUE)
            elif not self.winner and self.lives > 1:
                self.message(msg, GREEN)
            else:
                if self.lives == 1:
                    self.message(MSG_LIFE, YELLOW)
                else:
                    msg = ' '.join((MSG_LIVES, str(self.lives), MSG_LEFT))
                    self.message(msg)
            self.init()

    def rodent(self):
        while True:
            rat = pixel()
            if not rat in self.slug and not rat in self.rats: break
        lucky = random.randint(1, CHANCE * 2)
        if lucky == WINNER:
            if len(self.rats) < RATMAX:
                self.rats.append(rat)
                if rat in self.vegies:
                    self.vegies.remove(rat)
                if rat in self.fruits:
                    self.fruit.remove(rat)
            lucky = random.randint(1,CHANCE * 3)
            if lucky == WINNER and len(self.rats) > 0:
                pix = self.rats.pop(0)
                self.hat.set_pixel(*pix, BLACK)
        if VERBOSE: print('rats', self.rats)

    def fruit(self):
        fruit_len = len(self.fruits)
        while True:
            fruit = pixel()
            if (not fruit in self.slug) and (not fruit in self.vegies) and (not fruit in self.fruits):
                    break
        lucky = random.randint(1, CHANCE)
        if lucky == WINNER:
            if fruit_len < FRUITMAX:
                self.fruits.append(fruit)
                fruit_len += 1
            lucky = random.randint(1, CHANCE * 2)
            if lucky == WINNER:
                if 0 < fruit_len < FRUITMAX:
                    pix = self.fruits.pop(0)
                    self.hat.set_pixel(*pix, BLACK)
        if VERBOSE: print('fruits', self.fruits)

        

    def vegie(self):
        veg_len = len(self.vegies)
        while True:
            veg = pixel()
            if (not veg in self.slug) and (not veg in self.vegies) and (not veg in self.fruits):
                    break
        lucky = random.randint(1, CHANCE)
        if lucky == WINNER:
            if veg_len < VEGMAX:
                self.vegies.append(veg)
                veg_len += 1
            lucky = random.randint(1,CHANCE * 2)
            if lucky == WINNER:
                if 0 < veg_len < VEGMAX:
                    pix = self.vegies.pop(0)
                    self.hat.set_pixel(*pix, BLACK)
        if VERBOSE: print('vegies', self.vegies)

    def slug_grow(self):
        if not self.move:
            return
        
        if not self.grow and len(self.slug) > 0:
            pix = self.slug.pop(0) 
            self.hat.set_pixel(*pix, BLACK)
        self.grow = False
        
    def draw(self):
        ''' updates Sense Hat display '''
        for pix in self.vegies:
            self.hat.set_pixel(*pix, GREEN)
        for pix in self.rats:
            self.hat.set_pixel(*pix, RED)
        for pix in self.fruits:
            self.hat.set_pixel(*pix, YELLOW)
        color = WHITE
        blue = 0
        green = 255
        red = 255
        color_delta = int(255/len(self.slug))
        for pix in self.slug:
            if pix in self.vegies:
                self.vegies.remove(pix)
                self.score += 1
                self.grow = True
            elif pix in self.fruits:
                self.fruits.remove(pix)
                self.score += 1
                self.grow = False
                self.delay -= FRUIT_DELAY
            elif pix in self.rats:
                self.score -= 1
                self.move = STOP
                self.message(MSG_RAT, RED)
                if VERBOSE: print('RATS!')
                break
            
            red -= color_delta
            blue += color_delta
            green -= color_delta
            color = (red, green, blue)
            self.hat.set_pixel(*pix, color)
        if VERBOSE: print('slug', self.slug)
                
    def hat_action(self, event):
        if VERBOSE: print(event)
        if event.action == PRESS:
            self.move = event.direction
        if event.action == HELD:
            self.move = STOP
          
    def update_loop(self):
        ''' Hotspot function '''
        while self.move != STOP:
            sleep(self.delay)
            if self.move == RIGHT:
                self.right()
            elif self.move == LEFT:
                self.left()
            elif self.move == UP:
                self.up()
            elif self.move == DOWN:
                self.down()
            if VERBOSE: print(self.move)
            slug_len = len(self.slug) 
            if slug_len > PIXMAX:
                self.winner = True
                self.message(MSG_WIN, GREEN)
                self.delay -= self.delay / LIVES
                self.move = STOP
            elif slug_len > 0:
                self.rodent()
                self.vegie()
                self.fruit()
                self.draw()
                self.slug_grow()
            else:
                self.move = STOP
        else:
            self.stop()

    def slug_right(self):
        self.move = RIGHT
        for go in range(2):
            self.right()
              
    def slug_left(self):
        self.move = LEFT
        for go in range(2):
            self.left()
        
    def slug_up(self):
        self.move = UP
        for go in range(2):
            self.up()

    def slug_down(self):
        self.move = DOWN
        for go in range(2):
            self.down()

    def init_slug(self):
        slug_start = random.choice(
            (self.slug_right, self.slug_left,
             self.slug_up, self.slug_down))
        slug_start()

    def init_hat(self):
        self.hat = SenseHat()
        self.message(MSG_START, GREEN)
        self.hat.clear()
        self.hat.stick.direction_any = self.hat_action
        
    def init(self):
        self.slug = [pixel()]
        self.vegies = []
        self.fruits = []
        self.rats = []
        self.delay = DELAY
        self.grow = False
        self.winner = False
        self.init_slug()
        self.init_hat()
        self.update_loop()
    
    def __init__(self):
        self.delay = DELAY
        self.lives = LIVES
        self.level = 1
        self.score = 0
        self.init()
        

worm = Slug()


