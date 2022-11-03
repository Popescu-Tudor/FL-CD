class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self):
        self.capacity = 100
        self.size = 0
        self.elements = [None] * self.capacity

    def hash(self, key):
        return sum(ord(character) for character in str(key)) % 100

    def insert(self, key, value):
        self.size += 1
        index = self.hash(key)
        node = self.elements[index]
        if node is None:
            self.elements[index] = Node(key, value)
            return
        prev = node
        while node is not None:
            prev = node
            node = node.next
        prev.next = Node(key, value)   

    def find(self, key):
        index = self.hash(key)
        node = self.elements[index]
        while node is not None and node.key != key:
            node = node.next

        if node is None:
            return None
        else:
            return node.value     

    def remove(self, key):

        index = self.hash(key)
        node = self.elements[index]
        prev = None

        while node is not None and node.key != key:
            prev = node
            node = node.next

        if node is None:
            return None
        else:
            self.size -= 1
            result = node.value

            if prev is None:
                node = None
            else:
                prev.next = prev.next.next

        return result        

class ST:
    def __init__(self):
        self.table = HashTable()

    def add(self, key, value):
        someAux=self.table.find(key)
        if someAux is None:
            self.table.insert(key,value)
        return someAux

print("Hello world")
