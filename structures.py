#----------------------------------------------------
# This file implements the structures Stack and CircularQueue
# References: python 3 documentation
#----------------------------------------------------

class Stack:
    def __init__(self):
        self.items = []
        
    def push(self, item): 
        self.items.append(item)
        
    def pop(self):
        return self.items.pop()   
    
    def peek(self):
        return self.items[len(self.items)-1]
    
    def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)    
    
class CircularQueue:
    def __init__(self, capacity):
        if type(capacity) != int or capacity<=0:
            raise Exception ('Capacity Error')
        self.__items = []
        self.__capacity = capacity 
        self.__count=0
        self.__head=0
        self.__tail=0  
        
    def enqueue(self, item):
        if self.__count == self.__capacity:
            raise Exception('Error: Queue is full') 
        if len(self.__items) < self.__capacity:
            self.__items.append(item) 
        else:
            self.__items[self.__tail]=item 
        self.__count +=1
        self.__tail=(self.__tail +1) % self.__capacity
    
    def dequeue(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty')
        item = self.__items[self.__head] 
        self.__items[self.__head] = None
        self.__count -=1
        self.__head = (self.__head+1) % self.__capacity 
        return item

    def peek(self):
        if self.__count == 0:
            raise Exception('Error: Queue is empty') 
        return self.__items[self.__head]    
    
    def isEmpty(self):
        return self.__count == 0
    
    def isFull(self):
        return self.__count == self.__capacity
    
    def size(self):
        return self.__count
    
    def capacity(self):
        return self.__capacity  

    def clear(self):
        self.__items = [] 
        self.__count=0 
        self.__head=0 
        self.__tail=0
