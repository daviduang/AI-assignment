import json
import astar

def main():
    #  with open(sys.argv[1]) as file:

    with open("2020-part-a-test-cases/test-level-1.json") as file:
        data = json.load(file)

        # TODO: find and print winning action sequence
        print(data)

        white_dict = data_dict(data['white'])
        black_dict = data_dict(data['black'])

        black_list = list(black_dict.keys())
        start_list = list(white_dict.keys())

        # target for testing
        target_list = [(4, 5)]

        astar.search_path(black_list, start_list, target_list)


# A dictionary to store the coordinates contains pieces as keys, corresponding stacks as values
def data_dict(data_list):
    coordinates_dict = {}

    for item in data_list:
        coordinates_dict[item[1], item[2]] = item[0]

    return coordinates_dict


if __name__ == '__main__':
    main()
