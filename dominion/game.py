import random
import pandas as pd
import pickle

class Game:
    def __init__(self):
        self.allcards = Game.load_csv()
        self.deck = Game.load_deck()
        self.next_game()
        
    def _shelters(self, cards):
        return "Dark Ages" == [card["Set Name"] for card in cards][random.randrange(0, len(cards))]
        
    def _platcol(self, cards):
        return "Prosperity" == [card["Set Name"] for card in cards][random.randrange(0, len(cards))]
    
    def _card_to_str(self, card):
        return f'{card["Set Name"] + ":" :<11} {card["Card Name"]}'

    def _deck_stats(self):
        remaining_cards = len(self.deck)
        total_cards = len(self.allcards)
        return f'Remaining Cards: {remaining_cards}\nTotal Cards: {total_cards}'

    def __str__(self):
        cards_print = ""
        for card in self.cards:
            cards_print = cards_print + f"{self._card_to_str(card)}\n"
 
        if self.bane is not None:
            cards_print = cards_print + f"{self._card_to_str(self.bane)} (Bane)\n"

        return f"{cards_print}\nShelters: {self.has_shelters}\nPlatinums and Colonies: {self.has_platcol}\n\n{self._deck_stats()}"
    
    def pick(self, num_cards = 10):
        total_cards = len(self.deck)
        if total_cards < num_cards:
            reload = self.allcards
            count = 1
            for card in self.deck:
                indx = reload.index(card)
                reload[indx], reload[len(reload)-count] = reload[len(reload)-count], reload[indx]
                count = count + 1
            self.deck = self.shuffle(reload[:-total_cards], num_cards - total_cards) + reload[-total_cards:]
        else:
            self.deck = self.shuffle(self.deck, num_cards)
        game_cards = self.deck[-num_cards:]
        self.deck = self.deck[:-num_cards]
        Game.to_pickle(self.deck)
        return game_cards

    def _bane(self, cards):
        bane = None
        allcards = self.allcards[:]
        for card in cards:
            allcards.remove(card)
        for card in cards:
            if card['Card Name'] == 'Young Witch':
                twothree = [c for c in allcards if c['Cost'] == 2 or c['Cost'] == 3]
                bane = twothree[random.randrange(0, len(twothree))]
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
        self.has_shelters = self._shelters(self.cards)
        self.has_platcol = self._platcol(self.cards)

    @staticmethod
    def load_deck():
        try:
            with open('../data/puppies.pkl', 'rb') as f:
                return pickle.load(f)
        except:
            return Game.load_csv()

    @staticmethod
    def load_csv():
        df = pd.read_csv('../data/Owned Cards.csv')
        return df.to_dict("records")

    @staticmethod
    def to_pickle(cards):
        with open('../data/puppies.pkl', 'wb') as f:
            pickle.dump(cards, f)
