import random

PLAYER_TILES_NUM = 7
COMMUNITY_TILES_NUM = 21
BET_TEMBO = 100


class Janshi:
    def __init__(self,is_human,name):
        self.reset(is_human,name)
    
    def reset(self,is_human,name):
        self.points = 30000
        self.round_bet = 0
        self.tiles = []
        self.is_human = is_human
        self.name = name
    
    
class MahjongPokerGame:
    def __init__(self, ai_count,human_count=1):#プレイヤーは一人でいったん限定
        self.reset(ai_count,human_count)

    def reset(self, ai_count,human_count):
        self.human_count = human_count
        self.ai_count = ai_count
        self.current_bet = 0
        self.janshis = [Janshi(num < human_count, "雀士1" if num < human_count else "コンピュータ"+str(num)) for num in range(self.human_count + self.ai_count)]
        self.player = self.janshis[0]#仮
        self.pot = 0
        self.deck = self.create_deck()
        self.deal_tiles()
        self.round = -1
        self.community_tiles = [self.deck.pop() for _ in range(COMMUNITY_TILES_NUM)]
        self.not_folder = self.janshis.copy()
        random.shuffle(self.not_folder)
        self.allin_janshis = []
        self.better = self.not_folder[0]
        self.start_round(False)
        
        
    def start_round(self,is_betting_over):
        self.had_bet_janshis = []
        self.current_bet = 0
        for j in self.janshis:
            j.round_bet = 0
        self.pre_action = ""
        self.round += 1
        self.better = None if is_betting_over or self.is_show_down() else self.not_folder[0]
        

    def create_deck(self):
        suits = ['man', 'pin', 'sou']
        honors = ['east', 'south', 'west', 'north', 'white', 'green', 'red']
        deck = [f"{i}_{suit}" for suit in suits for i in range(1, 10, 8)] * 4
        deck += honors * 4
        random.shuffle(deck)
        return deck

    def deal_tiles(self):
        for j in self.janshis:
            j.tiles =  [self.deck.pop() for _ in range(PLAYER_TILES_NUM)]

    def get_player_tiles(self):
        return self.player.tiles
    
    def get_player_points(self):
        return self.player.points
    
    def get_janshi_name(self,janshi):
        return janshi.name

    def get_ai_tiles(self):
        return self.ai_tiles
    
    def get_current_bet(self):
        return self.current_bet 

    def get_pot(self):
        return self.pot 
    
    def get_round(self):
        return self.round

    def get_community_tiles(self):
        num_tiles = self.round * 7 if self.round < 4 else COMMUNITY_TILES_NUM
        return self.community_tiles[:num_tiles]
    
    def get_not_folder(self):
        if self.is_show_down():
            self.not_folder += self.allin_janshis
        return self.not_folder
    
    def get_better(self):
        return self.better
    
    def is_round_over(self):
        if len(self.had_bet_janshis) == len(self.not_folder)+len(self.allin_janshis):
            self.start_round(False)
            return True
        else:
            return False
    
    def is_betting_over(self):
        if len(self.not_folder) == 0 or (len(self.not_folder)==1 and self.not_folder[0].round_bet == self.current_bet):
            self.start_round(True)
            return True
        else:
            return False

    def is_show_down(self):
        return self.round >= 4
    
    


    def bet_action(self,janshi,action):
        copy_not_folder = self.not_folder.copy()
        if action == 'fold':
            self.not_folder.remove(janshi)
        elif action == 'allin':
            self.pot += janshi.points
            if self.current_bet < janshi.points:
                self.current_bet = janshi.points
                self.not_folder.remove(janshi)
                self.had_bet_janshis = []
            janshi.points = 0
            self.allin_janshis.append(janshi)

        
        elif action == 'bet':
            janshi.points -= BET_TEMBO
            self.pot += BET_TEMBO
            self.current_bet = BET_TEMBO
            janshi.round_bet = BET_TEMBO
            self.had_bet_janshis = [janshi]
        
        elif action == 'check':
            self.had_bet_janshis.append(janshi) 
        
        elif action == 'call':
            janshi.points -= (self.current_bet - janshi.round_bet)
            self.pot += (self.current_bet - janshi.round_bet)
            self.round_bet = self.current_bet
            self.had_bet_janshis.append(janshi)  
        
        elif action == 'raise':
            raise_amount = self.current_bet * 2
            janshi.points -= (raise_amount-janshi.round_bet)
            self.pot += (raise_amount-janshi.round_bet)
            self.current_bet = raise_amount
            self.had_bet_janshis = [janshi]
            
        
        self.pre_action = action
        if self.better == copy_not_folder[-1]:
            self.better = copy_not_folder[0]
        else:
            self.better = copy_not_folder[copy_not_folder.index(janshi)+1]

                  
        
        
    