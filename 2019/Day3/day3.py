import copy

def direction(p1, p2):
    v = [0,0]
    v[0] = p2[0] - p1[0]
    v[1] = p2[1] - p1[1]
    # Vertical
    if v[0] == 0:
        # Need to flip
        if v[1] < 0:
            return (1, 1)
        else:
            return (1, 0)
    # Horizontal
    elif v[1] == 0:
        if v[0] < 0:
            return (2, 1)
        else:
            return (2, 0)
    else:
        raise ValueError("Not horizontal or vertical!")

def check_intersection(hz1, hz2, vt1, vt2):

    if hz1[0] < vt1[0] and vt1[0] < hz2[0] and vt1[1] < hz1[1] and hz1[1] < vt2[1]:
        point = [vt1[0], hz1[1]]
        return (True, point)
    else:
        return (False, None)


def is_intersecting(p1, p2, p3, p4):

    dir1,flip1 = direction(p1,p2)
    dir2,flip2 = direction(p3,p4)

    if dir1 == dir2:
        return (False, None)
    else:
        l1 = []
        l2 = []
        if flip1:
            l1 = [p2, p1]
        else:
            l1 = [p1, p2]
        if flip2:
            l2 = [p4, p3]
        else:
            l2 = [p3, p4]
        # dir 1 is vertical
        if dir1 == 1:
            return check_intersection(l2[0], l2[1], l1[0], l1[1])
        else:
            return check_intersection(l1[0], l1[1], l2[0], l2[1])


def get_all_intersections(points1, points2):

    intersections = []
    for i in range(len(points1) - 1):
        for j in range(len(points2) - 1):
            p1 = points1[i]
            p2 = points1[i+1]
            p3 = points2[j]
            p4 = points2[j+1]
            intersect, point = is_intersecting(p1, p2, p3, p4)
            if intersect:
                intersections.append(point)

    return intersections

def get_closest(intersections):

    smallest = 99999
    for point in intersections:
        s = abs(point[0]) + abs(point[1])
        if  s < smallest:
            smallest = s
            

    return smallest

def sequence_to_points(sequence):
    points = [[0,0]]
    for dir in sequence:
        d = dir[0]
        n = int(dir[1:])
        p = copy.deepcopy(points[-1])
        if d == 'L':
            p[0] -= n
        if d == 'R':
            p[0] += n
        if d == 'D':
            p[1] -= n
        if d == 'U':
            p[1] += n
        points.append(p)
    return points

def is_point_on_line(p_test, p0, p1):
    dir, flip = direction(p0, p1)
    on_line = False
    if dir == 1: #vertical
        a = p_test[0] == p0[0]
        if flip:
            b = p1[1] < p_test[1] and p_test[1] < p0[1]
        else:
            b = p0[1] < p_test[1] and p_test[1] < p1[1]
        on_line = a and b
    else:
        a = p_test[1] == p0[1]
        if flip:
            b = p1[0] < p_test[0] and p_test[0] < p0[0]
        else:
            b = p0[0] < p_test[0] and p_test[0] < p1[0]
        on_line = a and b
    return on_line

def get_steps_to_point(p, points):

    total = 0
    for i in range(len(points) -1):
        p0 = points[i]
        p1 = points[i+1]
        if is_point_on_line(p, p0, p1):
            total += abs(p0[0] - p[0]) + abs(p0[1] - p[1])
            return total
        else:
            total += abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])


def get_best_sum_dist(intersections, p1, p2):
    smallest = 99999
    for point in intersections:
        l1 = get_steps_to_point(point, p1)
        l2 = get_steps_to_point(point, p2)
        if l1 + l2 < smallest:
            smallest = l1 + l2

    return smallest


def find_closest_from_sequences(s1, s2):
    p1 = sequence_to_points(s1)
    p2 = sequence_to_points(s2)

    intersections = get_all_intersections(p1, p2)

    closest = get_closest(intersections)

    return closest

def find_shortest_from_sequences(s1, s2):
    p1 = sequence_to_points(s1)
    p2 = sequence_to_points(s2)

    intersections = get_all_intersections(p1, p2)

    dist = get_best_sum_dist(intersections, p1, p2)
    return dist


if __name__ == '__main__':

    # s1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'.split(',')
    # s2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'.split(',')
    # p = find_shortest_from_sequences(s1, s2)
    # print(p)

    with open('Day3/input.txt','r') as f:
        s1 = f.readline().split(',')
        s2 = f.readline().split(',')
        p = find_shortest_from_sequences(s1, s2)
        print(p)


