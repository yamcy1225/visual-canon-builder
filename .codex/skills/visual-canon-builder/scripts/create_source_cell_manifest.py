#!/usr/bin/env python3
"""Create a source-cell manifest for exact visual preservation workflows."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import write_data


def parse_bbox(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {
            "x": "needs_user_or_script",
            "y": "needs_user_or_script",
            "width": "needs_user_or_script",
            "height": "needs_user_or_script",
        }
    parts = [part.strip() for part in raw.split(",")]
    if len(parts) != 4:
        raise SystemExit("--bbox must be formatted as x,y,width,height")
    try:
        x, y, width, height = [int(part) for part in parts]
    except ValueError as exc:
        raise SystemExit("--bbox values must be integers") from exc
    return {"x": x, "y": y, "width": width, "height": height}


def ready_state(asset_path: str | None, bbox: dict[str, Any]) -> str:
    bbox_ready = all(isinstance(value, int) for value in bbox.values())
    if asset_path and Path(asset_path).exists():
        return "ready"
    if asset_path or bbox_ready:
        return "coordinates_ready_crop_not_verified"
    return "blocked_until_crop_exists"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, help="Crop manifest id, e.g. CROP_SampleMascot_FrontFullBody_001")
    parser.add_argument("--source-image-id", required=True, help="Source image id, e.g. Image_SampleMascot_001")
    parser.add_argument("--label", default="front_full_body", help="Source region label")
    parser.add_argument("--bbox", help="Optional crop box: x,y,width,height")
    parser.add_argument("--asset-path", help="Path or attachment id for the actual cropped source cell")
    parser.add_argument("--role", action="append", default=[], help="Role; repeatable")
    parser.add_argument("--priority", action="append", default=[], help="Preservation priority; repeatable")
    parser.add_argument("-o", "--output", help="Output path; stdout when omitted")
    args = parser.parse_args()

    bbox = parse_bbox(args.bbox)
    manifest = {
        "source_cell_asset_manifest": {
            "id": args.id,
            "crop_id": args.id,
            "source_image_id": args.source_image_id,
            "source_region": {
                "label": args.label,
                "bbox": bbox,
            },
            "asset_path": args.asset_path,
            "role": args.role
            or [
                "identity_anchor",
                "style_anchor",
                "proportion_anchor",
            ],
            "preservation_priority": args.priority
            or [
                "silhouette",
                "head_body_ratio",
                "limb_length",
                "line_weight",
                "detail_density",
            ],
            "ready_state": ready_state(args.asset_path, bbox),
        }
    }
    write_data(manifest, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
