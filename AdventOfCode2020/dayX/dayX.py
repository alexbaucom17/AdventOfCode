def load_data(filename):
    with open(filename) as f:
        data = [line.rstrip() for line in f]
        return data


if __name__ == '__main__':

    sample_data = load_data("dayX/sample_input.txt")
    data = load_data("dayX/input.txt") 