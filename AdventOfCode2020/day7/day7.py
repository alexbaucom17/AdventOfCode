import queue

def parse_rule(rule):
    rule = rule.rstrip()
    a,b = rule.split('contain')
    idx = a.find('bag')
    outer_color = a[:idx-1].rstrip()
    if b.strip() == 'no other bags.':
        return (outer_color, None)
    else:
        inner_color_bags = b.split(',')
        inner_colors = []
        for bag in inner_color_bags:
            words = bag.split()
            name = words[1] + " " + words[2]
            num = int(words[0].strip())
            inner_colors.append((name, num))
        return (outer_color, tuple(inner_colors))

def load_data(filename):
    with open(filename) as f:
        data = {}
        for line in f:
            outer, inner = parse_rule(line)
            data[outer] = inner
        return data


class Node:
    def __init__(self, color):
        self.color = color
        self.parents = []
        self.children = []
    
    def add_parent(self, parent):
        self.parents.append(parent)

    def add_child(self, child_node, number):
        self.children.append((child_node, number))

def build_graph(rules):

    nodes = {}
    for outer_color, inner_colors in rules.items():
        if outer_color not in nodes.keys():
            nodes[outer_color] = Node(outer_color)
        if inner_colors is None:
            continue
        for color, num in inner_colors:
            if color not in nodes.keys():
                nodes[color] = Node(color)
            nodes[outer_color].add_child(nodes[color], num)
            nodes[color].add_parent(nodes[outer_color])
    return nodes

def count_parents(graph, color):
    explored = set()
    to_explore = queue.Queue()
    to_explore.put(graph[color])
    while not to_explore.empty():
        cur_node = to_explore.get()
        explored.add(cur_node.color)
        parents = cur_node.parents
        for p in parents:
            to_explore.put(p)
    return explored


def count_bags(graph, color):
    node = graph[color]
    total = 1
    for child_node, num in node.children:
        total += num*count_bags(graph, child_node.color)
    return total


if __name__ == '__main__':
    sample_data = load_data("day7/sample_input.txt")
    sample_data2 = load_data("day7/sample_input2.txt")
    data = load_data("day7/input.txt")
    
    #print(sample_data2)
    graph = build_graph(data)

    # part 1
    bags = count_parents(graph, 'shiny gold')
    print(len(bags)-1)

    # part 2
    print(count_bags(graph, 'shiny gold') - 1)
