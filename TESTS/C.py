import sys
import re

s = 0
path_input = sys.argv[1]
path_output = sys.argv[2]
with open(path_input, 'r') as inp:
    for line in inp:
        for number in re.findall(r'[-+]?\d+', line):
            s += int(number)
with open(path_output, 'w') as out:
    out.write(str(s % 256))
