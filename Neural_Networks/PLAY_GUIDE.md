# 🎮 Running Your Trained Agent in the Real Environment

## Overview
After training your neural network agent using evolutionary algorithms in `main.py`, you can now test the best trained model in a real game environment using the **`play.py`** script.

## How It Works

### Training vs. Inference
- **`main.py`** (Training): Runs 50+ AIs simultaneously for multiple generations, evolves the population, saves the best model
- **`play.py`** (Inference): Loads the best trained model and plays it solo in the game environment

### What "Real Environment" Means
The real environment is the same game engine (`AIGame`), but with:
- ✅ Only ONE trained agent playing (not multiple)
- ✅ No evolution or training happening (just inference)
- ✅ Deterministic behavior (same agent runs consistently)
- ✅ Real-time visualization of the agent playing

## Usage

### Step 1: Train Your Model
```bash
python main.py
```
This will train for `TOTAL_GENERATIONS` (default: 15) and save the best model to `best_model.pkl`

### Step 2: Run the Trained Agent
```bash
python play.py
```

You'll be prompted:
```
How many times would you like to run the agent? (default: 1):
```

Enter a number to run multiple tests (useful for averaging performance across runs).

## What You'll See

1. **Real-time Game Visualization**: Watch your trained agent play the Jetpack Joyride game
2. **Live Stats Display**:
   - `Max Points`: Highest score in this run
   - `Generation: -1`: Indicates inference mode (not training)
   - `Alive: 1/1`: Shows your single agent status

3. **Results Summary** after each run:
   ```
   Run 1: 2543 points
   Average Score: 2543.0
   ```

## Configuration

Edit `play.py` to customize:

```python
GAME_DURATION_FRAMES = 5000  # How long the agent plays (frames)
WINDOW_WIDTH = 1200          # Screen dimensions
WINDOW_HEIGHT = 675
FPS = 30                     # Frames per second
```

## Comparing Performance

### Single Run
```bash
python play.py
# Input: 1
```

### Multiple Runs (Average Performance)
```bash
python play.py
# Input: 5
```
This runs the agent 5 times and shows average, best, and worst scores—useful for evaluating consistency.

## Troubleshooting

**Error: Model file 'best_model.pkl' not found**
- Make sure you've trained the model first: `python main.py`
- Check the file exists in your project directory

**Agent plays poorly**
- The model may need more training generations
- Increase `TOTAL_GENERATIONS` in `main.py`
- Or try improving reward values for better incentive alignment

**Low FPS/Slow Performance**
- Reduce `FPS` value in `play.py`
- Or reduce `GAME_DURATION_FRAMES` for shorter test runs

## Next Steps

1. **Analyze Agent Behavior**: Watch what decisions it makes, coin collection patterns, etc.
2. **Compare Runs**: Run it multiple times to see if it's consistent
3. **Fine-tune Training**: Adjust hyperparameters in `main.py` if performance is unsatisfactory
4. **Visualize Vision**: Set `draw_vision=True` in play.py to see what the agent "sees"

---

**Note**: The game window has an X button—click it to close the game and stop play.py.
