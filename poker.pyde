# Poker
import random
import collections
import os
import itertools
import time
    
# cards with names (for face cards), values, suits
class Card:
    def __init__(self,value,suit):
        if value=='Ace':
            self.value=14
            self.name='Ace'
        elif value=='King':
            self.value=13
            self.name='King'
        elif value=='Queen':
            self.value=12
            self.name='Queen'
        elif value=='Jack':
            self.value=11
            self.name='Jack'
        else:
            self.value=value
            self.name=value
        self.suit=suit

    def __gt__(self,other):
        return self.value>other.value

    def __str__(self):
        return '{0} of {1}'.format(self.name,self.suit)

# creates deck as list of card instances
class Deck(list):
    def __init__(self):
        suits=['Spades','Hearts','Diamonds','Clubs']
        values=['Ace',2,3,4,5,6,7,8,9,10,'Jack','Queen','King']
        for i in suits:
            for j in values:
                card=Card(j,i)
                self.append(card)

    def deal(self):
        a=random.randint(0,len(self)-1)
        b=self.pop(a)
        return b

# human player, contains methods for betting
class Hand:
    def __init__(self,name):
        self.name=name
        self.card1=0
        self.card2=0
        self.credits=1000
        # determines special responsibilities of the position
        # specific ones will be switched to "true" later
        self.dealer=False
        self.small=False
        self.big=False
        self.stake=0
        self.done=False
        self.besthand=0
        self.besthandstring=''

    def __str__(self):
        if self.dealer==True:
            return '     Dealer: {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)
        
        elif self.small==True:
            return 'Small blind: {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)
        
        elif self.big==True:
            return '  Big blind: {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)
        
        else:
            return '             {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)

    def __gt__(self,other):
        return self.credits>other.credits

    def check(self):
        print("\n{0} will check.".format(self.name))
        print(self)

    def call(self):
        global minbet
        if minbet<=(self.credits+self.stake):
            self.credits-=(minbet-self.stake)
            self.stake+=(minbet-self.stake)
        else:
            print('***************')
            print("{0} doesn't have that much money.".format(self.name))
            print("{0} will go into the negatives.".format(self.name))
            print('***************')
            self.credits-=(minbet-self.stake)
            self.stake+=(minbet-self.stake)
        print("\n{0} will call.".format(self.name))
        print(self)

    def _raise(self,credit):
        global minbet
        if minbet>(self.credits+self.stake):
            if type(self)!=Computer:
                print("You don't have enough money to raise.")
                print("You'll automatically call the minimum and go into the negatives.")
            self.call()
        elif minbet<=credit<=(self.credits+self.stake):
            self.credits-=(credit-self.stake)
            self.stake+=(credit-self.stake)
            minbet=credit
            print("\n{0} will raise.".format(self.name))
            print('Minimum bet is now:',minbet)
        elif minbet>credit:
            print("You can't bet less than the minimum: {0}.".format(minbet))
            self._raise(getAmountFromUser('Total amount you want to bet: '))
        elif credit>(self.credits+self.stake):
            if type(self)!=Computer:
                print("You don't have that much money.")
                self._raise(getAmountFromUser('Enter an amount you can afford: '))
        print(self)

    def fold(self):
        global pot
        global activecount
        pot+=self.stake
        self.stake=0
        print('\n{0} will fold.'.format(self.name))
        self.done=True
        print(self)
        activecount=0
        for i in player_list:
            if i.done==False:
                activecount+=1
        print('Active players:',activecount)

