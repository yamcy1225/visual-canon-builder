#!/usr/bin/env python3
"""Run no-dependency contract tests for visual-canon-builder scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".codex" / "skills" / "visual-canon-builder"
SCRIPTS = SKILL / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
PYTHON = sys.executable


def run(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, *args],
        cwd=ROOT,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_reference_preserve_blocks_without_source_cell() -> None:
    fixture = FIXTURES / "sample_reference_preserve.input.json"
    run(str(SCRIPTS / "validate_canon.py"), str(fixture), "--kind", "visual_canon")
    built = run(str(SCRIPTS / "build_prompt_pack.py"), str(fixture))
    pack = json.loads(built.stdout)["prompt_pack"]
    assert pack["handoff_status"] == "blocked", pack
    assert pack["api_execution_profile"]["input_fidelity"] == "high", pack
    assert pack["source_cell_asset"]["required"] is True, pack
    assert "source_cell_asset required" in " ".join(pack["blocking_reasons"])
    run(str(SCRIPTS / "validate_canon.py"), "-", "--kind", "prompt_pack", input_text=built.stdout)


def test_approval_payload_application_creates_provenance() -> None:
    canon = FIXTURES / "sample_approval.input.json"
    payload = FIXTURES / "sample_approval.payload.json"
    run(str(SCRIPTS / "validate_canon.py"), str(payload), "--kind", "approval_payload")
    applied = run(str(SCRIPTS / "apply_approval_payload.py"), str(canon), str(payload))
    updated = json.loads(applied.stdout)
    by_id = {item["id"]: item for item in updated["canon_assertions"]}
    assert by_id["ASSERT_SampleMascot_StarPupils"]["approval_status"] == "approved"
    assert by_id["ASSERT_SampleMascot_StarPupils"]["canon_status"] == "confirmed"
    assert by_id["ASSERT_SampleMascot_LongboardProp"]["approval_status"] == "keep_provisional"
    assert updated["user_answers"][0]["id"].startswith("UA_REVIEW_SampleMascot_001")
    run(str(SCRIPTS / "validate_canon.py"), "-", "--kind", "visual_canon", input_text=applied.stdout)


def test_evaluation_rejects_source_cell_drift() -> None:
    fixture = FIXTURES / "sample_style_drift.evaluation.json"
    run(str(SCRIPTS / "validate_canon.py"), str(fixture), "--kind", "evaluation_result")
    result = load_json(fixture)["evaluation_result"]
    assert result["classification"] == "reject"
    assert "source_cell_preservation_failed" in result["drift_patterns"]


def test_mascot_skateboard_gate_rejects_failed_details() -> None:
    fixture = FIXTURES / "sample_skateboard_fail.evaluation.json"
    run(str(SCRIPTS / "validate_canon.py"), str(fixture), "--kind", "evaluation_result")
    proc = subprocess.run(
        [
            PYTHON,
            str(SCRIPTS / "score_generation_review.py"),
            str(fixture),
            "--profile",
            "mascot_skateboard",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "regenerate"
    assert "eye_construction_pass" in decision["failed_checks"]
    assert "hand_digit_count_pass" in decision["failed_checks"]
    assert "skateboard_proportion_pass" in decision["failed_checks"]


def test_mascot_skateboard_gate_accepts_pass_details() -> None:
    fixture = FIXTURES / "sample_skateboard_pass.evaluation.json"
    run(str(SCRIPTS / "validate_canon.py"), str(fixture), "--kind", "evaluation_result")
    proc = run(
        str(SCRIPTS / "score_generation_review.py"),
        str(fixture),
        "--profile",
        "mascot_skateboard",
    )
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "accept"


def test_sample_mascot_strict_gate_rejects_limb_proportion_drift() -> None:
    fixture = FIXTURES / "sample_compact_jump_limb_fail.evaluation.json"
    run(str(SCRIPTS / "validate_canon.py"), str(fixture), "--kind", "evaluation_result")
    proc = subprocess.run(
        [
            PYTHON,
            str(SCRIPTS / "score_generation_review.py"),
            str(fixture),
            "--profile",
            "compact_mascot_identity",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "regenerate"
    assert "compact_body_proportion_pass" in decision["failed_checks"]
    assert "arm_length_pass" in decision["failed_checks"]
    assert "leg_length_pass" in decision["failed_checks"]
    assert "limb_proportion_pass" in decision["failed_checks"]


def test_sample_mascot_strict_gate_accepts_compact_jump() -> None:
    fixture = FIXTURES / "sample_compact_jump_pass.evaluation.json"
    run(str(SCRIPTS / "validate_canon.py"), str(fixture), "--kind", "evaluation_result")
    proc = run(
        str(SCRIPTS / "score_generation_review.py"),
        str(fixture),
        "--profile",
        "compact_mascot_identity",
    )
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "accept"


def test_sample_mascot_strict_gate_rejects_wrong_hand_digit_count() -> None:
    fixture = FIXTURES / "sample_compact_jump_hand_fail.evaluation.json"
    run(str(SCRIPTS / "validate_canon.py"), str(fixture), "--kind", "evaluation_result")
    proc = subprocess.run(
        [
            PYTHON,
            str(SCRIPTS / "score_generation_review.py"),
            str(fixture),
            "--profile",
            "compact_mascot_identity",
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "regenerate"
    assert "hand_digit_count_pass" in decision["failed_checks"]


def test_visible_shortlist_keeps_pass_candidate_separately() -> None:
    fixture = FIXTURES / "sample_compact_jump_pass.evaluation.json"
    with tempfile.TemporaryDirectory() as td:
        candidate = Path(td) / "candidate.png"
        out_dir = Path(td) / "visible"
        candidate.write_bytes(b"placeholder")
        proc = run(
            str(SCRIPTS / "score_generation_review.py"),
            str(fixture),
            "--candidate-image",
            str(candidate),
            "--profile",
            "compact_mascot_identity",
            "--review-mode",
            "visible_shortlist",
            "--output-dir",
            str(out_dir),
        )
        decision = json.loads(proc.stdout)
        assert decision["decision"] == "keep_candidate"
        copied = Path(decision["copied_candidate"])
        assert copied.parent.name == "shortlist"
        assert copied.exists()


def test_visible_shortlist_discards_failed_candidate() -> None:
    fixture = FIXTURES / "sample_compact_jump_hand_fail.evaluation.json"
    with tempfile.TemporaryDirectory() as td:
        candidate = Path(td) / "candidate.png"
        out_dir = Path(td) / "visible"
        candidate.write_bytes(b"placeholder")
        proc = subprocess.run(
            [
                PYTHON,
                str(SCRIPTS / "score_generation_review.py"),
                str(fixture),
                "--candidate-image",
                str(candidate),
                "--profile",
                "compact_mascot_identity",
                "--review-mode",
                "visible_shortlist",
                "--output-dir",
                str(out_dir),
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert proc.returncode == 2, proc.stdout + proc.stderr
        decision = json.loads(proc.stdout)
        assert decision["decision"] == "discard"
        copied = Path(decision["copied_candidate"])
        assert copied.parent.name == "discarded"
        assert copied.exists()


def test_source_cell_manifest_ready_state() -> None:
    with tempfile.TemporaryDirectory() as td:
        crop = Path(td) / "crop.png"
        crop.write_bytes(b"placeholder")
        built = run(
            str(SCRIPTS / "create_source_cell_manifest.py"),
            "--id",
            "CROP_SampleMascot_FrontFullBody_001",
            "--source-image-id",
            "Image_SampleMascot_001",
            "--bbox",
            "10,20,300,600",
            "--asset-path",
            str(crop),
        )
    manifest = json.loads(built.stdout)["source_cell_asset_manifest"]
    assert manifest["ready_state"] == "ready"
    assert manifest["source_region"]["bbox"]["width"] == 300


def main() -> int:
    tests = [
        test_reference_preserve_blocks_without_source_cell,
        test_approval_payload_application_creates_provenance,
        test_evaluation_rejects_source_cell_drift,
        test_mascot_skateboard_gate_rejects_failed_details,
        test_mascot_skateboard_gate_accepts_pass_details,
        test_sample_mascot_strict_gate_rejects_limb_proportion_drift,
        test_sample_mascot_strict_gate_accepts_compact_jump,
        test_sample_mascot_strict_gate_rejects_wrong_hand_digit_count,
        test_visible_shortlist_keeps_pass_candidate_separately,
        test_visible_shortlist_discards_failed_candidate,
        test_source_cell_manifest_ready_state,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
