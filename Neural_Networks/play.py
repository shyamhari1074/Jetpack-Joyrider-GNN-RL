"""
Inference script to run a trained neural network agent in the game.
Loads the best model from training and plays in a real environment.
"""

import pickle
import os
import sys
from typing import Optional

from game import AIGame
from neural_network import NeuralNetwork

# Configuration
MODEL_PATH = "best_model.pkl"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 675
FPS = 30
SCREEN_DELTA = 15
ZAPPER_COUNT = 2
COINS_COUNT = 5
GAME_DURATION_FRAMES = 5000  # Frames to play (roughly 166 seconds at 30 FPS)

# Rewards (same as training for consistency)
ALIVE_REWARD = 1
COIN_REWARD = 10
COMPLETE_REWARD = 500


def load_trained_model(model_path: str) -> Optional[NeuralNetwork]:
    """Load the trained neural network from pickle file.
    
    Args:
        model_path: Path to the pickle file containing the trained model
        
    Returns:
        NeuralNetwork object if found, None otherwise
    """
    if not os.path.exists(model_path):
        print(f"[ERROR] Model file '{model_path}' not found!")
        print("   Please train the model first by running: python main.py")
        return None
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"[SUCCESS] Successfully loaded trained model from: {model_path}")
        return model
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
        return None


def play_game(trained_ai: NeuralNetwork, num_runs: int = 1) -> list:
    """Play the game with a trained AI agent.
    
    Args:
        trained_ai: The trained NeuralNetwork to use
        num_runs: Number of times to run the game (for averaging performance)
        
    Returns:
        List of final scores from each run
    """
    scores = []
    
    for run in range(num_runs):
        print(f"\n{'='*50}")
        print(f"[RUN {run + 1}/{num_runs}]")
        print(f"{'='*50}")
        
        # Create game with only the trained AI
        game = AIGame(
            screen_width=WINDOW_WIDTH,
            screen_height=WINDOW_HEIGHT,
            fps=FPS,
            screen_delta=SCREEN_DELTA,
            ais=[trained_ai],
            zapper_spacing=WINDOW_WIDTH // ZAPPER_COUNT,
            coin_spacing=WINDOW_WIDTH // COINS_COUNT,
            alive_reward=ALIVE_REWARD,
            coin_reward=COIN_REWARD,
            complete_reward=COMPLETE_REWARD,
        )
        
        # Initialize game objects
        game.init_game_objects()
        
        # Play the game (set generation=-1 to indicate inference mode)
        game.play_game(length=GAME_DURATION_FRAMES, generation=-1, draw_vision=False)
        
        # Get the final score
        final_score = game.players[0].score
        scores.append(final_score)
        
        print(f"Final Score: {final_score}")
    
    return scores


def main():
    """Main function to run the trained agent in the game."""
    print("="*60)
    print("TRAINED AGENT INFERENCE - REAL ENVIRONMENT TEST")
    print("="*60)
    
    # Load the trained model
    trained_ai = load_trained_model(MODEL_PATH)
    if trained_ai is None:
        sys.exit(1)
    
    # Ask user how many runs they want
    try:
        num_runs = int(input("\nHow many times would you like to run the agent? (default: 1): ") or "1")
        num_runs = max(1, num_runs)  # Ensure at least 1
    except ValueError:
        num_runs = 1
    
    print(f"\n[INFO] Running trained agent {num_runs} time(s) in the real environment...")
    print(f"[INFO] Each run will play for {GAME_DURATION_FRAMES} frames (~{GAME_DURATION_FRAMES/FPS:.1f} seconds)")
    
    # Play the game(s)
    scores = play_game(trained_ai, num_runs)
    
    # Print summary
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    for i, score in enumerate(scores, 1):
        print(f"Run {i}: {score} points")
    
    if len(scores) > 1:
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        print(f"\nAverage Score: {avg_score:.1f}")
        print(f"Best Score: {max_score}")
        print(f"Worst Score: {min_score}")
    
    print("="*60)
    print("[COMPLETE] Inference completed successfully!")


if __name__ == "__main__":
    main()
