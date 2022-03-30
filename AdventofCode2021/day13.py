import sys
sys.path.append('.')
import aoc
import math
from aoc_utils import grid

data_rows = aoc.get_input(13, sample=False).splitlines()

def parse():
    points = []
    folds = []
    do_folds = False
    for row in data_rows:
        if row.strip() == "":
            do_folds = True
            continue
        if do_folds:
            dir = row[11]
            num = int(row[13:])
            folds.append((dir, num))
        else:
            n1,n2 = row.split(",")
            points.append(grid.Point(int(n1),int(n2)))

    return (points, folds)

class Paper:
    def __init__(self, points):
        self.points = set(points)
        self.max_x = 0
        self.max_y = 0
        for p in points:
            if p.x > self.max_x:
                self.max_x = p.x
            if p.y > self.max_y:
                self.max_y = p.y
        self.max_x += 1
        self.max_y += 1

    def fold(self, dim, line):
        new_points = set()
        for point in self.points:
            if dim == "y":
                if point.y < line:
                    new_points.add(point)
                else:
                    new_y = point.y - 2 * (point.y - line)
                    new_points.add(grid.Point(point.x, new_y))
            if dim == "x":
                if point.x < line:
                    new_points.add(point)
                else:
                    new_x = point.x - 2 * (point.x - line)
                    new_points.add(grid.Point(new_x, point.y))
        self.points = new_points
        if dim == "x":
            self.max_x = line
        if dim == "y":
            self.max_y = line

    def draw(self):
        for y in range(self.max_y):
            row = ""
            for x in range(self.max_x):
                if grid.Point(x,y) in self.points:
                    row += "#"
                else:
                    row += "."
            print(row)

    def num_points(self):
        return len(self.points)

def part1():
    points, folds = parse()
    paper = Paper(points)
    dir, dist = folds[0]
    paper.fold(dir, dist)
    print(paper.num_points())

part1()

def part2():
    points, folds = parse()
    paper = Paper(points)
    for dir, dist in folds:
        paper.fold(dir, dist)
    paper.draw()

part2()