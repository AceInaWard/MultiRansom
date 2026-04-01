#imports
import random

# --- THE NEW FLASK "DASHBOARD" ---
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

THEMES_ALL = [
    "How to explain your browser history to your grandma",
    "A Yelp review for a public restroom",
    "Your wedding vows if you were a pirate",
    "How to quit your job via a skywriter",
    "The secret ingredient in your award-winning chili",
    "Giving a pep talk to a depressed hamster",
    "Describing your first date in three words",
    "A warning label for a mysterious unmarked bottle"
]

# Standard placeholders for before users join
PLAYER_NAMES = ["Guest_1", "Secret_Agent", "Word_Wizard"]

WORDS_ALL = [
    # Nouns
    "Grandpa", "toenail", "shrimp", "diaper", "lawyer", "moisture", "mayonnaise",
    "custody", "ferret", "shame", "glitter", "taco", "dignity", "sausage",

    # Verbs
    "lick", "explode", "weep", "accelerate", "smother", "forgive", "moisturize",
    "gallop", "evict", "marinate", "dance", "scrub",

    # Adjectives/Adverbs
    "greasy", "forbidden", "soggy", "suspicious", "aggressive", "shiny", "sticky",
    "accidentally", "violently", "tenderly", "crunchy",

    # Connectors
    "is", "the", "and", "my", "your", "with", "into", "because", "on", "not", "very"
]
INIT_WORDS = 75
START_PASS = "69lol"

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
        for _ in range(random.randrange(3,  8)):
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



class Game:
    def __init__(self):
        global START_PASS
        global PLAYER_NAMES
        players_names = PLAYER_NAMES
        self.players = [Player(n) for n in players_names]
        self.words_in_play = []
        self.themes_in_play = THEMES_ALL
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


    def round_start(self, first=False):
        # for player in game.players:
        #     print(f"{player.name} - hand is {player.hand}")
        if first:
            self.words_in_play = random.choices(WORDS_ALL, k=(len(self.players) * 150))
            self.deal_words(INIT_WORDS, "all")
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

    def add_player(self, name: str):
        if self.turn_index <= 0:
            PLAYER_NAMES.append(name)
            self.players.append(Player(name))
        else:
            print(f'game already started, aborting adding player function')

#   INITIALIZE ONCE GLOBALLY
my_game = Game()


@app.route('/status')
def status():
    return jsonify({
        "msg": "The game engine is running!",
        "player_count": len(my_game.players)
    })


@app.route('/joingame', methods=['POST'])
def joingame():
    from flask import request
    data = request.json
    name = data["name"]
    if name:
        my_game.add_player(name)
        return jsonify({"success": True, "msg": f"{name} joined the chaos"})
    else:
        return jsonify({"success": False, "error": "No name provided"}), 400

@app.route('/startgame', methods=['POST'])
def play():
    from flask import request
    data = request.json
    given_pass = data["pass"]
    if given_pass == START_PASS:
        my_game.round_start(True)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Wrong password"}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





#Game ------------



#Main --------


# if __name__ == '__main__':
#
#     game.deal_words(INIT_WORDS, "all")
#     game.round_start()


