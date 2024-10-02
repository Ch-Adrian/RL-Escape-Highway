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

class LearningValues:
    def __init__(self, height, width):
        self.learning_values = np.zeros([height, width])
        self.learning_rate = 0.25
    
    def funcV(self, position, result):
        result = self.learning_values[position] + self.learning_rate*(result - self.learning_values[position])
        self.learning_values[position] = round(result, 5)
        return result


class Escapist:
    def __init__(self, game):
        self.positions_all_the_way = []
        self.status = EscapistState.RUNNING
        self.actual_position = game.start_position
        self.game = game
        self.chaos_degree = 0.4
        self.directions = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

        self.learning_params = LearningValues(game.HEIGHT, game.WIDTH)

    def reset(self):
        self.positions_all_the_way = []
        self.status = EscapistState.RUNNING
        self.actual_position = self.game.start_position

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
            if self.game.check_possible_move(self.actual_position, next_position):
                return next_position

        print(self.actual_position)
        best_param = -100000000000000000000 
        for direction in self.directions:
            next_position = self.get_position_from_direction(direction, self.actual_position)
            print("next_position2: ", next_position)
            if self.game.check_possible_move(self.actual_position, next_position):
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
            self.status = self.game.check_state_in_position(move)

            return True
        else:
            result = self.status.value

            for pos in reversed(self.positions_all_the_way):
                result = self.learning_params.funcV(pos, result)

            return False 
