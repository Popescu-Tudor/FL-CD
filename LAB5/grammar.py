
class Grammar:

    def __init__(self, file_name):
        self.file_name = file_name
        self.non_terminals, self.terminals, self.program, self.productions = self.read_grammar()

    def read_grammar(self):
        f = open(self.file_name, "r")
        gr = []
        for line in f:
            gr.append(line)
        f.close()
        non_terminals = gr[0].strip().split(" ")
        terminals = gr[1].strip().split(" ")
        program = gr[2].strip()
        predictions_list = [t.strip() for t in gr[3:]]
        predictions = {}
        for p in predictions_list:
            pr = p.strip().split(":")
            key = pr[0]
            predictions[key] = []
            dest = pr[1].split("|")
            for d in dest:
                predictions[key].append(d.split(" "))
        return non_terminals, terminals, program, predictions

    def get_production(self, non_terminal):
        return self.productions[non_terminal]

    def cfg_check(self):
        for symbol in self.productions:
            if symbol not in self.non_terminals:
                return False
            productions = self.productions[symbol]
            for production in productions:
                for elem in production:
                    if elem not in self.non_terminals and elem not in self.terminals:
                        return False
        return True


if __name__ == "__main__":
    gr = Grammar("g1.txt")
    print("Non terminals: " + str(gr.non_terminals))
    print("Terminals: " + str(gr.terminals))
    print("Program: " + str(gr.program))
    if gr.cfg_check():
        for non_terminal in gr.non_terminals:
            print(str(non_terminal) + " -> " + str(gr.get_production(non_terminal)))
    
    print(gr.cfg_check())
