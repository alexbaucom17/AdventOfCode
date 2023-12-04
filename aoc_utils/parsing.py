
def int_grid(rows):
    return [[int(c) for c in row] for row in rows]

def group_by_blank_lines(rows):
    out = []
    tmp = []
    for row in rows:
        if not row.strip():
            out.append(tmp)
            tmp = []
        else:
            tmp.append(row)
    out.append(tmp)
    return out

def get_numbers_with_separator(row: str, sep: str=" ") -> list[int]:
    return [int(num.strip()) for num in row.strip().split(sep) if num]