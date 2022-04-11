import sys
sys.path.append('.')
import aoc
import math
import numpy as np
from joblib import Parallel, delayed
from anytree import Node, RenderTree, PostOrderIter
from queue import Queue
from aoc_utils.transformations import invH, rot_trans_to_H, transformPoints

data_rows = aoc.get_input(19, sample=False, index=0).splitlines()

rotX = np.asarray([[1,0,0],[0,0,-1],[0,1,0]])
rotY = np.asarray([[0,0,1],[0,1,0],[0,0,-1]])
rotZ = np.asarray([[0,-1,0],[1,0,0],[0,0,1]])
facings = [
    np.asarray([[1, 0, 0],[0, 1, 0],[0, 0, 1]]),
    np.asarray([[-1, 0, 0],[0, -1, 0],[0, 0, 1]]),
    np.asarray([[0, 1, 0],[-1, 0, 0],[0, 0, 1]]),
    np.asarray([[0, -1, 0],[1, 0, 0],[0, 0, 1]]),
    np.asarray([[0, 0, 1],[0, 1, 0],[-1, 0, 0]]),
    np.asarray([[0, 0, -1],[0, 1, 0],[1, 0, 0]])
]

def all_dir_rotations(base, R):
    out = [base]
    for i in range(1, 4):
        out.append(R @ out[-1])
    # print(out)
    return out

def build_all_rotations():
    rotations = \
        all_dir_rotations(facings[0], rotX) + \
        all_dir_rotations(facings[1], rotX) + \
        all_dir_rotations(facings[2], rotX) + \
        all_dir_rotations(facings[3], rotX) + \
        all_dir_rotations(facings[4], rotX) + \
        all_dir_rotations(facings[5], rotX)
    return rotations
all_rotations = build_all_rotations()

def parse():
    clouds = {}
    idx = 0
    for r in data_rows:
        if r.startswith("---"):
            idx = int(r.split()[2])
            clouds[idx] = {'x': [], 'y':[], 'z':[]}
        else:
            nums = r.strip().split(',')
            if len(nums) == 3:
                clouds[idx]['x'].append(int(nums[0]))
                clouds[idx]['y'].append(int(nums[1]))
                clouds[idx]['z'].append(int(nums[2]))

    outclouds = {}
    for k,v in clouds.items():
        arr = np.asarray(([v['x'],v['y'],v['z']]))
        outclouds[k] = arr
    return outclouds

def check_match(c1, c2):

    # Expand c2 to size [3, c2_points, all_R]
    c2_all_rotations = np.repeat(c2[:,:,np.newaxis], len(all_rotations), axis = 2)
    for i in range(len(all_rotations)):
        H = rot_trans_to_H(all_rotations[i], np.zeros((1,3)))
        c2_all_rotations[:,:,i] = transformPoints(c2_all_rotations[:,:,i], H)

    # This is size [3, c2_points, all_R, c1_points, c2_points]
    c2_all_translations = np.empty(list(c2_all_rotations.shape) + [c1.shape[1], c2.shape[1]], dtype=np.int32)
    for j in range(c2_all_translations.shape[4]):
        for i in range(c2_all_translations.shape[3]):
            for k in range(c2_all_translations.shape[2]):
                T = c1[:,i] - c2_all_rotations[:,j, k]
                c2_all_translations[:,:,k,i,j] = c2_all_rotations[:,:,k] + T[:, None]

    # print(c2_all_translations[:,:,1,0,0])
    # To check all points in c2_all_translations against all matches in c1, we need one more axis:
    # [3, c2_points, all_R, c1_points, c2_points, c1_points]
    c2_all_translations_expanded = np.repeat(c2_all_translations[:,:,:,:,:,np.newaxis], c1.shape[1], axis=5)
    # Swap axes for easy broadcasing of c1
    # [3, c1_points, all_R, c1_points, c2_points, c2_points]
    c2_all_translations_expanded = np.swapaxes(c2_all_translations_expanded, 1, 5)
    equality_mtx = np.equal(c2_all_translations_expanded, c1[:, :, None, None, None, None])
    # print(equality_mtx[:,:,0,0,0,:])
    # [c1_points, all_R, c1_points, c2_points, c2_points]
    equality_mtx = np.all(equality_mtx, axis=0)
    # print(equality_mtx[:,0,0,0,:])
    # [all_R, c1_points, c2_points, c2_points]
    equality_mtx = np.any(equality_mtx, axis=0)
    # print(equality_mtx[0,0,0,:])
    equality_mtx = np.sum(equality_mtx, axis=3) >= 12
    # print(equality_mtx)
    idxs = np.argwhere(equality_mtx)
    if idxs.shape[0] > 0:
        R = all_rotations[idxs[0,0]]
        T = c1[:, idxs[0,1]] - c2_all_rotations[:, idxs[0,2], idxs[0,0]] 
        return (True, R, T)
    return (False, None, None)

def join(c1, c2, R, T):
    H = rot_trans_to_H(R, T)
    return joinH(c1, c2, H)

def joinH(c1, c2, H):
    c2_transformed = transformPoints(c2, H)
    joined = np.concatenate((c1, c2_transformed), axis=1)
    joined_unique = np.unique(joined, axis=1)
    # print(f"Num points joined: {joined.shape[1]}, unique: {joined_unique.shape[1]}")
    return joined_unique

