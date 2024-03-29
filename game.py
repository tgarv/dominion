#qpy:console
from random import shuffle, randint

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

class TreasureCard(Card):
  monetary_value = 0

class VictoryCard(Card):
  victory_points = 0

  def get_victory_points(self):
      return self.victory_points    

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
      self.shuffle(discard_pile)
      print 'shuffling'
      discard_pile = []

    if len(self.cards) < number:
      # Won't actually throw an error, but still weird so print a message
      print 'Trying to draw too many cards'

    return_value.extend(self.cards[:number])
    self.cards = self.cards[number:]
    return return_value, discard_pile
    
  def add_card(self, card):
    self.cards.append(card)

  def get_score(self):
    score = 0
    for card in self.cards:
      if isinstance(card, VictoryCard):
        score += card.get_victory_points()

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
    cards, discard = self.deck.draw(self.discard_pile, number)
    self.hand.extend(cards)
    self.discard_pile = discard
    
  def add_card(self, card):
    self.deck.add_card(card)

  def buy_card(self, card):
    self.discard_pile.append(card)
    
  # Puts the current hand into the discard pile and draws a new one
  def end_turn(self):
    self.discard_pile.extend(self.hand)
    self.hand = []
    self.draw_hand()

  # gets the score of the player's Deck plus discard pile plus hand
  def get_score(self):
    score_deck = Deck()
    score_deck.cards = self.deck.cards + self.discard_pile + self.hand
    return score_deck.get_score()

class Game():
  players = []
  cards = {}
  card_counts = {}
  trash = []
  current_turn = {}
  current_player_index = -1
  current_player = None
  state = 'active'

  def start_game(self, players):
    number_of_starting_estates = 3
    number_of_starting_coppers = 7
    self.players = players
    for player in self.players:
      for i in xrange(number_of_starting_estates):
        estate = self.cards['Estate'].pop()
        player.add_card(estate)
      for i in xrange(number_of_starting_coppers):
        copper = self.cards['Copper'].pop()
        player.add_card(copper)
      self.card_counts['Estate'] -= number_of_starting_estates
      self.card_counts['Copper'] -= number_of_starting_coppers
      player.deck.shuffle([])
      player.draw_hand()

    # Random starting player
    self.current_player_index = randint(0, len(self.players))
    self.initialize_turn()

  def initialize_turn(self):
    self.current_player_index += 1
    self.current_player_index %= len(self.players)
    self.current_turn = {'actions_left':1, 'buys_left':1, 'money': 0}
    self.current_player = self.players[self.current_player_index]
    print 'Starting new turn. Player ' + self.current_player.name + '\'s turn'
    print 'Current hand: ', self.current_player.hand
  
  def add_card(self, card_constructor, quantity = 10):
    cards = []
    card = card_constructor()
    for i in xrange(quantity):
      cards.append(card_constructor())
    self.card_counts[card.name] = quantity
    self.cards[card.name] = cards
  
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
        self.current_player.draw_cards(card.cards_to_draw)
        print 'current hand:', self.current_player.hand
      print self.current_turn

    elif isinstance(card, TreasureCard):
      self.current_turn['money'] += card.monetary_value
      print self.current_turn['money'], ' money'

  def buy_card(self, card):
    if self.current_turn['buys_left'] > 0:
      if self.current_turn['money'] >= card.cost:
        self.current_turn['buys_left'] -= 1
        print 'Buying ' , card
        self.cards[card.name].pop()   # This is where the copy of the card actually gets removed from the hand
        print len(self.cards[card.name])
        self.current_player.buy_card(card)
        self.card_counts[card.name] -= 1
        self.current_turn['money'] -= card.cost
      else:
        print 'not enough money'
    else:
      print 'No buys left this turn'
    print self.card_counts
        
  def end_turn(self):
    self.current_player.end_turn()

    
  # Return True if we should end the game
  def next_turn(self):
    self.end_turn()
    if self.is_game_over():
      print 'GAME OVER'
      self.state = 'ended'
    self.initialize_turn()
    
  def parse_input(self, input):
    print self.is_game_over()
    words = input.split()
    player = self.current_player
    if len(words) and words[0] == 'end':
      self.next_turn()
      
    if input == 'all money':
      for i in xrange(len(player.hand) - 1, -1, -1):
        card = player.hand[i]
        if isinstance(card, TreasureCard):
          self.play_card(card)
          del player.hand[i]
          player.discard_pile.append(card)

    if len(words) == 2:
      action, target = words
      if action == 'buy':
        cards = self.cards.get(target, [])
        if len(cards):
          card = cards[0]
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
          cards = self.cards.get(target)
          if len(cards):
            print cards[0].get_details()

  def get_winner(self):
    best_player = None
    best_score = 0
    for player in self.players:
      player_score = player.get_score()
      if player_score > best_score:
        print 'Player ' + player.name + 'has score ' + str(player_score)
        best_score = player_score
        best_player = player

    return best_player

# Treasure Cards
class CopperCard(TreasureCard):
  cost = 0
  name = 'Copper'
  monetary_value = 1

class SilverCard(TreasureCard):
  cost = 3
  name = 'Silver'
  monetary_value = 2

class GoldCard(TreasureCard):
  cost = 6
  name = 'Gold'
  monetary_value = 3

# Victory Cards
class EstateCard(VictoryCard):
  name = 'Estate'
  victory_points = 1
  cost = 2

class DuchyCard(VictoryCard):
  name = 'Duchy'
  victory_points = 3
  cost = 5

class ProvinceCard(VictoryCard):
  name = 'Province'
  victory_points = 6
  cost = 1

class GardensCard(VictoryCard):
  name = 'Gardens'
  victory_points = 0
  cost = 4

  def get_victory_points(self, deck):
    return len(deck.cards)/10

#action cards
class VillageCard(ActionCard):
  name = 'Village'
  cost = 3
  action_increases = 2
  cards_to_draw = 1

class MarketCard(ActionCard):
  name = 'Market'
  cost = 5
  action_increases = 1
  cards_to_draw = 1
  buy_increases = 1
  money_increases = 1

class WoodcutterCard(ActionCard):
  name = 'Woodcutter'
  cost = 3
  action_increases = 0
  cards_to_draw = 0
  buy_increases = 1
  money_increases = 2

# Instantiate money cards
copper = CopperCard()
silver = SilverCard()
gold = GoldCard()

# Instantiate victory cards
estate = EstateCard()
duchy = DuchyCard()
province = ProvinceCard()
garden = GardensCard()

# Instantiate action cards
village = VillageCard()
woodcutter = WoodcutterCard()
market = MarketCard()


# Set up a normal starting hand: 7 coppers and 3 estates
player = Player()
player.name = '1'
player2 = Player()
player2.name = '2'

# Set up the game, add players, add cards, and start the game
game = Game()
game.players.append(player)
game.players.append(player2)
game.add_card(EstateCard, 50)
game.add_card(DuchyCard, 15)
game.add_card(ProvinceCard, 1)
game.add_card(CopperCard, 50)
game.add_card(SilverCard, 50)
game.add_card(GoldCard, 50)
game.add_card(VillageCard, 10)
game.add_card(MarketCard, 10)
game.add_card(WoodcutterCard, 10)
game.start_game([player, player2])

while game.state != 'ended':
  game.parse_input(raw_input('Enter command\n'))

winner = game.get_winner()
print winner
# TODO at game end, make sure to shuffle discard pile into deck before computing score
