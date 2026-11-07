"""Local checkpoint/resume simulation for the cloud-notebook lesson.

No cloud access, account credentials, or third-party packages are required.
The temporary scratch directory simulates an ephemeral runtime. The output
directory represents storage outside that runtime, not a real cloud service.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
from tempfile import TemporaryDirectory

TASK = "sum-squares-v1"
INPUTS = list(range(1, 11))

def advance(state, stop):
    """Resume a deterministic teaching task through the requested step."""
    if state.get("task") != TASK:
        raise ValueError("checkpoint belongs to a different task")
    step, total = state.get("step"), state.get("total")
    if type(step) is not int or type(total) is not int:
        raise ValueError("checkpoint step and total must be integers")
    if not 0 <= step <= len(INPUTS):
        raise ValueError("checkpoint step out of range")
    if total != sum(n*n for n in INPUTS[:step]):
        raise ValueError("checkpoint total is inconsistent")
    if type(stop) is not int or not step <= stop <= len(INPUTS):
        raise ValueError("invalid stopping step")
    return {"task": TASK, "step": stop,
            "total": total + sum(n*n for n in INPUTS[step:stop])}

def write_json(path, payload):
    """Replace a local JSON file after completing its sibling temporary file."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)

def run_demo(output_dir):
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = output_dir / "checkpoint.json"
    manifest = output_dir / "environment.json"
    initial = {"task": TASK, "step": 0, "total": 0}
    with TemporaryDirectory(prefix="runtime-", dir=output_dir) as scratch:
        scratch_file = Path(scratch) / "unsaved-result.json"
        memory = advance(initial, 4)
        write_json(scratch_file, memory)
        write_json(checkpoint, memory)
        write_json(manifest, {
            "task": TASK,
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "dependencies": "Python standard library only",
            "input_sha256": hashlib.sha256(
                json.dumps(INPUTS, separators=(",", ":")).encode()).hexdigest(),
            "steps": len(INPUTS),
            "expected_total": 385,
        })
        local_before = scratch_file.exists()
    # Simulate a fresh process: discard the old variable and reload saved state.
    del memory
    saved = json.loads(checkpoint.read_text(encoding="utf-8"))
    resumed = advance(saved, 10)
    uninterrupted = advance(initial, 10)
    if resumed != uninterrupted:
        raise AssertionError("resumed result differs from uninterrupted result")
    result = {
        "scratch_existed_before_reset": local_before,
        "scratch_exists_after_reset": scratch_file.exists(),
        "checkpoint_exists_after_reset": checkpoint.exists(),
        "saved_step": saved["step"],
        "saved_total": saved["total"],
        "resumed_total": resumed["total"],
        "matches_uninterrupted": resumed == uninterrupted,
    }
    write_json(output_dir / "result.json", result)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("lesson03-demo-output"),
                        help="dedicated local output folder; demo JSON files are replaced")
    args = parser.parse_args()
    print(json.dumps(run_demo(args.output_dir), indent=2))

if __name__ == "__main__":
    main()
