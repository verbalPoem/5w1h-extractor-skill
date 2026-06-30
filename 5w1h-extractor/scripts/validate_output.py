#!/usr/bin/env python3
"""Validate Event-5W1H hypergraph JSON.

Usage:
  python validate_output.py output.json
  type output.json | python validate_output.py -
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "event-5w1h-hypergraph-v1"
NODE_TYPES = ("who", "what", "when", "where", "why", "how")
REQUIRED_NODE_KEYS = (
    "id",
    "text",
    "node_type",
    "entity_type",
    "tag_start",
    "tag_end",
    "evidence",
    "confidence",
)


def fail(message: str) -> None:
    print(f"INVALID: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_dict(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{path} must be an object")
    return value


def require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        fail(f"{path} must be a list")
    return value


def load_json(arg: str) -> Any:
    if arg == "-":
        return json.load(sys.stdin)
    with Path(arg).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_offset(value: Any, path: str) -> None:
    if value is None:
        return
    if not isinstance(value, int) or value < 0:
        fail(f"{path} must be a non-negative integer or null")


def validate_node(node: Any, idx: int, original_text: str | None) -> str:
    path = f"nodes[{idx}]"
    obj = require_dict(node, path)
    for key in REQUIRED_NODE_KEYS:
        if key not in obj:
            fail(f"{path}.{key} is required")
    if obj["node_type"] not in NODE_TYPES:
        fail(f"{path}.node_type must be one of {', '.join(NODE_TYPES)}")
    validate_offset(obj["tag_start"], f"{path}.tag_start")
    validate_offset(obj["tag_end"], f"{path}.tag_end")
    require_list(obj["evidence"], f"{path}.evidence")

    start = obj["tag_start"]
    end = obj["tag_end"]
    text = obj["text"]
    if start is not None and end is not None:
        if end < start:
            fail(f"{path}.tag_end must be >= tag_start")
        if original_text is not None:
            if end > len(original_text):
                fail(f"{path}.tag_end exceeds text length")
            if original_text[start:end] != text:
                fail(f"{path}.text does not match text[tag_start:tag_end]")
    return str(obj["id"])


def validate_trigger(trigger: Any, path: str, original_text: str | None) -> None:
    obj = require_dict(trigger, path)
    for key in ("text", "tag_start", "tag_end"):
        if key not in obj:
            fail(f"{path}.{key} is required")
    validate_offset(obj["tag_start"], f"{path}.tag_start")
    validate_offset(obj["tag_end"], f"{path}.tag_end")
    start = obj["tag_start"]
    end = obj["tag_end"]
    if start is not None and end is not None:
        if end < start:
            fail(f"{path}.tag_end must be >= tag_start")
        if original_text is not None:
            if end > len(original_text):
                fail(f"{path}.tag_end exceeds text length")
            if original_text[start:end] != obj["text"]:
                fail(f"{path}.text does not match text[tag_start:tag_end]")


def validate_hyperedge(edge: Any, idx: int, node_ids: set[str], original_text: str | None) -> None:
    path = f"hyperedges[{idx}]"
    obj = require_dict(edge, path)
    for key in ("id", "event_type", "trigger", "summary", "nodes", "evidence", "confidence"):
        if key not in obj:
            fail(f"{path}.{key} is required")
    validate_trigger(obj["trigger"], f"{path}.trigger", original_text)
    require_list(obj["evidence"], f"{path}.evidence")

    nodes = require_dict(obj["nodes"], f"{path}.nodes")
    for node_type in NODE_TYPES:
        if node_type not in nodes:
            fail(f"{path}.nodes.{node_type} is required")
        refs = require_list(nodes[node_type], f"{path}.nodes.{node_type}")
        for ref in refs:
            if str(ref) not in node_ids:
                fail(f"{path}.nodes.{node_type} references unknown node id {ref}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("pass a JSON file path or '-' for stdin")
    data = require_dict(load_json(sys.argv[1]), "$")
    if data.get("schema_version") != SCHEMA_VERSION:
        fail(f"schema_version must be {SCHEMA_VERSION}")

    original_text = data.get("text")
    if original_text is not None and not isinstance(original_text, str):
        fail("text must be a string when present")

    require_dict(data.get("sentences", {}), "sentences")
    nodes = require_list(data.get("nodes"), "nodes")
    hyperedges = require_list(data.get("hyperedges"), "hyperedges")
    if not hyperedges:
        fail("hyperedges must not be empty")

    node_ids: set[str] = set()
    for idx, node in enumerate(nodes):
        node_id = validate_node(node, idx, original_text)
        if node_id in node_ids:
            fail(f"duplicate node id {node_id}")
        node_ids.add(node_id)

    for idx, edge in enumerate(hyperedges):
        validate_hyperedge(edge, idx, node_ids, original_text)

    print(f"VALID: {len(nodes)} node(s), {len(hyperedges)} hyperedge(s)")


if __name__ == "__main__":
    main()
