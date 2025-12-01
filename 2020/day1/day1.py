import copy


def load_data(filename):
    with open(filename) as f:
        data = [int(line.rstrip()) for line in f]
        return data


def find_sum(data, target_sum):
    data.sort()
    front_idx = 0
    end_idx = len(data) - 1
    while True:
        sum = data[front_idx] + data[end_idx]
        if sum < target_sum:
            front_idx += 1
        elif sum > target_sum:
            end_idx -= 1
        elif sum == target_sum:
            return (data[front_idx], data[end_idx])
        
        if end_idx < front_idx:
            raise ValueError("Didn't find any pair that summed")

def find_sum_three_way(data, target_sum):
    for random_idx in range(0, len(data)):
        data_copy = copy.copy(data)
        del data_copy[random_idx]
        new_target_sum = target_sum - data[random_idx]
        try:
            a,b = find_sum(data_copy, new_target_sum)
        except ValueError:
            continue
        return (a,b,data[random_idx])



if __name__ == '__main__':

    test_data = [1721,979,366,299,675,1456]

    # part 1
    data = load_data("day1/input.txt")
    a,b = find_sum(data, 2020)
    print(a*b)

    # part 2
    (a,b,c) = find_sum_three_way(data,2020)
    print(a*b*c)