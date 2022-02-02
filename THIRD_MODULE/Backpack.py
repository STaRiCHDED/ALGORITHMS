import sys
import re
import math


class BackPack:
    def __init__(self):
        self.__capacities = dict()
        self.__total_value = 0
        self.__total_weight = 0

    def add(self, capacity, cost, item, maxcapacity):
        if capacity > maxcapacity:
            return
        self.__capacities[len(self.__capacities) + 1] = (item, cost, capacity)

    def find_ans(self, maxcapacity, nod, ans):
        if nod == 0:
            nod = 1
        matrix = [[0 for _ in range((maxcapacity // nod) + 1)] for _ in range(len(self.__capacities) + 1)]
        for item in range(1, len(self.__capacities) + 1):
            for s in range(0, len(matrix[0])):
                if s >= self.__capacities[item][2] // nod:
                    matrix[item][s] = max(matrix[item - 1][s],
                                          matrix[item - 1][s - self.__capacities[item][2] // nod] +
                                          self.__capacities[item][1])
                else:
                    matrix[item][s] = matrix[item - 1][s]
        self.__find_items(len(self.__capacities), len(matrix[0]) - 1, nod, ans, matrix)
        self.__total_value = matrix[len(self.__capacities)][len(matrix[0]) - 1]
        self.__total_weight = BackPack.__find_weight(ans)

    def __find_items(self, item, s, nod, ans, matrix):
        if matrix[item][s] == 0:
            return
        if matrix[item - 1][s] == matrix[item][s]:
            self.__find_items(item - 1, s, nod, ans, matrix)
        else:
            self.__find_items(item - 1, s - self.__capacities[item][2] // nod, nod, ans, matrix)
            ans.append(self.__capacities[item])

    @staticmethod
    def __find_weight(ans: list):
        cap = 0
        for i in ans:
            cap += i[2]
        return cap

    def get_cost(self):
        return self.__total_value

    def get_cap(self):
        return self.__total_weight


def main():
    bp = BackPack()
    nod = capacity = k = 0
    flag = True
    # out = open('path', 'w')
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip('\n')
        if re.fullmatch(r'', line.strip()):
            continue
        if flag and re.fullmatch(r'^\d+$', line):
            nod = capacity = int(re.findall(r'\d+', line)[0])
            flag = False
            continue
        if not flag and re.fullmatch(r'^\d+ \d+$', line):
            n = re.findall(r'\d+', line)
            k += 1
            bp.add(int(n[0]), int(n[1]), k, capacity)
            if int(n[0]) <= capacity:
                nod = math.gcd(nod, int(n[0]))
        else:
            out.write('error\n')
    ans = []
    bp.find_ans(capacity, nod, ans)
    cap = bp.get_cap()
    cost = bp.get_cost()
    out.write(f'{cap} {cost}')
    out.write('\n')
    for i in ans:
        out.write(str(i[0]) + '\n')
    # out.close()


if __name__ == '__main__':
    main()
