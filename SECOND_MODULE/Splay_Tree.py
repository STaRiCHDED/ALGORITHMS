import sys
import re
import collections

sys.setrecursionlimit(10000000)


class SplayTreeException(Exception):
    pass


class Node:
    def __init__(self, index=None, value=None):
        self.index = index
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def __str__(self):
        if self.parent is None:
            return f'[{self.index} {self.value}]'
        else:
            return f'[{self.index} {self.value} {self.parent.index}]'


class SplayTree:
    def __init__(self):
        self.__root = None

    def __right_rotation(self, x):
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if y.parent is None:
            self.__root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def __left_rotation(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if y.parent is None:
            self.__root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def __zig(self, v):
        if v == v.parent.left:
            self.__right_rotation(v.parent)
        elif v == v.parent.right:
            self.__left_rotation(v.parent)

    def __zigzig(self, b, v):
        if b:
            self.__right_rotation(v.parent.parent)
            self.__right_rotation(v.parent)
        elif not b:
            self.__left_rotation(v.parent.parent)
            self.__left_rotation(v.parent)

    def __zigzag(self, b, v):
        if b:
            self.__right_rotation(v.parent)
            self.__left_rotation(v.parent)
        elif not b:
            self.__left_rotation(v.parent)
            self.__right_rotation(v.parent)

    def __splay(self, v):
        if v is None:
            return
        while v.parent is not None:

            if v.parent.parent is None:
                self.__zig(v)
            else:
                if v == v.parent.left and v.parent.parent.left == v.parent:
                    self.__zigzig(True, v)
                elif v == v.parent.right and v.parent.parent.right == v.parent:
                    self.__zigzig(False, v)
                elif v == v.parent.left and v.parent.parent.right == v.parent:
                    self.__zigzag(True, v)
                elif v == v.parent.right and v.parent.parent.left == v.parent:
                    self.__zigzag(False, v)

    @staticmethod
    def __max_in_splay(v):
        max_v = v
        while max_v.right is not None:
            max_v = max_v.right
        return max_v

    def max(self):
        if self.__root is None:
            raise SplayTreeException(False)
        max_v = self.__max_in_splay(self.__root)
        self.__splay(max_v)
        return max_v.index, max_v.value

    @staticmethod
    def __min_in_splay(v):
        min_v = v
        while min_v.left is not None:
            min_v = min_v.left
        return min_v

    def min(self):
        if self.__root is None:
            raise SplayTreeException(False)
        min_v = self.__min_in_splay(self.__root)
        self.__splay(min_v)
        return min_v.index, min_v.value

    def __search_helper(self, v, index):
        if v is None:
            return

        if v.index == index:
            return v

        elif v.index > index:
            if v.left is not None:
                return self.__search_helper(v.left, index)
            else:
                return v
        else:
            if v.right is not None:
                return self.__search_helper(v.right, index)
            else:
                return v

    def add(self, index, value):
        parent = self.__search_helper(self.__root, index)

        if parent is None:
            self.__root = Node(index, value)
            return

        if parent.index == index:
            self.__splay(parent)
            raise SplayTreeException(False)
        elif parent.index > index:
            new = Node(index, value)
            parent.left = new
        else:
            new = Node(index, value)
            parent.right = new

        new.parent = parent
        self.__splay(new)

    def set(self, index, value):

        set_v = self.__search_helper(self.__root, index)
        self.__splay(set_v)

        if set_v is None or set_v.index != index:
            raise SplayTreeException(False)
        self.__root.value = value

    def delete(self, index):
        del_v = self.__search_helper(self.__root, index)
        self.__splay(del_v)

        if del_v is None or del_v.index != index:
            raise SplayTreeException(False)
        if del_v.left is None and del_v.right is None:
            self.__root = None
        elif del_v.left is None:
            self.__root = del_v.right
            self.__root.parent = None
        elif del_v.right is None:
            self.__root = del_v.left
            self.__root.parent = None
        else:
            ch_root = self.__max_in_splay(del_v.left)
            self.__splay(ch_root)
            ch_root.right = del_v.right
            if ch_root.right is not None:
                ch_root.right.parent = ch_root

    def search(self, index):
        search_v = self.__search_helper(self.__root, index)
        self.__splay(search_v)

        if search_v is None or search_v.index != index:
            return
        return search_v.value

    class __PrintNodes:
        def __init__(self, v, k, l):
            self.node = v
            self.position = k
            self.level = l

        def __str__(self):
            return str(self.node)

    def print(self, out):
        if self.__root is None:
            out.write('_\n')
            return
        k = 1
        queue = collections.deque()
        queue.append(SplayTree.__PrintNodes(self.__root, 1, 0))
        i = 1
        level = 0
        k_first = True
        line = ''
        k_pred = 0
        while True:
            if not queue:
                line += ' _' * (k - i + 1)
                out.write(line)
                out.write('\n')
                break
            v = queue.popleft()
            if level != v.level:
                line += ' _' * (k - i + 1)
                out.write(line)
                out.write('\n')
                k *= 2
                i = 1
                k_first = True
                line = ''
                k_pred = 0
                level += 1
            if k_first and i <= v.position:
                line += '_ ' * (v.position - k_pred - 1) + str(v)
                i += v.position - k_pred
                k_pred = v.position
                k_first = False
            elif not k_first and i <= v.position:
                line += ' _' * (v.position - k_pred - 1) + ' ' + str(v)
                i += v.position - k_pred
                k_pred = v.position
            if v.node.left is not None:
                queue.append(SplayTree.__PrintNodes(v.node.left, v.position * 2 - 1, level + 1))
            if v.node.right is not None:
                queue.append(SplayTree.__PrintNodes(v.node.right, v.position * 2, level + 1))


def main():
    my_splay_tree = SplayTree()
    # out = open('path', 'w')
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip('\n')
        if re.fullmatch(r'', line.strip()):
            continue
        try:
            if re.fullmatch(r'^add -?\d+ \S+$', line):
                n = re.findall(r'\S+', line)
                my_splay_tree.add(int(n[1]), n[2])
            elif re.fullmatch(r'^set -?\d+ \S+$', line):
                n = re.findall(r'\S+', line)
                my_splay_tree.set(int(n[1]), n[2])
            elif re.fullmatch(r'^delete -?\d+$', line):
                n = re.findall(r'-?\d+', line)
                my_splay_tree.delete(int(n[0]))
            elif re.fullmatch(r'^search -?\d+$', line):
                n = re.findall(r'-?\d+', line)
                a = my_splay_tree.search(int(n[0]))
                if a is not None:
                    out.write(f'1 {a}\n')
                else:
                    out.write('0\n')
            elif re.fullmatch(r'^min$', line):
                a, b = my_splay_tree.min()
                out.write(f'{a} {b}\n')
            elif re.fullmatch(r'^max$', line):
                a, b = my_splay_tree.max()
                out.write(f'{a} {b}\n')
            elif re.fullmatch(r'^print$', line):
                my_splay_tree.print(out)
            else:
                out.write('error\n')
        except SplayTreeException:
            out.write('error\n')
    # out.close()


if __name__ == '__main__':
    main()
