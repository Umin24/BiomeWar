import pygame
import os
import sys


def load_map(name):
    with open('maps/' + name + '.txt') as f:
        map = f.readline().strip()
        if map == '':
            return ('empty',)

        newmap = []
        map_lines = f.read().split('\n')[1:]
        for _ in range(len(map_lines)):
            newmap_line = [map_lines[_][i:i + 3] for i in range(0, len(map_lines[_]), 3)]
            newmap.append(newmap_line)
        return map, newmap


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()

infoObject = pygame.display.Info()

WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
MAPS = [load_map('map1')[0], load_map('map2')[0],
        load_map('map3')[0], load_map('map4')[0], load_map('map5')[0]]

FPS = 400
STEP = 50

PRIC = {29: 50, 32: 50, 35: 50, 38: 50,
        30: 100, 33: 100, 36: 100, 39: 100,
        31: 200, 34: 200, 37: 200, 40: 200,
        27: 100, 28: 100}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
all_sprites_redactor = pygame.sprite.Group()
but_sprites = pygame.sprite.Group()
all_sprites_game = pygame.sprite.Group()
redactormenu_sprites = pygame.sprite.Group()
boardmenu_sprites = pygame.sprite.Group()
tiles_choose = pygame.sprite.Group()

tile_list = []
knight_list = []

choosing = '023'


