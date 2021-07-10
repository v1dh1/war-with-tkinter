#import statement
from Card import *


class War():
#contains methods used for playing the game of war 
    def __init__(self, userDeck, computerDeck):
        #takes 2 parameters, 2 lists of objects 
        #returns null 
        #initialises these lists 
        
        self.userDeck = userDeck
        self.computerDeck = computerDeck
        return 
    #end __init__

    def startARound(self):
        #no parameters
        #starts a round by getting the players next cards 
        #returns these cards 
        #userNextCard and computerNextCard both store Card objects 
        userNextCard = self.userDeck.nextCard()
        computerNextCard = self.computerDeck.nextCard()

        return userNextCard, computerNextCard
    #end startARound()

    def compareCards(self):
        #no parameters
        #returns a string and 2 card objects 
        #checks to see who the winner is in a round of War

        #the startARound method is called to get the Card object values 
        userNextCard, computerNextCard = self.startARound()
        #if/elif/else check who won the round by comparing who had a higher card value 
        if userNextCard.value == computerNextCard.value:
            winner='draw'
        #end if
        elif userNextCard.value > computerNextCard.value:
            winner='user'
        #end elif 
        else:
            winner='computer'
        #end else 
        return winner,userNextCard,computerNextCard 
    #end compareCards()

    def userWins(self,userNextCard,computerNextCard):
        #takes 2 parameters: the user and computer's next cards 
        #no returns 
        #adds the cards to the user's deck 
        #if the user won the round, they get both cards 
        self.userDeck.cards.append(userNextCard)
        self.userDeck.cards.append(computerNextCard)
        return 
    #end userWins()


    def computerWins(self,userNextCard,computerNextCard):
        #takes 2 parameters: the user and computer's next cards 
        #no returns 
        #adds the cards to the computer's deck 
        #if the computer won the round, they get both cards 
        self.computerDeck.cards.append(userNextCard)
        self.computerDeck.cards.append(computerNextCard)
        return 
    #end computerWins()

    def mainWarDeck(self,userNextCard,computerNextCard):
        #takes 2 parameters: the user and computer's next cards 
        #creates a war deck containing 2 cards 
        #returns this deck 
        #mainWarDeck is a list 
        mainWarDeck = [userNextCard,computerNextCard]
        return mainWarDeck
    #mainWarDeck()

    def getWarDeck(self, aDeck):
        #takes 1 parameter: a CardGroup object
        #creates a war deck based on how many cards are left in the deck 
        #returns the deck 

        #warDeck stores an empty list 
        warDeck = []
        #if the deck has more than 4 cards, 4 cards are added to their war deck 
        if aDeck.size() > 4:
            for i in range(4):
                warDeck.append(aDeck.nextCard())
            #end for 
        #end if
        #if the deck has 4 or less cards, cards are added to the war deck leaving the player with 1 card to flip 
        elif aDeck.size() in [4,3,2]:
            for i in range((aDeck.size())-1):
                warDeck.append(aDeck.nextCard())
            #end for 
        #end elif 

        return warDeck
    #end getWarDeck()

    
            

