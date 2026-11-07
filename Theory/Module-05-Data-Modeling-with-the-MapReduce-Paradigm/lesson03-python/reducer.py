"""Sum nonnegative integer counts from key-sorted tab-delimited input."""
import sys


def main():
    current, total = None, 0
    for line_number, line in enumerate(sys.stdin, 1):
        try:
            key, raw_count = line.rstrip("\r\n").split("\t", 1)
            count = int(raw_count)
            if not key or count < 0:
                raise ValueError("empty key or negative count")
        except ValueError as error:
            raise SystemExit(
                f"Invalid reducer record at line {line_number}: {error}"
            ) from error

        if current is not None and key < current:
            raise SystemExit("Reducer input must be sorted by key.")
        if key == current:
            total += count
        else:
            if current is not None:
                print(f"{current}\t{total}")
            current, total = key, count
    if current is not None:
        print(f"{current}\t{total}")


if __name__ == "__main__":
    main()
