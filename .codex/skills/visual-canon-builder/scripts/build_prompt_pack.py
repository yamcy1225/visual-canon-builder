#!/usr/bin/env python3
"""Build a two-layer $imagegen prompt pack from a visual canon artifact."""

from __future__ import annotations

import argparse
from typing import Any

from _common import (
    as_list,
    assertion_label,
    load_data,
    reference_preserve_requires_source_cell,
    source_cell_manifest,
    source_cell_ready,
    write_data,
)


IDENTITY_PREDICATE_HINTS = {
    "hasFaceGeometry",
    "hasEyeMotif",
    "hasHeadBodyRatio",
    "hasSilhouette",
    "hasBodySilhouette",
    "hasSignatureMark",
    "hasCostumeStructure",
    "hasLineLanguage",
}


def get_generation_contract(canon: dict[str, Any]) -> dict[str, Any]:
    contract = canon.get("generation_contract") or {}
    return contract if isinstance(contract, dict) else {}


def get_reference_policy(contract: dict[str, Any]) -> dict[str, Any]:
    policy = contract.get("reference_policy") or {}
    return policy if isinstance(policy, dict) else {}


def approved_assertions(canon: dict[str, Any]) -> list[dict[str, Any]]:
    approved: list[dict[str, Any]] = []
    for assertion in as_list(canon.get("canon_assertions")):
        if isinstance(assertion, dict) and assertion.get("approval_status") == "approved" and assertion.get("canon_status") == "confirmed":
            approved.append(assertion)
    return approved


def provisional_assertions(canon: dict[str, Any]) -> list[dict[str, Any]]:
    provisional: list[dict[str, Any]] = []
    for assertion in as_list(canon.get("canon_assertions")):
        if not isinstance(assertion, dict):
            continue
        if assertion.get("canon_status") in {"rejected", "confirmed"}:
            continue
        provisional.append(assertion)
    return provisional


def has_pending_identity_critical(canon: dict[str, Any]) -> bool:
    for assertion in provisional_assertions(canon):
        predicate = str(assertion.get("predicate"))
        if predicate in IDENTITY_PREDICATE_HINTS or assertion.get("risk_tier") in {"identity_critical", "canon_critical"}:
            return True
    return False


def build_api_execution_profile(
    canon: dict[str, Any],
    task_sensitivity: str,
    mode: str,
    source_manifest: dict[str, Any],
) -> dict[str, Any]:
    contract = get_generation_contract(canon)
    policy = get_reference_policy(contract)
    identity_anchor = policy.get("identity_anchor")
    style_anchor = policy.get("style_anchor")
    first_image = source_manifest.get("crop_id") or source_manifest.get("id") or identity_anchor

    action = "edit" if mode in {"edit", "edit_target_preserve", "edit_or_reference_image"} else "generate"
    if task_sensitivity in {"identity_sensitive", "style_sensitive"}:
        action = "edit" if first_image else "generate"

    return {
        "preferred_api": "responses_api" if first_image else "image_api",
        "reason": "multi_turn_reference_preserving_workflow" if first_image else "no_reference_input_available",
        "model_family": "gpt_image",
        "action": action,
        "input_fidelity": "high" if task_sensitivity in {"identity_sensitive", "style_sensitive"} else "low",
        "reference_ordering": {
            "first_image": first_image or "none",
            "second_image": style_anchor if style_anchor and style_anchor != first_image else None,
            "later_images": [
                item
                for item in [
                    policy.get("composition_reference"),
                    policy.get("prop_reference"),
                    policy.get("forbidden_examples"),
                ]
                if item
            ],
        },
        "mask": {
            "required": False,
            "use_when": [
                "localized_edit",
                "exact_text_change",
                "expression_or_arm_position_change",
            ],
            "rule": "mask_targets_change_area_only_keep_rest_preserved",
        },
        "output": {
            "size": canon.get("output_size", "auto_or_requested"),
            "format": canon.get("output_format", "png"),
            "background": canon.get("background", "transparent_or_opaque_or_auto"),
        },
    }