class Sprite:
    def __init__(self, name, size, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.size = size

        self.sprite = pygame.sprite.Sprite()
        image = pygame.image.load(f'{name}.png')
        image = pygame.transform.scale(image, size)
        self.sprite.image = image
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y

    def get_sprite(self):
        return self.sprite


class RedactorMenu:
    def __init__(self, width, height):
        self.w = width
        self.h = height

        self.active = False
        self.input_box = pygame.Rect(50, 100, 550, 50)
        self.name = ''

        self.font = pygame.font.Font('data/Stacked pixel.ttf', 45)
        self.text = self.font.render(self.name, True,
                          pygame.Color('black'))

        self.but5 = Button('enter', 610, 95)
        self.sprite5 = self.but5.get_sprite()
        redactormenu_sprites.add(self.sprite5)

        self.txt5 = Text('CReATe', 677, 105, 55, (255, 255, 255))


        self.but6 = Button('Idle 1', 50, 180)
        self.sprite6 = self.but6.get_sprite()
        redactormenu_sprites.add(self.sprite6)
        self.txt6 = Text(MAPS[0], 110, 190, 55, (255, 255, 255))


        self.but7 = Button('Idle 2', 50, 250)
        self.sprite7 = self.but7.get_sprite()
        redactormenu_sprites.add(self.sprite7)
        self.txt7 = Text(MAPS[1], 110, 260, 55, (255, 255, 255))


        self.but8 = Button('Idle 3', 50, 320)
        self.sprite8 = self.but8.get_sprite()
        redactormenu_sprites.add(self.sprite8)
        self.txt8 = Text(MAPS[2], 110, 330, 55, (255, 255, 255))


        self.but9 = Button('Idle 4', 50, 390)
        self.sprite9 = self.but9.get_sprite()
        redactormenu_sprites.add(self.sprite9)
        self.txt9 = Text(MAPS[3], 110, 400, 55, (255, 255, 255))


        self.but10 = Button('Idle 5', 50, 460)
        self.sprite10 = self.but10.get_sprite()
        redactormenu_sprites.add(self.sprite10)
        self.txt10 = Text(MAPS[4], 110, 470, 55, (255, 255, 255))


        box = Sprite('data/textbox', (565, 60), 45, 95)
        textbox = box.get_sprite()
        redactormenu_sprites.add(textbox)

    def render(self, screen):
        fon = pygame.transform.scale(load_image('fon.jpg'), (self.w, self.h))
        screen.blit(fon, (0, 0))

        pygame.draw.rect(screen, pygame.Color('white'), self.input_box)
        screen.blit(self.text, (62, 110))


class Redactor:
    def __init__(self, width, height, x, y, map, key):
        self.w = width
        self.h = height

        self.x = x
        self.y = y

        self.key = key
        self.map = map

        self.maptxt()

        self.centers = [[] for _ in range(14)]

        self.draw()

    def maptxt(self):
        with open(f'maps/map{self.key}.txt', 'wt') as f:
            f.write(MAPS[self.key - 1] + '\n')
            for i in range(14):
                f.write('\n' + ''.join(self.map[i]))

    def render(self, screen):
        pass

    def draw_one(self, x, y):
        sprite = pygame.sprite.Sprite()
        image = pygame.image.load(f'data/{self.map[x][y]}.png')
        image = pygame.transform.scale(image, (62, 91))
        sprite.image = image
        sprite.rect = sprite.image.get_rect()
        all_sprites_redactor.add(sprite)

        if y % 2 == 0:
            sprite.rect.center = (3 * self.w * x + self.w, self.h + self.h * y - self.h / 1.5)

        else:
            sprite.rect.center = (3 * self.w * x + 1.5 * self.w + self.w, self.h + self.h * y - self.h / 1.5)

    def draw(self):
        for y in range(self.y):
            for x in range(self.x):
                sprite = pygame.sprite.Sprite()
                image = pygame.image.load(f'data/{self.map[x][y]}.png')
                image = pygame.transform.scale(image, (62, 91))
                sprite.image = image
                sprite.rect = sprite.image.get_rect()
                all_sprites_redactor.add(sprite)

                if y % 2 == 0:
                    sprite.rect.center = (3 * self.w * x + self.w, self.h + self.h * y - self.h / 1.5)
                    center = (self.w / 2 + self.w * 3 * x + 8, 0 + self.h * y + 13.6)

                else:
                    sprite.rect.center = (3 * self.w * x + 1.5 * self.w + self.w, self.h + self.h * y - self.h / 1.5)
                    center = (self.w / 2 + self.w * 3 * x + 1.5 * self.w + 8, 0 + self.h * y + 13.85)
                self.centers[x].append(center)

        self.but11 = Button('list', WIDTH - 60, 0)
        self.sprite11 = self.but11.get_sprite()
        all_sprites_redactor.add(self.sprite11)

    def change_tile(self, index):
        global choosing

        if int(choosing) >= 100:
            choosing = '023'
        self.map[index[0]][index[1]] = choosing
        self.draw_one(index[0], index[1])


class TilesChoose:
    def __init__(self, money, profit):
        self.money = money
        self.profit = profit
        self.draw()



    def render(self, screen):
        pass

    def draw(self):
        for i in range(6):
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/00{i + 1}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * i, 16)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        for i in range(6):
            r = str(i + 7).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * i, 128)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        for i in range(6):
            r = str(i + 13).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * i, 240)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        for i in range(4):
            r = str(i + 19).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * i, 352)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        for i in range(6):
            r = str(i + 23).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * i, 464)
            tiles_choose.add(sprite)
            tile_list.append(sprite)


        for i in range(3):
            r = str(i + 29).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * (i + 6), 16)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        knight1 = Sprite('knight/1knight00', (128, 128), 800, 0).get_sprite()
        tiles_choose.add(knight1)
        knight_list.append(knight1)

        for i in range(3):
            r = str(i + 32).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * (i + 6), 240)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        knight2 = Sprite('knight/2knight00', (128, 128), 800, 100).get_sprite()
        tiles_choose.add(knight2)
        knight_list.append(knight2)


        for i in range(3):
            r = str(i + 35).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * (i + 4), 352)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        knight3 = Sprite('knight/3knight00', (128, 128), 800, 200).get_sprite()
        tiles_choose.add(knight3)
        knight_list.append(knight3)

        for i in range(3):
            r = str(i + 38).rjust(3, '0')
            sprite = pygame.sprite.Sprite()
            image = pygame.image.load(f'data/{r}.png')
            image = pygame.transform.scale(image, (62, 91))
            sprite.image = image
            sprite.rect = sprite.image.get_rect()
            sprite.rect.center = (32 + 96 * (i + 6), 128)
            tiles_choose.add(sprite)
            tile_list.append(sprite)

        knight4 = Sprite('knight/4knight00', (128, 128), 600, 300).get_sprite()
        tiles_choose.add(knight4)
        knight_list.append(knight4)


        self.text = Text(f'MOney: {self.money}', 20, 600, 55, (0, 0, 0))
        self.text2 = Text(f'profit: {self.profit}', 20, 700, 55, (0, 0, 0))


class AnimatedSprite:
    def __init__(self, name, size, x, y, key):
        self.cur = 0
        self.size = size
        self.key = key
        self.knight = Sprite(name, size, x, y).get_sprite()
        all_sprites_game.add(self.knight)

    def update(self, limit):
        self.cur += 1
        image = pygame.image.load(f"knight/{self.key}knight{str(self.cur).rjust(2, '0')}.png")
        image = pygame.transform.scale(image, self.size)
        self.knight.image = image

        self.cur %= limit



