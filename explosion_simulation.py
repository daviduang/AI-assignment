import math


# record the black chess information
class State:
    def __init__(self, black_dict):
        self.black_dict = black_dict


# the search point should be the mid point of two given point
def find_search_point(black_list):
    tmp_list = black_list.copy()

    target_list = []

    for black_piece in tmp_list:
        tmp_list.remove(black_piece)
        for other_piece in tmp_list:

            # case1: distance between 2 black pieces is 2
            if distance_cal(black_piece, other_piece) == 2:

                # if 2 black pieces are in a vertical relationship
                if black_piece[0] == other_piece[0]:

                    # compute y coordinates of all possible black pieces in case1 areas
                    y_list = [black_piece[1], other_piece[1], int((black_piece[1] + other_piece[1]) / 2)]

                    # check if any black piece inside these areas
                    for y_val in y_list:
                        x_val = black_piece[0]

                        # if there is a black piece on the right side of the area
                        if (x_val + 2, y_val) in black_list:
                            target_list.append((x_val + 1, int((black_piece[1] + other_piece[1]) / 2)))
                            break

                        # if there is a black piece on the left side of the area
                        if (x_val - 2, y_val) in black_list:
                            target_list.append((x_val - 1, int((black_piece[1] + other_piece[1]) / 2)))
                            break

                    # if there is no black piece on either left or right side of the area
                    else:
                        target_list.append((x_val, int((black_piece[1] + other_piece[1]) / 2)))

                # if 2 black pieces are in a horizontal relationship
                if black_piece[1] == other_piece[1]:

                    # compute x coordinates of all possible black pieces in case1 areas
                    x_list = [black_piece[0], other_piece[0], int((black_piece[0] + other_piece[0]) / 2)]

                    # check if any black piece inside these areas
                    for x_val in x_list:
                        y_val = black_piece[1]

                        # if there is a black piece on the top of the area
                        if (x_val, y_val + 2) in black_list:
                            target_list.append((int((black_piece[0] + other_piece[0]) / 2), y_val + 1))
                            break

                        # if there is a black piece on the bottom of the area
                        if (x_val, y_val - 2) in black_list:
                            target_list.append((int((black_piece[0] + other_piece[0]) / 2), y_val - 1))
                            break

                    # if there is no black piece on either top or bottom of the area
                    else:
                        target_list.append((int((black_piece[0] + other_piece[0]) / 2), y_val))

            # case2: distance between 2 black pieces is square root of 5
            if math.sqrt(5) - distance_cal(black_piece, other_piece) < 0.000001:

                if math.fabs(black_piece[0] - other_piece[0]) == 1:
                    y_check = black_piece[1] * 2 - other_piece[1]
                    x_check = other_piece[0]
                    if (x_check, y_check) in black_list:
                        target_list.append(black_piece[0], (black_piece[1] + other_piece[1]) / 2)

                    else:
                        target_list.append(black_piece[0], (black_piece[1] + other_piece[1]) / 2)
                        target_list.append(other_piece[0], (black_piece[1] + other_piece[1]) / 2)

                if math.fabs(black_piece[1] - other_piece[1]) == 1:
                    y_check = other_piece[1]
                    x_check = black_piece[0] * 2 - other_piece[0]
                    if (x_check, y_check) in black_list:
                        target_list.append((black_piece[0] + other_piece[0]) / 2, black_piece[1])

                    else:
                        target_list.append((black_piece[0] + other_piece[0]) / 2, black_piece[1])
                        target_list.append((other_piece[0] + other_piece[0]) / 2, black_piece[1])

            # case3: distance between 2 black pieces is square root of 8
            if math.sqrt(8) - distance_cal(black_piece, other_piece) < 0.000001:
                target_list.append(((black_piece[0] + other_piece[0]) / 2, (black_piece[1] + other_piece[1]) / 2))

        # target list with duplication
        print("tg: ", target_list)


# calculate distance between two tokens
def distance_cal(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def main():
    print(find_search_point([(2, 2), (4, 2), (4, 4)]))


if __name__ == '__main__':
    main()
