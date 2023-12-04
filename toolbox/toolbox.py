number_strings = [str(i) for i in range(10)]
directions_2d = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)]

input_file_name = 'input.txt'


def read_file_into_2d_array(file_path):
    try:
        with open(file_path, 'r') as file:
            return [list(line) for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def in_range(index, array):
    return -1 < index < len(array)
