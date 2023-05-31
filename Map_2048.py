import numpy as np
import random as rd


class MapClass:
    n = 0
    Map = None
    Map_prev = None
    input_ = None
    flag = True
    win_flag = False
    score = 0
    score_prev = 0
    highlight_flag = False
    result = 'playing'

    def __init__(self, n):
        self.n = n
        self.Map = np.full((n, n), 0)
        self.AddNew(2)
        self.Map_prev = self.Map.copy()  # сохранение предыдущего состояние
        self.score = 0
        self.score_prev = 0
        self.highlight_index = tuple()

    # создание начальных блоков 2 и 4 в случайном положении
    def AddNew(self, block=1):
        zero_list = np.argwhere(self.Map == 0)  # начальные координаты помещаются в (zero_list)
        rd_list = list()  # лист для эффекта выделения

        for _ in range(block):
            i, j = rd.choice(zero_list)
            self.Map[i, j] = rd.choice([2] * 10 + [4])
            zero_list = zero_list[~np.all(zero_list == [i, j], axis=1)]  # zero_list указанные выше координаты удаляются
            rd_list.append((i, j))
        return rd_list[0]

    def step(self, detail):
        inputs = str(detail.keysym)[0]

        temp_score = self.score
        temp_prev = self.Map.copy()

        if inputs == 'U':
            self.Up()

        elif inputs == 'D':
            self.Down()

        elif inputs == 'L':
            self.Left()

        elif inputs == 'R':
            self.Right()

        else:
            print("Error\n")
            return

        if np.array_equal(temp_prev, self.Map) is True:
            return

        self.Map_prev = temp_prev.copy()
        self.score_prev = temp_score

        # результаты
        if self.iswin():
            self.result = 'win'

        if not self.isfull():
            """highlight_flag :: on/off эффект выделения"""
            self.highlight_flag = True
            """highlight_index :: index эффекта выделения"""
            self.highlight_index = self.AddNew()

        if self.isfull():
            if self.islose():
                self.result = 'full'
        return

    # удаление пустого пространства
    def move_Up(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[:, i]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[:, i] = np.concatenate([tmp_values, tmp_zeros])

    def move_Down(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[:, i]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[:, i] = np.concatenate([tmp_zeros, tmp_values])

    # соединение блоков
    def merge_UpDown(self, line1, line2):
        for i in range(len(self.Map)):
            if self.Map[line1, i] == self.Map[line2, i]:
                self.Map[line1, i] = 0
                self.Map[line2, i] = self.Map[line2, i] * 2
                self.score += self.Map[line2, i]

    # удаление пустого пространства
    def move_Left(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[i, :]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[i, :] = np.concatenate([tmp_values, tmp_zeros])

    def move_Right(self):
        for i in range(len(self.Map)):
            tmp_list = self.Map[i, :]
            tmp_zeros = tmp_list[tmp_list == 0]
            tmp_values = tmp_list[tmp_list != 0]
            self.Map[i, :] = np.concatenate([tmp_zeros, tmp_values])

    # соединение блоков
    def merge_LeftRight(self, line1, line2):
        for i in range(len(self.Map)):
            if self.Map[i, line1] == self.Map[i, line2]:
                self.Map[i, line1] = 0
                self.Map[i, line2] = self.Map[i, line2] * 2
                self.score += self.Map[i, line2]

    # 1
    def Up(self):
        # print('input : вверх\n')
        for i in range(1, len(self.Map)):  # если 4*4    ==>    1,0    2,1    3,2
            self.move_Up()
            self.merge_UpDown(i, i - 1)

    # 2
    def Down(self):
        # print('input : вниз\n')
        for i in range(len(self.Map) - 1, 0, -1):  # если 4*4    ==>    2,3     1,2     0,1
            self.move_Down()
            self.merge_UpDown(i - 1, i)

    # 3
    def Left(self):
        # print('input : влево\n')
        for i in range(1, len(self.Map)):  # если 4*4    ==>    1,0    2,1    3,2
            self.move_Left()
            self.merge_LeftRight(i, i - 1)

    # 4
    def Right(self):
        # print('input : вправо\n')
        for i in range(len(self.Map) - 1, 0, -1):  # если 4*4    ==>    2,3     1,2     0,1
            self.move_Right()
            self.merge_LeftRight(i - 1, i)

    # boolean
    def iswin(self):
        if 2048 in self.Map and self.win_flag is False:
            self.win_flag = True
            return True

    def isfull(self):
        if len(self.Map[self.Map == 0]) == 0:
            return True
        return False

    def islose(self):
        for i in range(0, len(self.Map)):
            for j in range(0, len(self.Map)):
                if j != len(self.Map) - 1 and self.Map[i][j] == self.Map[i][j + 1]:
                    return False
                if i != len(self.Map) - 1 and self.Map[i][j] == self.Map[i + 1][j]:
                    return False
        self.flag = False
        return True
