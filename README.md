# Wordle Solver Bot

An automated Wordle puzzle solver that uses constraint satisfaction algorithms to eliminate impossible words and solve puzzles efficiently and systematically.

## Overview

This bot plays Wordle by processing color-coded feedback and filtering a dictionary of 12,972 five-letter words until the solution is found. An early-career project demonstrating constraint satisfaction and algorithm design fundamentals.

**Note**: This is an archived project from early in my development journey. It has known bugs in the word elimination logic that cause errors in ~30% of games. I'm sharing it to show growth and learning progression.

## How It Works

The solver uses a three-step approach:

1. **Initial Guess**: Starts with "louie" (optimized for common vowels)
2. **Feedback Processing**: Converts colors to constraints:
   - `2` = Correct position (green)
   - `1` = Wrong position (yellow)  
   - `0` = Not in word (gray)
3. **Word Elimination**: Filters remaining words based on all constraints

### Core Algorithm

```python
def remove_words(word_list, guess, feedback, secret_word):
    """Filters words that violate known constraints"""
    for word in word_list:
        for i, (letter, value) in enumerate(zip(guess, feedback)):
            if value == '2' and word[i] != letter:
                # Wrong position for green letter
            elif value == '1' and (word[i] == letter or letter not in word):
                # Yellow letter in same spot or missing
            elif value == '0' and letter in word:
                # Contains gray letter
```

## Performance

Running 1000 games:
```
Wins: 549 (55%)
Failed to solve: 131 (13%)  
Logic errors: 320 (32%)
```

**Project Context**: This is an early-career project that demonstrates core algorithmic concepts but has known bugs in edge case handling. Sharing it to show development progression and learning journey.

## Quick Start

```bash
# Run solver
python wordle.py

# Run tests
python -m unittest Test_wordle.py
```

## Project Structure

```
├── wordle.py              # Main solver logic
├── Test_wordle.py         # Unit tests
└── words.txt              # 12,972 valid words
```

## Technical Highlights

- **Constraint Satisfaction**: Eliminates words that don't match feedback patterns
- **Comprehensive Testing**: Six test cases covering edge cases
- **Clean Architecture**: Modular functions with clear separation of concerns

## Future Improvements

- [ ] Implement entropy maximization for optimal guesses
- [ ] Refactor and bug fix
- [ ] Add letter frequency analysis
- [ ] Create interactive mode
- [ ] Optimize starting word selection

## License

MIT License

## Contact

**Jacob Manhardt**  
📧 jemanhardt@comcast.net  
💼 [LinkedIn](https://www.linkedin.com/in/jacob-manhardt-b9b75025b)  
🐙 [GitHub](https://github.com/manhardt23)

---

*Constraint satisfaction and automated puzzle solving*
