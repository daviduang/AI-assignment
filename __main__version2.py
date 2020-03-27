import math
import sys
import json

from util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
    # TODO: find and print winning action sequence

    white_list = data['white'][0:len(data['white'])]
    black_list = data['black'][0:len(data['black'])]

    print(white_list)
    print(black_list)

    distance_list = create_distance_list(black_list)
    group_list = make_group(distance_list)
    print(group_list)

    search_list = create_search_list(black_list, distance_list, group_list)
    print(search_list)


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


# check whether a token is grouped or not
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
        search_point = (int((point1[0] + point2[0])/2), int((point1[1] + point2[1])/2))
    else:
        # two search point
        if abs(point1[0] - point2[0]) == 2:
            # horizontal distance is 2
            # move point1 downward for 1 unit,and find one search point
            search_point1 = (int((point1[0] + point2[0])/2), int((point1[1]-1 + point2[1])/2))
            search_point.append(search_point1)
            # move point1 upward for 1 unit
            search_point2 = (int((point1[0] + point2[0])/2), int((point1[1]+1 + point2[1])/2))
            search_point.append(search_point2)
        else:
            # vertical distance is 2
            # move point1 leftward for 1 unit,and find one search point
            search_point1 = (int((point1[0]-1 + point2[0])/2), int((point1[1] + point2[1])/2))
            search_point.append(search_point1)
            # move point1 rightward for 2 unit
            # which is 1 unit rightward from original position
            search_point2 = (int((point1[0]+1 + point2[0])/2), int((point1[1] + point2[1])/2))
            search_point.append(search_point2)

    return search_point


if __name__ == '__main__':
    main()
