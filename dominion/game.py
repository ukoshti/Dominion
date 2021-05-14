import random
import pandas as pd
import pickle

class Game:
    def __init__(self):
        self.cards = sorted(self.pick(), key = lambda x: (x["Set Name"], x["Card Name"]))
        self.has_shelters = self._shelters(self.cards)
        self.has_platcol = self._platcol(self.cards)
        
    def _shelters(self, cards):
        return "Dark Ages" == [card["Set Name"] for card in cards][random.randrange(0, len(cards))]
        
    def _platcol(self, cards):
        return "Prosperity" == [card["Set Name"] for card in cards][random.randrange(0, len(cards))]
    
    def _card_to_str(self, card):
        return f'{card["Set Name"] + ":" :<11} {card["Card Name"]}'

    def _deck_stats(self):
        remaining_cards = len(self.load_pickle())
        total_cards = len(self.reload_csv())
        return f'Remaining Cards: {remaining_cards}\nTotal Cards: {total_cards}'

    def __str__(self):
        cards_print = ""
        for card in self.cards:
            cards_print = cards_print + f"{self._card_to_str(card)}\n"
        return f"{cards_print}\nShelters: {self.has_shelters}\nPlatinums and Colonies: {self.has_platcol}\n\n{self._deck_stats()}"
    
    def pick(self, num_cards = 10): 
        available = self.load_pickle()
        total_cards = len(available)
        if total_cards < num_cards:
            reload = self.reload_csv()
            count = 1
            for card in available:
                indx = reload.index(card)
                reload[indx], reload[len(reload)-count] = reload[len(reload)-count], reload[indx]
                count = count + 1
            available = self.shuffle(reload[:-total_cards], num_cards - total_cards) + reload[-total_cards:]
        else:
            available = self.shuffle(available, num_cards)
        self.to_pickle(available[:-num_cards])
        return available[-num_cards:]

    def shuffle(self, cards, picks = 10):
        total_cards = len(cards)
        for i in range(picks):
            rng = random.randrange(0, total_cards-i)
            cards[rng], cards[total_cards-i-1] = cards[total_cards-i-1], cards[rng]
        return cards

    def load_pickle(self):
        try:
            with open('../data/puppies.pkl', 'rb') as f:
                return pickle.load(f)
        except:
            return self.reload_csv()

    def reload_csv(self):
        df = pd.read_csv('../data/Owned Cards.csv')
        return df.to_dict("records")

    def to_pickle(self, cards):
        with open('../data/puppies.pkl', 'wb') as f:
            pickle.dump(cards, f)

