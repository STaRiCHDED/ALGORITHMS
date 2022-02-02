import re
import sys


def find_ans(price: int):
    ans = list()
    while True:
        if price % 2 == 0:
            ans.append('dbl')
            price = int(price / 2)
        else:
            if price == 1:
                ans.append('inc')
                price -= 1
                return ans
            elif price == 3:
                ans.append('inc')
                price -= 1
            else:
                before, after = price + 1, price - 1
                res = after & before
                if res != after:
                    ans.append('dec')
                    price += 1
                else:
                    ans.append('inc')
                    price -= 1


def main():
    price = 0
    # out = open('path', 'w')
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip('\n')
        if re.fullmatch(r'', line.strip()):
            continue
        if re.fullmatch(r'^\d+$', line):
            price = int(re.findall(r'\d+', line)[0])
            break
        else:
            out.write('error')
    if price:
        ans = find_ans(price)
        for i in ans[::-1]:
            out.write(str(i) + '\n')
    # out.close()


if __name__ == '__main__':
    main()