class Board:
    def __init__(self, width, height, x, y, map, key):
        self.w = width
        self.h = height

        self.knights = []
        self.knightmap = []


        self.x = x
        self.y = y

        self.key = key
        self.map = map

        self.maptxt()
        self.put_money()
        self.get_profit()
        self.knightmaper()

        self.limit = 4

        self.centers = [[] for _ in range(14)]

        self.draw()

    def maptxt(self):
        with open(f'maps/map{self.key}.txt', 'wt') as f:
            f.write(MAPS[self.key - 1] + '\n')
            for i in range(14):
                f.write('\n' + ''.join(self.map[i]))

    def knightmaper(self):
        with open(f'maps/knight{self.key}.txt', 'rt') as f:
            map_lines = f.read().strip().split('\n')
            for _ in range(len(map_lines)):
                knight_line = [map_lines[_][i:i + 3] for i in range(0, len(map_lines[_]), 3)]
                self.knightmap.append(knight_line)

    def get_profit(self):
        self.profits = []
        a = 0
        b = 0
        c = 0
        d = 0
        for x in self.map:
            for y in x:
                if 29 <= int(y) <= 31:
                    a += 10
                elif 38 <= int(y) <= 40:
                    b += 10
                elif 32 <= int(y) <= 34:
                    c += 10
                elif 35 <= int(y) <= 37:
                    d += 10

        self.profits = [a, b, c, d]


    def put_money(self):
        with open('maps/money.txt', 'rt') as f:
            self.money = f.readlines()[self.key - 1].strip().split()
            self.money = [int(x) for x in self.money]
            self.order = self.money.pop()

    def save_game(self):
        with open('maps/money.txt', 'rt') as f:
            file = f.readlines()
            money_data = self.money + [self.order]
            money_data = [str(x) for x in money_data]
            file[self.key - 1] = ' '.join(money_data) + '\n'

        with open(f'maps/knight{self.key}.txt', 'wt') as f:
            knightmapline = [''.join(x) for x in self.knightmap]
            f.write('\n'.join(knightmapline))

        with open('maps/money.txt', 'wt') as f:
            f.write(''.join(file))

    def draw_one(self, x, y):
        sprite = pygame.sprite.Sprite()
        image = pygame.image.load(f'data/{self.map[x][y]}.png')
        image = pygame.transform.scale(image, (62, 91))
        sprite.image = image
        sprite.rect = sprite.image.get_rect()
        all_sprites_game.add(sprite)

        if y % 2 == 0:
            sprite.rect.center = (3 * self.w * x + self.w, self.h + self.h * y - self.h / 1.5)

        else:
            sprite.rect.center = (3 * self.w * x + 1.5 * self.w + self.w, self.h + self.h * y - self.h / 1.5)

    def draw(self):
        for y in range(self.y):
            for x in range(self.x):
                sprite = pygame.sprite.Sprite()
                image = pygame.image.load(f'data/{self.map[x][y]}.png')
                image = pygame.transform.scale(image, (62, 91))
                sprite.image = image
                sprite.rect = sprite.image.get_rect()
                all_sprites_game.add(sprite)

                if y % 2 == 0:
                    sprite.rect.center = (3 * self.w * x + self.w, self.h + self.h * y - self.h / 1.5)
                    center = (self.w / 2 + self.w * 3 * x + 8, 0 + self.h * y + 13.6)

                else:
                    sprite.rect.center = (3 * self.w * x + 1.5 * self.w + self.w, self.h + self.h * y - self.h / 1.5)
                    center = (self.w / 2 + self.w * 3 * x + 1.5 * self.w + 8, 0 + self.h * y + 13.85)
                self.centers[x].append(center)

        self.but11 = Button('list', WIDTH - 60, 0)
        self.sprite11 = self.but11.get_sprite()
        all_sprites_game.add(self.sprite11)

        self.but12 = Button('skip', WIDTH - 60, HEIGHT - 60)
        self.sprite12 = self.but12.get_sprite()
        all_sprites_game.add(self.sprite12)

        for i in range(len(self.knightmap)):
            self.knights.append([])
            for j in range(len(self.knightmap[i])):
                if self.knightmap[i][j] != '000':
                    knight = AnimatedSprite(f'knight/{int(self.knightmap[i][j])}knight00', (128, 128),
                                            self.centers[i][j][0] - 56, self.centers[i][j][1] - 64, int(self.knightmap[i][j]))
                    self.knights[i].append(knight)
                else:
                    self.knights[i].append(None)

    def change_tile(self, index):
        global choosing

        if self.knightmap[index[0]][index[1]] != '000':
            return

        if self.order == 1 and choosing == '100':
            if self.money[self.order - 1] >= 20:
                knight = AnimatedSprite('knight/1knight00', (128, 128), self.centers[index[0]][index[1]][0] - 56,
                                        self.centers[index[0]][index[1]][1] - 64, 1)
                self.money[self.order - 1] -= 20
                self.knights[index[0]].append(knight)
                self.knightmap[index[0]][index[1]] = choosing[::-1]

        if self.order == 2 and choosing == '200':
            if self.money[self.order - 1] >= 20:
                knight = AnimatedSprite('knight/2knight00', (128, 128), self.centers[index[0]][index[1]][0] - 56,
                                        self.centers[index[0]][index[1]][1] - 64, 2)
                self.money[self.order - 1] -= 20
                self.knights[index[0]].append(knight)
                self.knightmap[index[0]][index[1]] = choosing[::-1]

        if self.order == 3 and choosing == '300':
            if self.money[self.order - 1] >= 20:
                knight = AnimatedSprite('knight/3knight00', (128, 128), self.centers[index[0]][index[1]][0] - 56,
                                        self.centers[index[0]][index[1]][1] - 64, 3)
                self.money[self.order - 1] -= 20
                self.knights[index[0]].append(knight)
                self.knightmap[index[0]][index[1]] = choosing[::-1]

        if self.order == 4 and choosing == '400':
            if self.money[self.order - 1] >= 20:
                knight = AnimatedSprite('knight/4knight00', (128, 128), self.centers[index[0]][index[1]][0] - 56,
                                        self.centers[index[0]][index[1]][1] - 64, 4)
                self.money[self.order - 1] -= 20
                self.knights[index[0]].append(knight)
                self.knightmap[index[0]][index[1]] = choosing[::-1]


        if self.order == 1 and 1 <= int(choosing) <= 6 and self.money[self.order - 1] >= 10:
            self.map[index[0]][index[1]] = choosing
            self.draw_one(index[0], index[1])
            self.money[self.order - 1] -= 10

        if self.order == 1 and 29 <= int(choosing) <= 31:
            if self.money[self.order - 1] >= PRIC[int(choosing)]:
                self.map[index[0]][index[1]] = choosing
                self.draw_one(index[0], index[1])
                self.money[self.order - 1] -= PRIC[int(choosing)]


        if self.order == 2 and 7 <= int(choosing) <= 12 and self.money[self.order - 1] >= 10:
            self.map[index[0]][index[1]] = choosing
            self.draw_one(index[0], index[1])
            self.money[self.order - 1] -= 10

        if self.order == 2 and 38 <= int(choosing) <= 40:
            if self.money[self.order - 1] >= PRIC[int(choosing)]:
                self.map[index[0]][index[1]] = choosing
                self.draw_one(index[0], index[1])
                self.money[self.order - 1] -= PRIC[int(choosing)]


        if self.order == 3 and 13 <= int(choosing) <= 18 and self.money[self.order - 1] >= 10:
            self.map[index[0]][index[1]] = choosing
            self.draw_one(index[0], index[1])
            self.money[self.order - 1] -= 10

        if self.order == 3 and 32 <= int(choosing) <= 34:
            if self.money[self.order - 1] >= PRIC[int(choosing)]:
                self.map[index[0]][index[1]] = choosing
                self.draw_one(index[0], index[1])
                self.money[self.order - 1] -= PRIC[int(choosing)]


        if self.order == 4 and 19 <= int(choosing) <= 22 and self.money[self.order - 1] >= 10:
            self.map[index[0]][index[1]] = choosing
            self.draw_one(index[0], index[1])
            self.money[self.order - 1] -= 10

        if self.order == 4 and 35 <= int(choosing) <= 37:
            if self.money[self.order - 1] >= PRIC[int(choosing)]:
                self.map[index[0]][index[1]] = choosing
                self.draw_one(index[0], index[1])
                self.money[self.order - 1] -= PRIC[int(choosing)]


        if 27 <= int(choosing) <= 28 and 23 <= int(self.map[index[0]][index[1]]) <= 24:
            if self.money[self.order - 1] >= PRIC[int(choosing)]:
                if self.map[index[0]][index[1]] == 23:
                    choosing = '027'
                else:
                    choosing = '028'
                self.map[index[0]][index[1]] = choosing
                self.draw_one(index[0], index[1])
                self.money[self.order - 1] -= PRIC[int(choosing)]

        self.get_profit()


    def move(self):
        self.order %= 4
        self.order += 1

        for i in range(4):
            self.money[i] += self.profits[i]



