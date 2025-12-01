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


def find_xmas_encoding_error(data, preamble_size):
    start_idx = 0
    end_idx = preamble_size
    while True:
        prev_nums = copy.copy(data[start_idx:end_idx])
        target_num = data[end_idx]
        try:
            find_sum(prev_nums, target_num)
        except ValueError:
            return target_num
        start_idx += 1
        end_idx += 1
        if end_idx >= len(data):
            raise IndexError("Reached end of data")

def find_contiguous_sum(data, target_num):
    start_idx = 0
    end_idx = 1
    while True:
        s = sum(data[start_idx:end_idx])
        if s < target_num:
            end_idx += 1
        elif s > target_num:
            start_idx += 1
        else:
            break

    nums = copy.copy(data[start_idx:end_idx])
    nums.sort()
    return nums[0] + nums[-1]


if __name__ == '__main__':

    sample_data = load_data("day9/sample_input.txt")
    data = load_data("day9/input.txt")

    bad_num = find_xmas_encoding_error(data, 25)
    print(find_contiguous_sum(data, bad_num))