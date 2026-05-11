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


def deep_canon_policy_fixture(max_total_questions: int | str = "unbounded") -> dict:
    return {
        "entity_type": "Character",
        "id": "SampleNumericMascotCanon",
        "interview_policy": {
            "mode": "deep_canon",
            "max_active_questions_per_turn": 1,
            "max_total_questions": max_total_questions,
            "minimum_passes": [
                "source_authority",
                "source_cell_crop",
                "silhouette",
                "numeric_proportions",
                "face_construction",
                "anatomy_digits",
                "costume_structure",
                "style_rendering",
                "view_projection",
                "variant_budget",
                "forbidden_drift",
                "evaluation_gate",
            ],
        },
        "user_answers": [
            {
                "id": "UA_SampleMascot_ProportionLock_001",
                "answers_question": "Q_SampleMascot_ProportionLock_001",
                "applies_to": ["ASSERT_SampleMascot_ProportionLock"],
                "asserted_by": "user",
                "confidence": "user_confirmed",
            }
        ],
        "canon_assertions": [
            {
                "id": "ASSERT_SampleMascot_ProportionLock",
                "subject": "SampleNumericMascot",
                "predicate": "hasHeadBodyRatio",
                "object": "numeric ratio locks approved",
                "evidence_refs": ["EV_SampleMascot_FrontProportion_001"],
                "retrieval_scope": "current_conversation_only",
                "confidence": "user_confirmed",
                "canon_status": "confirmed",
                "approval_status": "approved",
            }
        ],
        "proportion_lock_profile": {
            "mode": "numeric_ratio_lock",
            "source_cell_id": "CROP_SampleMascot_FrontFullBody_001",
            "unit_basis": "full_height_1000",
            "ratio_locks": [
                {
                    "id": "torso_width_to_face_width",
                    "label": "torso center width / face width",
                    "numerator_landmark": "torso_center_width",
                    "denominator_landmark": "face_width",
                    "target": 0.77,
                    "min": 0.70,
                    "max": 0.82,
                    "prompt_phrase": "torso center width stays 0.70-0.82 of face width, target 0.77",
                    "reject_if": "above max = too wide/fat; below min = too skinny",
                    "evidence_refs": ["EV_SampleMascot_FrontProportion_001"],
                }
            ],
        },
        "generation_contract": {
            "task_sensitivity": "identity_sensitive",
            "reference_policy": {
                "identity_anchor": "CROP_SampleMascot_FrontFullBody_001"
            },
        },
    }


def numeric_loop_canon_fixture() -> dict:
    fixture = deep_canon_policy_fixture()
    fixture["proportion_lock_profile"]["ratio_locks"] = [
        {
            "id": "full_silhouette_width_to_height",
            "label": "full silhouette width / full height",
            "numerator_landmark": "full_silhouette_width",
            "denominator_landmark": "full_height",
            "target": 0.34,
            "min": 0.31,
            "max": 0.36,
            "prompt_phrase": "full silhouette width stays 0.31-0.36 of full height",
            "reject_if": "below min = too thin/tall; above max = too wide",
            "evidence_refs": ["EV_SampleMascot_FrontProportion_001"],
        },
        {
            "id": "head_plus_ears_height_to_full_height",
            "label": "head plus ears height / full height",
            "numerator_landmark": "head_plus_ears_height",
            "denominator_landmark": "full_height",
            "target": 0.50,
            "min": 0.48,
            "max": 0.53,
            "prompt_phrase": "head plus ears occupies 0.48-0.53 of full height",
            "reject_if": "outside range = head/body ratio changed",
            "evidence_refs": ["EV_SampleMascot_FrontProportion_001"],
        },
        {
            "id": "torso_width_to_face_width",
            "label": "torso center width / face width",
            "numerator_landmark": "torso_center_width",
            "denominator_landmark": "face_width",
            "target": 0.77,
            "min": 0.70,
            "max": 0.82,
            "prompt_phrase": "torso center width stays 0.70-0.82 of face width, target 0.77",
            "reject_if": "above max = too wide/fat; below min = too skinny",
            "evidence_refs": ["EV_SampleMascot_FrontProportion_001"],
        },
        {
            "id": "hip_width_to_face_width",
            "label": "hip width / face width",
            "numerator_landmark": "hip_width",
            "denominator_landmark": "face_width",
            "target": 0.78,
            "min": 0.70,
            "max": 0.84,
            "prompt_phrase": "hip width stays 0.70-0.84 of face width",
            "reject_if": "above max = lower body got too wide",
            "evidence_refs": ["EV_SampleMascot_FrontProportion_001"],
        },
        {
            "id": "limb_width_to_face_width",
            "label": "limb width / face width",
            "numerator_landmark": "limb_width",
            "denominator_landmark": "face_width",
            "target": 0.16,
            "min": 0.13,
            "max": 0.19,
            "prompt_phrase": "visible limb width stays 0.13-0.19 of face width",
            "reject_if": "outside range = limb thickness drift",
            "evidence_refs": ["EV_SampleMascot_FrontProportion_001"],
        },
    ]
    return fixture


def candidate_measurements_fixture(torso_ratio: float = 0.77) -> dict:
    return {
        "candidate_measurements": {
            "source": "test measurement fixture",
            "ratios": {
                "full_silhouette_width_to_height": 0.34,
                "head_plus_ears_height_to_full_height": 0.50,
                "torso_width_to_face_width": torso_ratio,
                "hip_width_to_face_width": 0.78,
                "limb_width_to_face_width": 0.16,
            },
            "checks": {
                "identity_pass": True,
                "style_pass": True,
                "semantic_pass": True,
            },
        }
    }


