import numpy as np

def load_data(filename):
    with open(filename) as f:
        fields = {}
        ticket = []
        nearby = []
        step = 0
        for line in f:
            line = line.rstrip()
            if step == 0:
                if line == '':
                    step = 1
                else:
                    name, rule_str = line.split(':')
                    rule_fn = generate_rule(rule_str)
                    fields[name.strip()] = (rule_fn, rule_str)
            elif step == 1:
                if line == '':
                    step = 2
                elif line == "your ticket:":
                    continue
                else:
                    ticket = [int(i) for i in line.split(',')]
            else:
                if line == "nearby tickets:":
                    continue
                else:
                    nearby.append([int(i) for i in line.split(',')])


        return (fields, ticket, nearby)

def generate_rule(rule_str):

    r1,r2 = rule_str.split('or')
    nums1 = [int(i) for i in r1.strip().split('-')]
    nums2 = [int(i) for i in r2.strip().split('-')]
    return lambda x : check_num(x, nums1[0], nums1[1], nums2[0], nums2[1])


def check_num(num, lo1, hi1, lo2, hi2):
    ok1 = num >= lo1 and num <= hi1
    ok2 = num >= lo2 and num <= hi2
    ok = ok1 or ok2
    return ok


def find_invalid_numbers(ticket, rules):
    invalid_nums = []
    for n in ticket:
        fails_all_rules = True
        for r in rules:
            rule_ok = r(n)
            if rule_ok:
                fails_all_rules = False
                break
        if fails_all_rules:
            invalid_nums.append(n)

    #print("Invalid: {}".format(invalid_nums))
    return invalid_nums


def check_all_tickets_for_invalid_numbers(tickets, fields):
    rule_fns = [r for r,s in fields.values()]
    invalid_nums = []
    for t in tickets:
        print("Ticket: {}".format(t))
        invalid_nums += find_invalid_numbers(t, rule_fns)

    print(sum(invalid_nums))


def all_tickets_match_rules(tickets, rule):
    ok = [rule(n) for n in tickets]
    return np.all(ok)


def reduce_feasible_mtx(feasible_mtx):
    ordering = -1*np.ones((feasible_mtx.shape[0],1), dtype=int)
    count = 0
    while True:
        print("Reduction iteration {}".format(count))
        count += 1
        for col_num in range(feasible_mtx.shape[0]):
            s = np.sum(feasible_mtx[:,col_num]) 
            if s != 1:
                continue
            elif s == 1:
                row_num = np.flatnonzero(feasible_mtx[:,col_num])
                ordering[col_num] = row_num
                feasible_mtx[row_num,:] = False

        if np.all(np.array(ordering) != -1):
            return ordering.transpose()    

def find_field_ordering(tickets, fields):
    rule_fns = [r for r,s in fields.values()]
    valid_tickets = []
    for t in tickets:
        if len(find_invalid_numbers(t, rule_fns)) == 0:
            valid_tickets.append(t)

    n_fields = len(fields.keys())
    num_mtx = np.array(valid_tickets, dtype=int)
    print(num_mtx)

    feasible_mtx = np.zeros((n_fields, n_fields), dtype=bool)
    for rule_num in range(n_fields):
        for col_num in range(n_fields):
            if all_tickets_match_rules(num_mtx[:,col_num], rule_fns[rule_num]):
                feasible_mtx[rule_num, col_num] = True
    
    print(feasible_mtx)

    ordering = reduce_feasible_mtx(feasible_mtx)

    return ordering


def find_value_of_departure_fields(ticket, fields, ordering):
    data_map = {}
    field_names = [f for f in fields.keys()]
    for ticket_num, field_num in enumerate(ordering[0]):
        data_map[field_names[field_num]] = ticket[ticket_num]

    print(data_map)
    total = 1
    for k, v in data_map.items():
        if k.startswith("departure"):
            total *= v

    print(total)

if __name__ == '__main__':

    sample_data = load_data("day16/sample_input.txt")
    sample_data2 = load_data("day16/sample_input2.txt")
    data = load_data("day16/input.txt") 

    using_data = data
    fields = using_data[0]
    ticket = using_data[1]
    nearby = using_data[2]

    print(using_data)

    # Part 1
    #check_all_tickets_for_invalid_numbers(nearby, fields)

    # Part 2
    ordering = find_field_ordering(nearby, fields)
    print(ordering)
    find_value_of_departure_fields(ticket, fields, ordering)