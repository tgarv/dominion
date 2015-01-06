#qpy:console
from random import shuffle

class Card():
  name = ''
  cost = 0
  def play(self, Turn):
    # Any special rules for a card will happen here
    pass

  def __str__(self):
    return '<Card>: ' + self.name

  def __repr__(self):
    return str(self)
    
  def get_details(self):
    return self.name + '\n' + (str)(self.cost) + 'G'

class ActionCard(Card):
  action_increases = 0
  buy_increases = 0
  money_increases = 0
  cards_to_draw = 0
  
  def get_details(self):
    value = '\n' + self.name + '\n' 
    if self.action_increases:
      value += '+' + (str)(self.action_increases) + ' action' + '\n'
    if self.buy_increases:
      value += '+' + (str)(self.buy_increases) + ' buy' + '\n'
    if self.cards_to_draw:
      value += '+' + (str)(self.cards_to_draw) + ' card' + '\n'
    if self.money_increases:
      value += '+' + (str)(self.money_increases) + ' G' + '\n'
      
    value += 'Cost: ' + (str)(self.cost) + '\n'
    return value

class AttackCard(ActionCard):
  def play(self, Turn):
    ActionCard.play(self, Turn)
    # Special Attack logic here

class MoneyCard(Card):
  monetary_value = 0

class VictoryCard(Card):
  victory_points = 0

  def get_score(self):
			return self.victory_points

class GardensCard(VictoryCard):
	def get_score(self, deck_length):
		return deck_length/10  		

class Deck():
  def __init__(self):
    self.cards = [] # list of Cards

  def shuffle(self, discard_pile):
    self.cards.extend(discard_pile)
    shuffle(self.cards)

  def draw(self, discard_pile, number=5):
    #TODO error checking, shuffling
    return_value = []
    if len(self.cards) < number:
      return_value = self.cards
      self.cards = []
      number -= len(return_value)
      self.shuffle(discard_pile) #TODO need to empty the discard pile
      print 'shuffling'

    if len(self.cards) < number:
      # Won't actually throw an error, but still weird so print a message
      print 'Trying to draw too many cards'

    return_value.extend(self.cards[:number])
    self.cards = self.cards[number:]
    return return_value
    
  def add_card(self, card):
    self.cards.append(card)

  def get_score(self):
    score = 0
    for card in self.cards:
      if isinstance(card, VictoryCard):
        score += card.get_score()

    return score

  def __repr__(self):
    return 'Deck: ' + ', '.join([str(card) for card in self.cards])

class Player():
  def __init__(self):
    self.name = ''
    self.deck = Deck()
    self.discard_pile = []
    self.hand = []

  def draw_hand(self):
    self.draw_cards(5)

  def draw_cards(self, number):
    print 'drawing ', number, ' cards'
    self.hand.extend(self.deck.draw(self.discard_pile, number))
    
  def add_card(self, card):
    self.deck.add_card(card)

  def buy_card(self, card):
    self.discard_pile.append(card)
    
  # Puts the current hand into the discard pile and draws a new one
  def end_turn(self):
    self.discard_pile.extend(self.hand)
    self.hand = []
    self.draw_hand()

class Game():
  players = []
  cards = {}
  card_counts = {}
  trash = []
  current_turn = {}
  current_player_index = 0
  
  def initialize_turn(self):
    self.current_player_index += 1
    self.current_player_index %= len(self.players)
    self.current_turn = {'actions_left':1, 'buys_left':1, 'money': 0, 'player': self.players[self.current_player_index]}
    print 'Starting new turn. Player ' + self.current_turn['player'].name + '\'s turn'
    print 'Current hand: ', self.current_turn['player'].hand
  
  def add_card(self, card, quantity = 10):
    self.card_counts[card.name] = quantity
    self.cards[card.name] = card
  
  def is_game_over(self):
    if self.card_counts.get('Province') == 0:
      return True
    # Now iterate through the cards -- if 3 piles are empty the game is over
    number_of_empty_piles = 0
    for name, quantity in self.card_counts.iteritems():
      if quantity == 0:
        number_of_empty_piles += 1
        if number_of_empty_piles >= 3:
          return True
    return False
    
  def play_card(self, card):
    print card
    if isinstance(card, ActionCard):
      print 'Playing:', card
      self.current_turn['actions_left'] -= 1
      self.current_turn['actions_left'] += card.action_increases
      self.current_turn['buys_left'] += card.buy_increases
      self.current_turn['money'] += card.money_increases
      if card.cards_to_draw > 0:
        self.current_turn['player'].draw_cards(card.cards_to_draw)
        print 'current hand:', self.current_turn['player'].hand
      print self.current_turn

    elif isinstance(card, MoneyCard):
  		   self.current_turn['money'] += card.monetary_value
  		   print self.current_turn['money'], ' money'

  def buy_card(self, card):
  	  if self.current_turn['buys_left'] > 0:
  	    if self.current_turn['money'] >= card.cost:
  	      self.current_turn['buys_left'] -= 1
  	      print 'Buying ' , card
  	      self.current_turn['player'].buy_card(card)
  	      self.card_counts[card.name] -= 1
  	    else:
  	      print 'not enough money'
  	  else:
  	    print 'No buys left this turn'
  	  print self.card_counts
  	    
  def end_turn(self):
  	  self.current_turn['player'].end_turn()
  	
  def next_turn(self):
    self.end_turn()
    self.initialize_turn()
    
  def parse_input(self, input):
    print self.is_game_over()
    words = input.split()
    player = self.current_turn['player']
    if len(words) and words[0] == 'end':
      self.next_turn()
      
    if input == 'all money':
      for i in xrange(len(player.hand) - 1, -1, -1):
        card = player.hand[i]
        if isinstance(card, MoneyCard):
          self.play_card(card)
          del player.hand[i]
          player.discard_pile.append(card)

    if len(words) == 2:
      action, target = words
      if action == 'buy':
        card = self.cards.get(target, None)
        if card:
          self.buy_card(card)
        else:
          print 'Invalid card: ', target
      elif action == 'play':
        for i in xrange(len(player.hand)):
          card = player.hand[i]
          if card.name == target:
            del player.hand[i]
            self.play_card(card)
            # Move the card to the discard pile and remove it from the hand
            # TODO this should probably happen somewhere else
            player.discard_pile.append(card)
            break
        else:
          print 'Card not found'
      elif action == 'show':
        if target == 'hand':
          print player.hand
        elif target == 'board':
          print self.card_counts
        elif target in self.cards:
          print self.cards[target].get_details()

