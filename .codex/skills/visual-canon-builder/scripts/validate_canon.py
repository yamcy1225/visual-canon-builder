#!/usr/bin/env python3
"""Validate visual-canon-builder artifacts without external dependencies."""

from __future__ import annotations

import argparse
from typing import Any

from _common import (
    as_list,
    assertion_has_user_answer,
    load_data,
    reference_preserve_requires_source_cell,
    source_cell_ready,
)


APPROVAL_ACTIONS = {"approve", "reject", "revise", "keep_provisional"}
CLASSIFICATIONS = {"pass", "fix", "reject"}
STRICT_REJECT_DRIFT = {
    "source_cell_preservation_failed",
    "face_geometry_changed",
    "head_body_ratio_changed",
    "eye_construction_changed",
    "star_pupil_missing_or_warped",
    "eyelid_structure_changed",
    "wrong_hand_digit_count",
    "hand_digit_count_wrong",
    "skateboard_proportion_invalid",
    "board_length_invalid",
    "oversized_longboard",
    "limb_proportion_changed",
    "limb_ratio_changed",
    "arms_too_short",
    "legs_too_long",
    "compact_body_ratio_lost",
    "compact_mascot_ratio_lost",
}


def detect_kind(data: dict[str, Any]) -> str:
    if "approval_payload" in data:
        return "approval_payload"
    if "prompt_pack" in data or "final_imagegen_prompt" in data:
        return "prompt_pack"
    if "evaluation_result" in data:
        return "evaluation_result"
    return "visual_canon"


