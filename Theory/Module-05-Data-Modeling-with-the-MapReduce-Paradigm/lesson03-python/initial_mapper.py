"""Change only the emitted key: count tokens by their first character."""
import sys


def main():
    for line in sys.stdin:
        for word in line.split():
            print(f"{word[0]}\t1")


if __name__ == "__main__":
    main()
