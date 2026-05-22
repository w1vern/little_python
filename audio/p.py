#!/usr/bin/env python3
"""
Blind pitch shift test generator.

Generates pitch-shifted versions of an audio file for absolute pitch testing.
Files are named with numbers in randomized order; a text file with the answer
key is saved alongside.

Requires ffmpeg and ffprobe in PATH. If ffmpeg is built with librubberband,
it will be used automatically for higher-quality pitch shifting (much better
for piano and other transient-heavy material). Otherwise falls back to the
asetrate/aresample/atempo chain.

Usage:
    python blind_pitch.py <file> <start> <end> <step>

Example:
    python blind_pitch.py nocturne.mp3 -2 2 0.5
"""

import argparse
import random
import shutil
import subprocess
import sys
from pathlib import Path


def check_ffmpeg() -> None:
    """Verify ffmpeg and ffprobe are available in PATH."""
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            print(f"Error: '{tool}' not found in PATH.", file=sys.stderr)
            sys.exit(1)


def has_rubberband() -> bool:
    """Check whether the rubberband filter is compiled into ffmpeg."""
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-filters"],
        capture_output=True, text=True, check=True,
    )
    # Filter listing has lines like " ..C rubberband        A->A   ..."
    for line in result.stdout.splitlines():
        if line.split()[1:2] == ["rubberband"]:
            return True
    return False


def ffprobe_value(file_path: Path, entry: str, stream: bool) -> str:
    """Run ffprobe for a single field, either at stream or format level."""
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", "a:0", "-show_entries", f"stream={entry}"]
    else:
        cmd += ["-show_entries", f"format={entry}"]
    cmd += ["-of", "default=nw=1:nk=1", str(file_path)]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def get_sample_rate(file_path: Path) -> int:
    rate = ffprobe_value(file_path, "sample_rate", stream=True)
    if not rate:
        print(f"Error: could not determine sample rate of {file_path}", file=sys.stderr)
        sys.exit(1)
    return int(rate)


def get_bitrate(file_path: Path) -> int | None:
    """
    Return audio bitrate in bps, or None if not applicable (e.g. lossless).
    Tries the stream first, then falls back to the container's overall bitrate.
    """
    for stream in (True, False):
        rate = ffprobe_value(file_path, "bit_rate", stream=stream)
        if rate and rate != "N/A":
            try:
                return int(rate)
            except ValueError:
                pass
    return None


def pitch_shift(
    input_path: Path,
    output_path: Path,
    semitones: float,
    sample_rate: int,
    bitrate: int | None,
    use_rubberband: bool,
) -> None:
    """
    Pitch shift via ffmpeg.

    Even for semitones=0 we still pass through ffmpeg so all output files
    share identical encoding characteristics — otherwise the untouched
    original could be detected by encoding artifacts alone.
    """
    ratio = 2 ** (semitones / 12)

    if use_rubberband:
        # transients=crisp + detector=percussive preserve piano hammer attacks
        # pitchq=quality favours audio quality over speed
        af = (
            f"rubberband=pitch={ratio}"
            f":transients=crisp:detector=percussive:pitchq=quality"
        )
    else:
        # asetrate/aresample/atempo fallback (WSOLA-based, smears transients)
        new_rate = sample_rate * ratio
        af = f"asetrate={new_rate},aresample={sample_rate},atempo={1 / ratio}"

    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", str(input_path), "-af", af]
    if bitrate:
        cmd += ["-b:a", str(bitrate)]
    cmd.append(str(output_path))

    subprocess.run(cmd, check=True)


def frange_inclusive(start: float, stop: float, step: float) -> list[float]:
    """Float range, inclusive of stop within rounding tolerance."""
    n = round((stop - start) / step)
    return [round(start + i * step, 6) for i in range(n + 1)]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate blind pitch-shifted versions of an audio file.",
    )
    parser.add_argument("file", type=Path, help="Input audio file")
    parser.add_argument("start", type=float, help="Interval start in semitones (e.g. -2)")
    parser.add_argument("end", type=float, help="Interval end in semitones (e.g. 2)")
    parser.add_argument("step", type=float, help="Step in semitones (e.g. 0.5)")
    parser.add_argument(
        "--no-rubberband",
        action="store_true",
        help="Force the asetrate/atempo fallback even if rubberband is available.",
    )
    args = parser.parse_args()

    check_ffmpeg()

    input_path: Path = args.file.resolve()
    if not input_path.is_file():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    if args.step <= 0:
        print("Error: step must be positive.", file=sys.stderr)
        sys.exit(1)
    if args.end < args.start:
        print("Error: end must be >= start.", file=sys.stderr)
        sys.exit(1)

    use_rubberband = (not args.no_rubberband) and has_rubberband()

    # Build list of shifts and guarantee that 0 (the original) is present.
    shifts = frange_inclusive(args.start, args.end, args.step)
    if not any(abs(s) < 1e-9 for s in shifts):
        shifts.append(0.0)
        shifts.sort()

    # Randomly assign shifts to file numbers 1..N.
    # SystemRandom uses OS entropy, so the mapping differs unpredictably
    # between runs.
    rng = random.SystemRandom()
    numbers = list(range(1, len(shifts) + 1))
    rng.shuffle(numbers)

    output_dir = input_path.parent
    extension = input_path.suffix
    sample_rate = get_sample_rate(input_path)
    bitrate = get_bitrate(input_path)

    method = "rubberband" if use_rubberband else "asetrate/atempo (fallback)"
    info = f"sample rate: {sample_rate} Hz"
    info += f", bitrate: {bitrate // 1000} kbps" if bitrate else ", bitrate: source default"
    info += f", method: {method}"
    print(f"Generating {len(shifts)} files in {output_dir} ({info})")

    mapping: list[tuple[int, float]] = []
    for shift, n in zip(shifts, numbers):
        output_path = output_dir / f"{n}{extension}"
        pitch_shift(input_path, output_path, shift, sample_rate, bitrate, use_rubberband)
        mapping.append((n, shift))

    # Write answer key, sorted by filename for easy lookup.
    mapping.sort(key=lambda x: x[0])
    answers_path = output_dir / f"{input_path.stem}_answers.txt"
    with answers_path.open("w", encoding="utf-8") as f:
        f.write(f"Blind pitch test answers for: {input_path.name}\n")
        f.write(f"Interval: {args.start} to {args.end} semitones, step: {args.step}\n")
        f.write(f"Method: {method}\n")
        f.write("-" * 50 + "\n")
        for n, shift in mapping:
            label = "ORIGINAL" if abs(shift) < 1e-9 else f"{shift:+.3f} semitones"
            f.write(f"{n}{extension}: {label}\n")

    print(f"Done. Answer key: {answers_path}")


if __name__ == "__main__":
    main()