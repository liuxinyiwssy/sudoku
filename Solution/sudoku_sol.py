import numpy as np
import copy
import time

sudo_que = np.array(
    [[0, 0, 5, 3, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 2, 0], [0, 7, 0, 0, 1, 0, 5, 0, 0],
     [4, 0, 0, 0, 0, 5, 3, 0, 0], [0, 1, 0, 0, 7, 0, 0, 0, 6], [0, 0, 3, 2, 0, 0, 0, 8, 0],
     [0, 6, 0, 5, 0, 0, 0, 0, 9], [0, 0, 4, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 9, 7, 0, 0]])


class sudoku_sol:
    sudomap = np.zeros([9, 9], int)  # 数独矩阵
    sudomap_history = []  # 循环迭代分支的历史数独矩阵，用于回溯
    sudomap_history_count = 0  # 循环迭代分支的次数
    sudomap_branch_location = []  # 循环迭代分支点的位置以及其他的信息
    blank_sol = [[[] for i in range(9)] for j in range(9)]  # 数据矩阵中空格的解
    blank_sol_history = []  # 循环迭代分支的历史空格解
    blank_sol_count = np.zeros([9, 9], int)  # 数独矩阵中空格解的个数

    # 初始化数独矩阵
    def __init__(self, sudomap):
        self.sudomap = sudomap

    # 检查（num_x,num_y）空格是否可以填入数字num，并返回True 或 False
    def check_number(self, num, num_x, num_y):
        a = np.where(self.sudomap[num_x, :] == num)
        b = np.where(self.sudomap[:, num_y] == num)
        grid_x = int(num_x / 3) + 1
        grid_y = int(num_y / 3) + 1
        c = np.where(
            self.sudomap[3 * (grid_x - 1):3 * grid_x, 3 * (grid_y - 1):3 * grid_y] == num)
        if len(a[0]) or len(b[0]) or len(c[0]):
            return False
        else:
            return True

    # 寻找数独中空格可以填入的数字并保存到三维列表blank_sol中
    def find_blank_sol(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if not self.sudomap[i, j]:
                    num = []
                    for k in range(1, 10):
                        if self.check_number(k, i, j):
                            num.append(k)
                    self.blank_sol[i][j] = num
                else:
                    self.blank_sol[i][j] = []
                self.blank_sol_count[i, j] = len(self.blank_sol[i][j])

    # 填入只有一种可能解的空格，并更新空格的可能解
    def fill_blank_single(self):
        for i in range(0, 9):
            for j in range(0, 9):
                single_blank_sol = self.blank_sol[i][j]
                if len(single_blank_sol) == 1:
                    self.sudomap[i, j] = single_blank_sol[0]
                    return 1
        return 0

    # 填入存在多种可能解的空格中的一种可能解
    def fill_blank_multi(self):
        a = 2
        while not len(np.where(self.blank_sol_count == a)[0]):
            a += 1
        num_x = np.where(self.blank_sol_count == a)[0][0]
        num_y = np.where(self.blank_sol_count == a)[1][0]
        b = copy.deepcopy(self.sudomap)
        self.sudomap_history.append(b)
        c = copy.deepcopy(self.blank_sol)
        self.blank_sol_history.append(c)
        self.sudomap_branch_location.append([num_x, num_y, 0, a])
        self.sudomap[num_x, num_y] = self.blank_sol[num_x][num_y][0]
        self.sudomap_history_count += 1

    # 判断数独中空格是否都被填入
    def sign_fill_all(self):
        a = np.where(self.sudomap == 0)
        if len(a[0]) == 0:
            return True
        else:
            return False

    # 判断数独是否满足规则
    def sudomap_feasible(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if not (self.sudomap[i, j] or self.blank_sol[i][j]):
                    return False
        return True

    # 循环迭代求出数独解
    def loop_iteration(self):
        while True:
            while True:
                self.find_blank_sol()
                if not self.fill_blank_single():
                    break
            if not self.sign_fill_all():
                if self.sudomap_feasible():
                    self.fill_blank_multi()
                else:
                    while True:
                        last_num_location = self.sudomap_branch_location[self.sudomap_history_count - 1]
                        num_x = last_num_location[0]
                        num_y = last_num_location[1]
                        if last_num_location[2] < last_num_location[3] - 1:
                            self.sudomap_branch_location[self.sudomap_history_count - 1][2] += 1
                            self.sudomap = copy.deepcopy(self.sudomap_history[self.sudomap_history_count - 1])
                            self.blank_sol = copy.deepcopy(self.blank_sol_history[self.sudomap_history_count - 1])
                            self.sudomap[num_x, num_y] = self.blank_sol[num_x][num_y][last_num_location[2]]
                            break
                        else:
                            del self.sudomap_history[self.sudomap_history_count - 1]
                            del self.sudomap_branch_location[self.sudomap_history_count - 1]
                            del self.blank_sol_history[self.sudomap_history_count - 1]
                            self.sudomap_history_count -= 1
            else:
                break

sudo = sudoku_sol(sudo_que)
sudo.loop_iteration()
print(sudo.sudomap)
