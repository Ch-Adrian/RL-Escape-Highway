import numpy as np 
from enum import Enum

class EscapistState(Enum):
    DEAD = -1 
    RUNNING = 0
    ALIVE = 1 

class Direction(Enum):
    NORTH = 1 
    EAST = 2
    SOUTH = 3 
    WEST = 4

class Grid:
    def __init__(self):
        self.WIDTH = 5
        self.HEIGHT = 10
        self.start_position = (self.HEIGHT-1, 2)
        self.win_positions = self.win_positions()
        self.lose_positions = self.lose_positions()
        self.blocked_positions = self.blocked_positions()

        self.grid = np.zeros([self.HEIGHT, self.WIDTH])
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

        for i in range(1,4):
            positions.append((5,i))
        
        return positions

    def blocked_positions(self):
        positions = []
        positions.append((3,2))
        positions.append((3,4))

        return positions 

    def setup_grid(self):
        self.grid = np.zeros([self.HEIGHT, self.WIDTH])

        for pos in self.win_positions:
            self.grid[pos] = 1

        for pos in self.lose_positions:
            self.grid[pos] = -1

    def check_possible_move(self, start_pos, end_pos):
        if abs(start_pos[0] - end_pos[0]) + abs(start_pos[1] - end_pos[1]) != 1:
            return False
        if end_pos[0] >= self.HEIGHT or end_pos[0] <= -1: return False 
        if end_pos[1] >= self.WIDTH or end_pos[1] <= -1: return False 

        for blocked_pos in self.blocked_positions:
            if end_pos == blocked_pos:
                return False 

        return True

    def check_state_in_position(self, position):
        if position in self.win_positions:
            return EscapistState.ALIVE 
        if position in self.lose_positions:
            return EscapistState.DEAD 
        return EscapistState.RUNNING 

    def show_grid(self):
        print(self.grid)

class LearningValues:
    def __init__(self, height, width):
        self.learning_values = np.zeros([height, width])
        self.learning_rate = 0.25
    
    def funcV(self, position, result):
        result = self.learning_values[position] + self.learning_rate*(result - self.learning_values[position])
        self.learning_values[position] = round(result, 5)
        return result

class Escapist:
    def __init__(self, grid):
        self.positions_all_the_way = []
        self.status = EscapistState.RUNNING
        self.actual_position = grid.start_position
        self.grid = grid
        self.chaos_degree = 0.4
        self.directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

        self.learning_params = LearningValues(grid.HEIGHT, grid.WIDTH)

    def reset(self):
        self.positions_all_the_way = []
        self.status = EscapistState.RUNNING
        self.actual_position = self.grid.start_position

    def get_position_from_direction(self, direction, pos):
        if direction == Direction.NORTH:
            return (pos[0]-1, pos[1])
        if direction == Direction.EAST:
            return (pos[0], pos[1]+1)
        if direction == Direction.SOUTH:
            return (pos[0]+1, pos[1])
        if direction == Direction.WEST:
            return (pos[0], pos[1]-1)


    def next_move(self):
        next_move = 0 
        print(self.actual_position)
        
        if np.random.rand() < self.chaos_degree:
            direction = np.random.choice(self.directions)
            next_position = self.get_position_from_direction(direction, self.actual_position)
            print("next_position: ", next_position)
            if self.grid.check_possible_move(self.actual_position, next_position):
                return next_position

        print(self.actual_position)
        best_param = -100000000000000000000 
        for direction in self.directions:
            next_position = self.get_position_from_direction(direction, self.actual_position)
            print("next_position2: ", next_position)
            if self.grid.check_possible_move(self.actual_position, next_position):
                param = self.learning_params.learning_values[next_position[0], next_position[1]] 
                if best_param < param:
                    next_move = next_position
                    best_param = param
        print("next_move3: ", next_move)
        return next_move

    def go(self):
        if self.status == EscapistState.RUNNING:
            move = self.next_move()
            print("go, move: ", move)
            self.positions_all_the_way.append(move)
            self.actual_position = move 
            print(f'New position: {move}.')
            self.status = self.grid.check_state_in_position(move)

            return True
        else:
            result = self.status.value

            for pos in reversed(self.positions_all_the_way):
                result = self.learning_params.funcV(pos, result)

            return False 

class Escape:
    def __init__(self, epoch, rounds, time_limit_in_a_round):
        self.time = 0
        self.epoch = epoch
        self.round = rounds 
        self.round_time_limit = time_limit_in_a_round

        self.grid = Grid()
        self.escapist = Escapist(self.grid)

    def time_tick(self):
        self.time += 1
        return self.escapist.go()


    def reset_round(self):
        self.escapist.reset()
        self.grid.reset()

    def start(self):

        for ep in range(self.epoch):
            for rnd in range(self.round):
                while self.time_tick():
                    if self.time > self.round_time_limit:
                        break

                print(f'Round {rnd} took {self.time} ticks.\n')
                self.reset_round()

    def show_result(self):
        print("Learning params: ")
        print(np.round(self.escapist.learning_params.learning_values,2))
        print("\nGrid: ")
        self.escapist.grid.show_grid()


if __name__ == "__main__":
    escape = Escape(3, 20, 10000)
    escape.start()

    escape.show_result()



