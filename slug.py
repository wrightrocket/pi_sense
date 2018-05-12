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

MSG_END = 'Game Over Slug :D'
MSG_START = 'Go Slug :)'
MSG_SCORE = 'You scored:'
MSG_VEGIES = 'vegies!!!'
MSG_LIVES = 'You have'
MSG_LIFE = 'You have 1 life left...'
MSG_LEFT = 'lives left...'

    
TIME_SLUG = 1.0
WHITE = (255,255,255)
BLACK = (0,0,0) 
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CHANCE = 5
WINNER = random.randint(1, CHANCE)
PIXMAX = 7
PIXMIN = 0
VEGMAX = 3
RATMAX = 3
LIVES = 3

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
        # print('left slug', self.slug)

    def right(self):
        x = coord(self.slug[-1][0] + 1)
        self.slug.append((x, self.slug[-1][1]))
        # print('right slug', self.slug)
                    
    def up(self):
        y = coord(self.slug[-1][1] - 1)
        self.slug.append((self.slug[-1][0], y))
        # print('up_slug', self.slug)

    def down(self):
        y = coord(self.slug[-1][1] + 1)
        self.slug.append((self.slug[-1][0], y))
        # print('down_slug', self.slug)
        
    def stop(self):
        if not self.winner:
            self.lives -= 1
        else:
            self.winner = False
        print('lives', self.lives)
        if not self.lives:
            self.hat.show_message(MSG_END)
            exit()
        else:
            self.hat.show_message(' '.join((MSG_SCORE, str(self.score), MSG_VEGIES)))
            if self.lives == 1:
                self.hat.show_message(MSG_LIFE)
            else:
                self.hat.show_message(' '.join((MSG_LIVES, str(self.lives), MSG_LEFT)))
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
        lucky = random.randint(1,CHANCE * 3)
        if lucky == WINNER and len(self.rats) > 0:
            pix = self.rats.pop(0)
            self.hat.set_pixel(*pix, BLACK)
        print('rats', self.rats)
        

    def vegie(self):
        veg_len = len(self.vegies)
        while True:
            veg = pixel()
            if (not veg in self.slug) and (not veg in self.vegies):
                break
        lucky = random.randint(5,10)
        if lucky == WINNER:
            if veg_len < VEGMAX:
                self.vegies.append(veg)
                veg_len += 1
            lucky = random.randint(1,20)
            if lucky == WINNER:
                if 0 < veg_len < VEGMAX:
                    pix = self.vegies.pop(0)
                    self.hat.set_pixel(*pix, BLACK)
        print('vegies', self.vegies)

    def slug_grow(self):
        if not self.move:
            return
        
        if not self.grow and len(self.slug) > 0:
            pix = self.slug.pop(0) 
            self.hat.set_pixel(*pix, BLACK)
        self.grow = False
        
    def draw(self):
        for pix in self.vegies:
            self.hat.set_pixel(*pix, GREEN)
        for pix in self.rats:
            self.hat.set_pixel(*pix, RED)
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
            elif pix in self.rats:
                self.move = STOP
                print('The rat got the slug')
                break
            
            red -= color_delta
            blue += color_delta
            green -= color_delta
            color = (red, green, blue)
            self.hat.set_pixel(*pix, color)
              

        print('draw slug', self.slug)
                
    def hat_action(self, event):
        print(event)
        if event.action == PRESS:
            self.move = event.direction
        if event.action == HELD:
            self.move = STOP
          
    def update_loop(self):
        while self.move != STOP:
            sleep(TIME_SLUG)
            if self.move == RIGHT:
                self.right()
            elif self.move == LEFT:
                self.left()
            elif self.move == UP:
                self.up()
            elif self.move == DOWN:
                self.down()
            print(self.move)
            slug_len = len(self.slug) 
            if slug_len > PIXMAX:
                self.winner = True
                self.move = STOP
            elif slug_len > 0:
                self.rodent()
                self.vegie()
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
        self.hat.show_message(MSG_START)
        self.hat.clear()
        self.hat.stick.direction_any = self.hat_action
        
    def init(self):
        self.slug = [pixel()]
        self.vegies = []
        self.rats = []
        self.score = 0
        self.grow = False
        self.winner = False
        self.init_slug()
        self.init_hat()
        self.update_loop()
    
    def __init__(self):
        self.lives = LIVES
        self.init()
        

worm = Slug()


