import cProfile

def load_data(filename):
    with open(filename) as f:
        data = [[int(c) for c in line.strip().split(',')] for line in f]
        return data


def play_number_game(starting_nums, iterations):
    data_map = {}
    prev_num = 0
    counter = 1
    for n in starting_nums:
        data_map[n] = [counter]
        counter += 1
        prev_num = n

    for i in range(counter, iterations+1):
        new_num = 0
        if prev_num in data_map.keys() and len(data_map[prev_num]) > 1:
            new_num = data_map[prev_num][-1] - data_map[prev_num][-2]

        if new_num in data_map.keys():
            data_map[new_num].append(i)
        else:
            data_map[new_num] = [i]

        prev_num = new_num
        #print(new_num)

        if i % 1000000 == 0:
            print(i)

    print("Total: ")
    print(prev_num)
            

    

if __name__ == '__main__':

    sample_data = load_data("day15/sample_input.txt")
    data = load_data("day15/input.txt") 

    # part 1
    play_number_game(data[0], 2020)

    # part 2
    cProfile.run('play_number_game(data[0], 30000000)')
    