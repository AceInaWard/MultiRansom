#imports
import random
THEMES_ALL = ["dark", "light", "not those", "another one", "gang gang", "no cap"]
PLAYER_NAMES = ["Johnny Test", "Emily", "Andrew"]
WORDS_ALL = ["weed", "acid", "tacobell", "Cono de Coballo"]
INIT_WORDS = 15

PLAYER_MAP = {}


def init_pname_map(name: str, instance: Player):
    PLAYER_MAP[name] = instance

#Player ---------

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.won_themes = []
        self.presenting = None
        init_pname_map(name, self)

    def draw_words(self, words: list):
        self.hand.extend(words)

    def won_theme(self, theme: str):
        self.won_themes.append(theme)

    def start_presenting(self):
        placeholder_present = []
        used_words = []
        for _ in range(random.randrange(2,  4)):
            ph_instance = random.choice(self.hand)
            self.hand.remove(ph_instance)
            placeholder_present.append(ph_instance)
            used_words.append(ph_instance)
        self.presenting = Presentment(placeholder_present, self)




#Presentment ------

class Presentment:
    def __init__(self, sentence: list, presenter: Player):
        self.sentence = sentence
        self.creator = presenter
        #bribe powerup type thing?????


#Game ------------

class Game:
    def __init__(self):
        global PLAYER_NAMES
        players_names = PLAYER_NAMES
        self.players = [Player(n) for n in players_names]
        self.themes_in_play = THEMES_ALL
        self.words_in_play = random.choices(WORDS_ALL , k=(len(self.players) * 150))
        self.players_in_play = []
        self.turn_index = 0
        self.current_judge = ""
        self.current_theme = ""
        self.judgement_presents = []
        self.used_words = []



    def deal_words(self, words: int, target: str):
        if target == "all":
            for p in self.players:
                p.draw_words(self.get_words(words))
            return
        for p in self.players:
            if target == p.name:
                p.draw_words(self.get_words(words))
                return
        print('this should not happen')
        return

    def get_words(self, num: int):  # add weighted system later
        words = []
        if len(self.words_in_play) >= num:
            for i in range(num):
                word = self.words_in_play.pop()
                words.append(word)
            return words
        else:
            print('this should not happen')
            return words

    def judge_prepare_start(self):
        self.players_in_play = list(PLAYER_NAMES)
        self.players_in_play.remove(self.current_judge)
        self.judgement_presents = []
        for p in self.players_in_play:
            PLAYER_MAP[p].start_presenting()


    def judge_prepare_end(self):
        pass

    def judgment_start(self):
        self.judgement_presents = []
        for p in self.players_in_play:
            self.judgement_presents.append(PLAYER_MAP[p].presenting)
            print(f"{PLAYER_MAP[p].presenting.sentence} -- Presented For -- {self.current_theme}")
        print(f"Judgment Is Now Underway")

    def judgment_call(self):
        placeholder_decision = random.choice(self.judgement_presents)
        print(f"{placeholder_decision.sentence} Is This Rounds Winner! Presented By {placeholder_decision.creator.name}")
        winner_player = placeholder_decision.creator
        winner_player.won_theme(self.current_theme)
        for p in self.players:
            print(f"{p.name} -- {len(p.won_themes)}")
        print(f"Beginning Round {self.turn_index + 1}!")
        self.round_start()


    def collect_used(self, words: list):
        self.used_words.append(words)


    def round_start(self):
        # for player in game.players:
        #     print(f"{player.name} - hand is {player.hand}")
        self.turn_index += 1
        judge = random.choice(self.players)
        self.current_judge = judge.name
        print(f"{judge.name} Is This Rounds Judge!")
        random.shuffle(self.themes_in_play)
        round_theme = self.themes_in_play.pop()
        self.current_theme = round_theme
        print(f"'{self.current_theme}'  Is This Rounds Theme!")
        # start countdown
        self.judge_prepare_start()
        self.judge_prepare_end()
        self.judgment_start()
        self.judgment_call()

#Main --------


if __name__ == '__main__':
    game = Game()
    game.deal_words(INIT_WORDS, "all")
    game.round_start()




