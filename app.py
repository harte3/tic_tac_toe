# app.py
from flask import Flask, render_template, request, jsonify
import math
import random
import time
app = Flask(__name__)

game_board = [' ']*9
player_turn = 'X'
# player_names = {'X': 'Player 1', 'O': 'Player 2'}  # Default player names
game_mode = 'Human vs Human'  # Default game mode
ai_difficulty = 'easy'  # Default AI difficulty


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_game_mode', methods=['POST'])
def set_game_mode():
    global game_mode, ai_difficulty
    game_mode = request.json['game_mode']
    if game_mode == 'Human vs AI':
        ai_difficulty = request.json.get('ai_difficulty', ai_difficulty)  # Set the AI difficulty here
    return jsonify({'status': 'OK'})

    return jsonify({'game_mode': game_mode})

@app.route('/set_ai_difficulty', methods=['POST'])
def set_ai_difficulty():
    global ai_difficulty
    ai_difficulty = request.json['ai_difficulty']
    return jsonify({'status': 'OK'})


def check_win():
    win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for condition in win_conditions:
        if game_board[condition[0]] == game_board[condition[1]] == game_board[condition[2]] != ' ':
            return str(game_board[condition[0]]) + ' wins!'
    if ' ' not in game_board:
        return 'Draw'
    return 'Continue'

@app.route('/human_move', methods=['POST'])
def make_move():
    global game_board, player_turn, game_mode, ai_difficulty
    if game_mode == 'Human vs Human':
        # if 'position' not in request.json:
        #     return jsonify({'status': 'ERROR', 'message': 'No position specified'})
        if game_board[int(request.get_json()['position']) ] != ' ':
            return jsonify({'status': 'ERROR', 'message': 'Position already taken'})

        position = int(request.get_json()['position'])  # Get the position of the move
        game_board[position] = player_turn # Make a move for the player
        human_won = check_win()
        if human_won != 'Continue':
            return jsonify({'status': 'OK', 'human_won': human_won})
        player_turn = 'O' if player_turn == 'X' else 'X' # Switch the turn to the other player (X or O)
        
        return jsonify({'status': 'OK', 'game_mode': game_mode, 'player_turn': player_turn})
    
    elif game_mode == 'Human vs AI' and player_turn == 'X':

        if game_board[int(request.get_json()['position']) ] != ' ':
            return jsonify({'status': 'ERROR', 'message': 'Position already taken'})
        
        position = int(request.get_json()['position'])  # Get the position of the move
        game_board[position] = player_turn # Make a move for the player
        human_won = check_win()
        if human_won != 'Continue':
            return jsonify({'status': 'OK', 'human_won': human_won})
        player_turn = 'O' if player_turn == 'X' else 'X' # Switch the turn to the other player (X or O)
    
    return jsonify({'status': 'OK'})  