class BoardMenu:
    def __init__(self, width, height):
        self.w = width
        self.h = height

        self.but6 = Button('Idle 1', 50, 180)
        self.sprite6 = self.but6.get_sprite()
        boardmenu_sprites.add(self.sprite6)
        self.txt6 = Text(MAPS[0], 110, 190, 55, (255, 255, 255))

        self.but7 = Button('Idle 2', 50, 250)
        self.sprite7 = self.but7.get_sprite()
        boardmenu_sprites.add(self.sprite7)
        self.txt7 = Text(MAPS[1], 110, 260, 55, (255, 255, 255))

        self.but8 = Button('Idle 3', 50, 320)
        self.sprite8 = self.but8.get_sprite()
        boardmenu_sprites.add(self.sprite8)
        self.txt8 = Text(MAPS[2], 110, 330, 55, (255, 255, 255))

        self.but9 = Button('Idle 4', 50, 390)
        self.sprite9 = self.but9.get_sprite()
        boardmenu_sprites.add(self.sprite9)
        self.txt9 = Text(MAPS[3], 110, 400, 55, (255, 255, 255))

        self.but10 = Button('Idle 5', 50, 460)
        self.sprite10 = self.but10.get_sprite()
        boardmenu_sprites.add(self.sprite10)
        self.txt10 = Text(MAPS[4], 110, 470, 55, (255, 255, 255))

    def render(self, screen):
        fon = pygame.transform.scale(load_image('fon.jpg'), (self.w, self.h))
        screen.blit(fon, (0, 0))


