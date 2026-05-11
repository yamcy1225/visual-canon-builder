#!/usr/bin/env python3
"""Apply approve/reject/revise/keep_provisional decisions to a visual canon."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
from typing import Any

from _common import as_list, assertion_hash, load_data, write_data


def index_assertions(canon: dict[str, Any]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for assertion in as_list(canon.get("canon_assertions")):
        if isinstance(assertion, dict) and assertion.get("id"):
            indexed[str(assertion["id"])] = assertion
    return indexed


def ensure_user_answers(canon: dict[str, Any]) -> list[dict[str, Any]]:
    answers = canon.setdefault("user_answers", [])
    if not isinstance(answers, list):
        raise SystemExit("user_answers must be a list when present")
    return answers


def make_answer(payload: dict[str, Any], decision: dict[str, Any], sequence: int) -> dict[str, Any]:
    review_id = payload.get("review_pack_id", "REVIEW")
    assertion_id = decision.get("assertion_id", "ASSERT")
    return {
        "id": f"UA_{review_id}_{sequence:03d}",
        "review_pack_id": review_id,
        "applies_to_assertion": assertion_id,
        "applies_to": [assertion_id],
        "decision_action": decision.get("action"),
        "value": decision.get("revised_value") if decision.get("action") == "revise" else decision.get("action"),
        "note": decision.get("note"),
        "asserted_by": "user",
        "confidence": "user_confirmed",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }


def append_derived_from(assertion: dict[str, Any], answer_id: str) -> None:
    derived = assertion.get("derived_from")
    if derived is None:
        assertion["derived_from"] = [answer_id]
    elif isinstance(derived, list):
        if answer_id not in derived:
            derived.append(answer_id)
    else:
        assertion["derived_from"] = [derived, answer_id]


def apply_decision(canon: dict[str, Any], assertion: dict[str, Any], decision: dict[str, Any], answer: dict[str, Any]) -> None:
    action = decision.get("action")
    answer_id = answer["id"]
    if action == "approve":
        assertion["approval_status"] = "approved"
        assertion["canon_status"] = "confirmed"
        assertion["confidence"] = "user_confirmed"
        assertion["needs_confirmation"] = False
        append_derived_from(assertion, answer_id)
    elif action == "reject":
        assertion["approval_status"] = "rejected"
        assertion["canon_status"] = "rejected"
        assertion["confidence"] = "rejected"
        append_derived_from(assertion, answer_id)
    elif action == "keep_provisional":
        assertion["approval_status"] = "keep_provisional"
        assertion["canon_status"] = "provisional"
        append_derived_from(assertion, answer_id)
    elif action == "revise":
        assertion["approval_status"] = "revised"
        assertion["canon_status"] = "rejected"
        append_derived_from(assertion, answer_id)

        replacement = copy.deepcopy(assertion)
        next_version = int(assertion.get("assertion_version", 1)) + 1
        replacement["id"] = f"{assertion.get('id')}_REV{next_version}"
        replacement["object"] = decision["revised_value"]
        replacement["assertion_version"] = next_version
        replacement["value_hash"] = assertion_hash(replacement)
        replacement["approval_status"] = "approved"
        replacement["canon_status"] = "confirmed"
        replacement["confidence"] = "user_confirmed"
        replacement["needs_confirmation"] = False
        replacement["supersedes"] = assertion.get("id")
        replacement["derived_from"] = [answer_id]
        canon.setdefault("canon_assertions", []).append(replacement)
    else:
        raise SystemExit(f"Unsupported action: {action}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("canon", help="Visual canon JSON/YAML path")
    parser.add_argument("approval_payload", help="Approval payload JSON/YAML path")
    parser.add_argument("-o", "--output", help="Output path; stdout when omitted")
    args = parser.parse_args()

    canon = load_data(args.canon)
    payload_doc = load_data(args.approval_payload)
    payload = payload_doc.get("approval_payload") if isinstance(payload_doc.get("approval_payload"), dict) else payload_doc
    assertions = index_assertions(canon)
    answers = ensure_user_answers(canon)

    for sequence, decision in enumerate(as_list(payload.get("decisions")), start=1):
        if not isinstance(decision, dict):
            raise SystemExit(f"Decision {sequence} is not an object")
        assertion_id = str(decision.get("assertion_id"))
        assertion = assertions.get(assertion_id)
        if not assertion:
            raise SystemExit(f"Unknown assertion_id: {assertion_id}")
        expected_version = decision.get("expected_assertion_version")
        if expected_version != assertion.get("assertion_version"):
            raise SystemExit(f"{assertion_id}: stale assertion_version")
        expected_hash = decision.get("expected_value_hash")
        if expected_hash != assertion.get("value_hash"):
            raise SystemExit(f"{assertion_id}: stale value_hash")
        answer = make_answer(payload, decision, sequence)
        answers.append(answer)
        apply_decision(canon, assertion, decision, answer)

    canon["canon_lock_state"] = "partially_locked"
    if all(
        isinstance(item, dict) and item.get("canon_status") in {"confirmed", "rejected", "provisional"}
        for item in as_list(canon.get("canon_assertions"))
    ):
        canon["canon_lock_state"] = "decisions_applied"

    write_data(canon, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
