import search
import math
import utils

id="318917010"

""" Rules """
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50

'''Constants'''
PACMAN = 77
DEAD_PACMAN = 88
GHOSTS = [20, 21, 30, 31, 40, 41, 50, 51]
DIRECTION = ['R', 'D', 'L', 'U']

class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""
    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman: 
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman.""" 

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

    @staticmethod
    def tuple_to_list(state):
        """ Converts a tuple to a list """
        return [list(row) for row in state]

    @staticmethod
    def list_to_tuple(list_state):
        """ Converts a list to a tuple """
        return tuple(tuple(row) for row in list_state)

    def get_manhattan_distance(self, x1, y1, x2, y2):
        """ Calculates the Manhattan distance between two points """
        return abs(x1 - x2) + abs(y1 - y2)

    def get_new_location(self, i, j, direction, state):
        """ Returns the new location of the point after moving in the given direction """
        if direction == 'R':
            if j + 1 < len(state[i]):
                return i, j + 1
        elif direction == 'D':
            if i + 1 < len(state):
                return i + 1, j
        elif direction == 'L':
            if j - 1 >= 0:
                return i, j - 1
        elif direction == 'U':
            if i - 1 >= 0:
                return i - 1, j
        return -1, -1


    def get_location(self, piece, state):
        """ Returns the location of the piece in the given state """
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] // 10 == piece // 10:
                    return i, j
        return -1, -1

    def update_ghosts_locations(self, state):
        """ Updates the ghosts locations, asuming that the pacman is not dead """
        res_state = [row[:] for row in state]  # copy the list
        x1, y1 = self.get_location(PACMAN, res_state)
        for ghost in [RED, BLUE, YELLOW, GREEN]:
            i, j = self.get_location(ghost, res_state)
            if (i, j) != (-1, -1):
                x_best, y_best = -1, -1
                manhattan_distance = math.inf
                for direction in DIRECTION:
                    if self.get_new_location(i, j, direction, res_state) != (-1, -1):
                        x2, y2 = self.get_new_location(i, j, direction, res_state)
                        if res_state[x2][y2] // 10 == 1 or res_state[x2][y2] == PACMAN:  # the new location is a walkable place
                            if self.get_manhattan_distance(x1, y1, x2, y2) < manhattan_distance:
                                manhattan_distance = self.get_manhattan_distance(x1, y1, x2, y2)
                                x_best, y_best = x2, y2
                if (x_best, y_best) != (-1, -1):
                    from_pill = res_state[i][j] % 10
                    to_pill = res_state[x_best][y_best] % 10
                    if res_state[x_best][y_best] == PACMAN:  # the new location is the pacman
                        res_state[x_best][y_best] = DEAD_PACMAN
                    else:  # the new location is a walkable place
                        res_state[x_best][y_best] = res_state[i][j] // 10 * 10 + to_pill
                    res_state[i][j] = 10 + from_pill
        return res_state

    def get_pacman_actions(self, list_state):
        res = []
        for direction in DIRECTION:
            if self.result(list_state, direction) != ():  # the new location is a walkable place
                res.append((direction, self.result(list_state, direction)))
        return self.list_to_tuple(res)

    def successor(self, state):
        """ Generates the successor state """
        if self.is_pacman_dead(state):
            return ()
        list_state = self.tuple_to_list(state)
        return self.get_pacman_actions(list_state)

    def result(self, state, move):
        """given state and an action and return a new state"""
        new_state = [row[:] for row in state]  # copy the list
        x, y = self.get_location(PACMAN, state)
        if self.get_new_location(x, y, move, state) != (-1, -1):
            x2, y2 = self.get_new_location(x, y, move, state)
            if state[x2][y2] // 10 == 1:  # the new location is a walkable place
                new_state[x][y] = 10
                new_state[x2][y2] = PACMAN
                new_state = self.update_ghosts_locations(new_state)
                return self.list_to_tuple(new_state)
            elif state[x2][y2] in GHOSTS:  # the new location is a ghost
                new_state[x][y] = 10
                new_state[x2][y2] = DEAD_PACMAN
                new_state = self.update_ghosts_locations(new_state)
                return self.list_to_tuple(new_state)
        return ()

    def is_success(self, state):
        """ given a state, checks if the player eaten all the tokens, returns True if so"""
        for row in state:
            for pos in row:
                if pos % 10 == 1:
                    # Only the places with 1 in the units digit are tokens
                    # The places: 11, 21, 31, 41, 51 with tokens
                    return False
        return True

    def is_pacman_dead(self, state):
        """ given a state, checks if the pacman is dead, returns True if so"""
        for row in state:
            for pos in row:
                if pos == DEAD_PACMAN:
                    return True
        return False

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        if (self.is_success(state) and not self.is_pacman_dead(state)):
            return True
        return False
        
    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        #  the heuristic is the sum of the pills that are not eaten
        state = node.state
        sum = 0
        for row in state:
            for pos in row:
                if pos % 10 == 1:
                    sum += 1
        return sum


def create_pacman_problem(game):
    print ("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)

game =()


create_pacman_problem(game)
