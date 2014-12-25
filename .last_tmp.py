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

class ActionCard(Card):
  action_increases = 0
  buy_increases = 0
  money_increases = 0
  cards_to_draw = 0

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
  cards = [] # list of Cards

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
      self.shuffle(discard_pile)

    if len(self.cards) < number:
      # Won't actually throw an error, but still weird so print a message
      print 'Trying to draw too many cards'

    return_value.extend(self.cards[:number])
    self.cards = self.cards[number:]
    return return_value

  def get_score(self):
    score = 0
    for card in self.cards:
      if isinstance(card, VictoryCard):
        score += card.get_score()

    return score

  def __repr__(self):
    return 'Deck: ' + ', '.join([str(card) for card in self.cards])

class Player():
  name = ''
  deck = Deck()
  discard_pile = [] # list of cards
  hand = [] # list of cards

  def draw_hand(self):
    self.draw_cards(5)

  def draw_cards(self, number):
    self.hand.append(self.deck.draw(self.discard_pile, number))

class Turn():
  player = None
  actions_left = 1
  buys_left = 1
  money = 0
  phase = 'action'
  
  def play_card(self, card):
  	  if isinstance(card, ActionCard):
  			  self.actions_left -= 1
  			  self.actions_left += card.action_increases
  			  self.buys_left += card.buy_increases
  			  self.money += card.money_increases
  			  if card.cards_to_draw > 0:

    elif isinstance(card, MoneyCard):
  		   self.money += card.monetary_value
  		

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
village = ActionCard():
village.name = 'Village'
village.cost = 3
village.action_increases = 2
village.cards_to_draw = 1


# Set up a normal starting hand: 7 coppers and 3 estates
deck = Deck()
for i in xrange(7):
  deck.cards.append(copper)
for i in xrange(3):
  deck.cards.append(estate)
deck.shuffle([])
#print deck.get_score()
#print deck
#print deck.draw([])
#print deck

player = Player()
player.deck = deck
player.name = '1'
player.draw_hand()



# TODO at game end, make sure to shuffle discard pile into deck before computing score