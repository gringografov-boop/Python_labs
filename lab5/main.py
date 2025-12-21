from src.simulation import run_simulation


def main() -> None:
    run_simulation(steps=25, seed=42)


if __name__ == "__main__":
    main()