@app.route('/ai_move', methods=['POST'])
def ai_move():
    global game_board, player_turn, game_mode, ai_difficulty
    if ai_difficulty == 'easy' and game_mode == 'Human vs AI' and player_turn == 'O':
        # Easy AI: choose a random empty position
        empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
        
        if empty_positions:
            computer_position = random.choice(empty_positions)
        
        game_board[computer_position] = player_turn
        player_turn = 'X' if player_turn == 'O' else 'O'
    
    elif ai_difficulty == 'medium' and game_mode == 'Human vs AI' and player_turn == 'O':
        # Hard AI: implement a more advanced strategy here
        human_moves = sum(1 for cell in game_board if cell == 'X')
        if human_moves < 2:
            # Choose a random move
            empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
            if 4 in empty_positions:
                computer_position = 4
            else:
                computer_position = random.choice(empty_positions)
        else:
            # Check win conditions and move accordingly
            win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            for condition in win_conditions:
                # Check if the computer can win the game
                if game_board[condition[0]] == game_board[condition[1]] == 'O' and game_board[condition[2]] == ' ':
                    computer_position = condition[2]
                    break
                elif game_board[condition[0]] == game_board[condition[2]] == 'O' and game_board[condition[1]] == ' ':
                    computer_position = condition[1]
                    break
                elif game_board[condition[1]] == game_board[condition[2]] == 'O' and game_board[condition[0]] == ' ':
                    computer_position = condition[0]
                    break
                # Check if the human can win the game
                elif game_board[condition[0]] == game_board[condition[1]] == 'X' and game_board[condition[2]] == ' ':
                    computer_position = condition[2]
                    break
                elif game_board[condition[0]] == game_board[condition[2]] == 'X' and game_board[condition[1]] == ' ':
                    computer_position = condition[1]
                    break
                elif game_board[condition[1]] == game_board[condition[2]] == 'X' and game_board[condition[0]] == ' ':
                    computer_position = condition[0]
                    break
            else:
                # If no win condition is found, choose a random move
                empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
                if empty_positions:
                    computer_position = random.choice(empty_positions)
        game_board[computer_position] = player_turn
        # check_win()
        player_turn = 'X' if player_turn == 'O' else 'O'

    elif ai_difficulty == 'hard' and game_mode == 'Human vs AI' and player_turn == 'O':
        # Hard AI: implement a more advanced strategy here
        human_moves = sum(1 for cell in game_board if cell == 'X')
        if human_moves < 2:
            # Choose a random move
            empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
            if 4 in empty_positions:
                computer_position = 4
            else:
                computer_position = random.choice([0, 2, 6, 8])
        else:
            # Check win conditions and move accordingly
            win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            for condition in win_conditions:
                # Check if the computer can win the game
                if game_board[condition[0]] == game_board[condition[1]] == 'O' and game_board[condition[2]] == ' ':
                    computer_position = condition[2]
                    break
                elif game_board[condition[0]] == game_board[condition[2]] == 'O' and game_board[condition[1]] == ' ':
                    computer_position = condition[1]
                    break
                elif game_board[condition[1]] == game_board[condition[2]] == 'O' and game_board[condition[0]] == ' ':
                    computer_position = condition[0]
                    break
                # Check if the human can win the game
                elif game_board[condition[0]] == game_board[condition[1]] == 'X' and game_board[condition[2]] == ' ':
                    computer_position = condition[2]
                    break
                elif game_board[condition[0]] == game_board[condition[2]] == 'X' and game_board[condition[1]] == ' ':
                    computer_position = condition[1]
                    break
                elif game_board[condition[1]] == game_board[condition[2]] == 'X' and game_board[condition[0]] == ' ':
                    computer_position = condition[0]
                    break
            else:
                # If no win condition is found, choose a random move
                empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
                if empty_positions:
                    computer_position = random.choice(empty_positions)
        game_board[computer_position] = player_turn
        # check_win()
        player_turn = 'X' if player_turn == 'O' else 'O'
    
    elif ai_difficulty == 'impossible' and game_mode == 'Human vs AI' and player_turn == 'O':
        # Impossible AI: implement the most advanced strategy here
        human_moves = sum(1 for cell in game_board if cell == 'X')
        if human_moves < 2:
            # Choose a random move
            empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
            if 4 in empty_positions:
                computer_position = 4
            else:
                computer_position = random.choice([0, 2, 6, 8])
        elif human_moves == 2:
            # Check win conditions and move accordingly
            win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            for condition in win_conditions:
                # Check if the human can win the game
                if game_board[condition[0]] == game_board[condition[1]] == 'X' and game_board[condition[2]] == ' ':
                    computer_position = condition[2]
                    break
                elif game_board[condition[0]] == game_board[condition[2]] == 'X' and game_board[condition[1]] == ' ':
                    computer_position = condition[1]
                    break
                elif game_board[condition[1]] == game_board[condition[2]] == 'X' and game_board[condition[0]] == ' ':
                    computer_position = condition[0]
                    break
                elif game_board[1] == game_board[3] == 'X' and game_board[0] == ' ':  # If the human starts in the middle, the computer should start in the corner
                    computer_position = 0
                    break   
                elif game_board[1] == game_board[5] == 'X' and game_board[2] == ' ':
                    computer_position = 2
                    break
                elif game_board[7] == game_board[3] == 'X' and game_board[6] == ' ':   
                    computer_position = 6
                    break
                elif game_board[7] == game_board[5] == 'X' and game_board[8] == ' ':    
                    computer_position = 8
                    break
                else:
                    # If no win condition is found, choose a random move
                    empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
                    if game_board[0] == 'O' or game_board[2] == 'O' or game_board[6] == 'O' or game_board[8] == 'O':
                        possible_positions = [pos for pos in [0, 2, 6, 8] if pos in empty_positions]
                        computer_position = random.choice(possible_positions)
                    else:
                        possible_positions = [pos for pos in [1, 3, 5, 7] if pos in empty_positions]
                        computer_position = random.choice(possible_positions)

        else:
            win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
            for condition in win_conditions:
                # Check if the computer can win the game
                if game_board[condition[0]] == game_board[condition[1]] == 'O' and game_board[condition[2]] == ' ':
                    computer_position = condition[2]
                    break
                elif game_board[condition[0]] == game_board[condition[2]] == 'O' and game_board[condition[1]] == ' ':
                    computer_position = condition[1]
                    break
                elif game_board[condition[1]] == game_board[condition[2]] == 'O' and game_board[condition[0]] == ' ':
                    computer_position = condition[0]
                    break
                # Check if the human can win the game
                elif game_board[condition[0]] == game_board[condition[1]] == 'X' and game_board[condition[2]] == ' ':
                    computer_position = condition[2]
                    break
                elif game_board[condition[0]] == game_board[condition[2]] == 'X' and game_board[condition[1]] == ' ':
                    computer_position = condition[1]
                    break
                elif game_board[condition[1]] == game_board[condition[2]] == 'X' and game_board[condition[0]] == ' ':
                    computer_position = condition[0]
                    break
            else:
                # If no win condition is found, choose a random move
                empty_positions = [i for i, cell in enumerate(game_board) if cell == ' ']
                if empty_positions:
                    computer_position = random.choice(empty_positions)
        game_board[computer_position] = player_turn
        # check_win()
        player_turn = 'X' if player_turn == 'O' else 'O'

    return jsonify({'status': 'OK'})  

@app.route('/reset', methods=['POST'])
def reset():
    global game_board, player_turn, game_mode, ai_difficulty
    game_board = [' ']*9
    player_turn = 'X'
    return jsonify({'status': 'OK'})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'board': game_board, 'turn': player_turn, 'status': check_win(), 'game_mode': game_mode})

if __name__ == '__main__':
    app.run(debug=True)