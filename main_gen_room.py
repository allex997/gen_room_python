"""
Created on Thu Oct 22 16:25:13 2020

@author: tormoz

# p - пустота
  d - дверь
  w - стена
  g - граница
  t - тунель
  b - лестница к боссу
"""
# тестирование
import os
#from algoritm2 import get_min_paths

import random
#from random import random as rand
from collections import deque, defaultdict
from re import findall as f
import copy as cp
from setting import *

def rl(arr: list, b=0):
    return range(b, len(arr))


ri = random.randint



# Класс направленного графа, использует представление списка смежности
class Graph:
    paths = []
    #graph = None

    def __init__(self, vertices):  # vertices
        #self.graph = graph

        # Нет. вершин
        self.V = vertices

        # словарь по умолчанию для хранения графа
        self.graph = defaultdict(list)

    # функция добавления ребра в граф
    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''Рекурсивная функция для печати всех путей от 'u' до 'd'.
    visit [] отслеживает вершины в текущем пути.
    path [] хранит актуальные вершины, а path_index является текущим
    индексом в path[]'''

    def printAllPathsUtil(self, u, d, visited, path):

        # Пометить текущий узел как посещенный и сохранить в path
        visited[list(self.graph.keys()).index(u)] = True
        path.append(u)

        # Если текущая вершина совпадает с точкой назначения, то
        # print(current path[])
        if u == d:
            # print(path)
            self.paths.append(cp.copy(path))
        else:
            # Если текущая вершина не является пунктом назначения
            # Повторить для всех вершин, смежных с этой вершиной
            for i in self.graph[u]:
                if i in list(self.graph.keys()):
                    if visited[list(self.graph.keys()).index(i)] == False:
                        self.printAllPathsUtil(i, d, visited, path)

        # Удалить текущую вершину из path[] и пометить ее как непосещенную
        path.pop()
        visited[list(self.graph.keys()).index(u)] = False

    # Печатает все пути от 's' до 'd'
    def printAllPaths(self, s, d):

        # Отметить все вершины как не посещенные
        visited = [False] * (self.V)

        # Создать массив для хранения путей
        path = []

        # Рекурсивный вызов вспомогательной функции печати всех путей
        self.printAllPathsUtil(s, d, visited, path)

# комната


class Room:
    # для основной комнаты
    rooms = []
    numberlastroom = 0

    # комната
    maps = [[]]
    tunnelsxy, diversiontunnels = {}, {}
    '''# двери
    doorxy = []
    countdoor = 0

    freedoorxy = []
    freedoor = 0

    # тунели
    links = cp.deepcopy([])
    linksdoor = []
    
    tunnelid = 0
    tunnelids = []
    tunnelsxy = {}#[]
    diversiontunnels = {}#[]
    path = []
    tunelpath = []'''
    # инциализация

    def __init__(self):

        # комната
        self.room = [[]]
        self.posx, self.posy = None, None
        self.height, self.width = None, None
        self.ids = 0

        # двери
        self.doorxy = []
        self.countdoor = 0

        self.freedoorxy = []
        self.freedoor = 0

        # тунели
        self.links = []
        self.linksdoor = []

        self.tunnelid = 0
        self.path = []
        self.tunnelids, self.tunelpath = [], []

    # получение минимального пути
    def get_min_paths(self, bpos: tuple, epos: tuple, maps2: list):
        maps = cp.deepcopy(maps2)
        cells_str = []  # пройденные ячейки
        # bpos,epos = (1,1),(3,3) # y,x
        # получаем строковое значение ячейки

        def number_cell(y, x, number, celli):
            #  номер конечной ячейки +N + направление + X + Y
            if str(celli) == '0':
                number = 0
            return str(celli) + 'N' + str(number) + 'X' + str(x) + 'Y' + str(y)

            # получаем значения из строки

        def get_string_number_cell(stroka):
            return int(f('(\d+)N', stroka)[0]), int(f('N(\d+)X', stroka)[0]), int(f('X(\d+)Y', stroka)[0]), int(f('Y(\d+)', stroka)[0])

        def li(bpos, epos, maps):
            ways = [-1, 0], [0, -1], [1, 0], [0, 1]

            def check_end():
                #ways = [-1,0],[0,-1],[1,0],[0,1]
                y5, x5 = epos
                maps[y5][x5] = '0'
                for x4, y4 in ways:
                    x3, y3 = x5+x4, y5+y4
                    if maps[y3][x3] == 'p':
                        return False

                return True

            Stack = deque()
            Stack.append(bpos)

            i = 0
            maps[bpos[0]][bpos[1]] = str(i)

            #global cells_str
            while len(Stack):
                cell = Stack.popleft()
                # i+=1
                for n in range(len(ways)):  # x,y

                    x, y = ways[n][0], ways[n][1]

                    x2, y2 = x+cell[1], y+cell[0]

                    if y2 > -1 and y2 < len(maps):
                        if x2 > -1 and x2 < len(maps[y2]):

                            if maps[y2][x2] == 'p':
                                celli = str(int(maps[cell[0]][cell[1]])+1)

                                # print(get_string_number_cell(nstr))
                                nstr = number_cell(y2, x2, n, celli)
                                if type(nstr) == str:
                                    get_string_number_cell(nstr)
                                if not (nstr in cells_str):
                                    cells_str.append(nstr)

                                Stack.append((y2, x2))
                                maps[y2][x2] = celli  # str(i)
                                if check_end():
                                    return maps

        map2 = li(bpos, epos, maps)

        def get_graph(maps):  # bpos,epos,maps
            #global maps
            #global cells_str
            ways = [-1, 0], [0, -1], [1, 0], [0, 1]
            paths = []
            path = []
            # point = epos#(epos[0],epos[1])

            graph = {}

            def create_graph(v, nd, point, maps):
                #global graph
                #ways = [-1,0],[0,-1],[1,0],[0,1]
                y5, x5 = point
                # path.append(point)
                #maps[y5][x5] = 'e'
                nstrm = number_cell(y5, x5, nd, v)  # v==maps[y5][x5]
                for n in range(len(ways)):  # x,y
                    x4, y4 = ways[n][0], ways[n][1]
                    x3, y3 = x5+x4, y5+y4
                    if y3 > -1 and y3 < len(maps) and y5 > -1 and y5 < len(maps):
                        if x3 > -1 and x3 < len(maps[y3]) and x5 > -1 and x5 < len(maps[y5]):

                            # try:
                            if maps[y3][x3].isdigit():  # вылетает
                                # если вокруг есть число и оно ни начало и ни конец
                                if int(maps[y5][x5]) < int(maps[y3][x3]) or int(maps[y3][x3]) == 0:
                                    #point = (y3,x3)

                                    nstr = number_cell(y3, x3, n, maps[y3][x3])
                                    if not(nstrm in list(graph.keys())):
                                        graph[nstrm] = []

                                    if not (nstr in graph[nstrm]):
                                        graph[nstrm].append(nstr)

            #global bpos,epos
            create_graph(0, 5, (bpos[0], bpos[1]), maps)
            for cs in cells_str:
                if type(cs) == str:
                    v, n, x, y = get_string_number_cell(cs)

                    create_graph(v, n, (y, x), maps)  # point

            create_graph(0, 5, (epos[0], epos[1]), maps)

            return graph
            # if type(myVariable) == int:
            # pass

        graph = get_graph(map2)

        g = Graph(len(graph.keys()))
        #g = Graph(graph)
        for i, v in graph.items():
            for e in v:
                g.addEdge(i, e)

        s = list(graph.keys())[0]  # 'A'#'A'
        d = list(graph.keys())[-1]  # 'D'
        #print ("Ниже приведены все различные пути от {} до {} :".format(s, d))
        g.printAllPaths(s, d)
        # print(len(g.paths))
        # найти пути с минимальным количество поворотов

        def min_rotate(paths):
            rotates = {}
            # получаем направления из строкового значения
            for path in range(len(paths)):
                rotates[path] = []
                for point in paths[path][1:-1]:
                    if type(point) == str:
                        v, n, x, y = get_string_number_cell(
                            point)  # n - направление
                        rotates[path].append(n)
                    # if n2 != n:

                    #    n2 = cp(n)
            rot = 0
            r = 5
            # получаем количество поворотов на каждом пути
            for path in rotates:
                for rotate in rotates[path]:
                    if r != rotate:
                        r = cp.copy(rotate)
                        rot += 1
                rotates[path] = cp.copy(rot-1)
                rot, r = 0, 5

            # выбиараем пути с минимальным количестом поворотов
            minrotate = min([rotates[key] for key in rotates])
            paths2 = [key for key in rotates if rotates[key] == minrotate]

            # пути с минимальным расстоянием
            minpath = min([len(paths[i]) for i in paths2])
            minpaths = [i for i in paths if len(i) == minpath]

            # получаем координаты в виде (y,x)
            for mp in range(len(minpaths)):
                for cell in range(len(minpaths[mp])):
                    if type(minpaths[mp][cell]) == str:
                        v, n, x, y = get_string_number_cell(minpaths[mp][cell])
                        minpaths[mp][cell] = (y, x)

            return minpaths  # y,x
            # return
            #    pass

            #rotates[path] = rotate
            # if <minrotate or minrotate==None:
            # pass

        # print_color_map(maps,'xx')
        return min_rotate(g.paths)  # y,x

    # создание комнаты внутриклассовая
    def cr_room(self, maxw: int, maxh: int, w1: str = 'g', p1: str = 'p'):

        probn = [[p1 for w in range(maxw)] for h in range(maxh)]

        # делаем границы
        probn[-1] = [w1 for w in range(maxw)]
        probn[0] = [w1 for w in range(maxw)]
        # границы по бокам
        for h in range(len(probn)):
            for w in range(len(probn[h])):
                if w == 0:
                    probn[h][w] = w1
                if w == maxw-1:
                    probn[h][w] = w1
        self.room = probn

    # вывод карты(комнаты)
    def print_map(self, s: str = ''):
        maps = self.maps
        for y in maps:
            for x in y:
                if not(s in str(x)):  # if not(s == str(x)):
                    print(x, end=' ')
                else:
                    print(' ', end=' ')
            print()

    # создание комнаты
    def create_room(self, n: int = 1, wb: int = ri(minwb, maxwb), hb: int = ri(minhb, maxhb), posx: int = ri(0, maxw-1), posy: int = ri(0, maxh-1)):
        self.ids = n
        maps = self.maps
        global mindoor  # , rooms
        #global wb,hb
        rr = random.randint
        self.width, self.height = wb, hb  # ширина и высота комнаты

        self.cr_room(wb, hb, 'w', 'p%s' % n)
        room = self.room

        def check_maps(room):  # проверяем свободно ли место
            #global maps
            maps = self.maps
            # проверяем свободно ли место
            for y in range(len(room)):
                for x in range(len(room[y])):
                    x1 = posx + x
                    y1 = posy + y
                    # если выходит за границы
                    if x1 > len(maps[0])-1 or -1 > x1 or y1 > len(maps)-1 or -1 > y1:
                        return False
                    # print(len(maps))
                    # print(len(maps[y1]))
                    # print(y1)
                    # print(x1)
                    if not (maps[y1][x1] in ['g', 'p']):
                        return False  # место занято
            return True

        # print(check_maps(room))
        cm = check_maps(room)
        if cm:  # добавляем комнату
            for y in range(len(room)):
                for x in range(len(room[y])):
                    x1 = posx + x
                    y1 = posy + y
                    if maps[y1][x1] != 'g':
                        maps[y1][x1] = room[y][x]
            self.room, self.posx, self.posy = room, posx, posy
            return
            # return room,posx,posy
        self.room, self.posx, self.posy = None, None, None
        return

    # создание дверей
    def create_random_door(self, mainself):
        #global rooms,posxA,posyA,mindoor,maps
        global mindoor
        #room, posx, posy, maps  = self.room, self.posx, self.posy, self.maps
        room, posx, posy, maps = self.room, self.posx, self.posy, mainself.maps
        # maxdoor = 0 #4 максимальное количество дверей

        maxwelldoor = 4
        # считаем количество стен для дверей
        # получаем координаты стен
        v1, v2, g1, g2 = [], [], [], []
        '''
        g1 - координаты верхний части комнаты 
        g2 - координаты нижний части комнаты 
        v1 - левой части комнаты 
        v2 - правой части комнаты 
        '''

        for y in range(len(room)):
            for x in range(len(room[y])):
                x1 = posx + x
                y1 = posy + y
                if maps[y1][x1] == 'w':
                    if maps[y1][x1+1] == 'w' and maps[y1][x1-1] == 'w':  # gorizontal
                        if maps[y1+1][x1] == 'p':
                            g2.append([x1, y1])  # x1
                        if maps[y1-1][x1] == 'p':
                            g1.append([x1, y1])

                    if maps[y1+1][x1] == 'w' and maps[y1-1][x1] == 'w':
                        if maps[y1][x1-1] == 'p':
                            v1.append([x1, y1])  # y1
                        if maps[y1][x1+1] == 'p':
                            v2.append([x1, y1])

        maxwelldoor -= sum([1 for i in [g1, g2, v1, v2] if len(i) < 1])
        
        ### --- FiX ---
        doorxy = []
        while len(doorxy) < 1:
            count_doors = random.randint(
                mindoor, maxwelldoor) if maxwelldoor >= mindoor else 0
            print(f'count_doors {count_doors} self.ids {self.ids}') #FiXME count_doors 1 self.ids 3 
            wells2 = [g1, g2, v1, v2]
            wells = []
            for r in range(count_doors-1):
                i = random.randint(0, len(wells2)-1)
                el = wells2[i]  # random.choice(wells2)
                wells.append(el)#FIXME !=wells
                print(f'wells {wells} self.ids {self.ids}')
                wells2.remove(el)
        ### --- FiX ---

            doorxy = []
            for w in wells:
                #print(f'len(w) {len(wells)}   self.ids {self.ids}')
                if len(w) > 0:
                    i = random.randint(0, len(w)-1)#-1
                    yd,xd  = w[i]  # random.choice(w)
                    ##print(f'w[i] {w[i]}   self.ids {self.ids}')
                    maps[xd][yd] = 'd'
                    doorxy.append([yd,xd])
                    #print(f'doorxy {doorxy}   self.ids {self.ids}')

        maxwelldoor = len(doorxy)
        # баг комната может быть без дверей вроде решил
        self.doorxy, self.countdoor = doorxy, maxwelldoor
        self.room, self.maps = room, maps

        self.freedoor, self.freedoorxy = maxwelldoor, cp.copy(doorxy)
        #print(f'self.freedoorxy {self.freedoorxy}   self.ids {self.ids}')

    # связываем комнаты
    def create_link_room(self, room, mainroom):
        #room2 = [cp.deepcopy(room) for room in mainroom.rooms if room.ids == self.ids][0]
        # room = cp.copy(room2) doorxy links freedoor
        def find_nearest_door(room2, room1=self):
            room = cp.copy(room2)
            mind = None  # координаты дверей
            mindist = None  # дистанция [x,y]
            mindist2 = None
            # self.doorxy room.doorxy
            for sxy in rl(room1.freedoorxy):
                for rxy in rl(room.freedoorxy):
                    dx = abs(room1.freedoorxy[sxy][0]-room.freedoorxy[rxy][0])
                    dy = abs(room1.freedoorxy[sxy][1]-room.freedoorxy[rxy][1])
                    if not(mindist == None):
                        if dx < mindist[0] or dy < mindist[1]:
                            if abs(dx+dy) < mindist2:
                                mindist2 = abs(dx+dy)
                                mindist = [dx, dy]
                                mind = [room1.freedoorxy[sxy],
                                        room.freedoorxy[rxy]]
                    else:
                        mindist2 = abs(dx+dy)
                        mindist = [dx, dy]
                        mind = [room1.freedoorxy[sxy], room.freedoorxy[rxy]] # room.freedoorxy[rxy] неправильная 2 раз

            # удалить координаты дверей неправильно работает
            # отрисовать их y x
            # print(mind[0][0])
            # удаляем из свободной двери
            
            self.freedoorxy.remove(mind[0])
            room.freedoorxy.remove(mind[1])

            #print(f'self freedoorxy{self.freedoorxy} room freedoorxy {room.freedoorxy}')
            #FM
            #self.freedoorxy.remove(mind[1])
            #room.freedoorxy.remove(mind[0])

            #print(f'self mind[0]{mind[0]} room mind[1]{mind[1]}')

            # добавляем координаты дверей FIXME
            self.linksdoor.append(mind[1])
            room.linksdoor.append(mind[0])
            #FM
            room.linksdoor.append(mind[1])
            self.linksdoor.append(mind[0])###

            # self.maps[mind[0][0]][mind[0][1]] = 'v' # test
            #self.maps[mind[1][0]][mind[1][1]] = 'v'
            mainroom.maps[mind[0][0]][mind[0][1]] = 'v'
            mainroom.maps[mind[1][0]][mind[1][1]] = 'v'
            # room.maps.
            return room

        # тут косяк
        if not (room.ids in self.links) and not (self.ids in room.links):
            #mainroom2 = cp.deepcopy(mainroom)
            #link = []
            self.links.append(cp.deepcopy(room.ids))  # с этим что-то ни так
            room.links.append(cp.deepcopy(self.ids))
            #mainroom = mainroom2
            self.freedoor -= 1
            room.freedoor -= 1
            room = find_nearest_door(room)
            #mainroom.maps = room.maps
            #self = room2
            mainroom.rooms[[roomz for roomz in range(
                len(mainroom.rooms)) if mainroom.rooms[roomz].ids == room.ids][0]] = room

            return True  # связываем комнаты
        else:
            return False

    # вывод цветной карты(комнаты)
    def print_color_map(self, maps: list, s: str = ''):
        import colorama
        from colorama import Fore, Back

        colorama.init()
        for y in maps:
            for x in y:
                if not(s in str(x)):  # if not(s == str(x)):
                    if x == 'w':
                        # print(colored(x, 'red'),end=' ')#, end=' ')
                        print(Fore.RED + x, end=' ')
                    elif x == 't':
                        print(Fore.BLUE + x, end=' ')
                    elif x == 'd':
                        print(Fore.GREEN + x, end=' ')
                    elif x == 'g':
                        print(Fore.CYAN + x, end=' ')
                    elif x == 'b':
                        print(Fore.BLACK + x, end=' ')

                else:
                    print(' ', end=' ')
            print()

    # создание связи дверей внутриклассовый
    def create_link_door(self, mainroom):
        #rooms = mainroom.rooms
        #mainroom2 = cp.copy(mainroom)

        # если у комнаты есть свободные двери и нету свизи с другой дверью
        #mainroom = cp.copy(mainroom2)
        without_link_room = [room for room in mainroom.rooms if not(self.ids in room.links) and not(
            room.ids in self.links)]  # не связанные комнаты # тут ошибка
        # print()
        # если у комнаты есть свободные двери и данная комната ни являеться
        without_link_room = [
            room for room in without_link_room if room.freedoor > 0 and self.ids != room.ids]
        # print()
        if len(without_link_room) > 0:
            without_link_room = cp.deepcopy(without_link_room[ri(
                0, len(without_link_room)-1)])  # берём случайную комнату

        if self.freedoor > 0 and type(without_link_room) != list:
            # создаём связь
            return self.create_link_room(without_link_room, mainroom)
        return False
        #self.rooms = rooms

    # создание тунеля в главной комнате
    def create_tunel(self, mainroom):
        #FIXME 
        b = self.create_link_door(mainroom)  # тут ошибка 
        maps = mainroom
        if b:
            maps.path = []
            maps.tunnelid += 1
            maps.tunnelids.append(maps.tunnelid)
            # 0 - все направления 1 - нет направления 2-3 - направления
            maps.diversiontunnels[maps.tunnelid] = random.randint(0, 3)
            for r in mainroom.rooms:
                for d in r.linksdoor:
                    y, x = d[0], d[1]  # d[1], d[0]
                    #ys,xs = [y-1,y+1],[x-1,x+1]
                    for yz in [y-1, y+1, y]:
                        for xz in [x-1, x+1, x]:
                            # y x
                            if maps.maps[yz][xz] == 'p' and (yz == y or xz == x):
                                maps.maps[yz][xz] = 't'

                                if not(maps.tunnelid in maps.tunnelsxy):
                                    maps.tunnelsxy[maps.tunnelid] = []
                                maps.tunnelsxy[maps.tunnelid].append([xz, yz])
                                maps.path.append([xz, yz])
                r.linksdoor = [] #FM
            if len(maps.path) > 1:
                cd = cp.deepcopy
                # ошибка
                tunels = maps.get_min_paths(
                    maps.path[0][::-1], maps.path[1][::-1], maps.maps)  # mapsd

                # tunels = get_min_paths(
                #    maps.path[0][::-1], maps.path[1][::-1], maps.maps)
                tunel = tunels[ri(0, len(tunels)-1)]
                maps.tunelpath.append(tunel)

                for y, x in tunel:
                    maps.maps[y][x] = 't'
                    mainroom.maps[y][x] = 't'
        mainroom = maps

    # создание комнаты внутри
    def create_room_inside(self, width: int = None, height: int = None, posx: int = None, posy: int = None):
        room = Room()  # создание комнаты
        room.maps = self.maps
        self.numberlastroom += 1  # счётчик комнат
        # None in [width,height,posx,posy]
        if None in [width,height,posx,posy]:#width == None or height == None or posx == None or posy == None:
            room.create_room(self.numberlastroom)
        else:
            room.create_room(self.numberlastroom, width, height, posx, posy)

        if room.room != None:  # если комната создалась
            room.create_random_door(self)  # делаем двери
        # добавляем комнату в массив комнат
        self.rooms.append(cp.deepcopy(room))

#        self.create_tunel(self)  # self room.create_tunel()
        room.create_tunel(self)  # создаём тунель

#ненужная функция
def create_path(p1, p2, maps):  # p1,p2 = [x,y]
    x, y = p1
    x2, y2 = p2

    ways = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    rand = random.randint(0, len(ways)-1)
    b = True
    while b:
        nx, ny = ways[rand]
        if maps[y+ny][x+nx] == 'p':
            maps[y+ny][x+nx] == 'n'
            b = False
        else:
            ways.remove(ways[rand])
            b = True
    return maps


def main():
    #b = True
    # while b:
    #    try:
    global maxw, maxh
    # создание основной комнаты
    maps = Room()
    maps.cr_room(maxw, maxh)
    maps.maps = maps.room

    # создание комнаты внутри
    maps.create_room_inside(4, 4, 0, 0)
    maps.create_room_inside(4, 4, 16, 16)
    maps.create_room_inside(4,4,8,8)
    # maps.create_room_inside(4,4,8,4)
    # except:
    #    b = False
    # for i in range(100):
    #    maps.create_room_inside()
    # maps.create_room_inside()
    # maps.create_room_inside()
    maps.print_map('p')


    # print(n)
main()
os.system('pause')