class Button:
    def __init__(self, name, x, y):
        self.sprite = pygame.sprite.Sprite()
        self.imagen = pygame.image.load(f'Buttons/{name}.png')
        self.imagen = pygame.transform.scale(self.imagen, (60, 60))

        self.image = pygame.image.load(f'Buttons/{name}2.png')
        self.image = pygame.transform.scale(self.image, (60, 60))

        self.sprite.image = self.imagen

        self.sprite.rect = self.sprite.image.get_rect()

        self.sprite.rect.x = x
        self.sprite.rect.y = y

    def get_pressed(self):
        return self.image

    def get_idle(self):
        return self.imagen

    def get_sprite(self):
        return self.sprite


class Text:
    def __init__(self, text, x, y, size, color):
        self.font = pygame.font.Font('data/Stacked pixel.ttf', size)
        self.text = self.font.render(text, True, color)
        self.x = x
        self.y = y

    def render(self, screen):
        screen.blit(self.text, (self.x, self.y))

    def get_text(self):
        return self.text


def terminate():
    pygame.quit()
    sys.exit()


def start_game(map, key):
    board = Board(32, 27, 14, 28, map, key)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    board.maptxt()
                    board.save_game()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dotcheck(event.pos[0], event.pos[1], board.sprite11.rect.x, board.sprite11.rect.y,
                            board.sprite11.rect.width, board.sprite11.rect.height):
                    start_tiles(board.money[board.order - 1], board.profits[board.order - 1])
                elif dotcheck(event.pos[0], event.pos[1], board.sprite12.rect.x, board.sprite12.rect.y,
                            board.sprite12.rect.width, board.sprite12.rect.height):
                    board.move()
                else:
                    board.change_tile(hexfind(event.pos, board.centers))
            elif event.type == pygame.MOUSEMOTION:
                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            board.sprite11.rect.x, board.sprite11.rect.y,
                            board.sprite11.rect.width, board.sprite11.rect.height):
                    board.sprite11.image = board.but11.get_idle()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            board.sprite11.rect.x, board.sprite11.rect.y,
                            board.sprite11.rect.width, board.sprite11.rect.height):
                    board.sprite11.image = board.but11.get_pressed()


                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            board.sprite12.rect.x, board.sprite12.rect.y,
                            board.sprite12.rect.width, board.sprite12.rect.height):
                    board.sprite12.image = board.but12.get_idle()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            board.sprite12.rect.x, board.sprite12.rect.y,
                            board.sprite12.rect.width, board.sprite12.rect.height):
                    board.sprite12.image = board.but12.get_pressed()


        for i in board.knights:
            for j in i:
                if j != None:
                    j.update(board.limit)
        screen.fill((255, 255, 255))
        all_sprites_game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_tiles(money, profit):
    global choosing

    tiles = TilesChoose(money, profit)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(40):
                    if tile_list[i].rect.collidepoint(event.pos):
                        choosing = str(i + 1).rjust(3, '0')
                        return
                for i in range(4):
                    if knight_list[i].rect.collidepoint(event.pos):
                        choosing = f'{(i + 1) * 100}'
                        return

        screen.fill((255, 255, 255))
        tiles.text.render(screen)
        tiles.text2.render(screen)
        tiles_choose.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_redactor(map, key):
    redactor = Redactor(32, 27, 14, 28, map, key)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    redactor.maptxt()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dotcheck(event.pos[0], event.pos[1], redactor.sprite11.rect.x, redactor.sprite11.rect.y,
                            redactor.sprite11.rect.width, redactor.sprite11.rect.height):
                    start_tiles('INFINITe', 'INFINITe')
                else:
                    redactor.change_tile(hexfind(event.pos, redactor.centers))
            elif event.type == pygame.MOUSEMOTION:
                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactor.sprite11.rect.x, redactor.sprite11.rect.y,
                            redactor.sprite11.rect.width, redactor.sprite11.rect.height):
                    redactor.sprite11.image = redactor.but11.get_pressed()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactor.sprite11.rect.x, redactor.sprite11.rect.y,
                            redactor.sprite11.rect.width, redactor.sprite11.rect.height):
                    redactor.sprite11.image = redactor.but11.get_idle()

        screen.fill((255, 255, 255))
        all_sprites_redactor.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_redactormenu():
    redactormenu = RedactorMenu(WIDTH, HEIGHT)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if redactormenu.active:
                    if event.key == pygame.K_BACKSPACE:
                        redactormenu.name = redactormenu.name[:-1]
                        redactormenu.text = redactormenu.font.render(redactormenu.name, True, pygame.Color('black'))
                    else:
                        if len(redactormenu.name) < 15:
                            redactormenu.name += event.unicode.upper()
                            redactormenu.text = redactormenu.font.render(redactormenu.name, True, pygame.Color('black'))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if redactormenu.input_box.collidepoint(event.pos):
                    redactormenu.active = True
                if dotcheck(event.pos[0], event.pos[1], redactormenu.sprite5.rect.x, redactormenu.sprite5.rect.y,
                            redactormenu.sprite5.rect.width, redactormenu.sprite5.rect.height):
                    if len(redactormenu.name) > 2 and redactormenu.name != 'empty':
                        if MAPS.count('empty') != 0 and redactormenu.name not in MAPS:
                            key = MAPS.index('empty') + 1
                            map = [['023'] * 28 for _ in range(14)]
                            MAPS[key - 1] = redactormenu.name
                            start_redactor(map, key)

                        elif redactormenu.name in MAPS:
                            redactormenu.name = 'THIS NAME IS TAKEN'
                            redactormenu.text = redactormenu.font.render(redactormenu.name, True, pygame.Color('black'))
                        else:
                            redactormenu.name = 'NOT ENOUGH PLACE'
                            redactormenu.text = redactormenu.font.render(redactormenu.name, True, pygame.Color('black'))

                if dotcheck(event.pos[0], event.pos[1], redactormenu.sprite6.rect.x, redactormenu.sprite6.rect.y,
                            redactormenu.sprite6.rect.width, redactormenu.sprite6.rect.height):
                    map = load_map('map1')
                    if map[0] != 'empty':
                        start_redactor(map[1], 1)
                        MAPS[0] = map[0]
                    else:
                        MAPS[0] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], redactormenu.sprite7.rect.x, redactormenu.sprite7.rect.y,
                            redactormenu.sprite7.rect.width, redactormenu.sprite7.rect.height):
                    map = load_map('map2')
                    if map[0] != 'empty':
                        start_redactor(map[1], 2)
                        MAPS[1] = map[0]
                    else:
                        MAPS[1] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], redactormenu.sprite8.rect.x, redactormenu.sprite8.rect.y,
                            redactormenu.sprite8.rect.width, redactormenu.sprite8.rect.height):
                    map = load_map('map3')
                    if map[0] != 'empty':
                        start_redactor(map[1], 3)
                        MAPS[2] = map[0]
                    else:
                        MAPS[2] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], redactormenu.sprite9.rect.x, redactormenu.sprite9.rect.y,
                            redactormenu.sprite9.rect.width, redactormenu.sprite9.rect.height):
                    map = load_map('map4')
                    if map[0] != 'empty':
                        start_redactor(map[1], 4)
                        MAPS[3] = map[0]
                    else:
                        MAPS[3] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], redactormenu.sprite10.rect.x, redactormenu.sprite10.rect.y,
                            redactormenu.sprite10.rect.width, redactormenu.sprite10.rect.height):
                    map = load_map('map5')
                    if map[0] != 'empty':
                        start_redactor(map[1], 5)
                        MAPS[4] = map[0]
                    else:
                        MAPS[4] = 'empty'

            elif event.type == pygame.MOUSEMOTION:
                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite5.rect.x, redactormenu.sprite5.rect.y,
                            redactormenu.sprite5.rect.width, redactormenu.sprite5.rect.height):
                    redactormenu.sprite5.image = redactormenu.but5.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite6.rect.x, redactormenu.sprite6.rect.y,
                            redactormenu.sprite6.rect.width, redactormenu.sprite6.rect.height):
                    redactormenu.sprite6.image = redactormenu.but6.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite7.rect.x, redactormenu.sprite7.rect.y,
                            redactormenu.sprite7.rect.width, redactormenu.sprite7.rect.height):
                    redactormenu.sprite7.image = redactormenu.but7.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite8.rect.x, redactormenu.sprite8.rect.y,
                            redactormenu.sprite8.rect.width, redactormenu.sprite8.rect.height):
                    redactormenu.sprite8.image = redactormenu.but8.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite9.rect.x, redactormenu.sprite9.rect.y,
                            redactormenu.sprite9.rect.width, redactormenu.sprite9.rect.height):
                    redactormenu.sprite9.image = redactormenu.but9.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite10.rect.x, redactormenu.sprite10.rect.y,
                            redactormenu.sprite10.rect.width, redactormenu.sprite10.rect.height):
                    redactormenu.sprite10.image = redactormenu.but10.get_pressed()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite5.rect.x, redactormenu.sprite5.rect.y,
                            redactormenu.sprite5.rect.width, redactormenu.sprite5.rect.height):
                    redactormenu.sprite5.image = redactormenu.but5.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite6.rect.x, redactormenu.sprite6.rect.y,
                            redactormenu.sprite6.rect.width, redactormenu.sprite6.rect.height):
                    redactormenu.sprite6.image = redactormenu.but6.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite7.rect.x, redactormenu.sprite7.rect.y,
                            redactormenu.sprite7.rect.width, redactormenu.sprite7.rect.height):
                    redactormenu.sprite7.image = redactormenu.but7.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite8.rect.x, redactormenu.sprite8.rect.y,
                            redactormenu.sprite8.rect.width, redactormenu.sprite8.rect.height):
                    redactormenu.sprite8.image = redactormenu.but8.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite9.rect.x, redactormenu.sprite9.rect.y,
                            redactormenu.sprite9.rect.width, redactormenu.sprite9.rect.height):
                    redactormenu.sprite9.image = redactormenu.but9.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            redactormenu.sprite10.rect.x, redactormenu.sprite10.rect.y,
                            redactormenu.sprite10.rect.width, redactormenu.sprite10.rect.height):
                    redactormenu.sprite10.image = redactormenu.but10.get_idle()

        redactormenu.render(screen)
        redactormenu_sprites.draw(screen)

        redactormenu.txt5.render(screen)
        redactormenu.txt6.render(screen)
        redactormenu.txt7.render(screen)
        redactormenu.txt8.render(screen)
        redactormenu.txt9.render(screen)
        redactormenu.txt10.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_boardmenu():
    boardmenu = BoardMenu(WIDTH, HEIGHT)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dotcheck(event.pos[0], event.pos[1], boardmenu.sprite6.rect.x, boardmenu.sprite6.rect.y,
                            boardmenu.sprite6.rect.width, boardmenu.sprite6.rect.height):
                    map = load_map('map1')
                    if map[0] != 'empty':
                        start_game(map[1], 1)
                        MAPS[0] = map[0]
                    else:
                        MAPS[0] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], boardmenu.sprite7.rect.x, boardmenu.sprite7.rect.y,
                            boardmenu.sprite7.rect.width, boardmenu.sprite7.rect.height):
                    map = load_map('map2')
                    if map[0] != 'empty':
                        start_game(map[1], 2)
                        MAPS[1] = map[0]
                    else:
                        MAPS[1] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], boardmenu.sprite8.rect.x, boardmenu.sprite8.rect.y,
                            boardmenu.sprite8.rect.width, boardmenu.sprite8.rect.height):
                    map = load_map('map3')
                    if map[0] != 'empty':
                        start_game(map[1], 3)
                        MAPS[2] = map[0]
                    else:
                        MAPS[2] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], boardmenu.sprite9.rect.x, boardmenu.sprite9.rect.y,
                            boardmenu.sprite9.rect.width, boardmenu.sprite9.rect.height):
                    map = load_map('map4')
                    if map[0] != 'empty':
                        start_game(map[1], 4)
                        MAPS[3] = map[0]
                    else:
                        MAPS[3] = 'empty'

                if dotcheck(event.pos[0], event.pos[1], boardmenu.sprite10.rect.x, boardmenu.sprite10.rect.y,
                            boardmenu.sprite10.rect.width, boardmenu.sprite10.rect.height):
                    map = load_map('map5')
                    if map[0] != 'empty':
                        start_game(map[1], 5)
                        MAPS[4] = map[0]
                    else:
                        MAPS[4] = 'empty'

            elif event.type == pygame.MOUSEMOTION:
                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite6.rect.x, boardmenu.sprite6.rect.y,
                            boardmenu.sprite6.rect.width, boardmenu.sprite6.rect.height):
                    boardmenu.sprite6.image = boardmenu.but6.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite7.rect.x, boardmenu.sprite7.rect.y,
                            boardmenu.sprite7.rect.width, boardmenu.sprite7.rect.height):
                    boardmenu.sprite7.image = boardmenu.but7.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite8.rect.x, boardmenu.sprite8.rect.y,
                            boardmenu.sprite8.rect.width, boardmenu.sprite8.rect.height):
                    boardmenu.sprite8.image = boardmenu.but8.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite9.rect.x, boardmenu.sprite9.rect.y,
                            boardmenu.sprite9.rect.width, boardmenu.sprite9.rect.height):
                    boardmenu.sprite9.image = boardmenu.but9.get_pressed()

                if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite10.rect.x, boardmenu.sprite10.rect.y,
                            boardmenu.sprite10.rect.width, boardmenu.sprite10.rect.height):
                    boardmenu.sprite10.image = boardmenu.but10.get_pressed()


                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite6.rect.x, boardmenu.sprite6.rect.y,
                            boardmenu.sprite6.rect.width, boardmenu.sprite6.rect.height):
                    boardmenu.sprite6.image = boardmenu.but6.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite7.rect.x, boardmenu.sprite7.rect.y,
                            boardmenu.sprite7.rect.width, boardmenu.sprite7.rect.height):
                    boardmenu.sprite7.image = boardmenu.but7.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite8.rect.x, boardmenu.sprite8.rect.y,
                            boardmenu.sprite8.rect.width, boardmenu.sprite8.rect.height):
                    boardmenu.sprite8.image = boardmenu.but8.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite9.rect.x, boardmenu.sprite9.rect.y,
                            boardmenu.sprite9.rect.width, boardmenu.sprite9.rect.height):
                    boardmenu.sprite9.image = boardmenu.but9.get_idle()

                if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            boardmenu.sprite10.rect.x, boardmenu.sprite10.rect.y,
                            boardmenu.sprite10.rect.width, boardmenu.sprite10.rect.height):
                    boardmenu.sprite10.image = boardmenu.but10.get_idle()

        boardmenu.render(screen)
        boardmenu_sprites.draw(screen)

        boardmenu.txt6.render(screen)
        boardmenu.txt7.render(screen)
        boardmenu.txt8.render(screen)
        boardmenu.txt9.render(screen)
        boardmenu.txt10.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


