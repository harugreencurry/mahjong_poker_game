from determine_winner import strong_hand
import random

MAX_COMMUNITY_HAI_NUM = 21
JANSHI_HAI_NUM = 7


def simulate_holdem(tehai, community_hai,pot,bet_amount,com_round_bet, num_opponents,com_points, num_trials=5000):
    hai_list = ['1_man','9_man', '1_pin', '9_pin','1_sou', '9_sou','east', 'south', 'west', 'north','white', 'green', 'red']
    def trial():
        deck = []
        for hai in hai_list:
            deck += [hai for _ in range(4 - tehai.count(hai) - community_hai.count(hai))] 
        random.shuffle(deck)
        temp_commutnity_hai = community_hai + deck[:MAX_COMMUNITY_HAI_NUM - len(community_hai)]
        my_best_hand = strong_hand(tehai,temp_commutnity_hai)
        opponent_hands = [deck[i:i+JANSHI_HAI_NUM] for i in range(MAX_COMMUNITY_HAI_NUM - len(community_hai), MAX_COMMUNITY_HAI_NUM - len(community_hai) + JANSHI_HAI_NUM * num_opponents, JANSHI_HAI_NUM)]
        opponent_best_hands = [strong_hand(opponent_hand,temp_commutnity_hai) for opponent_hand in opponent_hands]
        num_better_hands = sum(1 for opponent_best_hand in opponent_best_hands if opponent_best_hand > my_best_hand)
        return num_better_hands == 0
    
    num_wins = sum(1 for _ in range(num_trials) if trial())
    odds = num_wins / num_trials
    # コンピュータの確率表示
    print(str(odds * 100) + "%")
    if odds != 1:
        desired_bet = int(odds * pot / (1 - odds)) - com_round_bet
    else:
        desired_bet = com_points
    #下二桁切り捨て
    return desired_bet//100 * 100


    
# 希望追加bet額と場の状況からコンピュータの意思決定を行う関数
def computer_decide(better,game):
    desired_bet = simulate_holdem(better.tiles, game.get_community_tiles(),game.get_pot(),game.current_bet,better.round_bet, len(game.not_folder)-1,better.points)
    
    # 最初のbetの場合
    if game.pre_action == "" or game.pre_action == "check":
        if desired_bet < game.get_pot() / len(game.not_folder):
            behavior = "check"
        elif desired_bet >= game.get_pot() / len(game.not_folder) and desired_bet < better.points:
            behavior = "bet"
        # 希望追加bet額が所持チップよりも大きい場合
        else:
            behavior = "allin"

    #最初のbet以外
    else:
        if desired_bet < game.current_bet - better.round_bet:
            behavior = "fold"
        elif desired_bet >= game.current_bet - better.round_bet and desired_bet <= game.current_bet:
            behavior = "call"
        elif desired_bet > game.current_bet and desired_bet < better.points:
            behavior = "raise"
        # 希望bet額が所持チップよりも大きい場合
        else:
            behavior = "allin"

    return behavior

