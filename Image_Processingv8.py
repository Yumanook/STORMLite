import numpy as np
from PIL import Image
import pygame
#DONT FORGET TO IMPORT CALIBRATION METHOD STUFFS

def processed(imagename, output):
#keep in mind that output is declared when main method is initialized;
#imagename is produced by function takePic in main method 
    pygame.display.init()
    img = Image.open(imagename)
    win = pygame.display.set_mode((img.size[0],img.size[1]))
    blitter = pygame.image.load(output)
    win.blit(blitter,(0,0))
    pix = img.load()
    np.set_printoptions(threshold=np.inf)
    i = 0
    j = 0
    k = 0
    l = 0
    m = 0
    n = 0
    '''WRGBA = weighted rgb avg - refer to calibration method'''
    WRGBA = 90
    THRESHOLD = 3*WRGBA
    RGBVAL = np.zeros((img.size[0],img.size[1],3))
    PIXVAL = np.zeros((img.size[0],img.size[1]))
    SIZE = (img.size[0],img.size[1])
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    MAGENTA = (255,0,255)
    CYAN = (0,255,255)

    for i in range(0,img.size[0]):
        for j in range(0,img.size[1]):
            RGBVAL[i][j] = pix[i,j]
            PIXVAL[i][j] = (RGBVAL[i][j][0] + RGBVAL[i][j][1] + RGBVAL[i][j][2])/3

    for k in range(0,img.size[0] - 25,25):
        for l in range(0,img.size[1] - 25,25):
            if PIXVAL[k][l] > 120:
                AVGX = 0
                AVGY = 0
                TOTX = 0
                TOTY = 0
                TOTINT = 0
                for m in range(k, k+25):
                    for n in range(l, l+25):
                        TOTX = TOTX + (m+1)*PIXVAL[m][n]
                        TOTY = TOTY + (n+1)*PIXVAL[m][n]
                        TOTINT = TOTINT + PIXVAL[m][n]
                AVGX = TOTX/TOTINT - 1
                AVGY = TOTY/TOTINT - 1
                AVGX = int(AVGX)
                AVGY = int(AVGY)
                if RGBVAL[AVGX][AVGY][0] > RGBVAL[AVGX][AVGY][1] and RGBVAL[AVGX][AVGY][0] > RGBVAL[AVGX][AVGY][2]:
                    pygame.draw.circle(win,RED,(AVGX,AVGY),1,0)
                    pygame.display.flip()
                elif RGBVAL[AVGX][AVGY][1] > RGBVAL[AVGX][AVGY][0] and RGBVAL[AVGX][AVGY][1] > RGBVAL[AVGX][AVGY][2]:
                    pygame.draw.circle(win,GREEN,(AVGX,AVGY),1,0)
                    pygame.display.flip()
                elif RGBVAL[AVGX][AVGY][2] > RGBVAL[AVGX][AVGY][0] and RGBVAL[AVGX][AVGY][2] > RGBVAL[AVGX][AVGY][1]:
                    pygame.draw.circle(win,BLUE,(AVGX,AVGY),1,0)
                    pygame.display.flip() 
                elif RGBVAL[AVGX][AVGY][0] == RGBVAL[AVGX][AVGY][1] and RGBVAL[AVGX][AVGY][0] == RGBVAL[AVGX][AVGY][2]:
                    pygame.draw.circle(win,WHITE,(AVGX,AVGY),1,0)
                    pygame.display.flip()
                elif RGBVAL[AVGX][AVGY][0] == RGBVAL[AVGX][AVGY][1] and RGBVAL[AVGX][AVGY][0] > RGBVAL[AVGX][AVGY][2]:
                    pygame.draw.circle(win,YELLOW,(AVGX,AVGY),1,0)
                    pygame.display.flip()
                elif RGBVAL[AVGX][AVGY][0] == RGBVAL[AVGX][AVGY][2] and RGBVAL[AVGX][AVGY][0] > RGBVAL[AVGX][AVGY][1]:
                    pygame.draw.circle(win,MAGENTA,(AVGX,AVGY),1,0)
                    pygame.display.flip()
                elif RGBVAL[AVGX][AVGY][1] == RGBVAL[AVGX][AVGY][2] and RGBVAL[AVGX][AVGY][1] > RGBVAL[AVGX][AVGY][0]:
                    pygame.draw.circle(win,CYAN,(AVGX,AVGY),1,0)
                    pygame.display.flip()
    pygame.image.save(win, output)

#processed("/home/pi/Desktop/02-10-2017_18:48:19.jpg", "/home/pi/Desktop/larksfacelol1.jpg")