# computer player w/ decision making
class Computer(Hand):
    def __init__(self,name,aggr):
        Hand.__init__(self,name)
        self.aggr=aggr

    def __str__(self):
        if self.dealer==True:
            return '     Dealer: {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)
        
        elif self.small==True:
            return 'Small blind: {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)
        
        elif self.big==True:
            return '  Big blind: {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)
        
        else:
            return '             {0} - Credits: {1}; At stake: {2}'.format(self.name,self.credits,self.stake)

    def preflop1(self):
        if minbet==bigblind:
            if self.small is True:
                self.stake+=smallblind
                self.credits-=smallblind
                
                # pair
                if self.card1.value==self.card2.value:
                    if self.aggr>7:
                        self._raise(int(minbet*2))
                    elif self.aggr>5:
                        self._raise(int(minbet*1.5))
                    else:
                        if random.randint(1,4)==1:
                            self._raise(int(minbet*2))
                        else:
                            self.call()
                # suited high cards
                if self.card1.value>10 and self.card2.value>10 and self.card1.suit==self.card2.suit:
                    self.call()
                # high cards
                elif self.card1.value>10 and self.card2.value>10:
                    self.call()
                # suited cards
                elif self.card1.suit==self.card2.suit:
                    self.call()
                # possibility for straight
                elif abs(self.card1.value-self.card2.value)<=1:
                    if self.aggr>4:
                        self.call()
                    else:
                        if int(self.aggr)==random.randint(1,10):
                            self.call()
                        else:
                            self.fold()

                elif abs(self.card1.value-self.card2.value)<=2:
                    if self.aggr>4.25:
                        self.call()
                    else:
                        if int(self.aggr)==random.randint(1,10):
                            self.call()
                        else:
                            self.fold()

                elif abs(self.card1.value-self.card2.value)<=3:
                    if self.aggr>4.5:
                        self.call()
                    else:
                        if int(self.aggr)==random.randint(1,10):
                            self.call()
                        else:
                            self.fold()
                
                elif abs(self.card1.value-self.card2.value)<=4:
                    if self.aggr>4.75:
                        self.call()
                    else:
                        if int(self.aggr)==random.randint(1,10):
                            self.call()
                        else:
                            self.fold()
                # one high card
                elif self.card1.value>10 or self.card2.value>10:
                    if self.aggr>5:
                        self.call()
                    else:
                        if random.randint(1,4)==1:
                            self.call()
                        else:
                            self.fold()

                else:
                    if self.aggr>6:
                        self.call()
                    else:
                        if random.randint(1,4)==1:
                            self.call
                        else:
                            self.fold()
            
            elif self.big is True:
                self.stake+=50
                self.credits-=50
                self.check()
                    
            else:
                self.preflop()
        else:
            if self.small is True:
                self.stake+=smallblind
                self.credits-=smallblind
            if self.big is True:
                self.stake+=50
                self.credits-=50
            self.preflop()

    def preflop(self):
        # taking into account how much the bet is
        prob=(minbet/(self.credits+self.stake))
        # benefit of a high card
        boost=self.card1.value-7
        boost2=self.card2.value-7
        # general equation
        # else situation is for taking random chances
        # difference between aggression and threshold of betting will play into how much they raise
        '''
        if self.aggr>(([1(great)-3(okay)]*(1+prob))-(max(boost,boost2)/[3(value=big influence)-5(value=small influence)])):
            if (self.aggr-(([1(great)-3(okay)]*(1+prob))-(max(boost,boost2)/[3(value=big influence)-5(value=small influence)])))>4:
                self._raise(minbet+(10*int(self.aggr-(([1(great)-3(okay)]*(1+prob))-(max(boost,boost2)/[3(value=big influence)-5(value=small influence)]))))
            else:
                self.call()
        else:
            if int(self.aggr)==random.randint(1,10):
                self.call()
            else:
                self.fold()
        '''

        # pair
        if self.card1.value==self.card2.value:
            if self.aggr>((1*(1+prob))-(boost/5)):
                if (self.aggr-((1*(1+prob))-(boost/5)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((1*(1+prob))-(boost/5))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()
        # suited high cards
        elif self.card1.value>10 and self.card2.value>10 and self.card1.suit==self.card2.suit:
            if self.aggr>((1*(1+prob))-(max(boost,boost2)/3)):
                if (self.aggr-((1*(1+prob))-(max(boost,boost2)/3)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((1*(1+prob))-(max(boost,boost2)/3))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()
        # high cards
        elif self.card1.value>10 and self.card2.value>10:
            if self.aggr>((2*(1+prob))-(max(boost,boost2)/5)):
                if (self.aggr-((2*(1+prob))-(max(boost,boost2)/5)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((1.5*(1+prob))-(max(boost,boost2)/5))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()
        # suited cards
        elif self.card1.suit==self.card2.suit:
            if self.aggr>((2.5*(1+prob))-(max(boost,boost2)/5)):
                if (self.aggr-((2.5*(1+prob))-(max(boost,boost2)/5)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((1.75*(1+prob))-(max(boost,boost2)/5))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()
        # possibility for straight
        elif abs(self.card1.value-self.card2.value)<=1:
            if self.aggr>((2.5*(1+prob))-(max(boost,boost2)/4)):
                if (self.aggr-((2.5*(1+prob))-(max(boost,boost2)/4)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((1.5*(1+prob))-(max(boost,boost2)/4))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()

        elif abs(self.card1.value-self.card2.value)<=2:
            if self.aggr>((3*(1+prob))-(max(boost,boost2)/4)):
                if (self.aggr-((3*(1+prob))-(max(boost,boost2)/4)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((2*(1+prob))-(max(boost,boost2)/4))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()

        elif abs(self.card1.value-self.card2.value)<=3:
            if self.aggr>((4*(1+prob))-(max(boost,boost2)/4)):
                if (self.aggr-((4*(1+prob))-(max(boost,boost2)/4)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((2.5*(1+prob))-(max(boost,boost2)/4))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()
        
        elif abs(self.card1.value-self.card2.value)<=4:
            if self.aggr>((4*(1+prob))-(max(boost,boost2)/4)):
                if (self.aggr-((4*(1+prob))-(max(boost,boost2)/4)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((2.5*(1+prob))-(max(boost,boost2)/4))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()
        # one high card
        elif self.card1.value>10 or self.card2.value>10:
            if self.aggr>((5*(1+prob))-(max(boost,boost2)/3)):
                if (self.aggr-((5*(1+prob))-(max(boost,boost2)/3)))>4:
                    self._raise(min(self.credits+self.stake,minbet+(10*int(self.aggr-((3*(1+prob))-(max(boost,boost2)/3))))))
                else:
                    self.call()
            else:
                if int(self.aggr)==random.randint(1,10):
                    self.call()
                else:
                    self.fold()

        else:
            self.fold()

    def flop(self):
        checkok=True

        for i in player_list:
            if i.stake!=0:
                checkok=False
        # probability of check will depend on aggression/quality of hand

        if checkok==True:
            cardlist=[]
            cardlist.append(self.card1)
            cardlist.append(self.card2)
            cardlist+=c

            tempscore=winning(cardlist,self)
            if tempscore>=(1000-(100*self.aggr)):
                if random.randint(1,2)==1:
                    self._raise(min(self.credits+self.stake,minbet+(20*int(tempscore/((11-self.aggr)*15)))))
                else:
                    self.call()
            elif tempscore>(1000-(150*self.aggr)):
                self.call()
            else:
                self.check()

        if checkok==False:

            betok=False

            for i in player_list:
                if i.stake>self.stake:
                    betok=True

            if betok==True:
                cardlist=[]
                cardlist.append(self.card1)
                cardlist.append(self.card2)
                cardlist+=c

                tempscore=winning(cardlist,self)
                if tempscore<=100:
                    if random.randint(1,int(11-self.aggr))==1:
                        self.call()
                    else:
                        self.fold()
                elif tempscore>=(1000-(100*self.aggr)):
                    if random.randint(1,2)==1:
                        self._raise(min(self.credits+self.stake,minbet+(20*int(tempscore/((11-self.aggr)*15)))))
                    else:
                        self.call()
                elif tempscore>(1000-(150*self.aggr)):
                    self.call()
                elif minbet<((self.credits+self.stake)/(12-self.aggr)):
                    if random.randint(1,5)==1:
                        self.fold()
                    else:
                        self.call()
                else:
                    self.fold()
    
    def turn(self):
        checkok=True

        for i in player_list:
            if i.stake!=0:
                checkok=False
        # probability of check will depend on aggression/quality of hand
        if checkok==True:

            tempscore=winning(findhand(self,c),self)
            if tempscore>=(1000-(100*self.aggr)):
                if random.randint(1,2)==1:
                    self._raise(min(self.credits+self.stake,minbet+(20*int(tempscore/((11-self.aggr)*15)))))
                else:
                    self.call()
            elif tempscore>(1000-(150*self.aggr)):
                self.call()
            else:
                self.check()

        if checkok==False:

            betok=False

            for i in player_list:
                if i.stake>self.stake:
                    betok=True

            if betok==True:

                tempscore=winning(findhand(self,c),self)
                if tempscore<=100:
                    if random.randint(1,int(11-self.aggr))==1:
                        self.call()
                    else:
                        self.fold()
                elif tempscore>=(1000-(100*self.aggr)):
                    if random.randint(1,2)==1:
                        self._raise(min(self.credits+self.stake,minbet+(20*int(tempscore/((11-self.aggr)*15)))))
                    else:
                        self.call()
                elif tempscore>(1000-(150*self.aggr)):
                    self.call()
                elif minbet<((self.credits+self.stake)/(12-self.aggr)):
                    if random.randint(1,5)==1:
                        self.fold()
                    else:
                        self.call()
                else:
                    self.fold()

    def river(self):
        checkok=True

        for i in player_list:
            if i.stake!=0:
                checkok=False
        # probability of check will depend on aggression/quality of hand
        if checkok==True:

            tempscore=winning(findhand(self,c),self)
            if tempscore>=(1000-(100*self.aggr)):
                if random.randint(1,2)==1:
                    self._raise(min(self.credits+self.stake,minbet+(20*int(tempscore/((11-self.aggr)*15)))))
                else:
                    self.call()
            elif tempscore>(1000-(150*self.aggr)):
                self.call()
            else:
                self.check()

        if checkok==False:

            betok=False

            for i in player_list:
                if i.stake>self.stake:
                    betok=True

            if betok==True:

                tempscore=winning(findhand(self,c),self)
                if tempscore<=100:
                    if random.randint(1,int(11-self.aggr))==1:
                        self.call()
                    else:
                        self.fold()
                elif tempscore>=(1000-(100*self.aggr)):
                    if random.randint(1,2)==1:
                        self._raise(min(self.credits+self.stake,minbet+(20*int(tempscore/((11-self.aggr)*15)))))
                    else:
                        self.call()
                elif tempscore>(1000-(150*self.aggr)):
                    self.call()
                elif minbet<((self.credits+self.stake)/(12-self.aggr)):
                    if random.randint(1,5)==1:
                        self.fold()
                    else:
                        self.call()
                else:
                    self.fold()

# produces the 5 community cards
class Community(list):
    def __init__(self,deck):
        self.deck=deck
        burn=0
        
    def flop(self):
        burn=self.deck.deal()
        self.append(self.deck.deal())
        burn=self.deck.deal()
        self.append(self.deck.deal())
        burn=self.deck.deal()
        self.append(self.deck.deal())
        print('\nFlop: {0}, {1}, {2}'.format(self[0],self[1],self[2]))

    def turn(self):
        burn=self.deck.deal()
        self.append(self.deck.deal())
        print('\nTurn: {0}, {1}, {2}, {3}'.format(self[0],self[1],self[2],self[3]))

    def river(self):
        burn=self.deck.deal()
        self.append(self.deck.deal())
        print('\nRiver: {0}, {1}, {2}, {3}, {4}'.format(self[0],self[1],self[2],self[3],self[4]))

# assigns dealer, small blind, big blind
# if only 2 in list: small blind, big blind
def rolePick():
    global pot
    for i in player_list:
        i.dealer=False
        i.small=False
        i.big=False  

    if len(player_list)>2:
        player_list[-3].dealer=True
        player_list[-2].small=True
        player_list[-1].big=True
    else:
        player_list[0].small=True
        player_list[1].big=True

# will return float, unless invalid input then it repeats
def getAmountFromUser(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print('Please enter a valid number.')

# references getAmountFromUser with normal message
def getBet():
    return getAmountFromUser('Total amount you want to bet: ')

# only for very first bet preflop
def player1Turn():
    if h1.small is True:
        print('\nYou are the small blind.',
              '\n25 credits are automatically put up.')
        print('\nYour cards are:')
        print(h1.card1)
        print(h1.card2,'\n')
        h1.stake+=smallblind
        h1.credits-=smallblind
        
        print('Minimum bet is:',minbet)

        while True:
            bet=input('Would you like to (2) call, (3) raise, or (4) fold? ')
            
            if bet=='2':
                os.system('clear')
                h1.call()

            elif bet=='3':
                os.system('clear')
                h1._raise(getBet())

            elif bet=='4':
                os.system('clear')
                h1.fold()

            else:
                print('Try again.')
                continue
            break
    
    elif h1.big is True:
        print('\nYou are the big blind.',
              '\n50 credits are automatically put up.')
        print('\nYour cards are:')
        print(h1.card1)
        print(h1.card2,'\n')
        h1.stake+=50
        h1.credits-=50
        
        print('Minimum bet is:',minbet)

        if h1.stake==minbet:
            while True:
                bet=input('Would you like to (1) check, (3) raise, or (4) fold? ')
                
                if bet=='1':
                    os.system('clear')
                    h1.check()

                elif bet=='3':
                    os.system('clear')
                    h1._raise(getBet())

                elif bet=='4':
                    os.system('clear')
                    h1.fold()

                else:
                    print('Try again.')
                    continue
                break
        else:
            betok=False

            for i in player_list:
                if i.stake>h1.stake:
                    betok=True

            if betok==True:
                while True:
                    bet=input('Would you like to (2) call, (3) raise, or (4) fold? ')

                    if bet=='2':
                        os.system('clear')
                        h1.call()
                        
                    elif bet=='3':
                        os.system('clear')
                        h1._raise(getBet())

                    elif bet=='4':
                        os.system('clear')
                        h1.fold()

                    else:
                        print('Try again.')
                        continue
                    break
            
    elif h1.dealer is True:
        print('\nYou are the dealer.')

        print('\nYour cards are:')
        print(h1.card1)
        print(h1.card2,'\n')

        print('Minimum bet is:',minbet)

        while True:
            bet=input('Would you like to (2) call, (3) raise, or (4) fold? ')

            if bet=='2':
                os.system('clear')
                h1.call()
                
            elif bet=='3':
                os.system('clear')
                h1._raise(getBet())

            elif bet=='4':
                os.system('clear')
                h1.fold()

            else:
                print('Try again.')
                continue
            break

    else:
        print('\nYour cards are:')
        print(h1.card1)
        print(h1.card2,'\n')

        print('Minimum bet is:',minbet)

        while True:
            bet=input('Would you like to (2) call, (3) raise, or (4) fold? ')

            if bet=='2':
                os.system('clear')
                h1.call()
                
            elif bet=='3':
                os.system('clear')
                h1._raise(getBet())

            elif bet=='4':
                os.system('clear')
                h1.fold()

            else:
                print('Try again.')
                continue
            break

# for normal betting turns, sees if checking is ok
def playerTurn():
    checkok=True

    for i in player_list:
        if i.stake!=0:
            checkok=False

    if checkok==True:
        print('\nYour cards are:')
        print(h1.card1)
        print(h1.card2,'\n')

        print('Minimum bet is:',minbet)
        while True:
            bet=input('Would you like to (1) check, (2) call, (3) raise, or (4) fold? ')

            if bet=='1':
                os.system('clear')
                h1.check()
                
            elif bet=='2':
                os.system('clear')
                h1.call()
                
            elif bet=='3':
                os.system('clear')
                h1._raise(getBet())

            elif bet=='4':
                os.system('clear')
                h1.fold()

            else:
                print('Try again.')
                continue
            break

    if checkok==False:

        betok=False

        for i in player_list:
            if i.stake>h1.stake:
                betok=True

        if betok==True:
            print('\nYour cards are:')
            print(h1.card1)
            print(h1.card2,'\n')

            print('Minimum bet is:',minbet)

            while True:
                bet=input('Would you like to (2) call, (3) raise, or (4) fold? ')

                if bet=='2':
                    os.system('clear')
                    h1.call()
                    
                elif bet=='3':
                    os.system('clear')
                    h1._raise(getBet())

                elif bet=='4':
                    os.system('clear')
                    h1.fold()

                else:
                    print('Try again.')
                    continue
                break

# returns best 5 card hand for player as list of card objects
def findhand(player,community):
    hand=[player.card1,player.card2]+community
    scoredict=collections.defaultdict(list)
    combo=itertools.combinations(hand,5)

    combos=[]
    for i in combo:
        combos.append(list(i))

    for i in combos:
        score=(winning(i,player))
        scoredict[score].append(i)

    # besthand is the float returned by scorehands()
    besthand=max(scoredict)
    # best score assigned to player attribute
    player.besthand=besthand

    return scoredict[besthand][0]

# finds best possible hand (score) out of 5 given cards, returns scorehands()
def winning(cardlist,player):
    valuedict=collections.defaultdict(int)
    suitdict=collections.defaultdict(int)

    for i in cardlist:
        valuedict[i.value]+=1
        suitdict[i.suit]+=1

    sortedcardlist=sorted(cardlist,key=lambda x:x.value)

    handmin=sortedcardlist[0]
    handmax=sortedcardlist[-1]

    #FLUSH
    if len(suitdict)==1:
        kicker=[]
        checksum=0
        for i in cardlist:
            checksum+=i.value

        if handmin.value==10 and handmax.value==14:
            player.besthandstring=('{0} has a royal flush'.format(player.name))
            return scorehands('royalflush',handmax,kicker)
        elif handmax.value==14 and checksum-handmax.value==14:
            player.besthandstring=('{0} has a 5-high straight flush'.format(player.name))
            return scorehands('fivestraightflush',handmax,kicker)
        elif handmax.value==(handmin.value+4):
            player.besthandstring=('{0} has a {1}-high straight flush'.format(player.name,handmax.name))
            return scorehands('straightflush',handmax,kicker)
        else:
            for i in sortedcardlist:
                if i.value==handmax.value:
                    continue
                else:
                    kicker.append(i)
            player.besthandstring=('{0} has a {1}-high flush'.format(player.name,handmax.name))
            return scorehands('flush',handmax,kicker)

    #4 OF A KIND OR FULL HOUSE
    elif len(valuedict)==2:
        fourkind=[]
        threekind=[]
        pair=[]
        kicker=[]
        for i in valuedict:
            if valuedict[i]==4:
                for j in sortedcardlist:
                  if j.value==i:
                    fourkind.append(j)
            if valuedict[i]==3:
                for j in sortedcardlist:
                  if j.value==i:
                    threekind.append(j)
            if valuedict[i]==2:
                for j in sortedcardlist:
                  if j.value==i:
                    pair.append(j)
            if valuedict[i]==1:
                for j in sortedcardlist:
                  if j.value==i:
                    kicker.append(j)
        if fourkind!=[]:
            player.besthandstring=("{0} has a 4 of a kind of {1}s; kicker: {2}".format(player.name,fourkind[0].name,kicker[0].name))
            return scorehands('fourkind',fourkind,kicker)
        if threekind!=[]:
            player.besthandstring=("{0} has a full house: {1}s full of {2}s".format(player.name,threekind[0].name,pair[0].name))
            return scorehands('fullhouse',threekind,pair)
                
    #STRAIGHT OR HIGH CARD
    elif len(valuedict)==5:
        kicker=[]
        checksum=0
        for i in cardlist:
            checksum+=i.value

        if handmax.value==14 and checksum==14:
            player.besthandstring=('{0} has a 5-high straight'.format(player.name))
            return scorehands('fivestraight',handmax,kicker)
        if handmax.value==(handmin.value+4):
            player.besthandstring=('{0} has a {1}-high straight'.format(player.name,handmax.name))
            return scorehands('straight',handmax,kicker)
        else:
          for i in sortedcardlist:
            if i.value==handmax.value:
              continue
            else:
              kicker.append(i)
          player.besthandstring=('{0} has a high card: {1}; kicker: {2}, {3}, {4}, {5}'.format(player.name,handmax.name,kicker[3].name,kicker[2].name,kicker[1].name,kicker[0].name))
          return scorehands('highcard',handmax,kicker)

    #3 OF A KIND OR 2 PAIRS
    elif len(valuedict)==3:
        threekind=[]
        pair=[]
        kicker=[]
        for i in valuedict:
            if valuedict[i]==3:
                for j in sortedcardlist:
                  if j.value==i:
                    threekind.append(j)
            if valuedict[i]==2:
                for j in sortedcardlist:
                  if j.value==i:
                    pair.append(j)
        
        for i in sortedcardlist:
          if i in threekind:
            continue
          elif i in pair:
            continue
          else:
            kicker.append(i)

        if threekind!=[]:
            player.besthandstring=("{0} has a three of a kind of {1}s; kicker: {2}, {3}".format(player.name,threekind[0].name,kicker[1].name,kicker[0].name))
            return scorehands('threekind',threekind,kicker)
        if pair!=[]:
            player.besthandstring=("{0} has a 2 pair: {1}s and {2}s; kicker:{3}".format(player.name,pair[0].name,pair[2].name,kicker[0].name))
            return scorehands('twopairs',pair,kicker)

    #PAIR
    elif len(valuedict)==4:
      pair=[]
      kicker=[]
      for i in valuedict:
        if valuedict[i]==2:
          for j in sortedcardlist:
            if j.value==i:
              pair.append(j)

      for i in sortedcardlist:
        if i in pair:
          continue
        else:
          kicker.append(i)

      player.besthandstring=("{0} has a pair of {1}s; kicker: {2}, {3}, {4}".format(player.name,pair[0].name,kicker[2].name,kicker[1].name,kicker[0].name))
      return scorehands('pair',pair,kicker)

# returns float score of hand
def scorehands(name, hand, kicker):
    if name == 'royalflush':
        return float(900)
    if name == 'straightflush':
        return float(800 + hand.value)
    if name == 'fivestraightflush':
        return float(805)
    if name == 'fourkind':
        return float(700 + hand[0].value + (kicker[0].value/100))
    if name == 'fullhouse':
        return float(600 + hand[0].value + (kicker[0].value/100))
    if name == 'flush':
        sortedkicker=sorted(kicker,key=lambda x:x.value)
        return float(500 + hand.value + (sortedkicker[3].value/100) + (sortedkicker[2].value/10000) + (sortedkicker[1].value/1000000) + (sortedkicker[0].value/100000000))
    if name == 'straight':
        return float(400 + hand.value)
    if name == 'fivestraight':
        return float(405)
    if name == 'threekind':
        sortedkicker=sorted(kicker,key=lambda x:x.value)
        return float(300 + hand[0].value + (sortedkicker[1].value/100) + (sortedkicker[0].value/10000))
    if name == 'twopairs':
        sortedhand=sorted(hand,key=lambda x:x.value)
        return float(200 + sortedhand[2].value + (sortedhand[0].value/100) + (kicker[0].value/10000))
    if name == 'pair':
        sortedkicker=sorted(kicker,key=lambda x:x.value)
        return float(100 + hand[0].value + (sortedkicker[2].value/100) + (sortedkicker[1].value/10000) + (sortedkicker[0].value/1000000))
    if name == 'highcard':
        sortedkicker=sorted(kicker,key=lambda x:x.value)
        return float(hand.value + (sortedkicker[3].value/100) + (sortedkicker[2].value/10000) + (sortedkicker[1].value/1000000)+(sortedkicker[0].value/100000000))

##Texas hold'em
os.system('clear')
pot=0
smallblind=25
bigblind=50
h1=Hand(input('Enter player name: '))
# to my understanding, a list that can be rotated
player_list=collections.deque([])
player_list.append(h1)
playnum=input('How many other people at the table (minimum 2)? ')
for i in range(int(playnum)):
    h=Computer('Computer '+str(i+1),(10*random.random()))
    player_list.append(h)

print('\nCommands are: (1) Check (2) Call (3) Raise (4) Fold',
    '\n"Call" when you are the first bettor will bet the minimum amount (big blind).'
    '\nPlayers start with 1000 credits.',
    '\nSmall blind is {} credits.'.format(smallblind),
    '\nBig blind is {} credits.'.format(bigblind),
    '\nTo play the round, the small blind will need to at minimum match big blind.'
    '\nTo play the round, the big blind only needs to check,'
    '\nor if there is a higher bet, call.')


while True:
    activecount=len(player_list)
    d=Deck()
    pot=0
    rolePick()
    print('\nPot: {0}'.format(pot))
    for i in player_list:
        print(i)

    # Pre Flop
    for i in player_list:
        i.card1=d.deal()
        i.card2=d.deal()
    minbet=bigblind

    for i in player_list:
        if type(i)==Computer:
            time.sleep(random.random()*2)
            i.preflop1()
        else:
            player1Turn()

    checkok=True

    for i in player_list:
        if i.stake!=0:
            checkok=False

    if checkok==False:
        # should continue looping until all players (who haven't folded) have the same amount at stake
        should_restart=True
        while should_restart:
            should_restart=False
            for i in player_list:
                if i.done==False:
                    if (i.stake==minbet):
                        continue
                    else:
                        if activecount>1:
                            if i.credits>0:
                                if type(i)==Computer:
                                    time.sleep(random.random()*2)
                                    i.preflop()
                                else:
                                    playerTurn()
                                should_restart=True

    print()

    # Everything at stake should go into pot at this point
    for i in player_list:
        pot+=i.stake
        i.stake=0

    print('Pot: {0}'.format(pot))
    for i in player_list:
        if i.done==False:
            print(i)

    # Flop
    if activecount>1:
        print('\n***********************')
        c=Community(d)
        c.flop()
        minbet=bigblind
        for i in player_list:
            if i.done==False:
                if activecount>1:
                    if i.credits>0:
                        if type(i)==Computer:
                            time.sleep(random.random()*2)
                            i.flop()
                        else:
                            playerTurn()

        checkok=True

        for i in player_list:
            if i.stake!=0:
                checkok=False

        if checkok==False:
            # should continue looping until all players (who haven't folded) have the same amount at stake
            should_restart=True
            while should_restart:
                should_restart=False
                for i in player_list:
                    if i.done==False:
                        if (i.stake==minbet):
                            continue
                        else:
                            if activecount>1:
                                if i.credits>0:
                                    if type(i)==Computer:
                                        time.sleep(random.random()*2)
                                        i.flop()
                                    else:
                                        playerTurn()
                                    should_restart=True

        print()

        # Everything at stake should go into pot at this point
        for i in player_list:
            pot+=i.stake
            i.stake=0

        print('Pot: {0}'.format(pot))
        for i in player_list:
            if i.done==False:
                print(i)

    # Turn
    if activecount>1:
        print('\n***********************')
        c.turn()
        minbet=bigblind
        for i in player_list:
            if i.done==False:
                if activecount>1:
                    if i.credits>0:
                        if type(i)==Computer:
                            time.sleep(random.random()*2)
                            i.turn()
                        else:
                            playerTurn()

        checkok=True

        for i in player_list:
            if i.stake!=0:
                checkok=False

        if checkok==False:
            # should continue looping until all players (who haven't folded) have the same amount at stake
            should_restart=True
            while should_restart:
                should_restart=False
                for i in player_list:
                    if i.done==False:
                        if (i.stake==minbet):
                            continue
                        else:
                            if activecount>1:
                                if i.credits>0:
                                    if type(i)==Computer:
                                        time.sleep(random.random()*2)
                                        i.turn()
                                    else:
                                        playerTurn()
                                    should_restart=True

        print()

        # Everything at stake should go into pot at this point
        for i in player_list:
            pot+=i.stake
            i.stake=0

        print('Pot: {0}'.format(pot))
        for i in player_list:
            if i.done==False:
                print(i)

    # River
    if activecount>1:
        print('\n***********************')
        c.river()
        minbet=bigblind
        for i in player_list:
            if i.done==False:
                if activecount>1:
                    if i.credits>0:
                        if type(i)==Computer:
                            time.sleep(random.random()*2)
                            i.river()
                        else:
                            playerTurn()

        checkok=True

        for i in player_list:
            if i.stake!=0:
                checkok=False

        if checkok==False:
            # should continue looping until all players (who haven't folded) have the same amount at stake
            should_restart=True
            while should_restart:
                should_restart=False
                for i in player_list:
                    if i.done==False:
                        if (i.stake==max(minbet,0)):
                            continue
                        else:
                            if activecount>1:
                                if i.credits>0:
                                    if type(i)==Computer:
                                        time.sleep(random.random()*2)
                                        i.river()
                                    else:
                                        playerTurn()
                                    should_restart=True

        print()

    # Everything at stake should go into pot at this point
    for i in player_list:
        pot+=i.stake
        i.stake=0
    if activecount>1:
        print('Pot: {0}'.format(pot))
        for i in player_list:
            if i.done==False:
                x=findhand(i,c)
                # runs winning() again with returned value from findhand() (the best hand), to set player's besthandstring to the right hand
                winning(x,i)

        for i in player_list:
            if i.done==False:
                if activecount>1:
                    print(i.besthandstring)

        # determines winner/ties
        winner=0
        winnerlist=[]
        for i in player_list:
            if i.done==False:
                if i.besthand>winner:
                    winner=i.besthand

        for i in player_list:
            if i.done==False:
                if i.besthand==winner:
                    winnerlist.append(i)

        # prints winners/ties
        if len(winnerlist)==1:
            print('{0} is the winner'.format(winnerlist[0].name))
        else:
            print('There has been a tie between:')
            for i in winnerlist:
                print(i.name)

        # distributes winnings
        if len(winnerlist)==1:
            winnerlist[0].credits+=pot
            pot=0
        else:
            pot/=len(winnerlist)
            for i in winnerlist:
                i.credits+=pot
            pot=0

    else:
        for i in player_list:
            if i.done==False:
                print('{0} is the winner'.format(i.name))
                i.credits+=pot
                break

    # resets besthand and besthandstring for next round
    for i in player_list:
        i.besthand=0
        i.besthandstring=''

    # rotates positions, removes any players with 0 or negative credits, resets their fold attribute
    player_list.rotate()
    newplayer_list=collections.deque([])

    for i in player_list:
        i.done=False
        if i.credits>0:
            newplayer_list.append(i)

    player_list=newplayer_list

    # determines final game winner
    if len(player_list)==1:
        print('{0} is the final winner!'.format(player_list[0].name))
        exit()

    print('\n***** New Round *****')
























