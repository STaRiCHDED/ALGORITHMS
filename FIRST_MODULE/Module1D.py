import sys
import re
import collections

data_in = False
data = dict()
oriented = False
deep = False
start = ''
visited = set()
for line in sys.stdin:
    line = line.strip()
    if re.match(r'^[du] \S+ [bd]$', line) and data_in is False:
        if line[0] == 'd':
            oriented = True
        if line[-1] == 'd':
            deep = True
        n = re.search(r' \S+ ', line)
        start = n[0].strip()
        data_in = True
    elif re.match(r'^\S+ \S+$', line) and data_in is True:
        n = re.findall(r'\S+', line)
        if oriented is not True:
            if data.get(n[0]) is None:
                data[n[0]] = {n[1]}
            else:
                data[n[0]].add(n[1])
            if data.get(n[1]) is None:
                data[n[1]] = {n[0]}
            else:
                data[n[1]].add(n[0])
        else:
            if data.get(n[0]) is None:
                data[n[0]] = {n[1]}
            else:
                data[n[0]].add(n[1])
    else:
        continue
if deep is True:  # Поиск в глубину
    tops = collections.deque([start])
    while len(tops) > 0:
        v = tops.pop()
        if v in visited:
            continue
        visited.add(v)
        print(v)
        if v in data:
            for i in sorted(list(data[v]), reverse=True):
                if i not in visited:
                    tops.append(i)
        else:
            continue
else:  # Поиск в ширину
    tops = collections.deque([start])
    while len(tops) > 0:
        v = tops.popleft()
        if v in visited:
            continue
        visited.add(v)
        print(v)
        if v in data:
            for i in sorted(list(data[v])):
                if i not in visited:
                    tops.append(i)
        else:
            continue
