from typing import Tuple, List
import pickle
import os

from game import AIGame
from game_objects.player import Player
from neural_network import NeuralNetwork, generate_offspring

import random
import numpy as np

ALIVE_REWARD = 1
AI_COUNT = 50
AI_VISION = False
COIN_REWARD = 10  # IMPROVED: Increased from 2 to incentivize coin collection
COINS_COUNT = 5
COMPLETE_REWARD = 500  # IMPROVED: Reduced from 1000 to avoid score capping
FPS = 30
GAME_FRAME_LENGTH = 2000  # IMPROVED: Increased from 1000 to allow more gameplay
NOISE_RATIO = 500
SCREEN_DELTA = 15
SEED = 1
TOTAL_GENERATIONS = 15
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 675
ZAPPER_COUNT = 2
MODEL_SAVE_PATH = "best_model.pkl"  # NEW: Path to save/load best model

if SEED:
    random.seed(SEED)
    np.random.seed(SEED)

def main():
    # NEW: Load the best pre-trained model if it exists
    if os.path.exists(MODEL_SAVE_PATH):
        print(f"Loading pre-trained model from {MODEL_SAVE_PATH}...")
        with open(MODEL_SAVE_PATH, 'rb') as f:
            best_ai = pickle.load(f)
        # Start with the best AI and create offspring
        initial_ais = [best_ai] + [generate_offspring(best_ai, best_ai, noise=NOISE_RATIO/500) for _ in range(AI_COUNT - 1)]
    else:
        # First run: Create random AIs
        print("No pre-trained model found. Starting with random AIs...")
        initial_ais = [NeuralNetwork() for _ in range(AI_COUNT)]
    
    # Creating the game
    game = AIGame(
        screen_width=WINDOW_WIDTH,
        screen_height=WINDOW_HEIGHT,
        fps=FPS,
        screen_delta=SCREEN_DELTA,
        ais=initial_ais,
        zapper_spacing=WINDOW_WIDTH // ZAPPER_COUNT,
        coin_spacing=WINDOW_WIDTH // COINS_COUNT,
        alive_reward=ALIVE_REWARD,
        coin_reward=COIN_REWARD,
        complete_reward=COMPLETE_REWARD,
    )

    best_score = 0  # NEW: Track the best score across all generations
    
    for generation in range(TOTAL_GENERATIONS):
        # Loaging / Reloading the game objects
        game.init_game_objects()
        # Playing the game
        game.play_game(length=GAME_FRAME_LENGTH, generation=generation, draw_vision=AI_VISION)
        # sorting the best players
        ai_players: List[Tuple[Player, NeuralNetwork]] = sorted(
            zip(game.players, game.ais), key=lambda player: -player[0].score
        )
        
        # NEW: Update best score and save model if improved
        current_best_score = ai_players[0][0].score
        if current_best_score > best_score:
            best_score = current_best_score
            print(f"New best score: {best_score}! Saving model...")
            with open(MODEL_SAVE_PATH, 'wb') as f:
                pickle.dump(ai_players[0][1], f)
        
        # creating the next generation of AIs
        game.ais = [
            generate_offspring(
                ai_players[0][1],
                ai_players[1][1],
                noise=NOISE_RATIO / ai_players[0][0].score,
            )
            for index in range(len(game.ais) - 4)
        ]
        # keeping the winning 2 ais, as well as adding in 2 random ones
        game.ais.append(ai_players[0][1])
        game.ais.append(ai_players[1][1])
        game.ais.append(NeuralNetwork())
        game.ais.append(NeuralNetwork())
        # showing the matrix for the winning AI
        print(f'''------------------------------------------
Winning AI's Stat
Score: {ai_players[0][0].score}
Best Score Ever: {best_score}
Gen: {generation}

Input Weights: {ai_players[0][1].input_layer_weights}
Input Biases: {ai_players[0][1].input_layer_biases}

Output Weights: {ai_players[0][1].output_layer_weights}
Output Weights: {ai_players[0][1].output_layer_biases}
------------------------------------------
''')

if __name__ == "__main__":
    main()