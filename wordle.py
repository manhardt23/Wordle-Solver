import random

class game:
    def word_list():
        # method creates a list of all possible secret words from txt file
        fh = open("words.txt", "r")
        words = fh.readlines()
        fh.close()
        words = [line.strip("\n") for line in words]
        return words

    def get_Secret_Word(words):
        # method uses random method to choose the secret word
        secret_word = random.choice(words)
        return secret_word

    def letter_coloring(guess, secret_word):
        # method determines the value of each letter in the guessed word.
        current_values = ""
        used_letters = []
        for i in range(5):
            if guess[i] == secret_word[i]:
                current_values += "2"
                used_letters.append(guess[i])
            elif guess[i] in secret_word and guess[i] not in used_letters:
                    current_values += "1"
                    used_letters.append(guess[i])

            else:
                    current_values += "0"
    
        return current_values

    
    




class bot():
    word_list_recycle = []
    remaining_letters = {}
    value_at_index = {}
    guess_list = ""

    def set_word_list_recycled():
        bot.word_list_recycle = game.word_list()

    def set_value_at_index():
        bot.value_at_index = {2: [], 1: [], 0: []}

    def indexed_dict_starter():
        alphabet = list(map(chr, range(ord('a'), ord('z')+1)))
        for i in range(5):
            bot.remaining_letters.update({i : alphabet})
        return bot.remaining_letters
    
    def remove_words(word_list_recycle, guess_list, current_values, secret_word):
        new_list = []
        for word in word_list_recycle:
            match = True
            for i, (letter, value) in enumerate(zip(guess_list, current_values)):
                if  (value == '2' and word[i] != letter):
                    match = False
                    break
                elif(value == '1' and (word[i] == letter or letter not in word)):
                    match = False
                    break
                elif(value == '0' and letter in word):
                    match = False
                    break

            if (match) and (word not in new_list):
                new_list.append(word)
                
        return new_list
                
            
    def select_word(count, current_values, secret_word):
        remaining_words = bot.remove_words(bot.word_list_recycle, bot.guess_list, current_values, secret_word)
        #print(f"{bot.value_at_index}")
        #print(f"{remaining_words}")
        bot.value_at_index.clear()
        bot.word_list_recycle = remaining_words
        #if secret_word not in remaining_words:
            #print(False)
        if len(remaining_words) == 0:
            #print(f"fucked\n")
            return "messed up"
        return random.choice(remaining_words)

failed = 0
mess = 0
guessed = 0

def main():              
    words = game.word_list()
    secret_word = game.get_Secret_Word(words)
    count = 0
    
    while(True):
        count += 1
        if(count > 6):
            global failed 
            failed += 1
            break
        #print(f"Guess number {count} \n")
        if count == 1:
            bot.set_word_list_recycled()
            bot.indexed_dict_starter()
            guess = "louie"
        if count > 1:
            guess = bot.select_word(count, current_values, secret_word)
        #print(f"{guess}")
        if(guess not in words):
            global mess
            count -= 1
            mess += 1
            #print(f"the inputted word is not valid")
            break
        if(guess == secret_word):
            global guessed
            #print(f"You have Guessed the secret word {secret_word}")
            guessed += 1
            break
        bot.guess_list = guess
        current_values = game.letter_coloring(guess, secret_word)
        #print(f"{current_values}")
        

    #print(f"The secret word is {secret_word}")

if __name__ == "__main__":
    run = 100
    for i in range(run):
        #print(f'New Run')
        main()
        #print(f'run complete {i + 1}')
    print(f"\nWe won {guessed} we failed to guess correct {failed} time and we messed up in the code {mess} times\n")