def dotcheck(x, y, rx1, ry1, width, height):
    if rx1 <= x <= rx1 + width and ry1 <= y <= ry1 + height:
        return True


def hexfind(cords, centers):
    x, y = cords
    best_range = (-1, -1, 1000000)
    for i in range(len(centers)):
        for j in range(len(centers[i])):
            u, v = centers[i][j]
            dots = ((u - x) ** 2 + (v - y) ** 2) ** 0.5
            if dots < best_range[2]:
                best_range = (i, j, dots)
    return best_range[0], best_range[1]


but1 = Button('play', 200, 220)
sprite1 = but1.get_sprite()
txt1 = Text('PLAY', 265, 230, 55, (255, 255, 255))

but3 = Button('settings', 200, 360)
sprite3 = but3.get_sprite()
txt3 = Text('SETTINGS', 265, 370, 55, (255, 255, 255))

but2 = Button('redactor', 200, 290)
sprite2 = but2.get_sprite()
txt2 = Text('EDIT', 265, 300, 55, (255, 255, 255))

but4 = Button('turnoff', 200, 430)
sprite4 = but4.get_sprite()
txt4 = Text('QUIT', 265, 440, 55, (255, 255, 255))


but_sprites.add(sprite1, sprite2, sprite3, sprite4)

running = True
fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dotcheck(event.pos[0], event.pos[1], sprite1.rect.x, sprite1.rect.y, sprite1.rect.width,
                        sprite1.rect.height):
                start_boardmenu()
            elif dotcheck(event.pos[0], event.pos[1], sprite2.rect.x, sprite2.rect.y, sprite2.rect.width,
                          sprite2.rect.height):
                start_redactormenu()
            elif dotcheck(event.pos[0], event.pos[1], sprite3.rect.x, sprite3.rect.y, sprite3.rect.width,
                          sprite3.rect.height):
                pass
            elif dotcheck(event.pos[0], event.pos[1], sprite4.rect.x, sprite4.rect.y, sprite4.rect.width,
                          sprite4.rect.height):
                pygame.quit()
        elif event.type == pygame.MOUSEMOTION:
            if dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], sprite1.rect.x, sprite1.rect.y,
                        sprite1.rect.width, sprite1.rect.height):
                sprite1.image = but1.get_pressed()
            elif dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], sprite2.rect.x, sprite2.rect.y,
                          sprite2.rect.width, sprite2.rect.height):
                sprite2.image = but2.get_pressed()
            elif dotcheck(event.pos[0], event.pos[1], sprite3.rect.x, sprite3.rect.y, sprite3.rect.width,
                          sprite3.rect.height):
                sprite3.image = but3.get_pressed()
            elif dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], sprite4.rect.x, sprite4.rect.y,
                          sprite4.rect.width, sprite4.rect.height):
                sprite4.image = but4.get_pressed()

            if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], sprite1.rect.x, sprite1.rect.y,
                            sprite1.rect.width, sprite1.rect.height):
                sprite1.image = but1.get_idle()
            if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], sprite2.rect.x, sprite2.rect.y,
                            sprite2.rect.width, sprite2.rect.height):
                sprite2.image = but2.get_idle()
            if not dotcheck(event.pos[0], event.pos[1], sprite3.rect.x, sprite3.rect.y, sprite3.rect.width,
                            sprite3.rect.height):
                sprite3.image = but3.get_idle()
            if not dotcheck(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], sprite4.rect.x, sprite4.rect.y,
                            sprite4.rect.width, sprite4.rect.height):
                sprite4.image = but4.get_idle()


    screen.blit(fon, (0, 0))
    txt1.render(screen)
    txt2.render(screen)
    txt3.render(screen)
    txt4.render(screen)

    but_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()
