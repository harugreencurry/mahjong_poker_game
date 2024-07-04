# 勝者を判定するプログラムです。
from itertools import combinations

#役満時の牌を5進数で管理
def hai_to_num(hai):
    temp_l = [str(hai.count(h)) for h in hai_sorted_list]
    return (int(''.join(temp_l),5))

#5進数から役満時の牌の個数に変換(サブ)
def sub_num_to_hai(hai_n):
    upper = hai_n >= 5 and sub_num_to_hai(hai_n // 5) or []
    return upper + [hai_n % 5]

#5進数から役満時の牌に変換
def num_to_hai(hai_n):
    yakuman_hai= []
    head = []
    n = hai_n
    hai_count_list = [0 for h in range(len(terminals_and_honors) - len(sub_num_to_hai(n)))] +  sub_num_to_hai(n)
    for i in range(len(hai_count_list)):
        if hai_count_list[i] == 2:
            head += [hai_sorted_list[i]]*2
            continue
        for _ in range(hai_count_list[i]):
            yakuman_hai.append(hai_sorted_list[i])
    yakuman_hai.reverse()
    head.reverse()
    yakuman_hai = yakuman_hai + head
    return yakuman_hai

#役満の辞書を追加(役の複合を考慮)
def make_yakuman_dict(yakuman_hai,yakuman,all_yakuman_dict):
    yakuman_num = yaku_sorted_list.index(yakuman)
    yakuman_hai_num = hai_to_num(yakuman_hai)
    if yakuman_hai_num not in all_yakuman_dict:
        all_yakuman_dict[yakuman_hai_num] =  yakuman_num
    else:      
        all_yakuman_dict[yakuman_hai_num] =  int("".join(sorted(list(str(all_yakuman_dict[yakuman_hai_num])+str(yakuman_num)), reverse=True)))

#四暗刻
def check_Four_concealed_Triplets(quads_list,concealed_triplets_list,pairs_list,all_yakuman_dict):
    concealed_triplets_num = len(concealed_triplets_list)
    if concealed_triplets_num < 4:
        pass
    else:
        for ct in combinations(concealed_triplets_list,4):
            ct_list = list(ct)
            temp_pairs_list = list(set(pairs_list) - set(ct_list))
            if len(temp_pairs_list) > 0:
                for p in temp_pairs_list:
                    yakuman_hai = ct_list * 3 + [p] * 2 + [t for t in ct_list if t in quads_list]
                    make_yakuman_dict(yakuman_hai,"四暗刻",all_yakuman_dict)
                    
    
#国士無双
def check_Thirteen_Orphans(singles_list,pairs_list,all_yakuman_dict):
    yakuman_hai = []
    if len(singles_list)==len(terminals_and_honors) and len(pairs_list)>=1:
        for p in pairs_list:
            yakuman_hai = terminals_and_honors.copy()+[p]
            make_yakuman_dict(yakuman_hai,"国士無双",all_yakuman_dict)

#大三元
def check_Big_Dragons(quads_list,triplets_list,pairs_list,all_yakuman_dict):
    if set(three_dragons) <= set(triplets_list):
        for t in list(set(triplets_list) - set(three_dragons)):
            temp_triplets_list = three_dragons + [t]
            temp_pairs_list = list(set(pairs_list) - set(three_dragons))
            temp_pairs_list.remove(t)
            if len(temp_pairs_list) > 0 and len(temp_triplets_list) > 0 :
                for p in temp_pairs_list:
                    yakuman_hai = temp_triplets_list * 3 + [p] * 2 + [t for t in temp_triplets_list if t in quads_list]
                    make_yakuman_dict(yakuman_hai,"大三元",all_yakuman_dict)   

#小四喜
def check_Little_Winds(quads_list,triplets_list,pairs_list,all_yakuman_dict):
    triplets_wind = list(set(triplets_list) & set(wind_hai))
    if len(triplets_wind)==3:
        pair_wind = list(set(wind_hai)-set(triplets_wind))
        remove_wind_triple_list =  list(set(triplets_list.copy()) - set(wind_hai))
        
        for r in remove_wind_triple_list:
            t_list = triplets_wind + [r]
            yakuman_hai = t_list * 3 + pair_wind * 2 + [t for t in t_list if t in quads_list]
            make_yakuman_dict(yakuman_hai,"小四喜",all_yakuman_dict)

#字一色
def check_All_Honors(quads_list,triplets_list,pairs_list,all_yakuman_dict):
    for target_honors_tuple in combinations(honors,5): 
        target_honors_list = list(target_honors_tuple)
        if set(target_honors_list) <= set(triplets_list + pairs_list):        
            for honor in target_honors_list:     
                temp_triplets_list = list(set(target_honors_list.copy()) & set(triplets_list.copy()) ) 
                if honor in temp_triplets_list:
                    temp_triplets_list.remove(honor)
                if len(temp_triplets_list) == 4:
                    yakuman_hai = temp_triplets_list * 3 + [honor] * 2 + [t for t in temp_triplets_list if t in quads_list]
                    make_yakuman_dict(yakuman_hai,"字一色",all_yakuman_dict)

#清老頭
def check_All_terminals(quads_list,triplets_list,pairs_list,all_yakuman_dict): 
    for target_terminals_tuple in combinations(terminals,5): 
        target_terminals_list = list(target_terminals_tuple)
        if set(target_terminals_list) <= set(triplets_list + pairs_list):        
            for terminal in target_terminals_list:      
                temp_triplets_list = list(set(target_terminals_list.copy()) & set(triplets_list.copy()) ) 
                if terminal in temp_triplets_list:
                    temp_triplets_list.remove(terminal)
                if len(temp_triplets_list) == 4:
                    yakuman_hai = temp_triplets_list * 3 + [terminal] * 2 + [t for t in temp_triplets_list if t in quads_list]
                    make_yakuman_dict(yakuman_hai,"清老頭",all_yakuman_dict)
        
#大四喜
def check_Big_Winds(quads_list,triplets_list,pairs_list,all_yakuman_dict):
    if set(wind_hai) <= set(triplets_list):
        for hai in list(set(pairs_list) - set(wind_hai)):
            temp_pairs_list = [hai]
            if len(temp_pairs_list) > 0:
                for p in temp_pairs_list:
                    yakuman_hai = wind_hai * 3 + [p] * 2 + [w for w in wind_hai if w in quads_list]
                    make_yakuman_dict(yakuman_hai,"大四喜",all_yakuman_dict)

#四槓子
def check_Four_Quads(quads_list,pairs_list,all_yakuman_dict):
    quads_num = len(quads_list)
    if quads_num < 4:
        pass
    else:
        for cq in combinations(quads_list,4):
            cq_list = list(cq)
            temp_pairs_list = list(set(pairs_list) - set(cq_list))
            if len(temp_pairs_list) > 0:
                for p in temp_pairs_list:
                    yakuman_hai = cq_list * 4 + [p] * 2
                    make_yakuman_dict(yakuman_hai,"四槓子",all_yakuman_dict)

#大七星
def check_Great_Seven_Stars(pairs_list,all_yakuman_dict):
    if set(honors) <= set(pairs_list):
        yakuman_hai = honors * 2
        make_yakuman_dict(yakuman_hai,"大七星",all_yakuman_dict)

#各桁の和
def sum_of_digits(n):
    return sum(map(int, str(n)))

#役満チェック
def check_all_yakuman(quads_list,concealed_triplets_list,triplets_list,pairs_list,singles_list,all_yakuman_dict):
    #役チェック
    check_Four_concealed_Triplets(quads_list,concealed_triplets_list,pairs_list,all_yakuman_dict)
    check_Thirteen_Orphans(singles_list,pairs_list,all_yakuman_dict)
    check_Big_Dragons(quads_list,triplets_list,pairs_list,all_yakuman_dict)
    check_Great_Seven_Stars(pairs_list,all_yakuman_dict)
    check_Little_Winds(quads_list,triplets_list,pairs_list,all_yakuman_dict)
    check_All_Honors(quads_list,triplets_list,pairs_list,all_yakuman_dict)
    check_All_terminals(quads_list,triplets_list,pairs_list,all_yakuman_dict)
    check_Big_Winds(quads_list,triplets_list,pairs_list,all_yakuman_dict)
    check_Four_Quads(quads_list, pairs_list,all_yakuman_dict)


#雀士の役満のリストを作成
def check_all_hands(tehai,community_hai): 
    #牌のリスト
    global charcters,circles,bamboos,three_ones,three_nines,terminals,wind_hai,three_dragons,honors,terminals_and_honors,all_yakuman_dict,yaku_sorted_list,hai_sorted_list
    yaku_sorted_list = ["役無し","国士無双","四暗刻","字一色","大三元","小四喜","大七星","清老頭","大四喜","四槓子"]
    terminals_and_honors = ['1_man','9_man', '1_pin', '9_pin','1_sou', '9_sou','east', 'south', 'west', 'north','white', 'green', 'red']
    hai_sorted_list = list(reversed(terminals_and_honors.copy()))
    terminals = terminals_and_honors[:6]
    honors = terminals_and_honors[6:]
    wind_hai = honors[:4]
    three_dragons = honors[4:]
    charcters = terminals[:2]
    circles = terminals[2:4]
    bamboos = terminals[4:]

    
    all_yakuman_dict = {}
    
    #雀士の牌の辞書(キーは牌、値はその牌の枚数、ただし、暗刻確認のため、枚数の数え方を特殊にしている)
    j_all_hai_counts = {hai:tehai.count(hai)*10 + community_hai.count(hai) for hai in terminals_and_honors}
    
    #暗刻の候補リスト
    concealed_triplets_list = [hai for hai,count in j_all_hai_counts.items() if (count > 10 and sum_of_digits(count) >= 3)]
    
    #雀士の牌の辞書をもとに戻す
    j_all_hai_counts = {hai:sum_of_digits(count) for hai,count in j_all_hai_counts.items()}
    #国士無双の候補リスト
    singles_list = [hai for hai,count in j_all_hai_counts.items() if count >= 1]
    
    #対子の候補リスト
    pairs_list = [hai for hai,count in j_all_hai_counts.items() if count >= 2]
    
    #刻子の候補リスト
    triplets_list = [hai for hai,count in j_all_hai_counts.items() if count >= 3]
    
    #槓子の候補リスト
    quads_list = [hai for hai,count in j_all_hai_counts.items() if count >= 4]
    
    check_all_yakuman(quads_list, concealed_triplets_list,triplets_list, pairs_list, singles_list, all_yakuman_dict)
    
    return all_yakuman_dict

def strong_hand(tehai,community_hai):
    h_dict = check_all_hands(tehai,community_hai)
    strongest_hand = [hai_to_num(tehai),0]
    if h_dict != {}:
        for hai_num,yakuman_num in h_dict.items():
            #役が一番強い手を優先
            if yakuman_num > strongest_hand[1]:
                strongest_hand = [hai_num,yakuman_num]
            elif yakuman_num == strongest_hand[1]:
                if hai_num > strongest_hand[0]:
                    strongest_hand = [hai_num,yakuman_num]
    return strongest_hand
 
    
def determine_winner(game):
    #順に雀士の名前、役満、役満を構成している牌の番号
    not_folder = game.not_folder + game.allin_janshis
    winners_info = [[""],-1,-1]
    for j in game.janshis:
        j_name = j.name
        j_tehai = j.tiles
        if j in not_folder:
            
            hai_num,yakuman_num = strong_hand(j_tehai,game.get_community_tiles())
            yakuman_list = [yaku_sorted_list[int(y)] for y in list(str(yakuman_num))]
            
            print(f"{j_name}の構成牌:  {','.join(num_to_hai(hai_num))}    役:{','.join(yakuman_list)}")
            if yakuman_num > winners_info[1] or (yakuman_num == winners_info[1] and hai_num > winners_info[2]):
                winners_info = [[j_name],yakuman_num,hai_num]
            elif yakuman_num == winners_info[1] and hai_num == winners_info[2]:
                winners_info[0].append(j_name)
        
    
    if winners_info[0] == [str(-1)]:
        return "全員がfoldしました"  
    elif len(winners_info[0]) == 1:
         return str(winners_info[0][0])+"の勝利"
    else:
        return ','.join(winners_info[0])+"の勝利"
    
    return winners_info[0]


    
