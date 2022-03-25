import aoc
import sys
import os
import pathlib

year_folder = f'AdventofCode{aoc.YEAR}'
cur_files = os.listdir(os.path.join('.', year_folder))
max_day = 0
for file in cur_files:
    if file.startswith('day'):
        cur_day = int(file[3])
        if cur_day > max_day: 
            max_day = cur_day
aoc_path = pathlib.Path(__file__).parent.resolve()
aoc_path_str = str(aoc_path).replace('\\', '\\\\')

if len(sys.argv) > 1:
    if sys.argv[1] == 'next':
        next_day = max_day + 1
        next_file = os.path.join('.', year_folder, f'day{next_day}.py')
        if os.path.exists(next_file):
            print(f'{next_file} already exists, not overwriting')
        else:
            with open(next_file, 'w') as f:
                f.writelines(['import sys\n', "sys.path.append('.')\n", 'import aoc\n', '\n', f'data_rows = aoc.get_input({next_day}, sample=False).splitlines()\n'])