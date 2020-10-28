#----------------------------------------------------
# This file implements the classes.
# References: python 3 documentation
# Author: Urvi Patel
#----------------------------------------------------

import random

class Card:
    # creates a new card
    def __init__(self, value):
        assert value in range(-1,10), "Invalid value provided."  # if value not in range, assertion error is raised
        self.__value = value
        if self.__value == -1:
            self.__face = "*"
        else:
            self.__face = str(self.__value)
        
    def assign(self, value):
        """
        This method assigns a new value to the card if the face is "*"
        Inputs: value(int)
        Returns: None
        """
        assert value in range(-1,10), "Invalid value provided."  # if value not in range, assertion error is raised 
        if self.__face != "*":
            raise Exception("Card not joker, cannot change value.")
        else:
            self.__value = value
        # do we change self.__face here?
    
    def getValue(self):
        '''
        Return the value of the card.
        '''
        return self.__value
    
    def getFace(self):
        '''
        Returns the face of the card.
        '''
        return self.__face
    
    def __str__(self):
        """
        Returns the string representation of the card
        """
        return "[{:s}]".format(self.__face)
    
    def __repr__(self):
        """
        Returns the string representation of the card with face and value
        """
        return str(self) + "." + str(self.__value)
    
class PlayStack:
    def __init__(self):
        self.__cards = []
        
    def peekValue(self):
        '''
        Returns the value of the card on top of all the cards 
        '''
        if self.__cards == []:
            raise Exception("Error: No cards in the playing stack" )
        else:
            topCard = self.__cards[len(self.__cards)-1]
            return topCard.getValue()
        
    def peekFace(self):
        '''
        Returns the face of the card on top of all the cards
        '''
        if self.__cards == []:
            raise Exception("Error: No cards in the playing stack" )
        else:
            topCard = self.__cards[len(self.__cards)-1]
            return topCard.getFace()
        
    def playCard(self, card):
        '''
        This method takes a card and pushes it on top of the cards stack
        Inputs: card to push on stack
        Returns: either a list of the faces of all cards in stack or None
        '''
        newCard = card
        stackList = []
        if self.__cards == [] and (newCard.getValue() == 0 or newCard.getValue() == -1):
            self.__cards.append(newCard)
            return stackList
        topCard = self.peekValue()
        if (newCard.getValue()-1) == topCard:
            self.__cards.append(newCard)
            if newCard.getValue() == 9:
                for card in self.__cards:
                    stackList.append(card.getFace())
                self.__cards = []
            return stackList
        else:
            raise Exception("Error: Card rejected.")
            
    def __str__(self):
        '''
        Returns a string representation of the cards in the stack
        '''
        elements = ''
        for card in self.__cards:
            elements+=(str(card))
        return "|{}|".format(elements)
    
class Hand:
    def __init__(self):
        self.__hand = []
    
    def sort(self):
        '''
        This method sorts the cards in hand by increasing order by value
        '''
        self.__hand.sort(key=lambda card:card.getValue())
    
    def pop(self, pos=None):
        '''
        This method removes the card at the given position, if none given, then removes the card on the far right
        Inputs: position
        Returns: None
        '''
        if pos == None:
            pos = self.size()-1
        assert pos in range(self.size()), "Position out of range."
        if self.size() == 0:
            raise Exception("No cards in hand.")
        else:
            card = self.__hand.pop(pos) # can you use pop() inside pop method?
            return card
            
    def index(self, value):
        '''
        This method finds the index of the card with a value.
        Inputs: value(int) to search for
        Returns: index of first card with the value, otherwise -1
        '''
        assert value in range(-1,10), "Value not in range."
        found = False
        count = 0
        while not found and count < self.size():
            if self.__hand[count].getValue() == value:
                found = True
                return count
            count += 1
        return -1
        
    def check0(self):
        '''
        This method gets the index of the card with a value of 0
        Inputs: None
        Returns: the index of the first card with value of 0, otherwise -1
        '''
        found = False
        count = 0
        while not found and count < self.size():
            if self.__hand[count].getValue() == 0:
                found = True
                return count
            count += 1
        return -1
    
    def size(self):
        """
        This method returns the number of cards in the hand.
        """
        return len(self.__hand)
    
    def add(self, cardList):
        '''
        This method adds cards from cardList to the hand.
        Inputs: cardList(list)
        Returns: None
        '''
        if self.size() == 5:
            raise Exception("Hand full.")
        elif (len(cardList) + self.size()) > 5:
            raise Exception("Too many cards to add.")
        else:
            for card in cardList:
                self.__hand.append(card)
    
    def __str__(self):
        '''
        This method return a string representation of the cards in hand.
        '''
        elements = ''
        #print(self.__hand)
        for card in self.__hand:
            #print(card)
            elements+=(str(card))
            #print(elements)
        return "[{}]".format(elements)
  
def shuffle(cardList):
    newList = []
    while len(cardList) != 0:
        position = random.randint(0, len(cardList)-1)
        card = cardList.pop(position)
        newList.append(card)
    return newList

            
if __name__ == "__main__":
    play = PlayStack()
    mycard = Card(3)
    #print(str(mycard))
    #print(repr(mycard))
    #print(play)
    card1 = Card(0)
    #play.playCard(card1)
    #print(play)
    card2 = Card(1)
    #play.playCard(card2)
    #print(play)    
    card3 = Card(-1)
    #card3.assign(2)
    #play.playCard(card3)
    #print(play)
    #play.playCard(mycard)
    #print(play)
    
    held = Hand()
    print("Hand size: ",held.size())
    print(held)
    held.add([mycard])
    print(held)  
    print("Hand size: ",held.size())
    
    cards = [card2, mycard, card3]
    held.add(cards)
    print(held)
    held.sort()
    print(held)
    print("Hand size: ",held.size())
    print(held.index(5))
    print(held.check0())
    held.add([card1])
    print(held)
    print(held.check0())
    held.sort()
    print(held)
    print(held.check0())
    
    
    #cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #print(cards)
    #print(shuffle(cards))