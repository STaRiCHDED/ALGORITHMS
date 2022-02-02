import sys
import re


class HeapException(Exception):
    pass


class Vertex:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    @staticmethod
    def get_parent(index: int):
        return (index - 1) // 2

    @staticmethod
    def get_left(index: int):
        return 2 * index + 1

    @staticmethod
    def get_right(index: int):
        return 2 * index + 2


class MinHeap:
    def __init__(self):
        self.__indexes_vertexes = list()
        self.__keys_indexes = dict()

    @staticmethod
    def __siftdown(index: int, array_, dict_):
        while 2 * index + 1 < len(array_):
            change = left = Vertex.get_left(index)
            right = Vertex.get_right(index)
            if right < len(array_) and array_[right].key < array_[left].key:
                change = right
            if array_[index].key < array_[change].key:
                break
            dict_[array_[index].key], dict_[array_[change].key] = change, index
            array_[index], array_[change] = array_[change], array_[index]
            index = change

    @staticmethod
    def __siftup(index: int, array_, dict_):
        parent = Vertex.get_parent(index)
        while array_[index].key < array_[parent].key:
            dict_[array_[index].key], dict_[array_[parent].key] = parent, index
            array_[index], array_[parent] = array_[parent], array_[index]
            index = parent
            parent = Vertex.get_parent(index)
            if parent < 0:
                break

    def add(self, key, value):
        if key in self.__keys_indexes:
            raise HeapException()
        if not self.__indexes_vertexes:
            self.__indexes_vertexes.append(Vertex(key, value))
            self.__keys_indexes[key] = 0
        else:
            self.__indexes_vertexes.append(Vertex(key, value))
            self.__keys_indexes[key] = len(self.__indexes_vertexes) - 1
            MinHeap.__siftup(len(self.__indexes_vertexes) - 1, self.__indexes_vertexes, self.__keys_indexes)

    def set(self, key, value):
        if key not in self.__keys_indexes:
            raise HeapException()
        self.__indexes_vertexes[self.__keys_indexes[key]].value = value

    def delete(self, key):
        if key not in self.__keys_indexes:
            raise HeapException()
        if self.__keys_indexes[key] >= 0:
            ind = self.__keys_indexes[key]
            if ind == len(self.__indexes_vertexes) - 1:
                self.__indexes_vertexes.pop()
                del self.__keys_indexes[key]
            elif ind == 0:
                del self.__keys_indexes[key]
                self.__keys_indexes[self.__indexes_vertexes[len(self.__indexes_vertexes) - 1].key] = ind
                self.__indexes_vertexes[ind] = self.__indexes_vertexes[len(self.__indexes_vertexes) - 1]
                self.__indexes_vertexes.pop()
                MinHeap.__siftdown(ind, self.__indexes_vertexes, self.__keys_indexes)
            else:
                del self.__keys_indexes[key]
                self.__keys_indexes[self.__indexes_vertexes[len(self.__indexes_vertexes) - 1].key] = ind
                self.__indexes_vertexes[ind] = self.__indexes_vertexes[len(self.__indexes_vertexes) - 1]
                self.__indexes_vertexes.pop()
                parent = Vertex.get_parent(ind)
                if self.__indexes_vertexes[ind].key > self.__indexes_vertexes[parent].key:
                    MinHeap.__siftdown(ind, self.__indexes_vertexes, self.__keys_indexes)
                else:
                    MinHeap.__siftup(ind, self.__indexes_vertexes, self.__keys_indexes)

    def extract(self):
        if not self.__indexes_vertexes:
            raise HeapException()
        root = self.__indexes_vertexes[0]
        self.delete(root.key)
        return root.key, root.value

    def search(self, key):
        if key not in self.__keys_indexes:
            return None, None
        return self.__keys_indexes[key], self.__indexes_vertexes[self.__keys_indexes[key]].value

    def min_in_heap(self):
        if not self.__indexes_vertexes:
            raise HeapException()
        return self.__indexes_vertexes[0].key, self.__indexes_vertexes[0].value

    def max_in_heap(self):
        if not self.__indexes_vertexes:
            raise HeapException()
        max_v = self.__indexes_vertexes[0]
        max_ind = 0
        k = len(self.__indexes_vertexes)
        for i in range(k // 2, k):
            if self.__indexes_vertexes[i].key > max_v.key:
                max_v = self.__indexes_vertexes[i]
                max_ind = i
        return max_v.key, max_ind, max_v.value

    def print(self, out):
        if not self.__indexes_vertexes:
            out.write('_\n')
            return
        out.write(f'[{self.__indexes_vertexes[0].key} {self.__indexes_vertexes[0].value}]\n')
        k = 0
        border = 2
        line = ''
        first = True
        for i in range(1, len(self.__indexes_vertexes)):
            if first:
                first = False
                line += f'[{self.__indexes_vertexes[i].key} ' \
                        f'{self.__indexes_vertexes[i].value} ' \
                        f'{self.__indexes_vertexes[Vertex.get_parent(i)].key}]'
            else:
                line += ' ' + f'[{self.__indexes_vertexes[i].key} ' \
                              f'{self.__indexes_vertexes[i].value} ' \
                              f'{self.__indexes_vertexes[Vertex.get_parent(i)].key}]'
            k += 1
            if k == border:
                first = True
                k = 0
                border *= 2
                out.write(line)
                out.write('\n')
                line = ''
        if k > 0:
            line += ' _' * (border - k)
            out.write(line)
            out.write('\n')


def main():
    heap = MinHeap()
    # out = open('path', 'w')
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip('\n')
        if re.fullmatch(r'', line.strip()):
            continue
        try:
            if re.fullmatch(r'^add -?\d+ \S+$', line):
                n = re.findall(r'\S+', line)
                heap.add(int(n[1]), n[2])
            elif re.fullmatch(r'^set -?\d+ \S+$', line):
                n = re.findall(r'\S+', line)
                heap.set(int(n[1]), n[2])
            elif re.fullmatch(r'^delete -?\d+$', line):
                n = re.findall(r'-?\d+', line)
                heap.delete(int(n[0]))
            elif re.fullmatch(r'^search -?\d+$', line):
                n = re.findall(r'-?\d+', line)
                a, b = heap.search(int(n[0]))
                if type(a) == int:
                    out.write(f'1 {a} {b}\n')
                else:
                    out.write('0\n')
            elif re.fullmatch(r'^min$', line):
                a, b = heap.min_in_heap()
                out.write(f'{a} 0 {b}\n')
            elif re.fullmatch(r'^max$', line):
                a, b, c = heap.max_in_heap()
                out.write(f'{a} {b} {c}\n')
            elif re.fullmatch(r'^extract$', line):
                a, b = heap.extract()
                out.write(f'{a} {b}\n')
            elif re.fullmatch(r'^print$', line):
                heap.print(out)
            else:
                out.write('error\n')
        except HeapException:
            out.write('error\n')
    # out.close()


if __name__ == '__main__':
    main()
