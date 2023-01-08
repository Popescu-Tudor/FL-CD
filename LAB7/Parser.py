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

    def parse_table(self):
        rows = self.grammar.non_terminals + self.grammar.terminals + ['$']
        columns = self.grammar.terminals + ['$']

        for row in rows:
            if row == EPSILON:
                continue
            self.parsing_table[row] = {}
            for column in columns:
                if column == EPSILON:
                    continue
                self.parsing_table[row][column] = ()
                if row == column:
                    if row == '$':
                        self.parsing_table[row][column] = ("acc", None, None)
                    else:
                        self.parsing_table[row][column] = ("pop", None, None)

        for index in range(len(self.grammar.productions_with_numbers)):
            current_production = self.grammar.productions_with_numbers[index]
            left = current_production[0]
            right = current_production[1]

            first_list = self.first_of(right[0])
            for element in first_list:
                if element in self.grammar.terminals:
                    if len(self.parsing_table[left][element]) >= 1:
                        raise Exception(f"There is a conflict at row {left} and column {element} \n"
                                        f"The current value is {self.parsing_table[left][element]} \n")
                    self.parsing_table[left][element] = (left, right, index + 1)
            if EPSILON in first_list:
                follow_list = self.follow_map[left]
                for element in follow_list:
                    if element in self.grammar.terminals:
                        if len(self.parsing_table[left][element]) >= 1:
                            raise Exception(f"There is a conflict at row {left} and column {element} \n"
                                            f"The current value is {self.parsing_table[left][element]} \n")
                        self.parsing_table[left][element] = (left, [EPSILON], index + 1)
                if '$' in follow_list:
                    self.parsing_table[left]['$'] = (left, [EPSILON], index + 1)

    def parse_algorithm_start(self, sequence, output_file):
        input_stack = copy.deepcopy(sequence.split(" ")) + ['$']
        working_stack = [self.grammar.program, '$']
        output_stack = [EPSILON]

        output_stack = self.parse_algorithm(input_stack, working_stack, output_stack)
        with open("out1.txt","a") as f:
            print(output_stack)
            f.write(str(output_stack))
            f.write('\n\n')
        for el in output_stack:
            with open("out1.txt","a") as f:
                f.write(str(self.grammar.get_production_with_number(el-1)))
                f.write('\n')
    def parse_algorithm(self, input_stack, working_stack, output_stack):
        first_input = input_stack[0]
        first_working = working_stack[0]
        try:
            table_value = self.parsing_table[first_working][first_input]
            if table_value[0] == "pop":
                input_stack = input_stack[1:]
                working_stack = working_stack[1:]
                with open("out1.txt","a") as f:
                    f.write('----------\n')
                    f.write(str(input_stack)+'\n')
                    f.write(str(working_stack)+'\n')
                    f.write("matched\n")
                    f.write("-----------\n")
            elif table_value[0] == "acc":
                with open("out1.txt","a") as f:
                    f.write("valid\n")
                return output_stack
            else:
                with open("out1.txt","a") as f:
                    f.write('----------\n')
                    f.write(str(input_stack)+'\n')
                    f.write(str(working_stack)+'\n')
                    f.write(str(table_value)+"\n")
                    f.write("-----------\n")
                working_stack = working_stack[1:]
                

                if table_value[1][0] != EPSILON:
                    value = copy.deepcopy(table_value[1])
                    value.extend(working_stack)
                    working_stack = copy.deepcopy(value)

                if len(output_stack) == 1 and output_stack[0] == EPSILON:
                    output_stack = [table_value[2]]
                else:
                    output_stack += [table_value[2]]

        except Exception:
            raise Exception(f'The sequence has an error! ({first_working, first_input}) key does not exist '
                            f'in the parsing table.')

        return self.parse_algorithm(input_stack, working_stack, output_stack)
    def get_parsing_table_as_string(self):
        header = self.grammar.terminals + ['$']
        parse_table = []
        rows = self.grammar.non_terminals + self.grammar.terminals + ['$']
        for row in rows:
            row_list = [row]
            for col in header:
                data = self.parsing_table[row][col]
                if len(data) == 3:
                    string_data = str(data[0]) + " -> " + str(data[1]) + " | " + str(data[2])
                else:
                    string_data = ""
                row_list.append(string_data)
            parse_table.append(row_list)
        return tabulate(parse_table, headers=header, tablefmt="grid")

    def get_first_map(self):
        return self.first_map

    def get_follow_map(self):
        return self.follow_map