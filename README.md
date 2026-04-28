# Wordle Solver

Python Wordle solver that plays against random words from `words.txt`, updates constraints from feedback, and keeps narrowing the candidate set.

## Requirements

- Python 3.10+ (3.8+ should also work)
- No external dependencies

## Quick Start

```bash
# Run unit tests
python -m unittest Test_wordle.py

# Run one 1,000-game simulation
python wordle.py
```

## Metrics and Verification Runs

Two main benchmark metrics are tracked:

- `solve_rate = wins / total_runs`
- `avg_guesses_on_wins = total_guesses_for_won_games / wins`

Run repeatable benchmark batches:

```bash
python verify_runs.py --runs 1000 --batches 5
```

This prints per-batch metrics and aggregate min/mean/max solve rate.

### Example outputs

Recent single 1,000-game run:

- wins: `882`
- failed: `118`
- errors: `0`
- solve_rate: `88.20%`
- avg_guesses_on_wins: `4.52`

Recent 5-batch verification (`--runs 1000 --batches 5`):

- mean_solve_rate: `85.62%`
- min_solve_rate: `83.90%`
- max_solve_rate: `86.40%`
- mean_avg_guesses_on_wins: `4.57`

## Project Structure

- `wordle.py` - solver logic + reusable `run_simulation(run_count)` API
- `verify_runs.py` - benchmark runner for repeated simulation batches
- `Test_wordle.py` - unit tests for coloring/filtering/scoring behavior
- `words.txt` - valid 5-letter word list

## Notes

- Solver starts with `crane` as first guess.
- Feedback encoding:
  - `2` = green (correct letter, correct spot)
  - `1` = yellow (correct letter, wrong spot)
  - `0` = gray (letter absent, accounting for repeats)

## License

MIT