import sys
import re

arr = []
set_is = False
count = 0
head = 0
tail = -1

path_input = sys.argv[1]
path_output = sys.argv[2]

with open(path_input, 'r') as inp, open(path_output, 'w') as out:
    for line in inp:
        line = line.strip('\n')
        if re.fullmatch(r'^set_size\s\d+$', line) and set_is is False:
            set_is = True
            n = re.search(r'\d+$', line)
            arr = [None for i in range(int(n[0]))]
        elif re.fullmatch(r'^push \S+$', line) and set_is is True:
            n = re.search(r'\S+$', line)
            if count != len(arr):
                tail = (tail + 1) % len(arr)
                arr[tail] = n[0]
                count += 1
            else:
                out.write('overflow\n')
        elif re.fullmatch(r'^pop$', line) and set_is is True:
            if count != 0:
                out.write(str(arr[head]))
                out.write('\n')
                arr[head] = None
                head = (head + 1) % len(arr)
                count -= 1
            else:
                out.write('underflow\n')
        elif re.fullmatch(r'^print$', line) and set_is is True:
            if count != 0:
                if head <= tail:
                    string = (' '.join(arr[head:tail + 1])) + '\n'
                    out.write(string)
                elif head > tail:
                    n = arr[head:]
                    n += arr[:tail + 1]
                    string = (' '.join(n)) + '\n'
                    out.write(string)
            else:
                out.write('empty\n')
        elif re.fullmatch(r'', line.strip()):
            continue
        else:
            out.write('error\n')
