"""Adopted from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2 """

class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, stack_num):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    threshold = 0

    # Loop until you find the end
    while len(open_list) > 0 and threshold < 100:

        threshold += 1

        # print("threshold: ", threshold)

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in adjacent_squares(stack_num):  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():
    # (0, 1), (1, 1), (2, 0)
    """
    black_list = [(0, 1), (1, 1), (2, 0)]
    white_dict = {(0, 0): 1, (1, 0): 1}
    """

    black_list = [(0, 1), (1, 1), (2, 0)]
    white_dict = {(0, 0): 1, (1, 0): 1, (2, 2): 1}

    target_list = [(7, 7), (7, 6), (7, 5)]

    # the case that requires stack

    """
    if search_path(black_list, start_list, target_list) is None:
        for start in start_list:
            if start is not in target_list and search_path(black_list, [start], ):
    """


    search_path(black_list, white_dict, target_list)

"""2-by-2 matrix, '1' stand for the coordinates with a black piece, only black piece can block"""
def initialize_maze(black_list):
    maze = [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    for coordinates in black_list:
        maze[coordinates[0]][coordinates[1]] = 1

    return maze


"""search path in an dictionary of starting points to the targets in a list"""
def search_path(black_list, start_dict, target_list):

    maze = initialize_maze(black_list)

    output_dict = {}

    output = []

    # when the target list is not empty
    while len(target_list) != 0:

        print("dict: ", start_dict)

        start_item = start_dict.popitem()
        stack = start_item[1]
        start = start_item[0]
        target = target_list.pop()

        path = astar(maze, start, target, stack)

        if path is not None:
            #output_dict.update({stack: path})

            path_stack = [stack, path]
            output.append(path_stack)

        # if the explored coordinates have a stack of at least 2 pieces
        if stack >= 2:

            start_dict[target[0], target[1]] = stack

            start_dict[target[0], target[1]] -= 1

            print("dict1: ", start_dict)

        # if all paths to a given target have been blocked, attempt to move to another white piece to form a stack
        if path is None:
            target_list.append(target)
            for another_piece in start_dict:
                print(another_piece)
                print(start)

                if astar(maze, start, another_piece, stack) is not None:
                    #output_dict.update({stack: astar(maze, start, another_piece, stack)})

                    path_stack = [stack, astar(maze, start, another_piece, stack)]

                    output.append(path_stack)

                    start_dict[another_piece] += 1
    print(output)


"""compress Class1 relationship tipping points to a single tipping point per group"""
def compress_target(black_list, start_dict, total_target_list):

    maze = initialize_maze(black_list)
    output_target = []
    while len(total_target_list) != 0:

        start_item = start_dict.popitem()
        stack = start_item[1]
        start = start_item[0]

        # if the explored coordinates have a stack of at least 2 pieces
        if stack >= 2:

            start_dict[target[0], target[1]] = stack

            start_dict[target[0], target[1]] -= 1

            print("dict1: ", start_dict)

        for target_list in total_target_list:
            for target in target_list:
                path = astar(maze, start, target, stack)
                if path is not None:

                    print("target: ", target)

                    output_target.append(target)
                    total_target_list.remove(target_list)
                    break

    print("output_target: ", output_target)

# return all the adjacent squares in a list according to the number of stack
def adjacent_squares(size):
    adjacent_list = []
    for x in range(1, size + 1):
        adjacent_list.append((0, -1 * x))
        adjacent_list.append((0, x))
        adjacent_list.append((-1 * x, 0))
        adjacent_list.append((x, 0))

    return adjacent_list


if __name__ == '__main__':
    main()
