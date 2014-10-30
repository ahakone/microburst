##############################################################################
# microburst.py                                                              #
# current contributors: Sam Weiss, Anzu Hakone                               #
#                                                                            #
# This file will contain the main game loop as well as some supporting       #
# functions for the Microburst burst.                                        #
##############################################################################

import pygame, os, sys, random, time
from math import sqrt
from pygame.locals import *
from random import randint

'''
+----------------------------------------------------------------------------+
|                                                                            |
| Game Sprite Definitions                                                    |
|                                                                            |
+----------------------------------------------------------------------------+
'''
class sprite_base(pygame.sprite.Sprite):
    '''a base class for objects to streamline'''
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__(self, screen, x, y, dx, dy, img_name, scale, score):
        '''intit values that are in every sprite'''
        self.image_unscaled = self.load_image(img_name)
        self.unscaled_w, self.unscaled_h = self.image_unscaled.get_size()
        self.image = pygame.transform.scale(self.image_unscaled, (self.unscaled_w / scale, self.unscaled_h / scale))
        self.image_w, self.image_h = self.image.get_size()
        self.size = self.image_w * self.image_h
        self.score = score
        self.screen = screen
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = self.image.get_rect()
   
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

    def draw(self):
        '''call the screen draw function'''
        '''angles'''
        self.screen.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.dx
        self.y += self.dy
        '''update the rectangle if it does not'''
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

class player(sprite_base):
    '''create a class for the player'''
    def __init__(self, screen, x, y, dx, dy, img_name):
        self.score = 0
        super(player, self).__init__(screen, x, y, dx, dy, img_name, 20, self.score)

    def update(self, keys):
        self.image = pygame.transform.scale(self.image_unscaled, (self.image_w, self.image_w))
        self.image_w, self.image_h = self.image.get_size()
        self.size = self.image_w * self.image_h

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)

        self.dx = 0
        self.dy = 0
        for i in keys:
            if i == "UP":
                self.dy = - 5
            if i == "DOWN":
                self.dy = 5
            if i == "LEFT":
                self.dx = - 5
            if i == "RIGHT":
                self.dx = 5
        if self.x + self.dx < 50:
            self.dx = 1
        if self.x + self.dx > (770 - self.image_w):
            self.dx = -1
        if self.y + self.dy < 60:
            self.dy = 1
        if  self.y + self.dy > (560 - self.image_h):
            self.dy = -1
        super(player, self).update()
'''
def draw(self):
super(player, self).draw()
'''
class enemy(sprite_base):
    def __init__(self, screen, x, y, dx, dy, img_name, scale):
        self.counter = 0
        self.score = 10
        super(enemy, self).__init__(screen, x, y, dx, dy, img_name, scale, self.score)

    def update(self):
        self.counter += 1
        if(self.counter >= 120):
            if self.x + self.dx < 50 or self.x + self.dx > (770 - self.image_w):
                self.dx = -1 * self.dx
            if self.y + self.dy < 60 or self.y + self.dy > (560 - self.image_h):
                self.dy = -1 * self.dy
            super(enemy, self).update()

class food(sprite_base):
    def __init__(self, screen, x, y, dx, dy, img_name, scale):
        if img_name == "Apple.gif" or img_name == "Carrot.gif":
            self.score = 20
        else:
            self.score = -5
        super(food, self).__init__(screen, x, y, dx, dy, img_name, scale, self.score)

    def update(self):
        if self.x + self.dx < 50 or self.x + self.dx > (770 - self.image_w):
            self.dx = -1 * self.dx
        if self.y + self.dy < 60 or self.y+self.dy > (560 - self.image_h):
            self.dy = -1 * self.dy
        super(food, self).update()
    '''needswork'''

class static_background(sprite_base):
    def __init__(self, screen, img_name):
        super(static_background, self).__init__(screen, 0, 0, 0, 0, img_name, 1, 0)


'''
+----------------------------------------------------------------------------+
|                                                                            |
| Init function code                                                         |
|                                                                            |
+----------------------------------------------------------------------------+
'''

def init_game(objects, screen, num_enemies, num_food):
    foodsprites = ["Apple.gif", "Ice cream.gif", "Carrot.gif", "Hamburger.gif"]
    enemysprites = ["Enemy 1.gif", "Enemy 2.gif"]
    players = []
    enemies = []
    foodstuff = []
    backgrounds = []
    players.append(player(screen, 400, 300, 0, 0, "Freddy.gif"))
    for i in range(num_enemies):
        enemies.append(enemy(screen, randint(60, 700), randint(70, 500), randint(-3, 3), randint(-3,3), enemysprites[randint(0,1)], randint(3,50)))
    for i in range(num_food):
        foodstuff.append(food(screen, randint(60,700), randint(70,500), randint(-3, 3), randint(-3,3), foodsprites[randint(0, 3)], randint(10, 50)))
    backgrounds.append(static_background(screen,"Stomach.gif"))
    objects.append(backgrounds)
    objects.append(players)
    objects.append(enemies)
    objects.append(foodstuff)


