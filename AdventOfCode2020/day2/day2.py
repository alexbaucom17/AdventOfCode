    
def pw_and_policy_ok(pw, policy):

    p1 = policy.split("-", 1)
    min_num_letters = int(p1[0])
    p2 = p1[1].split()
    max_num_letters = int(p2[0])
    letter = p2[1]

    num_letters = pw.count(letter)
    return num_letters >= min_num_letters and num_letters <= max_num_letters


def count_valid_passwords(data):
    count = 0
    for line in data:
        line_info = line.split(":", 1)
        policy = line_info[0].strip()
        pw = line_info[1].strip()
        if (pw_and_policy_ok(pw, policy)):
            count += 1
    return count

def pw_and_policy_ok2(pw, policy):

    p1 = policy.split("-", 1)
    pos1 = int(p1[0])
    p2 = p1[1].split()
    pos2 = int(p2[0])
    letter = p2[1]

    found1 = pw[pos1-1] == letter
    found2 = pw[pos2-1] == letter
    return found1 ^ found2

def count_valid_passwords2(data):
    count = 0
    for line in data:
        line_info = line.split(":", 1)
        policy = line_info[0].strip()
        pw = line_info[1].strip()
        if (pw_and_policy_ok2(pw, policy)):
            count += 1
    return count

if __name__ == '__main__':

    test_data = ["1-3 a: abcde","1-3 b: cdefg","2-9 c: ccccccccc"]
    with open("day2/input.txt") as f:
        data = [line.rstrip() for line in f]

    # part 1
    print(count_valid_passwords(data))

    # part 1
    print(count_valid_passwords2(data))