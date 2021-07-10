#importing random to shuffle cards
import random

class Card:
    #stores values for a singular card to be able to get it's name in a desired format
    def __init__(self, value, suit):
        #function initialises value and suits values
        #takes value and suit parameter
        #no return
        self.value = value
        self.suit = suit
    #end __init__

    def __str__(self):
        #function takes self parameter
        #finds the value of a card based on value and suit parameters
        #returns the card as value and suit
        #namesOfCards stores a list of values of non-numerical values
        namesOfCards = ['Jack', 'Queen', 'King', 'Ace']

        #if the value is numerical, goes through this code
        if self.value <= 10:
            return f'{self.value} of {self.suit}.'
        #end if
        else:
            #if the value is non-numerical, then the value is indexed and found in the namesOfCards list
            return f'{namesOfCards[self.value-11]} of {self.suit}.'
        #end if
    #end __str__
#end Card


class CardGroup:
    #has methods which act on a list of cards

    #initialises the cards value (a list)
    def __init__(self, cards=[]):

        #self.cards stores a list
        self.cards = cards
    #end __init__

    def nextCard(self):
        #takes no parameters
        #returns null
        #removes the first card from the list and returns it
        return self.cards.pop(0)
    #end nextCard()

    def hasCard(self):
        #takes no parameters
        #returns null
        #True or False depending on if there are any cards left in the list
        return len(self.cards)>0
    #end hasCard()

    def size(self):
        #takes no parameters
        #returns null
        #returns how many cards are in the list
        return len(self.cards)
    #end size()

    def shuffle(self):

        #takes no parameters
        #returns null
        #shuffles the list.
        random.shuffle(self.cards)
    #end shuffle()

#end CardGroup

class StandardDeck(CardGroup):
    #Creates a 52-card deck
    #Child of CardGroup
    def __init__(self):
        #initialize a blank list for deck
        #return null
        #creates a deck
        self.cards = []
        for s in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            #sets up for statement for each suit
            for v in range(2,15):
                #sets up for statement for each value in suit
                self.cards.append(Card(v, s))
                #or self.cards=self.cards+[Card(v,s)]
            #end for

        #self.user stores half of the deck, is shuffled
        self.user = CardGroup(self.cards[:26])
        self.user.shuffle()

        #self.computer stores other half of the deck, is shuffled
        self.computer = CardGroup(self.cards[26:])
        self.computer.shuffle()
        return
        #end __init__

    def getDeck(self):
        #no parameters
        #returns 2 shuffled decks
        #2 decks are lists of CardGroup objects
        return self.user,self.computer
    #end getDeck()
#end StandardDeck
