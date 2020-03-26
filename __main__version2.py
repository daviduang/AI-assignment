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
    group_list = make_group(black_list, distance_list)
    print(group_list)


# calculate distance between two tokens
def distance_cal(token1, token2):
    return math.sqrt((token1[1] - token2[1]) ** 2 + (token1[2] - token2[2]) ** 2)


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
def make_group(black_list, distance_list):
    group_list = []
    length = len(distance_list)

    for i in range(0, length):
        if not isgrouped(group_list, i):
            group_list.append([i])
            current_group = i
            search_surrounding(distance_list, group_list, current_group, i)

    return group_list


# check whether a token is grouped or not
def isgrouped(group_list, token):
    for group in group_list:
        if token in group:
            return True

    return False


# look up the distance between a give token and all other tokens
# if the distance is 1 or sqrt of 2, add this token to the group
def search_surrounding(distance_list, group_list, current_group, token):
    for i in range(0, len(distance_list)):
        if distance_list[token][i] == 1.0 or distance_list[token][i] ==math.sqrt(2):
            if not (i in group_list[current_group]):
                group_list[current_group].append(i)
                search_surrounding(distance_list, group_list, current_group, i)


if __name__ == '__main__':
    main()
