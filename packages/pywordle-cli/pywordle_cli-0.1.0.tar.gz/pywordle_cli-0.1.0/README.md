# Wordle CLI Game

Play the classic Wordle game directly in your terminal! Guess the secret five letter word within six attempts!

![See how it looks like!](./game-example.png)

## Features

- **Interactive Gameplay:** Receive immediate feedback on your guesses.
- **Colour Coded Hints:** Letters are highlighted to indicate correct positions and presence in the secret word.
  - Requires a terminal that supports coloured output.
- **Command Support:**
  - `/list`: Display the status of all letters.
  - `/grid`: View your current guesses and their evaluations.
  - `/end`: End the current wordle game.

---

## Installation and Usage

### Step 1: Clone the Repository

First, clone the repository and navigate to the project directory:

```bash
git clone https://github.com/ousmanebarry/wordle-cli.git
cd wordle-cli
```

### Step 2: How to Run the Game

1. Install the package:
   ```bash
   pip install .
   ```
2. Start the game using the `wordle` command:
   ```bash
   wordle
   ```

---

## How to Play

1. **Gameplay Instructions:**

   - **Guessing:** Enter a valid five letter word and press Enter.
   - **Feedback:**
     - **Green:** Correct letter in the correct position.
     - **Yellow:** Correct letter in the wrong position.
     - **Red:** Letter not in the secret word.

2. **Commands:**

   - **`/list`:** Display the status of all letters.
   - **`/grid`:** View your current guesses and their evaluations.
   - **`/end`:** End the current wordle game.

3. **Winning the Game:**
   - Guess the secret word within six attempts to win.
   - If you fail to guess correctly after six tries, the secret word will be revealed.

---

## Dependencies

- **Python 3.7 or higher**
- **colorama:** For colored terminal text.
- A terminal that supports ANSI color codes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Acknowledgements

Inspired by the original [Wordle](https://www.nytimes.com/games/wordle/index.html) game.

---

Enjoy the game and happy guessing! 🎉
