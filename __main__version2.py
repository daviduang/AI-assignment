import math
import sys
import json
import astar

from util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    # TODO: find and print winning action sequence

    white_list = data['white']
    black_list = data['black']

    print(white_list)
    print(black_list)

    distance_list = create_distance_list(black_list)
    group_list = make_group(distance_list)
    print(group_list)

    search_list = create_search_list(black_list, distance_list, group_list)
    print(search_list)
    boom_list = []
    decide_boom_point(len(white_list), black_list, group_list, search_list, boom_list)
    print(boom_list)
    print(group_list)
    block_list = coordinate_only(black_list)
    start_dict = data_dict(white_list)
    surrounding_list = create_surrounding_list(block_list, group_list)
    print(surrounding_list)
    # no remaining group


# if len(group_list) == 0:
# find path and print.
#    astar.search_path(block_list, start_dict, boom_list)


# remove the number of token in front of the coordinates
def coordinate_only(old_list):
    new_list = []
    for point in old_list:
        new_list.append((point[1], point[2]))

    return new_list


# A dictionary to store the coordinates contains pieces as keys, corresponding stacks as values
def data_dict(data_list):
    coordinates_dict = {}

    for item in data_list:
        coordinates_dict[item[1], item[2]] = item[0]

    return coordinates_dict


# calculate distance between two tokens
def distance_cal(point1, point2):
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


# create a list that contains all the distance between two tokens
def create_distance_list(black_list):
    distance_list = []
    length = len(black_list)

    # initialise the distance list
    for i in range(0, length):

        distance_list.append([])

        for j in range(0, length):
            distance = distance_cal(black_list[i], black_list[j])
            distance_list[i].append(distance)

    return distance_list


# putting black tokens into different groups,
# tokens in the same group will boom together if one of the member in the group boomed
def make_group(distance_list):
    current_group = 0
    group_list = []
    length = len(distance_list)

    for i in range(0, length):
        if not is_grouped(group_list, i):
            group_list.append([i])
            search_surrounding(distance_list, group_list, current_group, i)
            current_group += 1

    return group_list


# check whether a token is in a grouped or not
def is_grouped(group_list, token):
    for group in group_list:
        if token in group:
            return True

    return False


# look up the distance between a give token and all other tokens
# if the distance is 1 or sqrt of 2, add this token to the group
def search_surrounding(distance_list, group_list, current_group, token):
    for i in range(0, len(distance_list)):
        if distance_list[token][i] == 1.0 or distance_list[token][i] == math.sqrt(2):
            if not (i in group_list[current_group]):
                group_list[current_group].append(i)
                search_surrounding(distance_list, group_list, current_group, i)


# create search list by find the distance between two tokens which is 2, square root 5 or square root 8
def create_search_list(black_list, distance_list, group_list):
    # search_dict has a point coordinate as its keys and the item is a weight of this point
    search_dict = {}
    length = len(distance_list)

    for i in range(0, length):
        for j in range(i + 1, length):
            if not is_same_group(group_list, i, j):
                distance = distance_list[i][j]
                # distance 2 or square root 8 has only one mid-point
                if distance == 2.0 or distance == math.sqrt(8):

                    search_point = find_search_point(black_list, 1, i, j)
                    # more time a point has been found, more weight it has
                    if search_point in search_dict:
                        search_dict[search_point] += 1
                    else:
                        search_dict[search_point] = 0

                elif distance == math.sqrt(5):
                    # distance square root 5 has two mid-point
                    search_point = find_search_point(black_list, 2, i, j)

                    if search_point[0] in search_dict:
                        search_dict[search_point[0]] += 1
                    else:
                        search_dict[search_point[0]] = 0

                    if search_point[1] in search_dict:
                        search_dict[search_point[1]] += 1
                    else:
                        search_dict[search_point[1]] = 0

    search_list = sorted(search_dict.items(), key=lambda x: x[1], reverse=True)

    return search_list


def is_same_group(group_list, token1, token2):
    for i in range(0, len(group_list)):
        if (token1 in group_list[i]) and (token2 in group_list[i]):
            return True

    return False