def validate_visual_canon(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    assertions = as_list(data.get("canon_assertions"))

    if not assertions:
        warnings.append("visual canon has no canon_assertions")

    for index, assertion in enumerate(assertions, start=1):
        if not isinstance(assertion, dict):
            errors.append(f"canon_assertions[{index}] is not an object")
            continue
        aid = assertion.get("id", f"#{index}")
        for field in ("subject", "predicate", "object"):
            if field not in assertion:
                errors.append(f"{aid}: missing {field}")
        if not as_list(assertion.get("evidence_refs")):
            errors.append(f"{aid}: evidence_refs must contain at least one evidence card")
        canon_status = assertion.get("canon_status")
        approval_status = assertion.get("approval_status")
        if canon_status == "confirmed":
            if approval_status != "approved":
                errors.append(f"{aid}: confirmed assertion must have approval_status=approved")
            if assertion.get("confidence") != "user_confirmed":
                errors.append(f"{aid}: confirmed assertion must have confidence=user_confirmed")
            if not assertion_has_user_answer(assertion, data):
                errors.append(f"{aid}: confirmed assertion must link to user_answers provenance")
        if approval_status == "approved" and not assertion_has_user_answer(assertion, data):
            errors.append(f"{aid}: approved assertion must link to user_answers provenance")

    handoff = data.get("imagegen_handoff") or data.get("handoff") or {}
    handoff_status = handoff.get("status") if isinstance(handoff, dict) else data.get("handoff_status")
    if reference_preserve_requires_source_cell(data):
        if source_cell_ready(data):
            pass
        elif handoff_status == "ready":
            errors.append("reference_preserve_model requires source_cell_asset, but handoff is ready without a ready source_cell_asset_manifest")
        else:
            warnings.append("reference_preserve_model requires source_cell_asset; keep handoff blocked/provisional until crop exists")

    exact_text_policy = data.get("exact_text_policy") or {}
    if isinstance(exact_text_policy, dict) and exact_text_policy.get("text_required"):
        source = exact_text_policy.get("text_source") or {}
        if isinstance(source, dict) and source.get("approval_status") not in {"approved", "not_applicable"}:
            errors.append("exact_text_policy.text_required needs an approved text_source or an explicit fallback strategy")

    return errors, warnings


def validate_prompt_pack(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    pack = data.get("prompt_pack") if isinstance(data.get("prompt_pack"), dict) else data

    for field in ("handoff_status", "api_execution_profile", "technical_contract", "final_imagegen_prompt"):
        if field not in pack:
            errors.append(f"prompt_pack missing {field}")

    prompt = pack.get("final_imagegen_prompt")
    if isinstance(prompt, str):
        if len(prompt) > 3000:
            errors.append("final_imagegen_prompt should stay executable; length exceeds 3000 chars")
        elif len(prompt) < 80:
            warnings.append("final_imagegen_prompt is unusually short")

    api_profile = pack.get("api_execution_profile") or {}
    if isinstance(api_profile, dict):
        if api_profile.get("input_fidelity") not in {"high", "low", None}:
            errors.append("api_execution_profile.input_fidelity must be high or low")
        if api_profile.get("action") not in {"auto", "generate", "edit", None}:
            errors.append("api_execution_profile.action must be auto, generate, or edit")

    source_cell = pack.get("source_cell_asset") or {}
    if isinstance(source_cell, dict) and source_cell.get("required") and pack.get("handoff_status") == "ready":
        if not source_cell.get("crop_id") and not source_cell.get("asset_path"):
            errors.append("ready prompt_pack cannot require source_cell_asset without crop_id or asset_path")

    return errors, warnings


def validate_approval_payload(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    payload = data.get("approval_payload") if isinstance(data.get("approval_payload"), dict) else data
    decisions = as_list(payload.get("decisions"))
    if not decisions:
        errors.append("approval_payload.decisions must contain at least one decision")
    for index, decision in enumerate(decisions, start=1):
        if not isinstance(decision, dict):
            errors.append(f"decisions[{index}] is not an object")
            continue
        for field in ("assertion_id", "expected_assertion_version", "expected_value_hash", "action"):
            if field not in decision:
                errors.append(f"decisions[{index}] missing {field}")
        if decision.get("action") not in APPROVAL_ACTIONS:
            errors.append(f"decisions[{index}] action must be one of {sorted(APPROVAL_ACTIONS)}")
        if decision.get("action") == "revise" and not decision.get("revised_value"):
            errors.append(f"decisions[{index}] revise action requires revised_value")
    return errors, []


def validate_evaluation_result(data: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    result = data.get("evaluation_result") if isinstance(data.get("evaluation_result"), dict) else data
    if result.get("classification") not in CLASSIFICATIONS:
        errors.append("evaluation_result.classification must be pass, fix, or reject")
    if not result.get("compared_against"):
        errors.append("evaluation_result.compared_against is required")
    drift = [str(item).lower() for item in as_list(result.get("drift_patterns"))]
    severe = any(item in STRICT_REJECT_DRIFT or "source_cell" in item for item in drift)
    if severe and result.get("classification") != "reject":
        errors.append("strict preservation drift must classify as reject")
    checks = result.get("checks") or {}
    if isinstance(checks, dict):
        strict_false = [
            key
            for key in (
                "eye_construction_pass",
                "star_pupil_pass",
                "hand_digit_count_pass",
                "skateboard_proportion_pass",
                "compact_body_proportion_pass",
                "arm_length_pass",
                "leg_length_pass",
                "limb_proportion_pass",
            )
            if checks.get(key) is False
        ]
        if strict_false and result.get("classification") != "reject":
            errors.append(f"strict failed checks must classify as reject: {', '.join(strict_false)}")
    if result.get("classification") == "pass" and not result.get("prompt_patch"):
        warnings.append("pass result can omit prompt_patch, but still needs user approval before canon promotion")
    return errors, warnings


VALIDATORS = {
    "visual_canon": validate_visual_canon,
    "prompt_pack": validate_prompt_pack,
    "approval_payload": validate_approval_payload,
    "evaluation_result": validate_evaluation_result,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", help="JSON artifact path, or '-' for stdin")
    parser.add_argument("--kind", choices=sorted(VALIDATORS), help="Artifact kind; auto-detected by default")
    args = parser.parse_args()

    data = load_data(args.artifact)
    kind = args.kind or detect_kind(data)
    errors, warnings = VALIDATORS[kind](data)

    for warning in warnings:
        print(f"WARN {warning}")
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"PASS {kind}: {args.artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
