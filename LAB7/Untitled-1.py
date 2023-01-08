from Parser import EPSILON
from Parser import Parser


class Grammar:

    def __init__(self, file_name):
        self.file_name = file_name
        self.non_terminals, self.terminals, self.program, self.productions = self.read_grammar()
        self.productions_with_numbers = []
        self.create_numbered_productions()

    def create_numbered_productions(self):
        for production_key in self.productions:
            production_values = self.productions[production_key]

            for prod in production_values:
                self.productions_with_numbers.append((production_key, prod))

    def read_grammar(self):
        f = open(self.file_name, "r")
        gr = []
        for line in f:
            gr.append(line)
        f.close()
        non_terminals = gr[0].strip().split(" ")
        terminals = gr[1].strip().split(" ")
        program = gr[2].strip()
        productions_list = [t.strip() for t in gr[3:]]
        productions = {}
        for p in productions_list:
            pr = p.strip().split(":")
            key = pr[0]
            productions[key] = []
            dest = pr[1].split("|")
            for d in dest:
                productions[key].append(d.split(" "))
        return non_terminals, terminals, program, productions

    def get_production(self, non_terminal):
        return self.productions[non_terminal]

    def get_production_with_number(self, num):
        return self.productions_with_numbers[num]


    def cfg_check(self):
        for symbol in self.productions:
            if symbol not in self.non_terminals:
                return False
            productions = self.productions[symbol]
            for production in productions:
                for elem in production:
                    if elem == EPSILON:
                        continue
                    if elem not in self.non_terminals and elem not in self.terminals:
                        return False
        return True

if __name__ == "__main__":
    with open('out1.txt', 'w') as f:    
        f.write('')
    gr = Grammar("g1.txt")
    if gr.cfg_check():
        for non_terminal in gr.non_terminals:
            print(str(non_terminal) + " -> " + str(gr.get_production(non_terminal)))

    pr = Parser(gr)
    pr.first()
    pr.follow()
    print()
    try:
        pr.parse_table()
    except Exception as e:
        print(e)
        exit()    
    with open('out1.txt', 'a') as f:    
        f.write(pr.get_parsing_table_as_string())
    print()

# https://www.geeksforgeeks.org/compiler-design-ll1-parser-in-python
    try:
        pr.parse_algorithm_start("a r k O", "parser_output.txt")
    except Exception as e:
        print(e)