import numpy as np 
from grid import Grid
from escapist import Escapist, EscapistState

class Escape:
    def __init__(self, epoch, rounds, time_limit_in_a_round):
        self.HEIGHT = 10
        self.WIDTH = 5
        self.time = 0
        self.epoch = epoch
        self.round = rounds 
        self.round_time_limit = time_limit_in_a_round
        self.start_position = (self.HEIGHT-1, 2)

        self.grid = Grid(self.start_position, self.HEIGHT, self.WIDTH)
        self.escapist = Escapist(self)
    
    def check_possible_move(self, start_pos, end_pos):
        return self.grid.check_possible_move(start_pos, end_pos)

    def check_state_in_position(self, position):
        if position in self.grid.win_positions:
            return EscapistState.ALIVE 
        if position in self.grid.lose_positions:
            return EscapistState.DEAD 
        return EscapistState.RUNNING 

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
        self.grid.show_grid()


if __name__ == "__main__":
    escape = Escape(5, 30, 10000)
    escape.start()

    escape.show_result()



