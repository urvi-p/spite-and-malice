#----------------------------------------------------
# This file implements the game and calls functions from other files
# References: python 3 documentation
# Author: Urvi Patel
#----------------------------------------------------
from SpiteAndMalice import Card
from SpiteAndMalice import PlayStack
from SpiteAndMalice import Hand
from SpiteAndMalice import shuffle
from lectureStructures import Stack
from lectureStructures import CircularQueue

def main():
    '''
    This function calls the game class to play the game
    Inputs: None
    Returns: None
    '''
    game = Game()
    winner = game.play()
    print("Congratulations Player{}, You Win!".format(winner))
    
        
class Game():

    def __init__(self):
        '''
        Initializes the game class
        Inputs: None
        Returns: None
        '''
        # deal cards at the start of the game
        deck = self.createCards()
        self.cardDeck = shuffle(deck)
        dealtList = self.dealCards(self.cardDeck)
        
        # create both players and separate their hand and goal cards
        self.playerA = Player(dealtList[0], dealtList[1])
        self.playerB = Player(dealtList[2], dealtList[3]) 
        self.playerA.initalCards()
        self.playerB.initalCards()

        # initially fill card shoe 
        self.cardShoe = CircularQueue(120)
        self.fillShoe()
        
        # create all the play stacks
        self.playStack1 = PlayStack()
        self.playStack2 = PlayStack()
        self.playStack3 = PlayStack()
        self.playStack4 = PlayStack()
                
    def gameOver(self):
        '''
        This method checks the conditions for game over
        Inputs: None
        Return: True if game over, False if game not over
        '''
        if self.playerA.goal.size() == 0 or self.playerB.goal.size() == 0:
            return True
        return False
        
    def play(self):
        '''
        This method calls other methods to play the game.
        Inputs: None
        Returns: who won the game
        '''
        turn = self.first()
        while not self.gameOver():  # play until game over       
            if turn == self.playerA:
                currentPlayer = self.playerA
                player = "A"
                self.playerTurn(currentPlayer, player)
                turn = self.playerB  
            else:
                currentPlayer = self.playerB
                player = "B"
                self.playerTurn(currentPlayer, player)
                turn = self.playerA 
        # once game ends switch player back
        if turn == self.playerA:
            win = "B"
        else:
            win = "A"
        return win
    
    def playerTurn(self, currentPlayer, player):
        '''
        This method controls each players turn.
        Inputs: currentPlayer object and player(str)
        Returns: None
        '''
        self.fiveInHand(currentPlayer)
        discardList = [currentPlayer.discard1, currentPlayer.discard2, currentPlayer.discard3, currentPlayer.discard4]
        endTurn = False
        while not endTurn:
            if currentPlayer.hand.size() == 0:
                self.fiveInHand(currentPlayer)
            winList = self.drawGame()
            if True in winList:
                return
            moves = self.makeMove(player)
            endTurn = moves[0]
            play = moves[1]
            target = int(moves[2])                    
            if not endTurn:                
                # check if there is a zero that can be played
                self.addToPlay(play, target, currentPlayer, discardList)        
        currentPlayer.addToDiscard(play, discardList[target-1])
        
    def fiveInHand(self, currentPlayer):
        '''
        This method adds card in hand to make sure player has five cards in hand
        Inputs: currentPlayer object
        Returns: None
        '''
        if not currentPlayer.fiveHand():
            numberToAdd = 5 - currentPlayer.hand.size()
            addCards = []
            for number in range(numberToAdd):
                addCards.append(self.cardShoe.dequeue())
            currentPlayer.hand.add(addCards)
            currentPlayer.hand.sort()        
                
    def addToPlay(self, play, target, currentPlayer, discardList):
        '''
        This method adds cards to playStack
        Inputs: the players input(from where:play, and to where: target), 
                currentPlayer target, list of all the discard piles
        Returns: None
        '''
        playList = [self.playStack1, self.playStack2, self.playStack3, self.playStack4]
        # check if there is a zero card the player can play
        if self.checkZero(currentPlayer, play, playList):
            return
        # remove the card the player selects and add to playStack
        if play[0].lower() == 'g':
            card = currentPlayer.goal.pop()
        elif play[0].lower() =="h":
            card = currentPlayer.hand.pop(int(play[1])-1)
        else:
            discardPile = discardList[int(play[1])-1]
            if discardPile.size() !=0:
                card = discardPile.pop()
            else:
                print("Discard Pile Empty")
                return
        stackToPlay = playList[target-1]
        if card.getValue() == -1:  
            try:
                value = stackToPlay.peekValue()
            except:
                value = -1
            finally:
                card.assign(value+1)                
        try:
            playingStack = stackToPlay.playCard(card)                    
        except Exception as error: # if cannot play card, put back where it was taken from
            print(error)
            if play[0].lower() == 'g':
                currentPlayer.goal.push(card)
            elif play[0].lower() =="h":
                currentPlayer.hand.add([card])
                currentPlayer.hand.sort()  
            else:
                currentPlayer.discardList.push()
            playingStack = []
        self.addToShoe(playingStack)
   
    def addToShoe(self, playList):
        '''
        This method takes the cards removed from the playStack and adds them to the card Shoe
        Inputs: List of removed cards(faces)
        Returns: None
        '''
        if playList == []:
            return
        else:
            deck = []
            for face in playList:
                if face == "*":
                    card = Card(-1)
                    deck.append(card)
                else:
                    card = Card(int(face))
                    deck.append(card)
            self.cardDeck = shuffle(deck)
            self.fillShoe()
                    
    def checkZero(self, currentPlayer, playerInput, playList):
        '''
        This method checks if there is a zero card that can be played
        Inputs: currentPlayer object, the players input(str), list of playStacks
        Returns: True if there is a zero that can be played, otherwise False
        '''
        # check if there is an empty playing stack
        emptyPlay = False
        for play in playList:
            try:
                play.peekValue()
            except Exception:
                emptyPlay = True  
        zero = False
        if emptyPlay: # if there is an empty playing stack, check if there is a zero that can be played
            card = currentPlayer.goal.peek()
            inHand = currentPlayer.hand.check0() 
            if card.getValue()==0 and inHand != -1:
                if playerInput == "g" or (playerInput[0] == "h" and inHand+1 != int(playerInput[1])):
                    zero = False
            elif playerInput != "g" and card.getValue() == 0:
                print("Must play zero card!")
                zero = True
            elif playerInput[0] != "h" and inHand != -1:
                print("Must play zero card!")
                zero = True  
            elif playerInput[0] == "h" and inHand != -1 and inHand+1 != int(playerInput[1]):
                print(int(playerInput[1]))
                print("Must play zero card!")
                zero = True             
        return zero
                   
    def makeMove(self, player):
        '''
        This method gets the input from the player
        Inputs: current player (str)
        Returns: list[bool(True if turn over, else False), str of what card 
                 to play, str of where to play card]....if no valid cards to discard, returns list[True]
        '''
        action = 0
        while type(action) != str or action.lower() not in ["p","x"]:           
            action = input("Player"+player+", choose action: p (play) or x (discard/end turn)\n")
        if action.lower() == "x":
            discard = self.chooseDiscard(player)
            if discard == None:  # if cannot discard
                return [True]
            else:
                play = discard[0]  # which pile to play from
                target = discard[1]  # where to play
                return [True, play, target]
        else:
            action = self.choosePlay()  # action is a list that has player input
            play = action[0]  # which pile to play from
            target = action[1]  # where to play            
            return [False, play, target]
        
    def chooseDiscard(self, player):
        '''
        This method gets input for which card to discard.
        Inputs: current player (str)
        Returns: None if no valid cards, else list[which card to discard, 
                 which discard pile]
        '''
        if player == "A":
            currentPlayer = self.playerA
        else:
            currentPlayer = self.playerB        
        if currentPlayer.allZeros():  # check if all cards are 0, cannot discard, so return
            print("No valid cards to discard")
            return
        card = self.getDiscardCard(currentPlayer)
        target = self.getDiscardPile()       
        return [card, target]
    
    def getDiscardCard(self, currentPlayer):
        '''
        This method ask which card to discard
        Inputs: currentPlayer object
        Returns: card to discard
        '''
        valid = False
        play = input("Which card do you want to discard(1..5)?\n")
        while not valid:
            try:
                assert type(int(play)) is int and int(play) in range(1,6)
                card = currentPlayer.hand.pop(int(play)-1)
                if card.getValue() == 0:  # check if card is zero
                    currentPlayer.hand.add([card])
                    currentPlayer.hand.sort()
                    print("Cannot discard [0], try again!")
                    raise Exception
                else:
                    valid = True                
            except:
                play = input("Which card do you want to discard(1..5)?\n")
        return card
    
    def getDiscardPile(self):
        '''
        This method gets which discard pile to discard card in
        Inputs: None
        Returns: the discard pile
        '''
        validTarget = False
        target = input("Which Discard Pile are you targeting (1..4)?\n")
        while not validTarget:
            try:
                assert type(int(target)) is int and int(target) in range(1,5)
                validTarget = True
            except:
                target = input("Which Discard Pile are you targeting (1..4)?\n")     
        return target
    
    def choosePlay(self):
        '''
        This method asks which pile to play from (hand, discard, or goal)
        Inputs: None
        Returns: list[which pile to play from, which playStack to put card in]
        '''
        passCheck = False
        while not passCheck:  # validates input
            action = input("Play from where: hi = hand at position i (1..4); g = goal; dj = discard pile j (1..4)?\n") 
            passCheck = self.validInput(action)
        # choose which play stack to target
        check = False
        while not check:
            target = input("Which Play Stack are you targeting (1..4)?\n")
            try:
                if type(int(target)) == int and int(target) in range(1,5):
                    check = True
                else:
                    print("Invalid Input")
            except Exception: 
                print("Invalid Input")
        return [action, target]
                    
    def validInput(self, action):
        '''
        This method checks it the users input is valid.
        Inputs: the users input
        Returns True if valid, False otherwise
        '''
        try:
            if len(action) == 1:
                assert action.lower() == "g"
                return True
            elif len(action) == 2:
                assert action[0].lower() in ["h","d"]
                assert type(int(action[1])) is int
                if action[0].lower()== "h":
                    assert int(action[1]) in range(1,6)                    
                elif action[0].lower()=='d':
                    assert int(action[1]) in range(1,5)
                return True
            elif len(action) > 2 or len(action) < 1:
                raise AssertionError()
        except Exception:
            print("Invalid input")
            return False

    def first(self):
        '''
        This method gets which player goes first.
        Inputs: None
        Returns: the starting player
        '''
        topA = self.playerA.goal.peek().getValue()
        topB = self.playerB.goal.peek().getValue()
        if topB == -1:
            start = self.playerB
        elif topA > topB or topA == topB or topA == -1:
            start = self.playerA           
        else:
            start = self.playerB 
        return start
    
    def fillShoe(self):
        '''
        This method fills the card shoe
        Inputs: None
        Returns: None
        '''
        for card in self.cardDeck:
            self.cardShoe.enqueue(card)
        self.cardDeck.clear() 
                
    def createCards(self):
        '''
        This method makes the 120 cards.
        Inputs: None
        Returns: list of the cards
        '''
        cardDeck = []
        values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # create joker cards
        for number in range(20):
            card = Card(-1)
            cardDeck.append(card)
        # create number cards
        for value in values:
            for number in range(10):
                card = Card(value)
                cardDeck.append(card)
        return cardDeck
    
    def dealCards(self, cards):
        '''
        This method deal the cards at the beginning of the game, 20 to each player(5 in hand, 15 in goal) and rest to card shoe
        Inputs: list of shuffled cards
        Returns: list dealt piles [playerA hand, playerA goal, playerB hand, 
                 playerB goal]    
        '''
        dealingCards = []  # list of inital 40 cards to be dealt(20 for each player)
        for number in range(40):
            card = cards.pop()
            dealingCards.append(card)
        dealtA = dealingCards[0::2]  # cards dealt to player A
        dealtB = dealingCards[1::2]  # cards dealt to player B
        handA = dealtA[:5]
        goalA = dealtA[5:]
        handB = dealtB[:5]
        goalB = dealtB[5:]
        return [handA, goalA, handB, goalB]
    
    def drawGame(self):
        '''
        This method draws the layout for the game
        Inputs: None
        Returns: list[if playerA won(True or False), if playerB won(True or 
                 False)]
        '''
        divider = "----------------------------------------"
        print(divider)
        win1 = self.drawPlayer("A", self.playerA)
        print()
        stacks = [self.playStack1, self.playStack2 ,self.playStack3 ,self.playStack4]
        for number in range(0,4):   
            print("Play Stack {} :".format(number+1), stacks[number])
        print()    
        win2 = self.drawPlayer("B", self.playerB)            
        print(divider)
        return [win1, win2]
            
    def drawPlayer(self, player, currentPlayer):
        '''
        This player draws each players layout
        Inputs: player(str), currentPlayer object
        Returns: True if current player has won, False otherwise
        '''
        print("Player{} Hand".format(player), currentPlayer.hand)
        discardPiles = [currentPlayer.discard1, currentPlayer.discard2, currentPlayer.discard3, currentPlayer.discard4]
        for number in range(0,4):   
            if discardPiles[number].isEmpty():
                print("Player{} Discard {}:".format(player, number+1), "[]")
            else:
                print("Player{} Discard {}:".format(player, number+1), discardPiles[number].peek())  
        win = self.checkWin(currentPlayer, player)
        return win
        
    def checkWin(self, currentPlayer, player):
        '''
        This method checks if the player had won
        Inputs: currentPlayer object, player(str)
        Return: True if win, else false
        '''
        if currentPlayer.goal.size() == 0:
            print("Player{} Goal [] {} cards left".format(player, currentPlayer.goal.size()))
            return True
        else:
            print("Player{} Goal [{}] {} cards left".format(player, currentPlayer.goal.peek(), currentPlayer.goal.size()))   
            return False        
    