# the search point should be the mid point of two given point
def find_search_point(black_list, num_point, token1, token2):
    point1 = [black_list[token1][1], black_list[token1][2]]
    point2 = [black_list[token2][1], black_list[token2][2]]
    search_point = []

    if num_point == 1:
        # one search point
        search_point = (int((point1[0] + point2[0]) / 2), int((point1[1] + point2[1]) / 2))
    else:
        # two search point
        if abs(point1[0] - point2[0]) == 2:
            # horizontal distance is 2
            # move point1 downward for 1 unit,and find one search point
            search_point1 = (int((point1[0] + point2[0]) / 2), int((point1[1] - 1 + point2[1]) / 2))
            search_point.append(search_point1)
            # move point1 upward for 1 unit
            search_point2 = (int((point1[0] + point2[0]) / 2), int((point1[1] + 1 + point2[1]) / 2))
            search_point.append(search_point2)
        else:
            # vertical distance is 2
            # move point1 leftward for 1 unit,and find one search point
            search_point1 = (int((point1[0] - 1 + point2[0]) / 2), int((point1[1] + point2[1]) / 2))
            search_point.append(search_point1)
            # move point1 rightward for 2 unit
            # which is 1 unit rightward from original position
            search_point2 = (int((point1[0] + 1 + point2[0]) / 2), int((point1[1] + point2[1]) / 2))
            search_point.append(search_point2)

    return search_point


def decide_boom_point(num_white, black_list, group_list, search_list, boom_list):
    current_group_list = group_list.copy()
    current_black_list = black_list.copy()
    for boom_point in search_list:
        # boom this point
        num_white -= 1
        # generate the nearby point
        nearby_point_list = find_nearby_point(boom_point[0])
        for i in range(0, len(black_list)):
            # removed black token has -1 as the number of token
            if black_list[i][0] > 0:
                # if a black token is inside the nearby region
                # and its group is still there
                if (black_list[i][1], black_list[i][2]) in nearby_point_list:
                    if is_grouped(current_group_list, i):
                        # update the group list
                        update_group_list(current_group_list, i)

        update_black_list(current_black_list, current_group_list)

        # search next search point
        if num_white >= len(current_group_list) or decide_boom_point(num_white, current_black_list, current_group_list,
                                                                     search_list[search_list.index(boom_point) + 1:],
                                                                     boom_list):
            boom_list.append((boom_point[0][0], boom_point[0][1]))
            # update the group list from previous function, will show the remaining group
            group_list.clear()
            for group in current_group_list:
                group_list.append(group)

            return True

    return False


# find the nearby point of a given point
def find_nearby_point(point):
    nearby_point_list = [(point[0] - 1, point[1] - 1), (point[0] - 1, point[1]), (point[0] - 1, point[1] + 1),
                         (point[0], point[1] + 1), (point[0] + 1, point[1] + 1), (point[0] + 1, point[1]),
                         (point[0] + 1, point[1] - 1), (point[0], point[1] - 1)]
    return nearby_point_list


# remove a group in the list which the token is inside it
def update_group_list(group_list, token):
    for group in group_list:
        if token in group:
            group_list.remove(group)
            return


# update the black list, remove all exploded token
def update_black_list(black_list, group_list):
    for point in black_list:
        if not is_grouped(group_list, black_list.index(point)):
            # -1 as the number of token in a point means removed
            point[0] = -1


# find all surrounding point for each group of token
def create_surrounding_list(block_list, group_list):
    group_surrounding_list = []
    surrounding_list = []
    for group in group_list:
        for token in group:
            nearby_point = find_nearby_point(block_list[token])
            for point in nearby_point:
                if point not in group_surrounding_list \
                        and point not in block_list:
                    if point[0] in range(0, 8) and point[1] in range(0, 8):
                        group_surrounding_list.append(point)
        surrounding_list.append(group_surrounding_list.copy())
        group_surrounding_list.clear()
    return surrounding_list


if __name__ == '__main__':
    main()
