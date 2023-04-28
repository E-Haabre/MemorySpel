import pygame
import numpy as np
from pygame.locals import * 
import sys
import random
import memory_spel_grafikk as msg


def prep(spriteList:list):
    transformed = []

    for sprite in spriteList:
        sprite = pygame.transform.scale(sprite, brett.rectsize)
        transformed.append(sprite)
    
    return transformed



class GameLoop:
    def __init__(self):
        self.count = 0

    def Meny(self, kjør = False):
        while kjør:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.clickrect = pygame.Rect(mouse_pos, (2, 2))
                if pygame.Rect.colliderect(self.clickrect, brett.menyKnappPos):
                    kjør = False
            
            window.fill(BACKGROUND)
            
            brett.startMeny()

            pygame.display.update()
            clock.tick(FPS)


    def hovedspill(self, kjør = False):
        while kjør:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if brett.clickable:    
                    for kort in bunke:
                        kort.checkClick(mouse_pos)

            keyPressedTuple = pygame.key.get_pressed()

            window.fill(BACKGROUND)
            
            for kort in bunke:
                kort.update()

            if len(bunke) > 0:
                klokke.tid()

            klokke.show()

            pygame.display.update()

            clock.tick(FPS)


class Brett:
    def __init__(self, window, w_height, w_width, brett_størrelse):
        # ESENSIELLE
        self.window = window
        self.w_height = w_height
        self.w_width = w_width

        # MENY
        self.fontStart = pygame.font.Font('freesansbold.ttf', 32)
        self.fontInfo = pygame.font.Font('freesansbold.ttf', 22)
        self.menyPosMult = 0.8
        self.infotekst = "I dette spillet er målet å fjerne alle kortene. \n Kortene forsvinner når man trykker på 2 av dem med lik farge og symbol. \n Det er om å gjøre på så kort tid som mulig"
        #self.menyTekst = ["LETT", "MEDIUM", "VANSKELIG"]
        
        # KORT
        self.brett_størr = brett_størrelse
        self.kortDim = int(120-(self.brett_størr*1.5))
        self.rectsize = (self.kortDim, self.kortDim)
        self.poses = []
        self.checklist = []
        self.kortsymb = []
        self.x = np.zeros(self.brett_størr)
        self.xposmult = self.kortDim * 1.2
        self.clickable = True
        self.trykk = 0

        for h in range(0, self.brett_størr):
            self.x[h] = h * self.xposmult + self.w_width/9
            for v in range(0,int(self.brett_størr/2)*2):
                self.rectposvert = (self.x[h], v*(self.kortDim * 1.1)  +20)
                self.poses.append(pygame.Rect(self.rectposvert, self.rectsize))


        for i in range(0, int(len(self.poses)/2)):
            self.kortsymb += 2*[i]
        
  
        random.shuffle(self.kortsymb)

    def LagKort(self):
        self.bilder_klare = prep(msg.bilder)
        
        for i in range(len(self.x)*(int(self.brett_størr/2)*2)):
            kort = Kort(self.window, self.poses[i], self.kortsymb[i])
            bunke.append(kort)

    def toLike(self, symbol, index):

        self.checklist.append(symbol)
        self.checklist.append(index)
        
        if len(self.checklist) == 4 and self.checklist[1] == self.checklist[3]:
                self.checklist.pop()
                self.checklist.pop()
                return

        if len(self.checklist) == 4 and self.checklist[0] == self.checklist[2]:
            self.clickable = False
            bunke[self.checklist[1]].timer.tid(min(bunke[self.checklist[1]].cooldown, bunke[self.checklist[3]].cooldown))
            bunke[self.checklist[3]].timer.tid(min(bunke[self.checklist[1]].cooldown, bunke[self.checklist[3]].cooldown))
            bunke[self.checklist[1]].parret = True
            bunke[self.checklist[3]].parret = True

            self.checklist = []
            
        elif len(self.checklist) == 4 and self.checklist[0] != self.checklist[2]:
            self.clickable = False
            bunke[self.checklist[1]].cooldown += 0.5
            bunke[self.checklist[3]].cooldown += 0.5
            bunke[self.checklist[1]].timer.tid(max(bunke[self.checklist[1]].cooldown, bunke[self.checklist[3]].cooldown))
            bunke[self.checklist[3]].timer.tid(max(bunke[self.checklist[1]].cooldown, bunke[self.checklist[3]].cooldown))
            bunke[self.checklist[1]].parret = False
            bunke[self.checklist[3]].parret = False
            

            self.checklist = []

    def startMeny(self):

        self.textLett = self.fontStart.render("Start", True, BLACK)
        self.menyKnappPos = pygame.Rect((((self.w_width/2)-200), self.w_height*self.menyPosMult), (220, 40))
        #self.textInfo = self.fontInfo.render(self.infotekst, True, BLACK)
        #self.infoPos = pygame.Rect((((self.w_width/2)-300), self.w_height*0.1), (220, 40))
        pygame.draw.rect(self.window, (255,255,255), self.menyKnappPos)
        window.blit(self.textLett, self.menyKnappPos)
        #window.blit(self.textInfo, self.infoPos)



class Kort:
    def __init__(self, window, plassering, symbol):
        self.window = window
        self.plassering = plassering
        self.symbol = symbol
        self.snudd = False
        self.parret = None
        self.cooldown = 0.5
        self.timer = Klokke()

        
    def checkClick(self, clickpos = (0,0)):
        index = bunke.index(self)
        self.clickrect = pygame.Rect(clickpos, (2, 2))
        self.collide = pygame.Rect.colliderect(self.clickrect, self.plassering)
        
        if self.collide:
            self.snudd = True
            brett.trykk += 1
            brett.toLike(self.symbol, index)     

    def update(self):
        if self.snudd:
            pygame.draw.rect(self.window, msg.colors[self.symbol], self.plassering) 
            window.blit(brett.bilder_klare[self.symbol], self.plassering)

        elif not self.snudd:
            pygame.draw.rect(self.window, BLACK, self.plassering)

        if self.parret:
            if self.timer.nedtelling():
                brett.clickable = True

                bunke.remove(self)

        elif self.parret == False:
            if self.timer.nedtelling():
                brett.clickable = True
                self.parret = None
                self.snudd = False


class Klokke:
    def __init__(self):
        self.count = 0
        
    def tid(self, sekunder = 0):    
        self.count +=1
        self.tidsklokke = self.count/FPS
        self.sekunder = sekunder * FPS


    def nedtelling(self):    
        if self.sekunder > 0:
            self.sekunder -= 1
            return False
    
        else:
            return True
    
    def show(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"{round(self.tidsklokke, 2)}", True, BLACK)
        textRect = text.get_rect()
        textRect = (20, 20)
        window.blit(text, textRect)


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0 ,255)
ORANGE = (255, 150, 0)
PURPLE = (220, 220, 255)
PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
INDIGO = (75, 0, 130)
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)
BACKGROUND = (240, 210, 200)
FPS = 10
bunke = []

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

brett = Brett(window, WINDOW_HEIGHT, WINDOW_WIDTH, 3)
brett.LagKort()

klokke = Klokke()


Loop = GameLoop()

Loop.Meny(True)

Loop.hovedspill(True)