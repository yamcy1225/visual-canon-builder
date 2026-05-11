#!/usr/bin/env python3
"""Shared helpers for visual-canon-builder operational scripts."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def load_data(path: str | Path) -> dict[str, Any]:
    source = sys.stdin.read() if str(path) == "-" else Path(path).read_text(encoding="utf-8")
    if not source.strip():
        return {}

    try:
        value = json.loads(source)
    except json.JSONDecodeError:
        if str(path).endswith((".yaml", ".yml")):
            try:
                import yaml  # type: ignore
            except ImportError as exc:
                raise SystemExit(
                    "YAML input requires PyYAML. Use JSON input or install PyYAML in the current environment."
                ) from exc
            value = yaml.safe_load(source)
        else:
            raise

    if not isinstance(value, dict):
        raise SystemExit("Top-level artifact must be an object.")
    return value


def write_data(data: dict[str, Any], output: str | Path | None = None) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def compact_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def assertion_hash(assertion: dict[str, Any]) -> str:
    basis = {
        "subject": assertion.get("subject"),
        "predicate": assertion.get("predicate"),
        "object": assertion.get("object"),
    }
    raw = json.dumps(basis, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def user_answer_ids(canon: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for answer in as_list(canon.get("user_answers")):
        if isinstance(answer, dict) and answer.get("id"):
            ids.add(str(answer["id"]))
    return ids


def assertion_has_user_answer(assertion: dict[str, Any], canon: dict[str, Any]) -> bool:
    ua_ids = user_answer_ids(canon)
    derived = {str(item) for item in as_list(assertion.get("derived_from"))}
    if ua_ids.intersection(derived):
        return True
    assertion_id = assertion.get("id")
    for answer in as_list(canon.get("user_answers")):
        if not isinstance(answer, dict):
            continue
        applies_to = {str(item) for item in as_list(answer.get("applies_to"))}
        if assertion_id and str(assertion_id) in applies_to:
            return True
        if assertion_id and str(answer.get("applies_to_assertion")) == str(assertion_id):
            return True
    return False


def source_cell_manifest(canon: dict[str, Any]) -> dict[str, Any]:
    manifest = canon.get("source_cell_asset_manifest") or {}
    if isinstance(manifest, list):
        return manifest[0] if manifest and isinstance(manifest[0], dict) else {}
    return manifest if isinstance(manifest, dict) else {}


def source_cell_ready(canon: dict[str, Any]) -> bool:
    manifest = source_cell_manifest(canon)
    ready_state = str(manifest.get("ready_state", "")).lower()
    if ready_state in {"ready", "available", "attached", "created"}:
        return True
    asset_path = manifest.get("asset_path") or manifest.get("crop_id")
    return bool(asset_path and ready_state not in {"blocked", "blocked_until_crop_exists"})


def reference_preserve_requires_source_cell(canon: dict[str, Any]) -> bool:
    model = canon.get("reference_preserve_model") or {}
    if not isinstance(model, dict):
        return False
    mode = model.get("mode")
    source_cell = model.get("source_cell_asset") or {}
    required = bool(isinstance(source_cell, dict) and source_cell.get("required"))
    blocked_full_sheet = str(source_cell.get("full_sheet_only", "")).startswith("blocked")
    return mode in {"identity_preserve", "edit_target_preserve"} or required or blocked_full_sheet


def assertion_label(assertion: dict[str, Any]) -> str:
    subject = assertion.get("subject", "<subject>")
    predicate = assertion.get("predicate", "<predicate>")
    obj = compact_text(assertion.get("object"))
    return f"{subject}.{predicate}={obj}"