class Player:
    def __init__(self, handCards, goalCards):
        '''
        Initializes player object
        Inputs: list of cards in hand, list of cards in goal
        Returns: None
        '''
        self.handCards = handCards
        self.goalCards = goalCards
        self.hand = Hand()
        self.goal = Stack()
        
        # create dicard piles
        self.discard1 = Stack()
        self.discard2 = Stack()
        self.discard3 = Stack()
        self.discard4 = Stack()
    
    def initalCards(self):
        '''
        This method adds the intial card to the hand and goal piles
        Inputs: None
        Returns: None
        '''
        self.hand.add(self.handCards)
        self.hand.sort()
        for card in self.goalCards:
            self.goal.push(card)
            
    def fiveHand(self):
        '''
        This method check if there are 5 cards in hand
        Inputs: None
        Returns: True if 5 cards in hand, else False
        '''
        # make sure player has 5 cards in the Hand
        return self.hand.size() == 5
    
    def allZeros(self):
        '''
        This method checks if all the cards in hand are zeros
        Inputs: None
        Returns: True is only zeros in hand, else False
        '''
        onlyZero = True
        for number in range(1,10):
            if self.hand.index(number) != -1:
                onlyZero = False
        if self.hand.index(-1) != -1:
            onlyZero = False
           
        return onlyZero
    
    def addToDiscard(self, card, discardPile):
        '''
        This method adds the card to the specific discard pile
        Inputs: card to add, which pile to discard in 
        Returns: None
        '''
        discardPile.push(card)
    
main()