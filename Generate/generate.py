import random
import numpy as np
import copy


class sudoku_generate:
    sudomap = np.zeros([9, 9], int)
    sudomap_state = np.zeros([9, 9], int)
    sudomap_no = np.zeros([9, 9], int)
    sudomap_back_loc = []
    sign_back = 0

    # 检查第row行和第col列是否有数字num
    def check_rule(self, num, row, col):
        count = np.where(self.sudomap[row, :] == num)
        if len(count[0]) > 0:
            return False
        count = np.where(self.sudomap[:, col] == num)
        if len(count[0]) > 0:
            return False
        return True

    # 检查第(temp_grid_x，temp_grid_y)宫格中能够填入数字num的空格，并返回坐标列表
    def check_blank(self, num, temp_grid_x, temp_grid_y):
        location = []
        for i in range(3 * (temp_grid_x - 1), 3 * temp_grid_x):
            for j in range(3 * (temp_grid_y - 1), 3 * temp_grid_y):
                state = self.sudomap_no[i, j]
                if state == 0:
                    if self.check_rule(num, i, j):
                        location.append([i, j])
        return location

    # 随机生成一个数独
    def generate(self):
        # count = 1
        num = 1
        while num <= 9:
            grid_x = 1
            grid_y = 1
            while grid_x <= 3:
                ava_location = self.check_blank(num, grid_x, grid_y)
                if ava_location:
                    [num_x, num_y] = random.choice(ava_location)
                    self.sudomap_state[num_x, num_y] = 1
                    self.sudomap[num_x, num_y] = num
                    if self.sign_back:
                        if [grid_x, grid_y] == self.sudomap_back_loc:
                            self.sudomap_no = copy.deepcopy(self.sudomap_state)
                            self.sign_back = 0
                    else:
                        self.sudomap_no = copy.deepcopy(self.sudomap_state)
                    grid_y = grid_y + 1
                    if grid_y == 4:
                        grid_x = grid_x + 1
                        grid_y = 1
                    # if count > 5000:
                    #     count = 5000
                    # print(count)
                    # print(self.sudomap)
                    # print([grid_x, grid_y])
                    # print(num)
                    # print(num_x, num_y)
                    # count = count + 1
                else:
                    if not self.sign_back:
                        self.sign_back = 1
                        self.sudomap_back_loc = [grid_x, grid_y]
                    grid_y = grid_y - 1
                    if grid_y == 0:
                        grid_x = grid_x - 1
                        grid_y = 3
                    if grid_x == 0:
                        grid_x = 3
                        grid_y = 3
                        location = np.where(self.sudomap == num - 1)
                        for i in range(0, len(location[0])):
                            self.sudomap[location[0][i], location[1][i]] = 0
                            self.sudomap_state[location[0][i], location[1][i]] = 0
                        self.sudomap_no = copy.deepcopy(self.sudomap_state)
                        self.sign_back = 0
                        self.sudomap_back_loc = []
                        num = num - 2
                        break;
                    location = np.where(
                        self.sudomap[3 * (grid_x - 1):3 * grid_x, 3 * (grid_y - 1):3 * grid_y] == num)
                    last_num_x = location[0][0] + 3 * (grid_x - 1)
                    last_num_y = location[1][0] + 3 * (grid_y - 1)
                    self.sudomap[last_num_x, last_num_y] = 0
                    self.sudomap_state[last_num_x, last_num_y] = 0
                    self.sudomap_no[last_num_x, last_num_y] = 1
            num = num + 1
