#!/usr/bin/env python3
"""Gate generated images so only pass-classified candidates are promoted."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from _common import as_list, load_data


PROFILE_REQUIRED_CHECKS = {
    "strict_identity": [
        "identity_pass",
        "style_pass",
        "proportion_pass",
        "semantic_pass",
    ],
    "mascot_skateboard": [
        "identity_pass",
        "style_pass",
        "proportion_pass",
        "semantic_pass",
        "eye_construction_pass",
        "star_pupil_pass",
        "hand_digit_count_pass",
        "skateboard_proportion_pass",
    ],
    "compact_mascot_identity": [
        "identity_pass",
        "style_pass",
        "proportion_pass",
        "semantic_pass",
        "character_identity_pass",
        "eye_construction_pass",
        "star_pupil_pass",
        "eyelash_pass",
        "hand_digit_count_pass",
        "ear_shape_pass",
        "compact_body_proportion_pass",
        "arm_length_pass",
        "leg_length_pass",
        "limb_proportion_pass",
        "exact_text_pass",
        "shoe_and_sock_design_pass",
        "source_sheet_style_pass",
    ],
}

REVIEW_MODES = {"pass_only", "visible_shortlist"}


def truthy(value: Any) -> bool:
    return value is True or str(value).lower() == "true"


def result_doc(data: dict[str, Any]) -> dict[str, Any]:
    return data.get("evaluation_result") if isinstance(data.get("evaluation_result"), dict) else data


def failed_checks(result: dict[str, Any], profile: str) -> list[str]:
    checks = result.get("checks") or {}
    if not isinstance(checks, dict):
        return PROFILE_REQUIRED_CHECKS.get(profile, [])
    return [key for key in PROFILE_REQUIRED_CHECKS.get(profile, []) if not truthy(checks.get(key))]


def prompt_patch_lines(result: dict[str, Any]) -> list[str]:
    patch = result.get("prompt_patch") or {}
    if not isinstance(patch, dict):
        return []
    return [str(line) for line in as_list(patch.get("instructions")) if line]


def copy_candidate(candidate: str | None, output_dir: Path, bucket: str) -> str | None:
    if not candidate:
        return None
    source = Path(candidate)
    if not source.exists():
        raise SystemExit(f"Candidate image does not exist: {candidate}")
    target_dir = output_dir / bucket
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    shutil.copy2(source, target)
    return str(target)


def gate_decision(classification: str | None, failures: list[str], review_mode: str) -> tuple[str, str, int]:
    accepted = classification == "pass" and not failures
    if review_mode == "pass_only":
        return ("accept", "accepted", 0) if accepted else ("regenerate", "rejected", 2)
    if accepted:
        return "keep_candidate", "shortlist", 0
    if classification == "fix" and not failures:
        return "repair_candidate", "repairable", 0
    return "discard", "discarded", 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evaluation_result", help="Evaluation result JSON/YAML path")
    parser.add_argument("--candidate-image", help="Generated candidate image to promote or reject")
    parser.add_argument("--output-dir", default="artifacts/generation-loop", help="Directory for accepted/rejected buckets")
    parser.add_argument("--profile", choices=sorted(PROFILE_REQUIRED_CHECKS), default="strict_identity")
    parser.add_argument(
        "--review-mode",
        choices=sorted(REVIEW_MODES),
        default="pass_only",
        help="pass_only hides failures from final promotion; visible_shortlist labels exposed candidates as shortlist/repairable/discarded.",
    )
    parser.add_argument("--write-next-prompt", help="Write prompt patch instructions for the next attempt")
    args = parser.parse_args()

    result = result_doc(load_data(args.evaluation_result))
    failures = failed_checks(result, args.profile)
    classification = result.get("classification")
    output_dir = Path(args.output_dir)
    decision, bucket, exit_code = gate_decision(classification, failures, args.review_mode)

    copied = copy_candidate(args.candidate_image, output_dir, bucket)
    response = {
        "decision": decision,
        "classification": classification,
        "profile": args.profile,
        "review_mode": args.review_mode,
        "failed_checks": failures,
        "drift_patterns": result.get("drift_patterns", []),
        "copied_candidate": copied,
        "prompt_patch": prompt_patch_lines(result),
    }

    if args.write_next_prompt and exit_code != 0:
        Path(args.write_next_prompt).write_text("\n".join(response["prompt_patch"]) + "\n", encoding="utf-8")

    print(json.dumps(response, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
