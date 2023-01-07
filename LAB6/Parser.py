import copy

from tabulate import tabulate

EPSILON = 'eps'


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_map = {}
        self.follow_map = {}
        self.parsing_table = {}

    def first(self):
        self.first_map = {}
        for symbol in self.grammar.non_terminals:
            self.first_map[symbol] = []
            self.first_map[symbol] = self.first_of(symbol)
        return self.first_map

    def first_of(self, symbol):
        first_set = set()

        if symbol in self.grammar.terminals:
            return [symbol]

        if symbol == EPSILON:
            return [EPSILON]

        for production in self.grammar.get_production(symbol):
            element = production[0]

            if element == EPSILON or element in self.grammar.terminals:
                first_set.add(element)
                continue

            for index in range(len(production)):
                element = production[index]
                set_of_symbol = self.first_of(element)
                for el in set_of_symbol:
                    first_set.add(el)

                if EPSILON not in set_of_symbol:
                    break

        return list(first_set)

    def follow(self):
        self.follow_map = {}
        for symbol in self.grammar.non_terminals:
            self.follow_map[symbol] = []
            self.follow_map[symbol] = self.follow_of(symbol)
        return self.follow_map

    def follow_of(self, symbol):
        follow_set = set()
        if symbol == self.grammar.program:
            follow_set.add('$')

        if symbol in self.grammar.terminals:
            return [symbol]

        if symbol == EPSILON:
            return [EPSILON]

        for non_terminal in self.grammar.non_terminals:
            if symbol == non_terminal:
                continue
            for production in self.grammar.get_production(non_terminal):
                if symbol not in production:
                    continue

                for index in range(len(production)):
                    if production[index] != symbol:
                        continue

                    # if symbol is at the end
                    if index + 1 >= len(production):
                        set_of_symbol = self.follow_of(non_terminal)
                        for el in set_of_symbol:
                            follow_set.add(el)
                        continue

                    set_of_symbol = self.first_of(production[index + 1])
                    for el in set_of_symbol:
                        if el != EPSILON:
                            follow_set.add(el)
                    if EPSILON in set_of_symbol:
                        set_of_symbol = self.follow_of(production[index + 1])
                        for el in set_of_symbol:
                            follow_set.add(el)

        return list(follow_set)

    def get_first_map(self):
        return self.first_map

    def get_follow_map(self):
        return self.follow_map
