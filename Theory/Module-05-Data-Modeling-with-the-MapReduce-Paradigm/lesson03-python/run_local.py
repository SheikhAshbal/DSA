"""Run the actual mapper and reducer locally; in-memory sort is for small files."""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 text input")
    parser.add_argument("--initial-letter", action="store_true")
    args = parser.parse_args()
    scripts = Path(__file__).resolve().parent
    mapper_name = "initial_mapper.py" if args.initial_letter else "mapper.py"
    commands = [sys.executable, "-X", "utf8"]

    mapped = subprocess.run(
        commands + [str(scripts / mapper_name)],
        input=args.input.read_text(encoding="utf-8"),
        text=True, encoding="utf-8", capture_output=True, check=True,
    )
    records = sorted(mapped.stdout.splitlines(), key=lambda row: row.split("\t", 1)[0])
    grouped = "\n".join(records) + ("\n" if records else "")
    reduced = subprocess.run(
        commands + [str(scripts / "reducer.py")],
        input=grouped, text=True, encoding="utf-8", capture_output=True, check=True,
    )
    sys.stdout.write(reduced.stdout)


if __name__ == "__main__":
    main()
