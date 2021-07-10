#import statements 
from tkinter import *
from PIL import ImageTk, Image
from Game import War
from Card import *


class GUI:
    #controls the GUI 


    def __init__(self):
        #takes no parameters
        #no returns 
        #initializes all variables used throughout the class 

        self.username = ''
        self.gameRound = 0

        self.mainWin: Tk()

        self.winningLabel: Label
        self.cardimg1: Label
        self.cardimg2: Label
        self.scoreboardLabel: Label
        self.userIdentifier: Label
        self.computerIdentifier: Label
        self.flipBtn: Button
        self.exitBtn: Button

        self.userCardDiplayText: Label
        self.computerCardDisplayText: Label
        self.userCardsLeft: Label
        self.computerCardsLeft: Label

        self.wasWar = False
        self.warDeckC1: Label
        self.warDeckC2: Label
        self.warDeckC3: Label
        self.warDeckC4: Label
        self.warDeckC5: Label
        self.warDeckC6: Label
        self.warDeckC7: Label
        self.warDeckC8: Label

        self.defaults = {
            'alertWinWidth': 400,
            'alertWinHeight': 200,
            'alertWinHeadingSize': 25,

            'cardImageDirectory': 'card-images/',
            'otherImageDirectory': 'other-images/',
            'splashImage': 'war.png',
            'icon': 'ico.png',
            'btnImage': 'button.png',
            'damask': 'damask.png',
        }

        self.alertAbout = {
            'title': 'About War',
            'heading': 'About War',
            'description':
                'This app is an implementation of War,\na simple card game, played by yourself and the computer.',
            'bg': 'about.png'
        }
        self.alertWelcome = {
            'title': 'Welcome to War',
            'heading': 'What is your name?',
            'description': 'Yo Wassup!',
            'headingSize': 20,
            'bg': 'welcome.png',
        }
        self.alertGoodbye = {
            'title': 'Bye!',
            'heading': 'Bye!',
            'description': 'Mehhh Bye',
            'bg': 'bye.png',
        }
        self.alertInstructions = {
            'title': 'How to play War',
            'heading': 'Rules of the Game',
            'description':
                'You are playing the game of War!\n\nPress on Play Game to begin\nYou will have to press next to see if you or the computer\nhas a winning card\nWhoever wins will receive both cards\nIf you both have the same card, war will occur.\nYou will then both take 4 cards and flip the last one,\nwith the winner receiving all of the cards\nBe careful! If you run\nout of cards before the computer, you will lose.',
            'width': 600,
            'height': 400,
        }
        self.setupMainWin()

        self.assignDeckValues()

        self.mainWin.mainloop()
        return
    #end __init__

    def assignDeckValues(self):
        #assigns values to create a deck by instantiating the war class 
        #no returns 
        #no parameters 

        #self.deck is instatiated as a StandardDeck object 
        self.deck = StandardDeck()
        #self.userDeck and self.computerDeck are assigned decks 
        self.userDeck, self.computerDeck = self.deck.getDeck()
        #the War class is intantiated 
        self.game = War(self.userDeck, self.computerDeck)
        return

    def setWinner(self, winnerName):
        #takes 1 parameter: a string 
        #updates a label based on who wins 
        #no returns 
        self.updateLabel(self.winningLabel, winnerName)
    #end setWinner()

    def updateCardName(self, cardName, isComputer=False):
        #updates a card's name 
        #no returns 
        #2 parameters: a cardName and a boolean value 
        #if false then the computer's card text gets updated 
        if isComputer:
            self.updateLabel(self.computerCardDisplayText, cardName)
        #if it is true, then the user's card text gets updated 
        else:
            self.updateLabel(self.userCardDiplayText, cardName)
        return 
    #end updateCardName()

    def flipCards(self):
        #no parameters 
        #no returns 
        #everything that happens when the "flip" button is clicked 

        #if there are cards left in either user's deck
        if self.userDeck.size() > 1 and self.computerDeck.size() > 1:
            #the war cards are reset 
            self.resetWarCardsDisplay()
            self.gameRound += 1
            #the winner of the round along with the 2 players cards are compared using the compareCards method from the War class
            winner, userNextCard, computerNextCard = self.game.compareCards()
            #the card image is set on screen 
            self.setCardImage(self.getCardImgName(userNextCard), 100, 100)
            #the user's card is upated 
            self.updateCardName(userNextCard, True)
            #the computer image is shown on screen 
            self.setCardImage(self.getCardImgName(computerNextCard), 100, 300)
            #the computer card is updated 
            self.updateCardName(computerNextCard)
            #if the user wins, a label is printed on screen where it shows the user won
            if winner == 'user':
                self.game.userWins(userNextCard, computerNextCard)
                self.setWinner(f'{self.username[:9]} has won the round')
            #end if 
            #if the computer wins, a label is printed on screen where it shows the computer won
            elif winner == 'computer':
                print('computer')
                self.game.computerWins(userNextCard, computerNextCard)
                self.setWinner('computer has won the round')
            #end elif 

            #if there is a war
            else:
                print('war')
                #war is printed on the scrren 
                self.setWinner('WAR')
                #userWarDeck stores a list of the user's war deck 
                userWarDeck = self.game.getWarDeck(self.userDeck)
                #computerWarDeck stores a list of the computer war deck 
                computerWarDeck = self.game.getWarDeck(self.computerDeck)
                #the war cards are displayed 
                self.warCardsDisplay(userWarDeck, computerWarDeck)
                #the mainWarDeck stores a list of the current players cards 
                mainWarDeck = [userNextCard, computerNextCard]
                #if the war decks have more than 1 card, the decks are compared 
                if len(userWarDeck) > 1 and len(computerWarDeck) > 1:
                    self.compareWarDeck(userWarDeck, computerWarDeck,
                                             mainWarDeck)
            #the cards left for both users are updated 
            self.updateLabel(self.userCardsLeft, self.userDeck.size())
            self.updateLabel(self.computerCardsLeft, self.computerDeck.size())

        else:
            #if either user has less than 1 card, a winner is declared 
            self.getGameWinner()
    #end flipCards()

    def compareWarDeck(self, Wardeck1, Wardeck2, mainWarDeck):
        #in the case of war, the war deck's last cards are compared 
        #takes 3 parameters: 3 war decks 
        #adds the cards to whoever has a higher card, returns null
                
        #if the user's card is higher, they get all the cards in all 3 wardecks 
        if Wardeck1[-1].value > Wardeck2[-1].value:
            for i in Wardeck1:
                self.userDeck.cards.append(i)
            #end for 
            
            for i in Wardeck2:
                self.userDeck.cards.append(i)
            #end for 

            for i in mainWarDeck:
                self.userDeck.cards.append(i)
            #end for 
        #end if 

        #if the computer's card is higher, they get all the cards in all 3 wardecks 
        elif Wardeck1[-1].value < Wardeck2[-1].value:
            for i in Wardeck1:
                self.computerDeck.cards.append(i)
            #end for 
            
            for i in Wardeck2:
                self.computerDeck.cards.append(i)
            #end for 

            for i in mainWarDeck:
                self.computerDeck.cards.append(i)
            #end for 
        #end elif 

        else:
            #if there is a tie within the war 
            
            #both players move the top card to the bottom of their decks 
            self.userDeck.cards.append(Wardeck1.pop(-1))
            self.computerDeck.cards.append(Wardeck2.pop(-1))
            
            #if they have more than 2 cards, they compare more cards 
            if self.userDeck.size() > 2 and self.computerDeck.size() > 2:
                self.compareWarDeck(Wardeck1,Wardeck2,mainWarDeck)

            else:
                self.getGameWinner()
                #the game is over 


    def getGameWinner(self):
        #no parameters 
        #no returns 
        #gets the game winner 

        #winner stores an empty string
        winner = ''
        #if the user has more cards, they win, and winner is set to the user 
        if self.userDeck.size() > self.computerDeck.size():
            winner = self.username
        #end if 

        #if the computer has more cards, winner is set to the computer 
        elif self.userDeck.size() < self.computerDeck.size():
            winner = 'computer'
        #end elif 

        #if they have the same amount of cards, it's a draw 
        else:
            winner = 'It is a draw!'
        #end else 

        #winnerWin creates a window with the winner's name 
        winnerWin = self.newAlertWin('Winner', winner)
        #the window has a quit button and restarts the game 
        self.newBtn(winnerWin, 'Quit', lambda: (self.quitWin(winnerWin), self.restartGame()), 120, 140)
    #end getGameWinner()

    def updateImg(self, img):
        #updates images 
        #takes 1 parameter:an image 
        #No returns 

        #destroys the image 
        img.destroy()
        return
    #end updateImg()

    def setupMainWin(self):
        #sets up the main window 
        #no returns 
        #no parameters 

        #win stores a new window 
        win = self.newWin('War', 'WAR')
        #an image is set as the background
        self.newImg(win, self.defaults['splashImage'],
                    self.defaults['otherImageDirectory'])
        self.addLabel(win, 'WAR', 300, 260, 45)
        #Instructions, Exit and Play game buttons are created 
        self.newBtn(win, 'Instructions', self.displayInstructions, 75, 540)
        self.newBtn(win, 'Play Game', self.getUserName, 200, 540)
        self.newBtn(win, 'Exit', lambda: (self.quitWin(win)), 600, 540)
        self.mainWin = win
    #end setupMainWin()

    def newBtn(self,
               window,
               buttonName,
               buttonCommand,
               xPlacement=0,
               yPlacement=0):
        #creates a new button 
        #returns the new button 
        #takes 4 parameters: the window, name, command, x and y placement

        #the button is created with all parameters 
        btn = Button(window,
                     text=buttonName,
                     command=buttonCommand,
                     cursor="hand1",
                     width=10,
                     height=2,
                     bg="#fff",
                     borderwidth=0)
        #the button is placed 
        btn.place(x=xPlacement, y=yPlacement)
        return btn
    #end newBtn()

    def addMainMenu(self):
        #creates a main menu 
        #no parameters 
        #no returns 

        #menuBar stores a menu 
        menubar = Menu(self.mainWin)
        # helpMenu creates the menu
        helpMenu = self.getHelpMenu(menubar)
        aboutMenu = self.getAboutMenu(menubar)
        #adding the menu options 
        menubar.add_cascade(label='Help?', menu=helpMenu)
        menubar.add_cascade(label='About...', menu=aboutMenu)
        self.mainWin.config(menu=menubar)
    #end addMainMenu()

    def getAboutMenu(self, menubar):
        #takes 1 parameter: a menubar 
        #returns a menu 
        #makes the about option on the menu 

        #menu makes a menu 
        menu = Menu(menubar, tearoff=0)
        # adding the about war tab
        menu.add_command(label='About War', command=self.aboutWar)
        return menu
    #end getAboutMenu

    def getHelpMenu(self, menubar):
        #creates help menu 
        #takes 1 parameter: a menu bar 
        #returns the menu 

        #menu stores a menu 
        menu = Menu(menubar, tearoff=0)
        # adding the How to play, restart game and exit tabs
        menu.add_command(label='How to play?',
                         command=self.displayInstructions)
        menu.add_separator()
        # adding the exit tab
        menu.add_command(label='Restart Game', command=self.restartGame)
        menu.add_command(label='Exit',
                         command=lambda: (self.quitWin(self.mainWin)))
        return menu
    #end getHelpMenu()

    def newImg(self, window, imgName, path, cx=0, cy=0):
        # takes 4 parameters (a window, a string, x and y coordinates)
        # creates a new image based on parameters
        # returns the new image

        # img stores the photo as a PhotoImage
        img = PhotoImage(file=path + imgName)
        # lbl stores the Label in the parent window
        lbl = Label(window)
        # lbl.img stores the img
        lbl.img = img
        # confugures and places image according to coordinates
        lbl.config(image=lbl.img)
        lbl.place(x=cx, y=cy)
        return lbl

    def updateLabel(self, lbl, txt):
        # takes 2 parameters (a label and a string)
        # replaces the old text with the new text
        # no returns
        lbl['text'] = txt

    # end updateLabel()

    def updateBtnTxt(btn, txt):
        # takes 2 parameters (a button and a string)
        # replaces the old text with the new text
        # no returns
        btn['text'] = txt

    def addLabel(self, win, txt, xc=450, yc=0, size=15):
        # takes 2 parameters (a window, a string), 3 pre-set parameters for placing labels
        # places labels on frame
        # returns the label

        # lbl is a Label
        lbl = Label(win, text=txt, bg='#fff', font=("Arial", size))
        # lbl is placed
        lbl.place(x=xc, y=yc)
        return lbl

    # end addLabel()

    def displayInstructions(self):
        #displays the instructions 
        #no parameters 
        #no returns 

        #instructionsWin creates a new instructions window 
        instructionWIN = self.newAlertWin(self.alertInstructions['title'],
                                          self.alertInstructions['heading'],
                                          self.alertInstructions['width'],
                                          self.alertInstructions['height'])
        self.addLabel(instructionWIN, self.alertInstructions['description'],
                      50, 100, 12)
        #a close button is added to the window to close it
        self.newBtn(instructionWIN, 'Close', lambda:
        (self.quitWin(instructionWIN)), 220, 340)

        return
    #end displayInstructions()

    def aboutWar(self):
        #creates the about tab 
        #no parameters
        #no returns 

        #instructionsWin creates a new window 
        instructionWIN = self.newAlertWin(self.alertAbout['title'],
                                          self.alertAbout['heading'],
                                          self.alertInstructions['width'],
                                          self.alertInstructions['height'])
        self.addLabel(instructionWIN, self.alertAbout['description'], 10, 100,
                      12)
        #creates a new butto to press to close the window 
        self.newBtn(instructionWIN, 'Cool!', lambda:
        (self.quitWin(instructionWIN)), 220, 340)

        return
    #end aboutWar()

    def clearScreen(self, win):
        #clears the screen by destorying all widgets within it
        #takes 1 parameter: a window 
        #no returns 

        #emptyList is an empty list 
        emptyList = []
        #for loop iterates through all widgets in the window and adds them to the empty list 
        for i in win.winfo_children():
            emptyList.append(i)
            i.destroy()
        #end for 

        return
    #end clearScreen()

    def newWin(self,
               title,
               heading,
               width=800,
               height=600,
               headingSize=50,
               bg='fff',
               xCoordinate=0,
               yCoordinate=0):
        # Add a new window
        # takes 2 parameters (2 strings) and 6 pre-set parameters for placement
        # returns the new window
        # win stores tkinter frame
        win = Tk()
        # setting the frame geometry
        win.geometry(
            str(width) + 'x' + str(height) + '+' + str(xCoordinate) + '+' +
            str(yCoordinate))
        # making it unable to resize
        win.resizable(width=0, height=0)
        # setting it's title
        win.title(title)
        # setting background colour
        win.configure(bg='#' + bg)
        # if the string is "WAR":
        # if title == 'WAR':
        # a newimage is placed on the frame with the given parameters
        # pass
        # end if
        # adding a label to the new window
        winTitle = self.addLabel(win, heading, 450, 0, headingSize)
        # packing the new window
        winTitle.pack()
        return win
    #end newWin()

    def newAlertWin(self,
                    title,
                    heading,
                    w=400,
                    h=200,
                    headingSize=25,
                    bg='fff',
                    xc=150,
                    yc=150):
        # takes 2 parameters (2 strings) and 6 set parameters
        # creates a new window
        # returns the new window
        win = self.newWin(title, heading, w, h, headingSize, bg, xc, yc)
        #put window on the top 
        win.wm_attributes("-topmost", 1)
        return win
    #end newAlertWin()

    def goodbyeAlert(self):
        # takes no paramters
        # has no returns
        # tells user who wins the game
        # msg stores the name of the winning player based on who wins
        msg = self.username if self.userWins > self.computerWins else 'The Computer Wins!'
        # end if, else
        # win calls newAlertWin method and prints out message with given parameters
        win = self.newAlertWin('Thank you for playing!', msg, 770, 475, 25,
                               'fff', 15, 40)
        # adding a label to the win widget
        self.addLabel(win, self.theUser + ', Thank you for trying War!', 125,
                      75)
        # adding a button to the win widget (restarts the game)
        return 
    #end goodbyeAlert()

    def gameOver(self):
        # takes no parameters
        # no returns
        # is called when the game is over and calls on methods to ensure the game stops

        # sets gameRound to 0
        self.gameRound = 0

    # end gameOver()

    def quitWin(self, win):
        # takes 1 parameter (a window widget)
        # no returns
        # destroys the window
        win.destroy()

    # end quitWin()

    def getUserName(self):
        #gets the user's name by asking them for input 
        #no parameters 
        #no returns 

        #userInputWindow creates new window 
        userInputWindow = self.newAlertWin(self.alertWelcome['title'],
                                           self.alertWelcome['heading'],
                                           self.defaults['alertWinWidth'],
                                           self.defaults['alertWinHeight'],
                                           self.alertWelcome['headingSize'])
        #alertContent creates an entry box, which is placed
        alertContent = Entry(userInputWindow)
        alertContent.place(x=125, y=75)
        alertContent.focus_set()
        #a new button is made to close the window 
        self.newBtn(
            userInputWindow, 'ok', lambda: (self.startGame(alertContent.get()),
                                            self.quitWin(userInputWindow)),
            150, 140)
        return
    #end getUserName()

    def setScoreboard(self):
        # self.addLabel(self.mainWin, 'Scoreboard', 300, 425, 15)
        # self.scoreboardLabel = self.addLabel(self.mainWin, '', 300, 455)
        pass

    # end setScoreboard
    def restartGame(self):
        #restarts the game 
        #no returns 
        #no parameters 

        #methods are called to restart the entire game 
        self.gameOver()
        self.quitWin(self.mainWin)
        self.setupMainWin()
        self.assignDeckValues()
    #end restartGame()

    def startGame(self, username):
        #the game is started 
        #takes 1 parameter: the user's name 
        #no returns 

        #the username is set 
        self.username = username
        #the screen is cleared 
        self.clearScreen(self.mainWin)
        #the background is set 
        self.newImg(self.mainWin, self.defaults['damask'],
                    self.defaults['otherImageDirectory'])
        #the main menu is added 
        self.addMainMenu()
        #Labels are added to aesthetic values 
        self.addLabel(self.mainWin, 'Press the Flip button to play', 30, 15, 10)
        self.addLabel(self.mainWin, self.username[:9], 100,
                      50)  # for user's name
        self.addLabel(self.mainWin, 'computer', 100, 250)
        self.newImg(self.mainWin, 'blank.png', 'card-images/', 150, 100)
        self.newImg(self.mainWin, 'blank.png', 'card-images/', 150, 300)
        #flip button is added 
        self.newBtn(self.mainWin, 'Flip', self.flipCards, 100, 480)
        self.userCardDiplayText = self.addLabel(self.mainWin, '', 300, 50)
        self.computerCardDisplayText = self.addLabel(self.mainWin, '', 300, 250)
        self.winningLabel = self.addLabel(self.mainWin, '', 100, 550)
        self.userCardsLeft = self.addLabel(self.mainWin, '', 40, 130)
        self.computerCardsLeft = self.addLabel(self.mainWin, '', 40, 310)

        # an exit button is shown
        self.exitBtn = self.newBtn(self.mainWin, 'Restart Game',
                                   self.restartGame, 680, 0)
        # a Scoreboard is shown
        self.setScoreboard()
    #end startGame()

    def getDefaultVal(self, item):
        #takes 1 parameter: an item 
        #resets it to the default value 
        #returns the new item 

        return self.defaults[item]
    #end getDefaultVal()

    def getCardImgName(self, card):
        # takes a Card object as a parameter
        # gets the name of the file of a card that was played
        # returns the file name as a string
        return f'{str(card.value).lower()}-{card.suit.lower()}.png'

    # end getCardImgName()

    def setCardImage(self, img, xPlacement, yPlacement):
        #sets a card image 
        #takes 3 parameters: an image, x and y placement 
        #returns the new image 

        #newImg stores the new image 
        newImg = self.newImg(self.mainWin, img, 'card-images/', xPlacement,
                             yPlacement)
        return newImg
    #end setCardImage()

    def updateCardImage(self):
        #updates a card image 
        #no returns 
        #no parameters 

        #destroys the image first and then resets it 
        self.cardimg1.destroy()
        self.newImg(self.mainWin, self.cardimg1)
    #end updateCardImage()

    def resetWarCardsDisplay(self):
        #resets the war cards display 
        #destroys all card image widgets 
        #no returns or parameters 

        #if there was war then all the widgets are destroyed 
        if self.wasWar == True:
            self.warDeckC1.destroy()
            self.warDeckC2.destroy()
            self.warDeckC3.destroy()
            self.warDeckC4.destroy()
            self.warDeckC5.destroy()
            self.warDeckC6.destroy()
            self.warDeckC7.destroy()
            self.warDeckC8.destroy()
            #self.wasWar is set to false once the widgets are destroyed 
            self.wasWar = False
    #end resetWarCardsDisplay()

    def warCardsDisplay(self, userWarDeck, computerWarDeck):
        #takes 2 parameters: 2 lists 
        #no returns 
        #dislays the war deck on screen 

        # for user: displays blank cards 
        self.warDeckC1 = self.addBlankImg()
        self.warDeckC2 = self.addBlankImg(350)
        self.warDeckC3 = self.addBlankImg(400)
        #shows the war deck last card
        self.warDeckC4 = self.newImg(self.mainWin, self.getCardImgName(userWarDeck[-1]),
                                     'card-images/', 500, 100)

        # for comp: displays blank cards
        # self.newImg(self.mainWin, 'blank.png', 'card-images/', 300, 300)
        self.warDeckC5 = self.addBlankImg(300, 300)
        self.warDeckC6 = self.addBlankImg(350, 300)
        self.warDeckC7 = self.addBlankImg(400, 300)
        #shows the war deck last card
        self.warDeckC8 = self.newImg(self.mainWin, self.getCardImgName(computerWarDeck[-1]),
                                     'card-images/', 500, 300)
        #since there was war, self.wasWar is set to true 
        self.wasWar = True

        return
    #end warCardsDisplay()

    def addBlankImg(self, xc=300, yc=100):
        #a blank card is added 
        #2 parameters: x and y coordinates 
        #returns the blank card 
        return self.newImg(self.mainWin, 'blank.png', 'card-images/', xc, yc)
    #end addBlankImg
