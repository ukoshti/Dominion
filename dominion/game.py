import random
import pandas as pd
import pickle

class Game:
    def __init__(self):
        self.allcards = Game.load_csv()
        self.decks = Game.load_decks()
        self.next_game()
        
    def _shelters(self, cards):
        return "Dark Ages" == [card["Set Name"] for card in cards][random.randrange(0, len(cards))]
        
    def _platcol(self, cards):
        return "Prosperity" == [card["Set Name"] for card in cards][random.randrange(0, len(cards))]
    
    def _card_to_str(self, card):
        return f'{card["Set Name"] + ":" :<11} {card["Card Name"]}'

    def _deck_stats(self):
        remaining_cards = len(self.decks['current'])
        used_cards = len(self.decks['used'])
        next_cards = len(self.decks['next'])
        total_cards = len(self.allcards)
        return f'Remaining Cards: {remaining_cards}\nTotal Cards: {total_cards}\nUsed Cards: {used_cards}\nNext Cards: {next_cards}'

    def __str__(self):
        cards_print = ""
        for card in self.cards:
            cards_print = cards_print + f"{self._card_to_str(card)}\n"
 
        if self.bane is not None:
            cards_print = cards_print + f"{self._card_to_str(self.bane)} (Bane)\n"

        return f"{cards_print}\nShelters: {self.has_shelters}\nPlatinums and Colonies: {self.has_platcol}\n\n{self._deck_stats()}"
    
    def pick(self, num_cards = 10):
        total_cards = len(self.decks['current'])
        if total_cards < num_cards:
            self.decks['next'] = self.decks['next'] + self.decks['used']
            self.decks['used'] = []
            self.decks['next'] = self.shuffle(self.decks['next'], num_cards - total_cards)
            game_cards = self.decks['current'] + self.decks['next'][-(num_cards - total_cards):]
            self.decks['current'] = self.decks['next'][:-(num_cards - total_cards)]
            self.decks['next'] = []
        else:
            self.decks['current'] = self.shuffle(self.decks['current'], num_cards)
            game_cards = self.decks['current'][-num_cards:]
            self.decks['current'] = self.decks['current'][:-num_cards]
        return game_cards

    def _bane(self, cards):
        bane = None
        for card in cards:
            if card['Card Name'] == 'Young Witch':
                twothree = [c for c in self.decks['current'] if c['Cost'] == 2 or c['Cost'] == 3]
                if twothree:
                    bane = twothree[random.randrange(0, len(twothree))]
                    self.decks['current'].remove(bane)
                else:
                    self.decks['next'] = self.decks['used']
                    self.decks['used'] = []
                    twothree = [c for c in self.decks['next'] if c['Cost'] == 2 or c['Cost'] == 3]
                    if twothree:
                        bane = twothree[random.randrange(0, len(twothree))]
                        self.decks['next'].remove(bane)
                break
        return bane

    def shuffle(self, cards, picks = 10):
        total_cards = len(cards)
        for i in range(picks):
            rng = random.randrange(0, total_cards-i)
            cards[rng], cards[total_cards-i-1] = cards[total_cards-i-1], cards[rng]
        return cards

    def next_game(self, num_cards = 10):
        self.cards = sorted(self.pick(), key = lambda x: (x["Set Name"], x["Card Name"]))
        self.bane = self._bane(self.cards)
        self.decks['used'] = self.decks['used'] + self.cards
        if self.bane:
            self.decks['used'].append(self.bane)
        Game.save_decks(self.decks)
        self.has_shelters = self._shelters(self.cards)
        self.has_platcol = self._platcol(self.cards)

    @staticmethod
    def load_decks():
        try:
            with open('../data/puppies.pkl', 'rb') as f:
                return pickle.load(f)
        except:
            return {
                'current': Game.load_csv(),
                'next': [],
                'used': []
            }

    @staticmethod
    def load_csv():
        df = pd.read_csv('../data/Owned Cards.csv')
        return df.to_dict("records")

    @staticmethod
    def save_decks(cards):
        with open('../data/puppies.pkl', 'wb') as f:
            pickle.dump(cards, f)
