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
        secret_letter_counts = {}
        
        # Count occurrences of each letter in secret_word
        for letter in secret_word:
            secret_letter_counts[letter] = secret_letter_counts.get(letter, 0) + 1
        
        # First pass: mark all greens (correct position)
        for i in range(5):
            if guess[i] == secret_word[i]:
                current_values += "2"
                secret_letter_counts[guess[i]] -= 1
            else:
                current_values += "?"  # Placeholder
        
        # Second pass: mark yellows and grays
        result = ""
        for i in range(5):
            if current_values[i] == "2":
                result += "2"
            elif guess[i] in secret_letter_counts and secret_letter_counts[guess[i]] > 0:
                result += "1"
                secret_letter_counts[guess[i]] -= 1
            else:
                result += "0"
        
        return result

    
    




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
    
    def remove_words(word_list_recycle, guess_list, current_values):
        new_list = []
        
        for word in word_list_recycle:
            match = True
            
            for i in range(len(guess_list)):
                letter = guess_list[i]
                value = current_values[i]
                
                if value == '2':
                    if word[i] != letter:
                        match = False
                        break
                        
                elif value == '1':
                    if word[i] == letter or letter not in word:
                        match = False
                        break
                        
                elif value == '0':
                    has_green_or_yellow = any(
                        guess_list[j] == letter and current_values[j] in ['1', '2']
                        for j in range(len(current_values))
                    )
                    
                    if not has_green_or_yellow:
                        if letter in word:
                            match = False
                            break

            if match:
                new_list.append(word)
                    
        return new_list
    
    def calculate_position_frequencies():
        """Calculate letter frequency at each position from remaining words"""
        position_freq = [{} for _ in range(5)]
        
        for word in bot.word_list_recycle:
            for i, letter in enumerate(word):
                position_freq[i][letter] = position_freq[i].get(letter, 0) + 1
        
        return position_freq

    def score_word(word, position_freq):
        """Score a word based on position-specific letter frequencies"""
        score = 0
        seen = set()
        
        for i, letter in enumerate(word):
            # Add position-specific frequency
            score += position_freq[i].get(letter, 0)
            
            # Bonus for unique letters (avoid duplicates)
            if letter not in seen:
                score += 10  # Bonus for letter diversity
                seen.add(letter)
        
        return score
                
    def select_word(count, current_values):
        remaining_words = bot.remove_words(bot.word_list_recycle, bot.guess_list, current_values)
        bot.value_at_index.clear()
        bot.word_list_recycle = remaining_words
        
        if len(remaining_words) == 0:
            return "messed up"
        
        if len(remaining_words) == 1:
            return remaining_words[0]
        
        # Calculate position frequencies from remaining words
        position_freq = bot.calculate_position_frequencies()
        
        # Score all remaining words
        scored_words = []
        for word in remaining_words:
            score = bot.score_word(word, position_freq)
            scored_words.append((word, score))
        
        # Sort by score (highest first) and return best word
        scored_words.sort(key=lambda x: x[1], reverse=True)
        return scored_words[0][0]
    
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
            guess = "crane"
        if count > 1:
            guess = bot.select_word(count, current_values)
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