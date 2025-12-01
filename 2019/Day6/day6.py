from queue import LifoQueue, Queue


orbits = {}

def insert_orbit(node, leaf):
    if node in orbits:
        orbits[node]['leaves'].append(leaf)
    else:
        orbits[node] = {'leaves': [leaf], 'parent': [], 'count': 0}

    if leaf in orbits:
        orbits[leaf]['parent'] = node
    else:
        orbits[leaf] = {'parent': node, 'leaves': [], 'count': 0}

def build_orbits(orbit_list):
    for node,leaf in orbit_list:
        insert_orbit(node, leaf)

def parse_orbit_string(orbit_str):
    return [(s.strip().split(')')) for s in orbit_str.splitlines()]

def count_orbits_dfs():

    queued = LifoQueue()
    queued.put('COM')
    total_count = 0

    while not queued.empty():
        node = queued.get()

        if orbits[node]['parent']:
            parent = orbits[orbits[node]['parent']]
            orbits[node]['count'] = parent['count'] + 1

        total_count += orbits[node]['count']

        if orbits[node]['leaves']:
            for leaf in orbits[node]['leaves']:
                queued.put(leaf)

    return total_count

def build_path_to_com(node):
    path = []
    cur_node = node
    while True:
        path.append(cur_node)
        if cur_node == 'COM':
            break
        else:
            cur_node = orbits[cur_node]['parent']
    return path[::-1]


def find_common_parent(node1, node2):
    n1_path = build_path_to_com(node1)
    n2_path = build_path_to_com(node2)

    count = 0
    while True:
        if n1_path[count] == n2_path[count]:
            count += 1
        else:
            break

    return n1_path[count - 1]

def find_num_transfers():

    you_parent = orbits['YOU']['parent']
    san_parent = orbits['SAN']['parent']
    common_parent = find_common_parent(you_parent, san_parent)

    n_you_parent = orbits[you_parent]['count']
    n_san_parent = orbits[san_parent]['count']
    n_parent = orbits[common_parent]['count']

    num_transfers = (n_you_parent - n_parent) + (n_san_parent - n_parent)
    return num_transfers


if __name__ == '__main__':

    with open('Day6/input.txt','r') as f:
        text = f.read()
        orbit_list = parse_orbit_string(text)
        build_orbits(orbit_list)
        print(count_orbits_dfs())
        print(find_num_transfers())