
class Automata:

    def __init__(self, transitions, alphabet, states, initial_states, final_states):
        self.transitions = transitions
        self.alphabet = alphabet
        self.states = states
        self.initial_states = initial_states
        self.final_states = final_states

    def testInput(self, input, state):
        if input != "":
            for transition in self.transitions:
                if transition[0] == state:
                    if transition[1] != "a-z" and transition[1] != "A-Z" and transition[1] != "0-9" and transition[1] != "1-9":
                        if transition[1] == input[0]:
                            return False or self.action(input[1:], transition[2])
                    elif input[0] in self.get_range(transition[1]):
                        return False or self.testInput(input[1:], transition[2])
            return False
        else:
            if state in self.final_states:
                return True
            else:
                return False

    def show_states(self):
        print(self.states)

    def show_alphabet(self):
        print(self.alphabet)

    def show_transitions(self):
        for transition in self.transitions:
            print(transition)

    def show_final_states(self):
        print(self.final_states)

    def get_range(self, interval):
        aux = []

        if interval == "a-z":
            for i in range(ord("a"), ord("z")+1):
                aux.append(chr(i))
            return aux

        if interval == "A-Z":
            for i in range(ord("A"), ord("Z")+1):
                aux.append(chr(i))
            return aux

        if interval == "0-9":
            for i in range(ord("0"), ord("9")+1):
                aux.append(chr(i))
            return aux

        if interval == "1-9":
            for i in range(ord("1"), ord("9")+1):
                aux.append(chr(i))
            return aux

        return None

def print_menu():
    print("1. Show states")
    print("2. Show alphabet")
    print("3. Show transitions")
    print("4. Show final states")
    print("0. Exit")

def read_transitions():
    f = open("FA.in", "r")
    alphabet = []
    transitions = []
    states = []
    initial_states = []
    final_states = []
    line = ""
    f.readline()
    while line.lower() != "alphabet":
        line = f.readline().strip("\n")    
        transitions.append(line.split(","))

    while line.lower() != "states":
        line = f.readline().strip("\n")
        alphabet.append(line)

    while line.lower() != "initial_states":
        line = f.readline().strip("\n")
        states.append(line)

    while line.lower() != "final_states":
        line = f.readline().strip("\n")
        initial_states.append(line)

    while line:
        line = f.readline().strip("\n")
        if not line:
            break
        final_states.append(line)

    return transitions[:-1], alphabet[:-1], states[:-1], initial_states[:-1], final_states


def run():

    transitions, alphabet, states, initial_states, final_states = read_transitions()
    a = Automata(transitions, alphabet, states, initial_states, final_states)
    inputt = "variabilaCorecta123DA"
    input2 = "-INCORECT2"
    input3 = "siAstaincorecta!!!"
    input4 = "astaEfoarteBuna10din10"

    while True:
        print_menu()
        option = input("Choose option: ")

        if option == "1":
            a.show_states()
        if option == "2":
            a.show_alphabet()
        if option == "3":
            a.show_transitions()
        if option == "4":
            a.show_final_states()
        if option == "0":
            break


    print(a.testInput(inputt, "p"))
    print(a.testInput(input2, "p"))
    print(a.testInput(input3, "p"))
    print(a.testInput(input4, "p"))

run()

