import importlib.resources
import random, json, string
from colorama import Fore

WORD_LEN = 5
TRIES_LEN = 6

class Letter:
  def __init__(self, letter: str, state: str):
    self.letter = letter
    self.state = state

class Wordle:
  def __init__(self, dictionary: set) -> None:
    list_dictionary = list(dictionary)
    uppercase_letters = set(string.ascii_uppercase)
    random_secret_word = random.choice(list_dictionary)
    
    self.tries : list[list[Letter]] = []
    self.word_found = False
    self.letters_green = set()
    self.letters_eliminated = set()
    self.end_game = False
    self.letters_unused = uppercase_letters
    self.dictionary = dictionary
    self.secret_word = random_secret_word
    self.commands = ["/LIST", "/GRID", "/END"]

  def run_command(self, command: str) -> None:
    if command == "/LIST":
      build_str = ""

      for letter in self.letters_eliminated:
        build_str += (Fore.RED + f"{letter} {Fore.RESET}")
      
      for letter in self.letters_green:
        build_str += (Fore.GREEN + f"{letter} {Fore.RESET}")

      for letter in (self.letters_unused - self.letters_green):
        build_str += (Fore.WHITE + f"{letter} {Fore.RESET}")
      
      print(f"\n{build_str}\n")

    if command == "/GRID":
      print(self)

    if command == "/END":
      self.end_game = True

  def guess(self, word: str) -> None:
    dictionary = self.dictionary
    secret_word = self.secret_word
    word = word.upper()

    if word in self.commands:
      self.run_command(word)
      return

    if len(word) != WORD_LEN:
      print(Fore.RED + f"\nINVALID WORD!\nTOO LONG OR SHORT!\n{Fore.RESET}")
      return
    
    if word not in dictionary:
      print(Fore.RED + f"\nINVALID WORD!\nNOT IN DICTIONARY!\n{Fore.RESET}")
      return

    word_state = self.check_word(word)
    self.tries.append(word_state)
    print(self)

    if word == secret_word:
      print(Fore.GREEN + f"YOU HAVE FOUND THE WORD!{Fore.RESET}")
      self.word_found = True

  def check_word(self, word: str) -> list[Letter]:
    word_state = [''] * len(word)
    secret_word = self.secret_word
    secret_word_list = list(secret_word)

    for i in range(len(word)):
      if word[i] == secret_word[i]:
        word_state[i] = Letter(word[i], "GREEN")
        secret_word_list[i] = None
        self.letters_green.add(word[i])

    for i in range(len(word)):
      if word_state[i] == '':
        if word[i] in secret_word_list:
          word_state[i] = Letter(word[i], "YELLOW")
          secret_word_list[secret_word_list.index(word[i])] = None

    for i in range(len(word)):
      if word_state[i] == '':
        word_state[i] = Letter(word[i], "RED")
        self.letters_eliminated.add(word[i])
        if word[i] in self.letters_unused:
          self.letters_unused.remove(word[i])

    return word_state
    
  def __str__(self) -> str:
    build_str = "\n"

    for trie in self.tries:
      for letter in trie:
        if letter.state == "GREEN":
          build_str += (Fore.GREEN + f"{letter.letter} {Fore.RESET}")
        if letter.state == "YELLOW":
          build_str += (Fore.YELLOW + f"{letter.letter} {Fore.RESET}")
        if letter.state == "RED":
          build_str += (Fore.RED + f"{letter.letter} {Fore.RESET}")

      build_str += "\n"
    
    return build_str

def main():
  with importlib.resources.open_text('wordle.data', 'dictionary.json') as file:
    data = json.load(file)

  word_dictionary = set(data)
  wordle = Wordle(word_dictionary)

  while not wordle.word_found and len(wordle.tries) != TRIES_LEN:
    if wordle.end_game:
      print(Fore.RED + f"\nTHE GAME HAS ENDED!{Fore.RESET}")
      break

    tries_remaining = TRIES_LEN - len(wordle.tries)
    word = input(f"Guess a 5 letter word ({tries_remaining} tries left): ") 
    wordle.guess(word)
  
  tries_left = TRIES_LEN - len(wordle.tries)

  if tries_left == 0 and not wordle.word_found:
    print(Fore.RED + f"YOU RAN OUT OF TRIES!{Fore.RESET}")
  
  print(Fore.WHITE + f"THE SECRET WORD IS : {wordle.secret_word}!{Fore.RESET}")

if __name__=="__main__":
  main()