def part1(filename):
    with open(filename) as f:
        data = []
        cur_group = set()
        for line in f:
            line = line.rstrip()
            if line == "":
                data.append(len(cur_group))
                cur_group = set()
            else:
                for c in line:
                    cur_group.add(c)

        data.append(len(cur_group))
        return data, sum(data)

def part2(filename):
    with open(filename) as f:
        data = []
        cur_group_data = []
        for line in f:
            line = line.rstrip()
            if line == "":
                final_set = set.intersection(*cur_group_data)
                data.append(len(final_set))
                cur_group_data = []
            else:
                person = set()
                for c in line:
                    person.add(c)
                cur_group_data.append(person)

        final_set = set.intersection(*cur_group_data)
        data.append(len(final_set))
        return data, sum(data)


if __name__ == '__main__':
    #data, s = part1("day6/input.txt")
    # print(data)
    # print(s)

    data, s = part2("day6/input.txt")
    print(data)
    print(s)