def compute_handoff_status(canon: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    contract = get_generation_contract(canon)
    task_sensitivity = contract.get("task_sensitivity")
    policy = get_reference_policy(contract)

    if reference_preserve_requires_source_cell(canon) and not source_cell_ready(canon):
        reasons.append("source_cell_asset required before exact preservation can be ready")
    if task_sensitivity == "identity_sensitive" and not policy.get("identity_anchor") and not source_cell_ready(canon):
        reasons.append("identity_sensitive handoff has no identity anchor")
    if reasons:
        return "blocked", reasons
    if has_pending_identity_critical(canon):
        return "provisional", ["identity-critical assertions still need user approval"]
    if not approved_assertions(canon) and as_list(canon.get("canon_assertions")):
        return "provisional", ["assertions are present but none are confirmed"]
    return "ready", []


def compact_constraints(assertions: list[dict[str, Any]]) -> list[str]:
    return [assertion_label(assertion) for assertion in assertions]


def proportion_lock_lines(canon: dict[str, Any], limit: int = 8) -> list[str]:
    profile = canon.get("proportion_lock_profile") or {}
    if not isinstance(profile, dict):
        return []
    lines: list[str] = []
    for lock in as_list(profile.get("ratio_locks")):
        if not isinstance(lock, dict):
            continue
        label = lock.get("label") or lock.get("id")
        if not label:
            continue
        target = lock.get("target")
        low = lock.get("min")
        high = lock.get("max")
        phrase = lock.get("prompt_phrase")
        reject = lock.get("reject_if")
        if phrase:
            line = str(phrase)
        elif target is not None and low is not None and high is not None:
            line = f"{label}: target {target}, pass range {low}-{high}"
        else:
            line = str(label)
        if reject:
            line += f" (reject if {reject})"
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def build_final_prompt(
    canon: dict[str, Any],
    handoff_status: str,
    api_profile: dict[str, Any],
    confirmed: list[str],
    provisional: list[str],
    blocking_reasons: list[str],
) -> str:
    contract = get_generation_contract(canon)
    reference_model = canon.get("reference_preserve_model") or {}
    source_manifest = source_cell_manifest(canon)
    task = canon.get("primary_request") or contract.get("task_type") or "identity-preserving visual generation"
    allowed = as_list((contract.get("mutation_policy") or {}).get("allowed_to_change"))
    forbidden = as_list((contract.get("mutation_policy") or {}).get("must_not_change"))
    invariants = as_list((contract.get("invariant_restatement") or {}).get("lines"))
    first_image = (api_profile.get("reference_ordering") or {}).get("first_image")

    lines = [
        "This is an identity/style-preserving image task, not a redesign.",
        f"Task: {task}.",
        f"Handoff status: {handoff_status}.",
    ]
    if blocking_reasons:
        lines.append("Blocking reasons: " + "; ".join(blocking_reasons) + ".")
    if first_image and first_image != "none":
        lines.append(f"Use {first_image} as the first input image and main identity/style/proportion anchor.")
    if source_manifest:
        lines.append(
            "Source cell: preserve "
            + ", ".join(as_list(source_manifest.get("preservation_priority")) or ["silhouette", "proportions", "line style"])
            + "."
        )
    if allowed:
        lines.append("Change only: " + ", ".join(str(item) for item in allowed) + ".")
    if invariants:
        lines.extend(str(item) for item in invariants)
    ratio_lines = proportion_lock_lines(canon)
    if ratio_lines:
        lines.append("Numeric proportion locks: " + "; ".join(ratio_lines) + ".")
    if forbidden:
        lines.append("Do not change: " + ", ".join(str(item) for item in forbidden) + ".")
    if confirmed:
        lines.append("Confirmed constraints: " + "; ".join(confirmed[:8]) + ".")
    if provisional:
        lines.append("Provisional guidance, not canon: " + "; ".join(provisional[:5]) + ".")
    if isinstance(reference_model, dict) and reference_model.get("mode"):
        lines.append(f"Reference preserve mode: {reference_model.get('mode')}.")
    lines.append("Avoid identity-only similarity, style drift, proportion redesign, extra realism, wrong exact text, and unrequested props.")
    return "\n".join(lines)


def build_prompt_pack(canon: dict[str, Any]) -> dict[str, Any]:
    contract = get_generation_contract(canon)
    task_sensitivity = contract.get("task_sensitivity", "loose_inspiration")
    mode = contract.get("default_mode", "reference_image_preferred")
    source_manifest = source_cell_manifest(canon)
    handoff_status, blocking_reasons = compute_handoff_status(canon)
    confirmed = compact_constraints(approved_assertions(canon))
    provisional = compact_constraints(provisional_assertions(canon))
    api_profile = build_api_execution_profile(canon, task_sensitivity, mode, source_manifest)
    final_prompt = build_final_prompt(canon, handoff_status, api_profile, confirmed, provisional, blocking_reasons)

    source_asset = {
        "required": reference_preserve_requires_source_cell(canon),
        "crop_id": source_manifest.get("crop_id") or source_manifest.get("id"),
        "asset_path": source_manifest.get("asset_path"),
        "ready_state": source_manifest.get("ready_state", "not_declared"),
        "full_sheet_only": ((canon.get("reference_preserve_model") or {}).get("source_cell_asset") or {}).get("full_sheet_only"),
    }

    return {
        "prompt_pack": {
            "use_case": canon.get("use_case", "visual_canon_imagegen_handoff"),
            "asset_type": canon.get("entity_type", "VisualAsset"),
            "task_sensitivity": task_sensitivity,
            "handoff_status": handoff_status,
            "blocking_reasons": blocking_reasons,
            "api_execution_profile": api_profile,
            "source_cell_asset": source_asset,
            "technical_contract": {
                "generation_contract": contract,
                "reference_preserve_model": canon.get("reference_preserve_model"),
                "source_cell_asset_manifest": source_manifest or None,
                "interview_policy": canon.get("interview_policy"),
                "proportion_lock_profile": canon.get("proportion_lock_profile"),
                "exact_text_policy": canon.get("exact_text_policy"),
                "evaluation_contract": canon.get("evaluation_contract"),
            },
            "final_imagegen_prompt": final_prompt,
            "confirmed_constraints": confirmed,
            "provisional_constraints": provisional,
            "unresolved_questions": canon.get("unresolved_questions") or canon.get("question_queue") or [],
            "avoid": canon.get("forbidden", []),
            "evaluation_checklist": [
                "identity_pass",
                "style_pass",
                "proportion_pass",
                "numeric_proportion_lock_pass",
                "semantic_pass",
                "composition_pass",
                "drift_notes",
                "next_prompt_patch",
            ],
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("canon", help="Visual canon JSON/YAML path")
    parser.add_argument("-o", "--output", help="Output path; stdout when omitted")
    args = parser.parse_args()

    pack = build_prompt_pack(load_data(args.canon))
    write_data(pack, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
