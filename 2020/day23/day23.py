
class GameState:

    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self, data, n_extra=0):
        # Create nodes with data
        self.nodes = []
        max_val = 0
        for d in data:
            self.nodes.append(GameState.Node(d))
            if d > max_val:
                max_val = d

        # Add any extra nodes
        for i in range(n_extra):
            self.nodes.append(GameState.Node(max_val+i+1))
        
        # Link nodes
        for i in range(len(self.nodes)):
            self.nodes[i-1].next = self.nodes[i]

        self.current_node = self.nodes[0]

        # Map values to nodes
        self.node_map = {self.nodes[i].data: self.nodes[i] for i in range(len(self.nodes))}
        self.n_nodes = len(self.nodes)

    def simulate_step(self):
        # Extract subset after current
        extracted_head = self.current_node.next

        # Link up portion after extracted section
        split_head = extracted_head
        extracted_str = "extracted:"
        extracted_vals = set()
        for i in range(3):
            extracted_str += " {}".format(split_head.data)
            extracted_vals.add(split_head.data)
            split_head = split_head.next
        self.current_node.next = split_head
        # print(extracted_str)

        # Find desination value that isn't in the nodes we extracted and then use map to quickly get the node
        dest_val = ((self.current_node.data - 2) % self.n_nodes) + 1
        while dest_val in extracted_vals:
            dest_val = ((dest_val - 2) % self.n_nodes) + 1
        destination_node = self.node_map[dest_val]
        # print("Destination value: {}".format(dest_val))

        # Insert extracted values after destination
        split_head = destination_node.next
        destination_node.next = extracted_head
        extracted_tail = extracted_head
        for i in range(2):
            extracted_tail = extracted_tail.next
        extracted_tail.next = split_head

        # Increment current node
        self.current_node = self.current_node.next

    def print(self):
        str = "state: ({})".format(self.current_node.data)
        check_node = self.current_node.next
        while check_node != self.current_node:
            str += " {}".format(check_node.data)
            check_node = check_node.next
        print(str)

    def print_final_id(self):
        one_node = self.current_node
        while one_node.data != 1:
            one_node = one_node.next
        
        final_id = ""
        cur_node = one_node.next
        for i in range(len(self.nodes) - 1):
            final_id += "{}".format(cur_node.data)
            cur_node = cur_node.next
        print(final_id)

    def print_part2_answer(self):
        one_node = self.node_map[1]
        first_after_one = one_node.next
        print(first_after_one.data)
        next_after_one = first_after_one.next
        print(next_after_one.data)
        print(first_after_one.data * next_after_one.data)


def simulate_n_steps(state, n):

    for i in range(n):
        if i % (n/10) == 0:
            print("Step: {}".format(i+1))
        # state.print()
        state.simulate_step()

    return state


if __name__ == '__main__':

    sample_data = [int(c) for c in "389125467"]
    data = [int(c) for c in "624397158"]

    # Part 1
    # state = GameState(data)
    # simulate_n_steps(state,100)
    # state.print()
    # state.print_final_id()

    # Part 2
    state = GameState(data, 1000000-len(data))
    simulate_n_steps(state,10000000)
    state.print_part2_answer()
