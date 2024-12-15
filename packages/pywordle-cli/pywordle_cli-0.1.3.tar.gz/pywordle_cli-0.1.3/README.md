# Wordle CLI Game

Play the classic Wordle game directly in your terminal! Guess the secret five letter word within six attempts!

[See how it looks like!](https://github.com/ousmanebarry/wordle-cli/blob/main/game-example.png)

## Features

- **Interactive Gameplay:** Receive immediate feedback on your guesses.
- **Colour Coded Hints:** Letters are highlighted to indicate correct positions and presence in the secret word.
  - Requires a terminal that supports coloured output.
- **Command Support:**
  - `/list`: Display the status of all letters.
  - `/grid`: View your current guesses and their evaluations.
  - `/end`: End the current wordle game.

---

## Installation

### Option 1: Install from PyPI (Recommended)

The easiest way to install and start playing is by using `pip`:

```bash
pip install pywordle-cli
```

Once installed, you can start the game by typing:

```bash
wordle
```

---

### Option 2: Install from Source

If you'd like to install the package yourself, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/ousmanebarry/wordle-cli.git
   cd wordle-cli
   ```

2. Install the package:

   ```bash
   pip install .
   ```

3. Start the game:

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

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ousmanebarry/wordle-cli/blob/main/LICENSE) file for details.

---

## Acknowledgements

Inspired by the original [Wordle](https://www.nytimes.com/games/wordle/index.html) game.

---

Enjoy the game and happy guessing! 🎉
