class HashTable:
    def __init__(self):
        self.capacity = 6789
        self.size = 0
        self.elements = {}


    def insert(self, key, value):
        position = hash(key)
        self.size += 1

        if position not in self.elements:
            self.elements[position] = []

        self.elements[position].append((key,value))

    def get(self, key):
        position = hash(key)

        if position not in self.elements:
            return -1

        for pair in self.elements[position]:
            if pair[0] == key:
                return pair[1]

        return -1

    def hash(self, key):
         return sum(ord(character) for character in str(key)) % 100

    def __str__(self):
        res = ""
        entries = []

        for t in self.elements.values():
            for entry in t:
                entries.append(entry)

        entries.sort(key=lambda x: x[1])

        for entry in entries:
            res += str(entry) + "\n"

        return res
