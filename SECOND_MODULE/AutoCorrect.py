import sys


class Node:
    def __init__(self, word: str):
        self.word = word
        self.words = {}
        self.end = False


'''
Класс узел, данный класс предназначен для хранения информации о словах префиксного дерева, 
находится ли данное слово в словаре, а также хранит словарь узлов образованных от этого слова,
путём добавления следующего символа.

'''


class PrefixTree:
    def __init__(self):
        self.__root = Node('')

    '''
    Класс префиксное дерево, данный класс предназначен для хранения корня нашего дерева.
    '''

    def add(self, word: str):
        begin = self.__root
        line = ''
        for sign in word:
            line += sign
            if sign not in begin.words:
                begin.words[sign] = Node(line)
            begin = begin.words[sign]
        begin.end = True

    '''
    Функция вставки слова в префиксное дерево;
    В начале мы берём наш корень, и начинаем посимвольно проверять,если такого символа нет, то происходит добавление
    нового узла в словаре, в протвном случае просто переходим по этому символу.
    Сложность по времени O(l), где l - длина входного слова, так как нам необходимо проверить каждый символ. 
    Сложность по памяти O(l), где l - длина входного слова,так как нам необходимо добавить каждый символ в дерево
    '''

    def is_word_in_tree(self, word):
        begin = self.__root
        for sign in word:
            if sign not in begin.words:
                return False
            else:
                begin = begin.words[sign]
        return begin.end

    '''
    Функция проверки наличия слова в префиксное дерево;
    В начале мы берём наш корень, и начинаем посимвольно проверять,если такого символа нет, то выводим,
    что такого слова нет, в противном случае просто переходим по этому символу,и ищем дальше,дойдя до конца
    мы смотрим есть ли это слово в словаре.
    Сложность по времени O(l), где l - длина входного слова, так как нам необходимо проверить каждый символ. 
    Сложность по памяти O(1), так как мы храним ссылку на вершину (узел), в которой мы сейчас находимся.
    '''

    @staticmethod
    def __search_helper(word, node, letter, letter_before, before_c_row, before_before_row, result):
        columns = len(word) + 1
        current_row = [before_c_row[0] + 1]
        for column in range(1, columns):
            insert_cost = current_row[column - 1] + 1
            delete_cost = before_c_row[column] + 1
            if word[column - 1] != letter:
                replace_cost = before_c_row[column - 1] + 1
            else:
                replace_cost = before_c_row[column - 1]
            if column >= 2 and letter_before is not None and letter == word[column - 2] and letter_before == \
                    word[column - 1] and letter != word[column - 1]:
                current_row.append(min(insert_cost, delete_cost, replace_cost, before_before_row[column - 2] + 1))
                continue
            current_row.append(min(insert_cost, delete_cost, replace_cost))
        if current_row[-1] <= 1 and node.end:
            result.append(node.word)
        if min(current_row) <= 1:
            for next_letter in node.words:
                PrefixTree.__search_helper(word, node.words[next_letter], next_letter, letter, current_row,
                                           before_c_row, result)

    '''
    Алгоритм поиска похожих слов:
    Функция создана на основе алгоритма Дамерау-Левенштейна, но вместо проверки двух слов сразу,
    мы проверяем каждый символ
    Сложность по времени O(n*l), 
    где n - число узлов в префиксном дереве, 
    l - длина проверяемого слова. 
    Для слова, проверяется символ из ветви дерева, тем самым мы для каждого узла в дереве создаем
    одну строку в таблице

    Сложность по памяти O(n*l), 
    где n - число узлов в префиксном дереве, 
    l - длина проверяемого слова. 
    Для обхода узлов  мы используем рекурсивный метод, следовательно заполняем стек вызовов. 
    # O(n) - сложность этого метода. А так как для проверки мы храним три строки длиной l,
    то сложность по памяти будет составлять O(l).
    А всё вместе даст нам рзультат O(n*l).
    '''

    def search(self, word):
        current_row = range(len(word) + 1)
        result = []
        for letter in self.__root.words:
            PrefixTree.__search_helper(word, self.__root.words[letter], letter, None, current_row, None, result)
        return sorted(result)

    '''
    Функция поиска похожих слов
    '''


def main():
    pref_tree = PrefixTree()
    size = int(input())
    k = 0
    while k < size:
        pref_tree.add(input().lower())
        k += 1
    # out = open('path', 'w')
    out = sys.stdout
    for line in sys.stdin:
        line = line.strip('\n')
        if line == '':
            continue
        if pref_tree.is_word_in_tree(line.lower()):
            out.write(f'{line} - ok')
        else:
            same_words = pref_tree.search(line.lower())
            if same_words:
                out.write(f'{line} -> ')
                out.write(', '.join(same_words))
            else:
                out.write(f'{line} -?')
        out.write('\n')
    # out.close()


if __name__ == '__main__':
    main()
