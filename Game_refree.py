#Game refree

from dataclasses import dataclass
import random

@dataclass
class GameState:
    round_number: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    max_rounds: int = 3

def validate_move(move: str, state: GameState, player: str):
    valid_moves = ["rock", "paper", "scissors", "bomb"]
    if move not in valid_moves:
        return False, "Invalid move. Round wasted."
    if move == "bomb":
        if player == "user" and state.user_bomb_used:
            return False, "Bomb already used. Round wasted."
        if player == "bot" and state.bot_bomb_used:
            return False, "Bot bomb already used."
    return True, "Valid"

def resolve_round(user_move: str, bot_move: str):
    if user_move == bot_move:
        return "draw"
    if user_move == "bomb" and bot_move != "bomb":
        return "user"
    if bot_move == "bomb" and user_move != "bomb":
        return "bot"
    rules = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    return "user" if rules[user_move] == bot_move else "bot"

def update_game_state(state: GameState, user_move: str, bot_move: str, winner: str):
    if user_move == "bomb":
        state.user_bomb_used = True
    if bot_move == "bomb":
        state.bot_bomb_used = True
    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1
    state.round_number += 1
    return state

def bot_choose_move(state: GameState):
    moves = ["rock", "paper", "scissors"]
    if not state.bot_bomb_used:
        moves.append("bomb")
    return random.choice(moves)

def run_game():
    state = GameState()
    print("Rock–Paper–Scissors–Plus")
    print("Best of 3 | Bomb usable once\n")
    while state.round_number <= state.max_rounds:
        print(f"\nRound {state.round_number}")
        user_move = input("Your move: ").strip().lower()
        valid, msg = validate_move(user_move, state, "user")
        if not valid:
            print(msg)
            state.round_number += 1
            continue
        bot_move = bot_choose_move(state)
        print(f"Bot move: {bot_move}")
        winner = resolve_round(user_move, bot_move)
        print("Result:", "Draw" if winner == "draw" else f"{winner.capitalize()} wins")
        state = update_game_state(state, user_move, bot_move, winner)
        print(f"Score → You: {state.user_score} | Bot: {state.bot_score}")
    print("\nGame Over")
    if state.user_score > state.bot_score:
        print("Final Result: YOU WIN")
    elif state.bot_score > state.user_score:
        print("Final Result: BOT WINS")
    else:
        print("Final Result: DRAW")

if __name__ == "__main__":
    run_game()