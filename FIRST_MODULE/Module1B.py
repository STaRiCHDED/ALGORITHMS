import sys
import re

arr = []
count = 0
set_is = False

for line in sys.stdin:
    line = line.strip('\n')
    if re.fullmatch(r'^set_size\s\d+$', line) and set_is is False:
        set_is = True
        n = re.search(r'\d+$', line)
        arr = [None for i in range(int(n[0]))]
    elif re.fullmatch(r'^push \S+$', line) and set_is is True:
        n = re.search(r'\S+$', line)
        if count != len(arr):
            for i in range(len(arr)):
                if arr[i] is None:
                    arr[i] = n[0]
                    count += 1
                    break
        else:
            print('overflow')
    elif re.fullmatch(r'^pop$', line) and set_is is True:
        if count != 0:
            print(arr[count - 1])
            arr[count - 1] = None
            count -= 1
        else:
            print('underflow')
    elif re.fullmatch(r'^print$', line) and set_is is True:
        if count != 0:
            print(' '.join(arr[:count]))
        else:
            print('empty')
    elif re.fullmatch(r'', line.strip()):
        continue
    else:
        print('error')
