#!/usr/bin/env python3
"""Validate indexed Event-5W1H hypergraph JSON.

Usage:
  python validate_output.py output.json
  type output.json | python validate_output.py -
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "event-5w1h-hypergraph-v3"
NODE_GROUPS = ("who", "what", "when", "where", "why", "how")
REQUIRED_NODE_KEYS = ("node_type", "text", "entity_type", "tag_start", "tag_end", "evidence", "confidence")


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


def validate_sentence(sentence_id: str, sentence: Any) -> None:
    if not re.fullmatch(r"S[1-9][0-9]*", sentence_id):
        fail(f"invalid sentence id {sentence_id}")
    obj = require_dict(sentence, f"sentences.{sentence_id}")
    for key in ("text", "tag_start", "tag_end"):
        if key not in obj:
            fail(f"sentences.{sentence_id}.{key} is required")
    validate_offset(obj["tag_start"], f"sentences.{sentence_id}.tag_start")
    validate_offset(obj["tag_end"], f"sentences.{sentence_id}.tag_end")
    start = obj["tag_start"]
    end = obj["tag_end"]
    if start is not None and end is not None and end < start:
        fail(f"sentences.{sentence_id}.tag_end must be >= tag_start")


def validate_node(node_id: str, node: Any, sentence_ids: set[str]) -> None:
    if not re.fullmatch(r"N[1-9][0-9]*", node_id):
        fail(f"invalid node id {node_id}")
    obj = require_dict(node, f"nodes.{node_id}")
    for key in REQUIRED_NODE_KEYS:
        if key not in obj:
            fail(f"nodes.{node_id}.{key} is required")
    if obj["node_type"] not in NODE_GROUPS:
        fail(f"nodes.{node_id}.node_type must be one of {', '.join(NODE_GROUPS)}")
    validate_offset(obj["tag_start"], f"nodes.{node_id}.tag_start")
    validate_offset(obj["tag_end"], f"nodes.{node_id}.tag_end")
    start = obj["tag_start"]
    end = obj["tag_end"]
    if start is not None and end is not None and end < start:
        fail(f"nodes.{node_id}.tag_end must be >= tag_start")
    for ev in require_list(obj["evidence"], f"nodes.{node_id}.evidence"):
        if ev not in sentence_ids:
            fail(f"nodes.{node_id}.evidence references unknown sentence id {ev}")


def validate_trigger(trigger: Any, path: str) -> None:
    obj = require_dict(trigger, path)
    for key in ("text", "tag_start", "tag_end"):
        if key not in obj:
            fail(f"{path}.{key} is required")
    validate_offset(obj["tag_start"], f"{path}.tag_start")
    validate_offset(obj["tag_end"], f"{path}.tag_end")
    start = obj["tag_start"]
    end = obj["tag_end"]
    if start is not None and end is not None and end < start:
        fail(f"{path}.tag_end must be >= tag_start")


def validate_hyperedge(edge: Any, idx: int, node_ids: set[str], sentence_ids: set[str]) -> None:
    path = f"hyperedges[{idx}]"
    obj = require_dict(edge, path)
    for key in ("id", "event_type", "trigger", "summary", "nodes", "evidence", "missing", "confidence"):
        if key not in obj:
            fail(f"{path}.{key} is required")
    validate_trigger(obj["trigger"], f"{path}.trigger")
    nodes = require_dict(obj["nodes"], f"{path}.nodes")
    for group in NODE_GROUPS:
        if group not in nodes:
            fail(f"{path}.nodes.{group} is required")
        for ref in require_list(nodes[group], f"{path}.nodes.{group}"):
            if ref not in node_ids:
                fail(f"{path}.nodes.{group} references unknown node id {ref}")
    for ev in require_list(obj["evidence"], f"{path}.evidence"):
        if ev not in sentence_ids:
            fail(f"{path}.evidence references unknown sentence id {ev}")
    require_list(obj["missing"], f"{path}.missing")


def main() -> None:
    if len(sys.argv) != 2:
        fail("pass a JSON file path or '-' for stdin")
    data = require_dict(load_json(sys.argv[1]), "$")
    if data.get("schema_version") != SCHEMA_VERSION:
        fail(f"schema_version must be {SCHEMA_VERSION}")
    sentences = require_dict(data.get("sentences"), "sentences")
    nodes = require_dict(data.get("nodes"), "nodes")
    hyperedges = require_list(data.get("hyperedges"), "hyperedges")
    if not hyperedges:
        fail("hyperedges must not be empty")

    sentence_ids = set(sentences.keys())
    node_ids = set(nodes.keys())
    for sentence_id, sentence in sentences.items():
        validate_sentence(sentence_id, sentence)
    for node_id, node in nodes.items():
        validate_node(node_id, node, sentence_ids)
    for idx, edge in enumerate(hyperedges):
        validate_hyperedge(edge, idx, node_ids, sentence_ids)
    print(f"VALID: {len(sentences)} sentence(s), {len(nodes)} node(s), {len(hyperedges)} hyperedge(s)")


if __name__ == "__main__":
    main()
