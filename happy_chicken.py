import pygame
import json
from sys import argv
from random import randint
from time import time
from time import ctime
from os import sep
from os import path


#当前工作目录
path0 = path.dirname(path.realpath(argv[0])) + sep

fps = 60    #帧数

pygame.init()
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
pygame.display.set_caption("Happy Chicken")
gameclock = pygame.time.Clock()
font = pygame.font.SysFont('simhei', 40)
chicken_model = pygame.image.load(path.join(path0, "chicken0.png"))


def rwfile(path, score):
    #将分数写入json文件
	dic = {}
	with open(path, "r") as file:
		dic = json.load(file)
		dic[ctime()] = score
		file.close()
	with open(path, "w") as file:
		file.write(json.dumps(dic))
		file.close()


#将字典进行排序
def sort_dict(dic):
    keys = list(dic.keys())
    values = list(dic.values())
    for i in range(len(values)):
        for j in range(len(values)):
            if values[j] < values[i]:
                #将值列表进行排序
                temp = values[j]
                values[j] = values[i]
                values[i] = temp
                #将键列表进行排序
                temp = keys[j]
                keys[j] = keys[i]
                keys[i] = temp
    return dict(zip(keys, values))
    

def display_list():
    #显示排行榜
    dic = {}
    with open(path.join(path0, "Scores.json"), "r") as file:
        dic = json.load(file)
        file.close()
    dic = sort_dict(dic)    #排序
    font_list = pygame.font.SysFont('simhei', 30)
    text_title = font.render("History (Your grades have been ranked here)", True, (0, 0, 0))
    screen.blit(text_title, (screen.get_width()/2-text_title.get_width()/2, screen.get_height()/2+chicken_model.get_height()))
    y_bottom_of_title = screen.get_height()/2+chicken_model.get_height()+text_title.get_height()
    i = 0
    model = font_list.render("Sun Jul 31 19:02:47 2022"+":     "+"4", True, (0, 0, 0))
    x = screen.get_width()/2-model.get_width()/2
    for key, value in dic.items():
        text_list = font_list.render(str(key)+":     "+str(value), True, (0, 0, 0))
        screen.blit(text_list, (x, y_bottom_of_title+i*text_list.get_height()))
        # x坐标改成screen.get_width()/2-text_list.get_width()/2便是让每一行居中显示, 这种为了对齐比较美观
        i += 1
        if i>=6:
            break



def start():
    class Chicken():
        def __init__(self):
            self.img = [pygame.image.load(path.join(path0, "chicken0.png")),
                        pygame.image.load(path.join(path0, "chicken1.png")),
                        pygame.image.load(path.join(path0, "jump.png")),
                        ]
            self.state = 0
            self.t0 = int(time())  #眨眼起始时间
            self.tb = 0     #眨眼时间
            self.isJumping = False    #起跳状态
            self.tj = 0     #起跳时间
            self.rect = self.img[0].get_rect()
            self.rect.centerx = screen.get_width()/2
            self.rect.centery = screen.get_height()/2

        def blit(self):
            if int(time())%self.t0 < 3:
                self.state = 0
            else:
                self.state = 1
                self.tb += 1
                if self.tb >= int(fps/3):
                    self.state = 0
                    self.tb = 0
                    self.t0 = int(time())
            #上面这一大段就是为了让小鸡眨眼……
            if chicken1.isJumping:
                chicken1.state = 2
                chicken1.tj += 1
                if chicken1.tj >= fps/2:
                    chicken1.state = 0
                    chicken1.tj = 0
                    chicken1.isJumping = False
            #这里是实现小鸡的起跳动作
            screen.blit(self.img[self.state], self.rect)

        def random_move(self):
            # self.rect.centerx, self.rect.centery = pygame.mouse.get_pos()
            self.rect.centerx = randint(self.rect.width, screen.get_width()-self.rect.width)
            self.rect.centery = randint(self.rect.height, screen.get_height()-self.rect.height)
        
        def layegg(self):
            egg = Egg(self.rect.centerx, self.rect.centery + self.rect.height/2)
            egg_list.append(egg)
            self.rect.centery -= egg.rect.height
            self.isJumping = True



    class Egg():
        def __init__(self, x, bottomy):
            self.img = pygame.image.load(path.join(path0, "egg.png"))
            self.rect = self.img.get_rect()
            self.rect.centerx = x
            self.rect.centery = bottomy - self.rect.height/2


    chicken1 = Chicken()
    egg_list = []
    k_g = True
    while k_g:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    k_g = False
                    rwfile(path.join(path0, "Scores.json"), len(egg_list))
                    
                else:
                    chicken1.random_move()
                    chicken1.layegg()

            if event.type == pygame.MOUSEBUTTONDOWN:
                chicken1.random_move()
                chicken1.layegg()
                

        screen.fill((42, 181, 255))
        for i in egg_list:
            screen.blit(i.img, i.rect)
        chicken1.blit()
        text = font.render("Score: " + str(len(egg_list)), True, (0, 0, 0))     #显示分数
        screen.blit(text, (screen.get_width()-text.get_width(), 0))
        #y坐标改成screen.get_height()-text.get_height(), 使分数显示在右下角
        
        gameclock.tick(fps)     #帧数
        pygame.display.update()


def tips():
    # 操作提示
    f = 1
    font_big = pygame.font.SysFont('simhei', 40)
    font_small = pygame.font.SysFont('simhei', 30)
    while(f):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    f = 0
                elif event.key == pygame.K_RETURN:
                    start()
        
        screen.fill((42, 181, 255))
        t_list = [font_big.render("Instructions", True, (0, 0, 0)),
            font_small.render('''"Enter": Start Playing''', True, (0, 0, 0)),
            font_small.render('''Any Key Except "Esc": Move And Lay Eggs''', True, (0, 0, 0)),
            font_small.render('''"Esc": Exit the Game''', True, (0, 0, 0)),
        ]
        posy = t_list[0].get_height()*2
        gap = t_list[1].get_height()
        for index in t_list:
            screen.blit(index, (screen.get_width()/2-t_list[2].get_width()/2, posy))
            posy += gap*6
        gameclock.tick(fps)
        pygame.display.update()

is_first_time = False
#检查Scores.json文件
if not path.exists(path.join(path0, "Scores.json")):
    is_first_time = True
    with open(path.join(path0, "Scores.json"), 'w') as f:
        f.write(json.dumps({}))

#程序入口
keep_going = True
while keep_going:
    screen.fill((42, 181, 255))
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keep_going = False
                else:
                    tips()
    
    text = font.render("Press any key to start", True, (0, 0, 0))
    screen.blit(text, (screen.get_width()/2-text.get_width()/2, screen.get_height()-text.get_height()*2))
    title = font.render("Happy Chicken", True, (0, 0, 0))
    screen.blit(title, (screen.get_width()/2-title.get_width()/2, title.get_height()*4))
    #在屏幕中央显示小鸡
    screen.blit(chicken_model, (screen.get_width()/2-chicken_model.get_width()/2, screen.get_height()/2-chicken_model.get_height()/2))
    if not is_first_time:
        display_list()      #显示排行榜
    gameclock.tick(fps)     #帧数
    pygame.display.update()

