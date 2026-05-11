#!/usr/bin/env python3
"""Run generate -> evaluate -> gate loops and keep only accepted candidates."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROFILE_CHOICES = ["strict_identity", "mascot_skateboard", "compact_mascot_identity", "numeric_mascot_identity"]


def run_command(template: str, **values: str) -> None:
    command = template.format(**values)
    subprocess.run(shlex.split(command), check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True, help="Base prompt text file")
    parser.add_argument("--workdir", required=True, help="Loop work directory")
    parser.add_argument("--max-attempts", type=int, default=4)
    parser.add_argument("--profile", default="strict_identity", choices=PROFILE_CHOICES)
    parser.add_argument(
        "--review-mode",
        default="pass_only",
        choices=["pass_only", "visible_shortlist"],
        help="Use visible_shortlist when candidates were already exposed and should be labeled shortlist/repairable/discarded.",
    )
    parser.add_argument(
        "--generate-command",
        required=True,
        help="Command template that writes {candidate}. Available placeholders: {attempt}, {prompt}, {candidate}, {workdir}.",
    )
    parser.add_argument(
        "--evaluate-command",
        required=True,
        help="Command template that writes {evaluation}. Available placeholders: {attempt}, {prompt}, {candidate}, {evaluation}, {workdir}.",
    )
    args = parser.parse_args()

    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    base_prompt = Path(args.prompt).read_text(encoding="utf-8").strip()
    active_prompt = base_prompt

    for attempt in range(1, args.max_attempts + 1):
        prompt_path = workdir / f"attempt_{attempt:02d}.prompt.txt"
        candidate_path = workdir / f"attempt_{attempt:02d}.png"
        evaluation_path = workdir / f"attempt_{attempt:02d}.evaluation.json"
        patch_path = workdir / f"attempt_{attempt:02d}.next_patch.txt"
        prompt_path.write_text(active_prompt + "\n", encoding="utf-8")

        values = {
            "attempt": str(attempt),
            "prompt": str(prompt_path),
            "candidate": str(candidate_path),
            "evaluation": str(evaluation_path),
            "workdir": str(workdir),
        }
        run_command(args.generate_command, **values)
        run_command(args.evaluate_command, **values)

        gate = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_DIR / "score_generation_review.py"),
                str(evaluation_path),
                "--candidate-image",
                str(candidate_path),
                "--output-dir",
                str(workdir),
                "--profile",
                args.profile,
                "--review-mode",
                args.review_mode,
                "--write-next-prompt",
                str(patch_path),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(gate.stdout, end="")
        if gate.returncode == 0:
            result = json.loads(gate.stdout)
            summary = {
                "status": "pass",
                "attempt": attempt,
                "decision": result.get("decision"),
                "output_dir": result.get("copied_candidate"),
            }
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0
        if gate.returncode not in {0, 2}:
            print(gate.stderr, file=sys.stderr)
            return gate.returncode

        patch = patch_path.read_text(encoding="utf-8").strip() if patch_path.exists() else ""
        active_prompt = base_prompt
        if patch:
            active_prompt += "\n\nMandatory correction patch for next attempt:\n" + patch

    print(json.dumps({"status": "failed", "attempts": args.max_attempts, "accepted_dir": str(workdir / "accepted")}, ensure_ascii=False, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
