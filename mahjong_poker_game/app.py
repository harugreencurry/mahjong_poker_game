from flask import Flask, render_template, jsonify, request
from threading import Thread, Event
from mahjong_poker import MahjongPokerGame
from ai import computer_decide
from determine_winner import determine_winner

app = Flask(__name__)

game = None
better = None
player_action = None
player_action_event = Event()  # プレイヤーのアクションのためのイベントを作成
game_winner_data = None  # 勝者データを保持するグローバル変数

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    ai_count = request.json['ai_count']
    game = MahjongPokerGame(ai_count)
    return jsonify({'success': True})

@app.route('/game')
def index():
    global game_progress_thread

    player_tiles = game.get_player_tiles()
    player_points = game.get_player_points()
    community_tiles = game.get_community_tiles()
    better = game.get_better()

    # index.htmlを表示
    rendered_template = render_template('index.html', player_tiles=player_tiles, player_points=player_points, current_bet=game.get_current_bet(), pot=game.get_pot(), community_tiles=community_tiles, round=game.get_round(), is_player=False if game.get_better() is None else game.get_better().is_human)

    # スレッドを作成してgame_progress()を実行
    game_progress_thread = Thread(target=game_progress)
    game_progress_thread.start()

    return rendered_template

@app.route('/get_game_state', methods=['GET'])
def get_game_state():
    return jsonify({
        'player_tiles': game.get_player_tiles(),
        'player_points': game.get_player_points(),
        'current_bet': game.get_current_bet(),
        'pot': game.get_pot(),
        'community_tiles': game.get_community_tiles(),
        'round': game.get_round(),
        'is_player': False if game.get_better() is None else game.get_better().is_human
    })

@app.route('/get_winner_data', methods=['GET'])
def get_winner_data():
    global game_winner_data
    if game_winner_data:
        return jsonify(game_winner_data)
    else:
        return jsonify({'status': 'No winner yet'}), 204

def game_progress():
    global game_winner_data
    print(game.get_player_tiles())
    with app.app_context():
        while not game.is_show_down(): 
            while not game.is_round_over() and not game.is_betting_over():
                better = game.get_better()
                better_bet(better)
        
        winner_data = determine_and_update_winner()
        game_winner_data = winner_data
        app.logger.debug(f"Winner data: {winner_data}")

def better_bet(better):
    global player_action
    if game.get_round() == 0 and game.get_pot() == 0:  # BB
        action = "bet"
    elif better.is_human:
        player_action_event.clear()  # 待機する前にイベントをクリア
        print("プレイヤーのアクションを待っています...")
        player_action_event.wait()  # handle_player_betによってイベントがセットされるのを待つ
        action = player_action
    else:
        action = computer_decide(better, game)
    print(game.get_janshi_name(better), action)
    game.bet_action(better, action)
    
    # player_actionをリセットして再利用を避ける
    player_action = None

    # 処理結果を返す
    player_points = game.get_player_points()
    current_bet = game.get_current_bet()
    pot = game.get_pot()
    community_tiles = game.get_community_tiles()
    round_num = game.get_round()
    is_player = False if game.get_better() is None else game.get_better().is_human
    return {
        'player_points': player_points,
        'current_bet': current_bet,
        'pot': pot,
        'community_tiles': community_tiles,
        'round': round_num,
        'is_player': is_player
    }

def determine_and_update_winner():
    winner = determine_winner(game)
    game_winner_data = {
        'player_points': game.get_player_points(),
        'current_bet': game.current_bet,
        'pot': game.pot,
        'winner': winner,
        'community_tiles': game.get_community_tiles(),
        'round': game.round
    }
    return game_winner_data

@app.route('/betting_act', methods=['POST'])
def handle_player_bet():
    global player_action
    data = request.get_json(force=True, silent=True)
    action = data.get('betting_action')
    player_action = action
    print(f"受け取ったアクション: {action}")
    player_action_event.set()  # better_betを解除するためにイベントをセット
    return jsonify({'action': action})

if __name__ == '__main__':
    app.run(debug=True)
