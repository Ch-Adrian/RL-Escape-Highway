import numpy as np

class Highway:
    def __init__(self, start_pos, height=10, width=5):
        self.WIDTH = width
        self.HEIGHT = height
        self.start_position = start_pos
        self.win_positions = self.win_positions()
        self.lose_positions = self.lose_positions()
        self.blocked_positions = self.blocked_positions()

        self.road = np.zeros([self.HEIGHT, self.WIDTH])
        self.setup_grid()

    def reset(self):
        pass

    def win_positions(self):
        positions = []

        for i in range(0, self.WIDTH):
            positions.append((0, i))
        
        return positions 

    def lose_positions(self):
        positions = []
        distances = []
        w = self.WIDTH * 3//4

        for level in range(2, self.HEIGHT-3, 2):
            distances.append(int(w))
            w += (w+w*np.random.rand())%self.WIDTH
        
        # print(distances)

        for i, level in enumerate(range(2, self.HEIGHT-3, 2)):
            for column in range(distances[i], int(distances[i]+self.WIDTH//3+2)):
                positions.append((level, column%self.WIDTH))
        # print("lose_positions: ", positions)
        
        return positions

    def blocked_positions(self):
        positions = []
        positions.append((3,2))
        positions.append((3,4))

        return positions

    def update_lose_positions(self):
        for lose_position in self.lose_positions:
            self.road[lose_position] = 0

        for lose_position in self.lose_positions:
            self.road[lose_position[0], (lose_position[1]+1)%self.WIDTH] = -1

    def tick(self):
        self.update_lose_positions()

    def setup_grid(self):
        self.road = np.zeros([self.HEIGHT, self.WIDTH])

        for pos in self.win_positions:
            self.road[pos] = 1

        for pos in self.lose_positions:
            self.road[pos] = -1

    def check_possible_move(self, start_pos, end_pos):
        if abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1]) != 1:
            return False
        if end_pos[0] >= self.HEIGHT or end_pos[0] <= -1: return False 
        if end_pos[1] >= self.WIDTH or end_pos[1] <= -1: return False 

        for blocked_pos in self.blocked_positions:
            if end_pos == blocked_pos:
                return False 

        return True

    def show_grid(self):
        print(self.road)