# record each piece information
class Piece:
    def __init__(self, xco, yco, colour):
        self.x = xco  # x coordinate of piece
        self.y = yco  # y coordinate of piece
        self.type = colour  # colour of piece, black or white
        self.stack_num = 1  # number of pieces in a stack, initially 1

    def add_stack(self):
        self.stack_num += 1

    def remove_stack(self):
        self.stack_num -= 1


# record the whole chess board information
class State:
    def __init__(self):
        self.white_list = []  # record the list of white pieces
        self.black_list = []  # record the list of black pieces

    def add_white(self, new_piece):
        self.white_list.append(new_piece)

    def remove_white(self, dead_piece):
        self.white_list.remove(dead_piece)

    def add_black(self, new_piece):
        self.black_list.append(new_piece)

    def remove_black(self, dead_piece):
        self.white_list.remove(dead_piece)


