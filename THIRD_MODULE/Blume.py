import sys
import re
import math


class FilterException(Exception):
    pass


class Bits:
    def __init__(self, size: int):
        self.__bits = bytearray(math.ceil(size / 8))

    def equal_bit(self, bit_index: int):
        if self.__bits[bit_index // 8] & (2 ** (bit_index % 8)) > 0:
            return True
        else:
            return False

    def bit_set(self, bit_index: int):
        self.__bits[bit_index // 8] |= 2 ** (bit_index % 8)


class Filter:
    def __init__(self, n: int, p: float):
        if n == 0 or p == 0:
            raise FilterException()
        self.__hash_number = Filter.__h_number(p)
        self.__size = Filter.__size_of_filter(n, p)
        self.bit_array = Bits(self.__size)
        self.__prime_numbers = Filter.__primes(self.__hash_number)

    def get_parameters(self):
        return self.__size, self.__hash_number

    @staticmethod
    def __h_number(p: float):
        h = int(round(-math.log2(p)))
        if h == 0:
            raise FilterException()
        return h

    @staticmethod
    def __size_of_filter(n: int, p: float):
        return int(round(-n * math.log2(p) / math.log(2)))

    @staticmethod
    def __primes(kol: int):
        ans = [0 for _ in range(kol)]
        ans[0] = 2
        count = 1
        value = 2
        while count != kol:
            flag = False
            for i in range(count):
                if value % ans[i] == 0:
                    value += 1
                    break
                if i == count - 1:
                    flag = True
            if flag:
                ans[count] = value
                count += 1
                value += 1
        return ans

    def __hash(self, i, v):
        return int((((i + 1) * v + self.__prime_numbers[i]) % (pow(2, 31) - 1)) % self.__size)

    def add(self, value: int):
        for i in range(self.__hash_number):
            self.bit_array.bit_set(self.__hash(i, value))

    def search(self, value: int):
        for i in range(self.__hash_number):
            index = self.__hash(i, value)
            if not self.bit_array.equal_bit(index):
                return False
        return True

    def print(self, out):
        for i in range(self.__size):
            if self.bit_array.equal_bit(i):
                out.write('1')
            else:
                out.write('0')


def main():
    fb = None
    flag = True
    # out = open('path', 'w')
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip('\n')
        if re.fullmatch(r'', line.strip()):
            continue
        if flag:
            try:
                if re.fullmatch(r'^set \d+ 0.\d+$', line):
                    n = re.findall(r'\S+', line)
                    fb = Filter(int(n[1]), float(n[2]))
                    a, b = fb.get_parameters()
                    out.write(f'{a} {b}\n')
                    flag = False
                else:
                    out.write('error\n')
            except FilterException:
                out.write('error\n')
        else:
            if re.fullmatch(r'^add \d+$', line):
                n = re.findall(r'\d+', line)
                fb.add(int(n[0]))
            elif re.fullmatch(r'^search \d+$', line):
                n = re.findall(r'\d+', line)
                ans = fb.search(int(n[0]))
                if ans:
                    out.write('1\n')
                else:
                    out.write('0\n')
            elif re.fullmatch(r'^print$', line):
                fb.print(out)
                out.write('\n')
            else:
                out.write('error\n')
    # out.close()


if __name__ == '__main__':
    main()
