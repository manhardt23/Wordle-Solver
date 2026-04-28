import argparse
from statistics import mean

from wordle import run_simulation


def main():
    parser = argparse.ArgumentParser(
        description="Run repeatable Wordle solver benchmarks."
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1000,
        help="Number of games per batch (default: 1000)."
    )
    parser.add_argument(
        "--batches",
        type=int,
        default=5,
        help="How many batches to run (default: 5)."
    )
    args = parser.parse_args()

    if args.runs <= 0 or args.batches <= 0:
        raise ValueError("--runs and --batches must both be positive integers.")

    results = []
    for batch in range(1, args.batches + 1):
        stats = run_simulation(args.runs)
        results.append(stats)
        print(
            f"Batch {batch}: "
            f"wins={stats['wins']}/{stats['runs']} "
            f"solve_rate={stats['solve_rate']:.2f}% "
            f"avg_guesses_on_wins={stats['avg_guesses_on_wins']:.2f} "
            f"failed={stats['failed']} "
            f"errors={stats['errors']}"
        )

    solve_rates = [result["solve_rate"] for result in results]
    avg_guesses = [result["avg_guesses_on_wins"] for result in results if result["wins"] > 0]

    print("\nAggregate")
    print(f"- batches: {args.batches}")
    print(f"- runs_per_batch: {args.runs}")
    print(f"- mean_solve_rate: {mean(solve_rates):.2f}%")
    print(f"- min_solve_rate: {min(solve_rates):.2f}%")
    print(f"- max_solve_rate: {max(solve_rates):.2f}%")
    if avg_guesses:
        print(f"- mean_avg_guesses_on_wins: {mean(avg_guesses):.2f}")


if __name__ == "__main__":
    main()
