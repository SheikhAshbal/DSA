"""Emit case-sensitive, whitespace-delimited word counts for Streaming."""
import sys


def main():
    for line in sys.stdin:
        for word in line.split():
            print(f"{word}\t1")


if __name__ == "__main__":
    main()
