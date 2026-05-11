#!/usr/bin/env python3
"""Evaluate candidate measurements against a canon proportion_lock_profile."""

from __future__ import annotations

import argparse
from typing import Any

from _common import as_list, load_data, write_data


CATEGORY_CHECKS = {
    "full_silhouette": "full_silhouette_ratio_pass",
    "full_width": "full_silhouette_ratio_pass",
    "head_body": "head_body_ratio_pass",
    "head_plus_ears": "head_body_ratio_pass",
    "head": "head_body_ratio_pass",
    "torso": "torso_width_ratio_pass",
    "shirt": "torso_width_ratio_pass",
    "hip": "hip_width_ratio_pass",
    "leg": "limb_width_ratio_pass",
    "arm": "limb_width_ratio_pass",
    "limb": "limb_width_ratio_pass",
}


def numeric(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def measurements_doc(data: dict[str, Any]) -> dict[str, Any]:
    if isinstance(data.get("candidate_measurements"), dict):
        return data["candidate_measurements"]
    return data


def measurement_values(data: dict[str, Any]) -> dict[str, Any]:
    measurements = data.get("measurements")
    return measurements if isinstance(measurements, dict) else {}


def candidate_ratios(data: dict[str, Any]) -> dict[str, Any]:
    ratios = data.get("ratios")
    return ratios if isinstance(ratios, dict) else {}


def ratio_value(lock: dict[str, Any], measured: dict[str, Any], ratios: dict[str, Any]) -> tuple[float | None, str]:
    lock_id = str(lock.get("id", ""))
    if lock_id in ratios:
        return numeric(ratios[lock_id]), f"ratios.{lock_id}"

    numerator = str(lock.get("numerator_landmark", ""))
    denominator = str(lock.get("denominator_landmark", ""))
    numerator_value = numeric(measured.get(numerator))
    denominator_value = numeric(measured.get(denominator))
    if numerator_value is None or denominator_value in {None, 0.0}:
        return None, f"measurements.{numerator}/measurements.{denominator}"
    return numerator_value / denominator_value, f"measurements.{numerator}/measurements.{denominator}"


def category_check_key(lock: dict[str, Any]) -> str | None:
    text = " ".join(str(lock.get(key, "")) for key in ("id", "label", "numerator_landmark")).lower()
    for hint, check_key in CATEGORY_CHECKS.items():
        if hint in text:
            return check_key
    return None


def format_number(value: Any) -> str:
    num = numeric(value)
    if num is None:
        return str(value)
    return f"{num:.3f}".rstrip("0").rstrip(".")


def evaluate(canon: dict[str, Any], candidate_data: dict[str, Any]) -> dict[str, Any]:
    profile = canon.get("proportion_lock_profile") or {}
    if not isinstance(profile, dict):
        profile = {}
    candidate = measurements_doc(candidate_data)
    measured = measurement_values(candidate)
    ratios = candidate_ratios(candidate)
    base_checks = candidate.get("checks") if isinstance(candidate.get("checks"), dict) else {}

    checks: dict[str, bool] = {
        "identity_pass": bool(base_checks.get("identity_pass", True)),
        "style_pass": bool(base_checks.get("style_pass", True)),
        "semantic_pass": bool(base_checks.get("semantic_pass", True)),
    }
    ratio_results: list[dict[str, Any]] = []
    drift_patterns: list[str] = []
    prompt_instructions: list[str] = []
    category_seen: set[str] = set()

    for lock in as_list(profile.get("ratio_locks")):
        if not isinstance(lock, dict):
            continue
        lock_id = str(lock.get("id") or f"ratio_{len(ratio_results) + 1}")
        low = numeric(lock.get("min"))
        high = numeric(lock.get("max"))
        value, source = ratio_value(lock, measured, ratios)
        passed = value is not None and low is not None and high is not None and low <= value <= high
        check_key = category_check_key(lock)
        if check_key:
            category_seen.add(check_key)
            checks[check_key] = checks.get(check_key, True) and passed

        result = {
            "id": lock_id,
            "label": lock.get("label"),
            "value": value,
            "min": low,
            "max": high,
            "target": numeric(lock.get("target")),
            "passed": passed,
            "value_source": source,
            "reject_if": lock.get("reject_if"),
        }
        ratio_results.append(result)

        if not passed:
            drift_key = f"{lock_id}_out_of_range"
            drift_patterns.append(drift_key)
            prompt_phrase = lock.get("prompt_phrase")
            if prompt_phrase:
                prompt_instructions.append(str(prompt_phrase))
            elif low is not None and high is not None:
                prompt_instructions.append(
                    f"Correct {lock.get('label') or lock_id}: keep ratio between {format_number(low)} and {format_number(high)}."
                )

    for key in (
        "full_silhouette_ratio_pass",
        "head_body_ratio_pass",
        "torso_width_ratio_pass",
        "hip_width_ratio_pass",
        "limb_width_ratio_pass",
    ):
        if key not in checks:
            checks[key] = True

    numeric_pass = bool(ratio_results) and all(item["passed"] for item in ratio_results)
    checks["numeric_proportion_lock_pass"] = numeric_pass
    checks["proportion_pass"] = numeric_pass

    classification = "pass" if numeric_pass and all(checks.values()) else "reject"
    if not ratio_results:
        classification = "reject"
        drift_patterns.append("missing_proportion_locks")
        prompt_instructions.append("Add measured candidate ratios before promotion; no numeric ratio locks were evaluated.")

    return {
        "evaluation_result": {
            "classification": classification,
            "compared_against": profile.get("source_cell_id") or canon.get("id") or "proportion_lock_profile",
            "summary": "Pass: candidate measurements satisfy numeric proportion locks."
            if classification == "pass"
            else "Reject: candidate measurements violate numeric proportion locks.",
            "checks": checks,
            "ratio_results": ratio_results,
            "drift_patterns": drift_patterns,
            "prompt_patch": {
                "instructions": prompt_instructions,
            },
            "notes": {
                "candidate_measurement_source": candidate.get("source") or "candidate_measurements",
                "unchecked_ratio_categories": sorted(
                    set(
                        [
                            "full_silhouette_ratio_pass",
                            "head_body_ratio_pass",
                            "torso_width_ratio_pass",
                            "hip_width_ratio_pass",
                            "limb_width_ratio_pass",
                        ]
                    )
                    - category_seen
                ),
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canon", required=True, help="Visual canon JSON/YAML with proportion_lock_profile")
    parser.add_argument("--candidate-measurements", required=True, help="Candidate measurement JSON/YAML")
    parser.add_argument("-o", "--output", help="Output evaluation_result path; stdout when omitted")
    args = parser.parse_args()

    result = evaluate(load_data(args.canon), load_data(args.candidate_measurements))
    write_data(result, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
