### Simple code to simulate a Queue via two stacks.
### The cost of any sequence of n commands
### of enqueue and dequeue will be O(n).
### This bound comes from -amortized-
### cost analysis.

class Queue:
    def __init__(self,initial_list=[]):
        self.S1 = initial_list
        self.S2 = []
        
    def enqueue(self,x):
        self.S1.append(x)
        
    def dequeue(self):
        if self.S2 == []:
            self.switch()
        if self.S2 == []:
            return NULL # nothing to dequeue
        return self.S2.pop()
        
    def switch(self):
        while self.S1 != []:
            self.S2.append(self.S1.pop())
            
    def show(self): # prints newest to oldest
        print self.S1 + self.S2

### EXAMPLE
### >>> q = Queue()
### >>> q.show()
### []
### >>> q.enqueue(5)
### >>> q.enqueue(6)
### >>> q.enqueue(7)
### >>> q.dequeue()
### 5
### >>> q.enqueue(8)
### >>> q.show()
### [8, 7, 6]

