class Grammar:
       
    def __init__(self,nonterminals,terminals,starting,productions):
        self.nonterminals=nonterminals
        self.terminals=terminals
        self.starting=starting
        self.productions=productions
    
    def show_nonterminals(self):
        print(self.nonterminals)
    
    def show_terminals(self):
        print(self.terminals)

    def show_starting(self):
        print(self.starting)    

    def show_productions(self):
        print(self.productions) 
    
    def show_forGiven_nonterminal(self,aux):
        pass   

    def cfg_check(self):
        pass

def read_from_file(filename):
        productions={}
        with open(filename) as f:
            nonterminals = f.readline().strip().split(" ")
            terminals = f.readline().strip().split(" ")
            starting = f.readline().strip()
            for line in f:
                aux = line.strip().split("->")
                productions.setdefault(aux[0], []).append(aux[1].strip().split(" "))
        return nonterminals,terminals,starting,productions                
       
def show_menu():
        print("1. Show nonterminals")
        print("2. Show terminals")
        print("3. Show starting nonterminal")
        print("4. Show productions")
        print("0. Exit")
    
def run():
         nonterminals,terminals,starting,productions=read_from_file("g1.txt")
         gram= Grammar(nonterminals,terminals,starting,productions)
