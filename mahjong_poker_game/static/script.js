function updateGame(data) {
    if(data.round==0){
        document.getElementById('round').innerText = "プリフロップ"
    }
    else if(data.round==1){
        document.getElementById('round').innerText = "フロップ"
    }
    else if(data.round==2){
        document.getElementById('round').innerText = "ターン"
    }
    else if(data.round==3){
        document.getElementById('round').innerText = "リバー"
    }
    else{
        document.getElementById('round').innerText = "ショーダウン"
    }
    document.getElementById('player-points').innerText = data.player_points;
    document.getElementById('current-bet').innerText = data.current_bet;
    document.getElementById('pot').innerText = data.pot;

    if (data.winner) {
        document.getElementById('winner').innerText = data.winner;
        clearInterval(gameStateInterval); // ゲーム状態のポーリングを停止
    } else {
        document.getElementById('winner').innerText = '';
    }
    updateCommunityTiles(data.community_tiles, data.round);
    updatePlayerTiles(data.player_tiles);
    updateButtons(data.current_bet, data.is_player);
}

function updateCommunityTiles(community_tiles, round) {
    const communityTilesDiv = document.getElementById('community-tiles');
    communityTilesDiv.innerHTML = ''; // Clear existing tiles

    const rows = Math.ceil((round * 7) / 7); // Number of rows to show based on the round
    for (let r = 0; r < rows; r++) {
        const rowDiv = document.createElement('div');
        rowDiv.classList.add('community-row');
        for (let i = 0; i < 7; i++) {
            const tileIndex = r * 7 + i;
            if (tileIndex < community_tiles.length) {
                const tile = community_tiles[tileIndex];
                const img = document.createElement('img');
                img.src = `/static/images/${tile}.png`;
                img.alt = tile;
                rowDiv.appendChild(img);
            }
        }
        communityTilesDiv.appendChild(rowDiv);
    }
}

function updatePlayerTiles(player_tiles) {
    const playerTilesDiv = document.getElementById('player-tiles');
    playerTilesDiv.innerHTML = ''; // Clear existing tiles

    player_tiles.forEach(tile => {
        const img = document.createElement('img');
        img.src = `/static/images/${tile}.png`;
        img.alt = tile;
        playerTilesDiv.appendChild(img);
    });
}

function updateButtons(currentBet, is_player) {
    const betButton = document.getElementById('bet-button');
    const checkButton = document.getElementById('check-button');
    const callButton = document.getElementById('call-button');
    const raiseButton = document.getElementById('raise-button');
    const foldButton = document.getElementById('fold-button');
    const allinButton = document.getElementById('allin-button');
    if (!is_player) {
        betButton.style.display = 'none';
        checkButton.style.display = 'none';
        callButton.style.display = 'none';
        raiseButton.style.display = 'none';
        foldButton.style.display = 'none';
        allinButton.style.display = 'none';
    } else if (currentBet === 0) {
        betButton.style.display = 'inline';
        checkButton.style.display = 'inline';
        callButton.style.display = 'none';
        raiseButton.style.display = 'none';
        foldButton.style.display = 'inline';
        allinButton.style.display = 'inline';
    } else {
        betButton.style.display = 'none';
        checkButton.style.display = 'none';
        callButton.style.display = 'inline';
        raiseButton.style.display = 'inline';
        foldButton.style.display = 'inline';
        allinButton.style.display = 'inline';
    }
}

function bettingAct(betting_action) {
    fetch('/betting_act', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ betting_action: betting_action })
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error:', error);
    });
}

let gameStateInterval;

function updateGameState() {
    fetch('/get_game_state')
        .then(response => response.json())
        .then(data => {
            updateGame(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// 定期的にゲーム状態を更新する
document.addEventListener('DOMContentLoaded', function() {
    updateGameState();  // ページ読み込み時に初期更新
    gameStateInterval = setInterval(updateGameState, 1000);  // 1秒ごとに更新

    document.getElementById('bet-button').addEventListener('click', function() {
        bettingAct('bet');
    });

    document.getElementById('check-button').addEventListener('click', function() {
        bettingAct('check');
    });

    document.getElementById('call-button').addEventListener('click', function() {
        bettingAct('call');
    });

    document.getElementById('raise-button').addEventListener('click', function() {
        bettingAct('raise');
    });

    document.getElementById('fold-button').addEventListener('click', function() {
        bettingAct('fold');
    });

    document.getElementById('allin-button').addEventListener('click', function() {
        bettingAct('allin');
    });
});

// 勝者データを定期的に取得して更新する
function pollWinnerData() {
    fetch('/get_winner_data')
        .then(response => {
            if (response.status === 204) {
                // No winner data yet, continue polling
                setTimeout(pollWinnerData, 1000);
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data) {
                updateGame(data);
                // Stop updating the game state once winner data is received
                clearInterval(gameStateInterval);
            }
        })
        .catch(error => console.error('Error fetching winner data:', error));
}

// ゲーム開始時やリロード時にポーリングを開始
window.onload = function() {
    pollWinnerData();
}