# Instantiate money cards
copper = MoneyCard()
copper.cost = 0
copper.name = 'Copper'
copper.monetary_value = 1
silver = MoneyCard()
silver.cost = 3
silver.name = 'Silver'
silver.monetary_value = 2
gold = MoneyCard()
gold.cost = 6
gold.name = 'Gold'
gold.monetary_value = 3

# Instantiate victory cards
estate = VictoryCard()
estate.name = 'Estate'
estate.victory_points = 1
estate.cost = 2
duchy = VictoryCard()
duchy.name = 'Duchy'
duchy.victory_points = 3
duchy.cost = 5
province = VictoryCard()
province.name = 'Province'
province.victory_points = 6
province.cost = 8
# TODO Gardens has a special function to compute its VP
gardens = VictoryCard()
gardens.name = 'Gardens'
gardens.cost = 4
gardens.victory_points = 0

#action cards
village = ActionCard()
village.name = 'Village'
village.cost = 3
village.action_increases = 2
village.cards_to_draw = 1

market = ActionCard()
market.name = 'Market'
market.cost = 5
market.action_increases = 1
market.cards_to_draw = 1
market.buy_increases = 1
market.money_increases = 1

woodcutter = ActionCard()
woodcutter.name = 'Woodcutter'
woodcutter.cost = 3
woodcutter.action_increases = 0
woodcutter.cards_to_draw = 0
woodcutter.buy_increases = 1
woodcutter.money_increases = 2


# Set up a normal starting hand: 7 coppers and 3 estates
player = Player()
player.name = '1'
player2 = Player()
player2.name = '2'

for i in xrange(7):
  player.add_card(copper)
  player2.add_card(copper)
for i in xrange(3):
  player.add_card(estate)
  player2.add_card(estate)
player.deck.shuffle([])
player2.deck.shuffle([])
<<<<<<< HEAD
=======
#player2.draw_hand()
>>>>>>> branch 'master' of https://github.com/tgarv/dominion.git
player.draw_hand()
player2.draw_hand()

game = Game()
game.players.append(player)
game.players.append(player2)
game.add_card(estate, 50)
game.add_card(duchy, 15)
game.add_card(province, 12)
game.add_card(copper, 50)
game.add_card(silver, 50)
game.add_card(gold, 50)
game.add_card(village, 10)
game.add_card(market, 10)
game.add_card(woodcutter, 10)
game.initialize_turn()
print player.hand
#game.parse_input('play Copper')
#game.parse_input('play Copper')
#game.parse_input('play Copper')
#game.parse_input('play Copper')
#game.parse_input('play Copper')
#game.parse_input('buy Village')
#game.parse_input('end turn')
#game.parse_input('end turn')

while True:
  game.parse_input(raw_input('Enter command\n'))

"""
for card in player.hand:
  game.play_card(card)
game.buy_card(silver)
game.next_turn()
for card in player.hand:
  game.play_card(card)
game.buy_card(silver)
print player.hand
game.next_turn()
for card in player.hand:
  game.play_card(card)
game.buy_card(silver)
print player.hand
game.next_turn()
for card in player.hand:
  game.play_card(card)
game.buy_card(silver)
print player.hand
game.next_turn()
game.buy_card(silver)
print player.hand
"""

# TODO at game end, make sure to shuffle discard pile into deck before computing score