import sys
import re
s = 0
for line in sys.stdin:
    for number in re.findall(r'[-+]?\d+', line):
        s += int(number)
print(s)