def build_registered_points(clouds):
    joined_idx = set([0])
    n_clouds = len(clouds)
    joined_points = clouds[0]
    while len(joined_idx) != n_clouds:
        found_one_match = False
        for i in range(n_clouds):
            if i in joined_idx:
                continue
            print(f"Checking for match with scanner {i}...")
            match, R, T = check_match(joined_points, clouds[i])
            if match:
                joined_points = join(joined_points, clouds[i], R, T)
                joined_idx.add(i)
                print(f"Found match for scanner {i} with offset {T}")
                found_one_match = True
        if not found_one_match:
            raise ValueError("Matching failed")
    return joined_points

def invH(H):
    R = H[:3, :3]
    d = H[:3, 3]
    Hinv = np.zeros((4,4), dtype=np.int32)
    Rinv = np.transpose(R)
    Hinv[:3,:3] = Rinv
    Hinv[:3, 3] = -Rinv @ d
    Hinv[3,3] = 1
    return Hinv

def build_registered_points2(clouds):

    matched_data = []
    for i in range(len(clouds)-1):
        matches = Parallel(n_jobs=12)(delayed(check_match)(clouds[i], clouds[j]) for j in range(i+1, len(clouds)))
        match, R, T = zip(*matches)
        for k in range(len(match)):
            match_idx = k + i + 1
            if match[k]:
                print(f"Found match between clouds {i} and {match_idx}")
                H = rot_trans_to_H(R[k], T[k])
                matched_data.append((i, match_idx, H))

    nodes = [Node(f"{i}", points=clouds[i], H=None, scanners=None) for i in range(len(clouds))]
    to_check = Queue()
    to_check.put(0)
    already_checked = set([0])
    while not to_check.empty():
        idx = to_check.get()
        already_checked.add(idx)
        matches_to_remove = []
        for match_idx, data in enumerate(matched_data):
            i, j, H = data
            if idx == i:
                nodes[j].parent = nodes[i]
                nodes[j].H = H
                T = H[:3,3].reshape((3,1))
                if nodes[j].parent.scanners is None:
                    nodes[j].parent.scanners = T
                else:
                    nodes[j].parent.scanners = np.concatenate((nodes[j].parent.scanners, T), axis=1)
                if j not in already_checked:
                    to_check.put(j)
                matches_to_remove.append(match_idx)
            elif idx == j:
                nodes[i].parent = nodes[j]
                nodes[i].H = invH(H)
                T = nodes[i].H[:3,3].reshape((3,1))
                if nodes[i].parent.scanners is None:
                    nodes[i].parent.scanners = T
                else:
                    nodes[i].parent.scanners = np.concatenate((nodes[i].parent.scanners, T), axis=1)
                if i not in already_checked:
                    to_check.put(i)
                matches_to_remove.append(match_idx)
        matched_data = [matched_data[i] for i in range(len(matched_data)) if i not in matches_to_remove]

    print(RenderTree(nodes[0]).by_attr())

    for node in PostOrderIter(nodes[0]):
        if node.is_root:
            continue
        node.parent.points = joinH(node.parent.points, node.points, node.H)
        if node.scanners is None:
            continue
        elif node.parent.scanners is not None:
            node.parent.scanners = joinH(node.parent.scanners, node.scanners, node.H)
        else:
            node.parent.scanners = joinH(np.zeros((3,1), dtype=np.int32), node.scanners, node.H)

    return (nodes[0].points, nodes[0].scanners.astype(np.int32))

def max_dist(points):
    dist = 0
    for i in range(points.shape[1]-1):
        for j in range(i+1, points.shape[1]):
            d = np.sum(np.abs(points[:, i] - points[:, j]))
            if d > dist:
                dist = d
    print(dist)

# def test_match():
#     c1 = np.asarray([
#        -618,-824,-621,
#         -537,-823,-458,
#         -447,-329,318,
#         404,-588,-901,
#         544,-627,-890,
#         528,-643,409,
#         -661,-816,-575,
#         390,-675,-793,
#         423,-701,434,
#         -345,-311,381,
#         459,-707,401,
#         -485,-357,347 
#     ]).reshape((3,-1), order='F')
#     c2 = np.asarray([
#         686,422,578,
#         605,423,415,
#         515,917,-361,
#         -336,658,858,
#         -476,619,847,
#         -460,603,-452,
#         729,430,532,
#         -322,571,750,
#         -355,545,-477,
#         413,935,-424,
#         -391,539,-444,
#         553,889,-390
#     ]).reshape((3,-1), order='F')
#     ok, R, T = check_match(c1,c2)
#     if ok:
#         joined = join(c1, c2, R, T)
#         print(check_match(joined, c2))

# test_match()

# def part1():
#     clouds = parse()
#     # print(check_match(clouds[2], clouds[4]))
#     points = build_registered_points(clouds)
#     print(points.shape[1])

# part1()

def part2():
    clouds = parse()
    points,scanners = build_registered_points2(clouds)
    print(points.shape[1])
    print(scanners)
    max_dist(scanners)
part2()