'''
+----------------------------------------------------------------------------+
|                                                                            |
| Main Execution code                                                        |
|                                                                            |
+----------------------------------------------------------------------------+
'''
def quit():
    '''quits the game if the game quit signal is provided'''
    pygame.quit()
    sys.exit(0)

#setup pygame and the window
pygame.init()
pygame.font.init()
foodsprites = ["Apple.gif", "Ice cream.gif", "Carrot.gif", "Hamburger.gif"]
enemysprites = ["Enemy 1.gif", "Enemy 2.gif"]
font = pygame.font.Font(None, 20)
screenDimensions = (800, 600)
window = pygame.display.set_mode(screenDimensions, pygame.RESIZABLE)
pygame.display.set_caption('Microbust')
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
pressed = []
clock = pygame.time.Clock()
'''limit framerate to 60 FPS'''
FPS = 60
'''game length in seconds'''
gamelength = 20
pygame.time.set_timer(USEREVENT + 1, 1000)
'''keep track of the objects'''
objects = []
'''keep track of what screen we're on'''
screen_status = 1
gamestart = 0
MAX_SCORE = 460

EXPERIMENTAL = -1

pygame.mixer.init()
pygame.mixer.music.load("Microburst.ogg")
pygame.mixer.music.play(99999999, 0.0)

while True:
    clock.tick(FPS)
    if screen_status == 1:
        splash_screen = static_background(screen, "Splash screen.gif")
        splash_screen.draw()
        pygame.display.flip()
        '''draw some intro screen'''
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_SPACE:
                    screen_status = 2
                    gamestart = time.clock()
                    print str(gamestart) + " " + str(time.clock())
                    init_game(objects, screen, 10, 10)
    elif screen_status == 3:
        splash_screen = static_background(screen, "Fail screen.gif")
        splash_screen.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_SPACE:
                    screen_status = 2
                    objects[1][0].dx = 0
                    objects[1][0].dy = 0
                    objects = []
                    pressed = []
                    gamestart = time.clock()
                    print str(gamestart) + " " + str(time.clock())
                    init_game(objects, screen, 10, 10)

    elif screen_status == 4:
        splash_screen = static_background(screen, "Win screen.gif")
        splash_screen.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quit()

    elif screen_status == 2:
        if len(objects[2]) == 0 and len(objects[3]) == 0:
            screen_status = 4
        for e in objects[2]:
            if pygame.sprite.collide_rect(objects[1][0],e):
                if objects[1][0].size > e.size:
                    objects[2].remove(e)
                    objects[1][0].size += e.size
                    objects[1][0].image_w = int(sqrt(objects[1][0].size))

                else:
                    screen_status = 3
        for f in objects[3]:
            if pygame.sprite.collide_rect(objects[1][0],f):
                if objects[1][0].size > f.size:
                    objects[1][0].size += f.size
                    objects[1][0].score += f.score
                    objects[1][0].image_w = int(sqrt(objects[1][0].size))
                    objects[3].remove(f)
                else:
                    f.dx = objects[1][0].dx * 2
                    f.dy = objects[1][0].dy * 2
        for l in objects:
            for o in l:
                o.draw()
                if type(o) is player:
                    o.update(pressed)
                else:
                    o.update()
        if randint(0,1000) <= (20 - len(objects[2])):
            objects[3].append(food(screen, randint(60,700), randint(70,500), randint(-3, 3), randint(-3,3), foodsprites[randint(0, 3)], randint(10, 50)))
            objects[2].append(enemy(screen, randint(60, 700), randint(70, 500), randint(-3, 3), randint(-3,3), enemysprites[randint(0,1)], randint(3,50)))
        size = objects[1][0].size
        score = objects[1][0].score
        text = font.render("Time left : " + str(gamelength - (time.clock() - gamestart)) + " Your size is : " + str(size) + " Your score is : " + str(score), 1, (255,255,255))
        screen.blit(text, (20, 20))
        pygame.display.flip()
        if(time.clock() - gamestart >= gamelength):
            screen_status = 3
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                elif event.key == K_UP:
                    pressed.append("UP")
                elif event.key == K_DOWN:
                    pressed.append("DOWN")
                elif event.key == K_LEFT:
                    pressed.append("LEFT")
                elif event.key == K_RIGHT:
                    pressed.append("RIGHT")
                elif event.key == K_SPACE:
                    pressed.append("SPACE")
            elif event.type == KEYUP:
                if event.key == K_UP:
                    pressed.remove("UP")
                elif event.key == K_DOWN:
                    pressed.remove("DOWN")
                elif event.key == K_LEFT:
                    pressed.remove("LEFT")
                elif event.key == K_RIGHT:
                    pressed.remove("RIGHT")
                elif event.key == K_SPACE:
                    pressed.remove("SPACE")
