from anytree import Node, RenderTree, PostOrderIter

def load_data(filename):
    with open(filename) as f:
        data = [line.rstrip() for line in f]
        return data


def build_sub_tree(expr, idx):
    nodes = []
    root_node = None
    prev_op = None
    prev_val = None
    while idx >= 0:
        c = expr[idx]
        idx -= 1
        if c == " ":
            continue
        elif c == ')':
            sub_tree,idx = build_sub_tree(expr, idx)
            prev_val = sub_tree
        elif c == '(':
            if prev_val is not None:
                prev_op.children = list(prev_op.children) + [prev_val]
                prev_val = None
            return (root_node, idx)
        elif c == '+' or c == '*':
            n = Node(c, parent=prev_op)
            nodes.append(n)
            prev_op = n
            if root_node is None:
                root_node = prev_op
            if prev_val is not None:
                prev_op.children = list(prev_op.children) + [prev_val]
                prev_val = None
        else:
            n = Node(c)
            nodes.append(n)
            prev_val = n

        # print(idx)
        # if root_node is not None:
        #     print(RenderTree(root_node))
        
    if prev_val is not None:
        prev_op.children = list(prev_op.children) + [prev_val]
        prev_val = None
    return (root_node, idx)

def build_tree(expr):
    tree,idx = build_sub_tree(expr, len(expr)-1)
    # print(expr)
    # if tree is not None:
    #         print(RenderTree(tree))
    return tree

def evaluate_tree(tree):
    if tree.name == '+':
        return evaluate_tree(tree.children[0]) + evaluate_tree(tree.children[1]) 
    elif tree.name == '*':
        return evaluate_tree(tree.children[0]) * evaluate_tree(tree.children[1]) 
    elif tree.is_leaf:
        return int(tree.name)


def solve_all_equations(equations):
    solutions = []
    for e in equations:
        tree = build_tree(e)
        solutions.append(evaluate_tree(tree))
    return solutions


def find_matching_paren(expr, idx):
    paren_levels = 1
    while idx < len(expr):
        c = expr[idx]
        idx += 1
        if c == "(":
            paren_levels += 1
        elif c == ")":
            paren_levels -= 1
            if paren_levels == 0:
                return idx-1
    return None


def evaluate_parens(expr):
    idx_start = expr.find("(")
    if idx_start != -1:
        # print("paren")
        idx_end = find_matching_paren(expr, idx_start+1)
        sub_expr = evaluate_expr_advanced(expr[idx_start+1:idx_end])
        
        front_str = ""
        if idx_start > 1:
            front_str = expr[:idx_start]
        
        end_str = ""
        if idx_end < len(expr)-1:
            end_str = expr[idx_end+1:]

        expr = front_str + str(sub_expr) + end_str
        return evaluate_parens(expr)
    else:
        return expr

def get_num(str, start_idx, rev):
    step = 1
    if rev:
        step = -1

    idx = start_idx + step
    n_str = ''
    while idx >=0 and idx < len(str) and str[idx].isdigit():
        n_str += str[idx]
        idx += step

    if rev:
        n_str = n_str[::-1]

    return (int(n_str), idx)
    

def evaluate_op(expr, op):
    idx = expr.find(op)
    if idx != -1:
        n1,rev_idx = get_num(expr, idx, True)
        n2,fwd_idx = get_num(expr, idx, False)

        front_str = ""
        if rev_idx > 0:
            front_str = expr[:rev_idx+1]
        
        end_str = ""
        if fwd_idx < len(expr):
            end_str = expr[fwd_idx:]

        if op == "*":
            expr = front_str + str(n1*n2) + end_str
        elif op == "+":
            expr = front_str + str(n1+n2) + end_str

        # print(expr)
        return evaluate_op(expr, op)

    else:
        return expr


def evaluate_expr_advanced(expr):
    expr = expr.replace(' ', '')
    expr = evaluate_parens(expr)
    # print(expr)
    expr = evaluate_op(expr,"+")
    # print(expr)
    expr = evaluate_op(expr,"*")
    # print(expr)
    return int(expr)

def evaluate_all_expr_advanced(exprs):
    results = []
    for e in exprs:
        results.append(evaluate_expr_advanced(e))
    return results


if __name__ == '__main__':

    sample_data = load_data("day18/sample_input.txt")
    data = load_data("day18/input.txt") 

    #print(sum(solve_all_equations(data)))
    print(sum(evaluate_all_expr_advanced(data)))