def test_deep_canon_policy_accepts_unbounded_questions_and_numeric_locks() -> None:
    fixture = deep_canon_policy_fixture()
    payload = json.dumps(fixture, ensure_ascii=False)
    run(str(SCRIPTS / "validate_canon.py"), "-", "--kind", "visual_canon", input_text=payload)
    built = run(str(SCRIPTS / "build_prompt_pack.py"), "-", input_text=payload)
    pack = json.loads(built.stdout)["prompt_pack"]
    assert pack["technical_contract"]["interview_policy"]["mode"] == "deep_canon"
    assert pack["technical_contract"]["proportion_lock_profile"]["ratio_locks"][0]["id"] == "torso_width_to_face_width"
    assert "torso center width stays 0.70-0.82" in pack["final_imagegen_prompt"]


def test_deep_canon_policy_rejects_four_question_total_cap() -> None:
    fixture = deep_canon_policy_fixture(max_total_questions=4)
    proc = subprocess.run(
        [
            PYTHON,
            str(SCRIPTS / "validate_canon.py"),
            "-",
            "--kind",
            "visual_canon",
        ],
        cwd=ROOT,
        input=json.dumps(fixture, ensure_ascii=False),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "short fixed total-question cap" in proc.stdout


def test_numeric_proportion_evaluator_accepts_candidate_measurements() -> None:
    with tempfile.TemporaryDirectory() as td:
        canon_path = Path(td) / "canon.json"
        measurements_path = Path(td) / "measurements.json"
        canon_path.write_text(json.dumps(numeric_loop_canon_fixture(), ensure_ascii=False), encoding="utf-8")
        measurements_path.write_text(json.dumps(candidate_measurements_fixture(), ensure_ascii=False), encoding="utf-8")
        evaluated = run(
            str(SCRIPTS / "evaluate_proportion_locks.py"),
            "--canon",
            str(canon_path),
            "--candidate-measurements",
            str(measurements_path),
        )
    result = json.loads(evaluated.stdout)["evaluation_result"]
    assert result["classification"] == "pass"
    assert result["checks"]["numeric_proportion_lock_pass"] is True
    assert result["checks"]["torso_width_ratio_pass"] is True
    run(str(SCRIPTS / "validate_canon.py"), "-", "--kind", "evaluation_result", input_text=evaluated.stdout)


def test_numeric_proportion_evaluator_rejects_out_of_range_candidate() -> None:
    with tempfile.TemporaryDirectory() as td:
        canon_path = Path(td) / "canon.json"
        measurements_path = Path(td) / "measurements.json"
        candidate = Path(td) / "candidate.png"
        canon_path.write_text(json.dumps(numeric_loop_canon_fixture(), ensure_ascii=False), encoding="utf-8")
        measurements_path.write_text(json.dumps(candidate_measurements_fixture(torso_ratio=0.90), ensure_ascii=False), encoding="utf-8")
        candidate.write_bytes(b"placeholder")
        evaluated = run(
            str(SCRIPTS / "evaluate_proportion_locks.py"),
            "--canon",
            str(canon_path),
            "--candidate-measurements",
            str(measurements_path),
        )
        result = json.loads(evaluated.stdout)["evaluation_result"]
        assert result["classification"] == "reject"
        assert result["checks"]["numeric_proportion_lock_pass"] is False
        assert result["checks"]["torso_width_ratio_pass"] is False

        evaluation_path = Path(td) / "evaluation.json"
        evaluation_path.write_text(evaluated.stdout, encoding="utf-8")
        proc = subprocess.run(
            [
                PYTHON,
                str(SCRIPTS / "score_generation_review.py"),
                str(evaluation_path),
                "--candidate-image",
                str(candidate),
                "--profile",
                "numeric_mascot_identity",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    decision = json.loads(proc.stdout)
    assert decision["decision"] == "regenerate"
    assert "numeric_proportion_lock_pass" in decision["failed_checks"]
    assert "torso_width_ratio_pass" in decision["failed_checks"]


def test_generation_loop_accepts_numeric_proportion_candidate() -> None:
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td) / "loop"
        workdir.mkdir()
        prompt = Path(td) / "prompt.txt"
        prompt.write_text("Generate a numeric-locked sample mascot.", encoding="utf-8")
        (workdir / "seed.png").write_bytes(b"placeholder")
        (workdir / "canon.json").write_text(json.dumps(numeric_loop_canon_fixture(), ensure_ascii=False), encoding="utf-8")
        (workdir / "measurements.json").write_text(json.dumps(candidate_measurements_fixture(), ensure_ascii=False), encoding="utf-8")

        proc = run(
            str(SCRIPTS / "run_generation_loop.py"),
            "--prompt",
            str(prompt),
            "--workdir",
            str(workdir),
            "--profile",
            "numeric_mascot_identity",
            "--max-attempts",
            "1",
            "--generate-command",
            "cp {workdir}/seed.png {candidate}",
            "--evaluate-command",
            f"{PYTHON} .codex/skills/visual-canon-builder/scripts/evaluate_proportion_locks.py --canon {{workdir}}/canon.json --candidate-measurements {{workdir}}/measurements.json --output {{evaluation}}",
        )
        assert "\"status\": \"pass\"" in proc.stdout
        accepted = workdir / "accepted" / "attempt_01.png"
        assert accepted.exists()

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
        test_deep_canon_policy_accepts_unbounded_questions_and_numeric_locks,
        test_deep_canon_policy_rejects_four_question_total_cap,
        test_numeric_proportion_evaluator_accepts_candidate_measurements,
        test_numeric_proportion_evaluator_rejects_out_of_range_candidate,
        test_generation_loop_accepts_numeric_proportion_candidate,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
