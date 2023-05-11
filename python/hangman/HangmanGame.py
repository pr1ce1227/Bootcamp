import Hangman

game_running = True 
game_won = False
print("Welcome to hangman") 
key_Word = input("Player 1 enter a word \n")
char_guess = []
lives = 5

while(game_running):

    for i in key_Word: 
        if i in char_guess:
            print(i, end="",)
        else:
            print('_', end="") 
    char_guess.append(input("\n \n Enter your guess ply2: \n"))
    print()
    if char_guess[-1] not in key_Word:
        lives = lives - 1
        print("Bad guess: -1 life")
        print(lives, "Remaining \n")
    game_won = True
    for i in key_Word: 
        if i not in char_guess:
            game_won = False 
    if game_won:
        print("You won!!!!!!!!!")
        game_running = False
    if lives == 0: 
        print("You lost...........")
        game_running = False
    


