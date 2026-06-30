---
name: 5w1h-extractor
description: Center-event 5W1H extractor and knowledge-hypergraph frame builder for Chinese or multilingual news, military, policy, incident, technical, and report text. Use when asked to extract who/what/when/where/why/how, identify the essential event or claim, create evidence-backed event frames, generate n-ary hyperedges, reduce noisy side-event extraction, build data for knowledge hypergraphs, or apply skill-guided finite-state extraction.
---

# Event 5W1H Hypergraph Extractor

## Overview

Use this skill as a center-event extractor, not as a general information highlighter.

The method is **Event-5W1H-HG**: event-as-hyperedge 5W1H knowledge hypergraph generation.

Core idea: lock one essential event or claim, extract 5W1H spans as indexed nodes, then connect those node IDs with one event hyperedge. Use micro-skills only when their trigger fits the current text.

Default output is valid JSON only. Do not use Markdown tables unless the user asks for an explanation.

## Resource Loading

Always read:

- `references/schema.md` before producing JSON.
- `references/state-machine.md` when input is long, noisy, or multi-event.
- `references/skill-library.md` before extracting military, policy, incident, deployment, test, construction, exhibition, or casualty reports.
- `references/quality-checks.md` before final output.

Read as needed:

- `references/extraction-rules.md` for ambiguous 5W1H node types or batch splitting.
- `references/evaluation.md` when designing experiments, ablations, metrics, or paper sections.
- `references/research-basis.md` when explaining why the skill is designed this way.

## Default Workflow

1. Segment the text into independent snippets only at natural document boundaries. Do not split every sentence.
2. Score candidate events and select one center event per snippet.
3. Extract 5W1H spans into indexed `nodes` with `tag_start`, `tag_end`, and sentence evidence IDs.
4. Attach nodes to the selected event only if they pass the center-lock test.
5. Apply relevant trigger/action micro-skills from `skill-library.md`.
6. Project the event into one hyperedge whose `nodes` field connects `who/what/when/where/why/how` to node IDs.
7. Validate offsets, source support, missing node groups, discarded side events, and compactness.

## Center-Lock Test

Keep a candidate node only if all four checks pass:

```text
has_evidence && fits_5w1h_node_type && attaches_to_center_event && improves_hyperedge
```

If a candidate fails, put it in optional top-level `discarded` only when it is important enough to explain. Otherwise omit it.

## Default Output Contract

Use `schema_version: "event-5w1h-hypergraph-v3"`.

```json
{
  "schema_version": "event-5w1h-hypergraph-v3",
  "sentences": {},
  "nodes": {},
  "hyperedges": []
}
```

Default output must keep `sentences` and indexed `nodes`; they are needed for evidence tracing and graph construction.

Each indexed node contains:

```json
{
  "node_type": "who|what|when|where|why|how",
  "text": "source span",
  "entity_type": "ORG|PERSON|COUNTRY|WEAPON|SYSTEM|TIME|PLACE|CAUSE|METHOD|CLAIM|QUANTITY|OTHER",
  "tag_start": 0,
  "tag_end": 0,
  "evidence": ["S1"],
  "confidence": 0.0
}
```

Each hyperedge contains one event and a `nodes` map of node ID lists:

```json
{
  "id": "HE1",
  "event_type": "disclosure|deployment|test|construction|exhibition|casualty|announcement|other",
  "trigger": {
    "text": "source trigger",
    "tag_start": 0,
    "tag_end": 0
  },
  "summary": "one concise event sentence",
  "nodes": {
    "who": ["N1"],
    "what": [],
    "when": [],
    "where": [],
    "why": [],
    "how": []
  },
  "evidence": ["S1"],
  "missing": [],
  "confidence": 0.0
}
```

`tag_start` and `tag_end` are zero-based character offsets in `text`; `tag_end` is exclusive.
Offsets are relative to the user-provided input text. Use `sentences.S1`, `sentences.S2`, etc. for sentence-level evidence.

## Output Modes

Default:

- Return only the JSON object.
- Extract main event hyperedges only.
- Keep `sentences`, indexed `nodes`, and `hyperedges`.

When the user asks for diagnosis, method, or paper writing:

- Also explain the state path and applied micro-skills.
- Use `references/evaluation.md` for experiment design.

When the user asks for graph database import:

- Add a separate `node_index` / graph-database export after the default hypergraph JSON.
- Do not replace the default event frame.

## Non-Negotiables

- Do not enumerate all side events.
- Do not convert one event into many unrelated triples.
- Do not treat the news source as `who` unless the reporting act is the center event.
- Do not fill `why` from consequences.
- Do not fill `how` from motives.
- Preserve source wording for weapons, organizations, dates, places, quantities, and model names.
- Use `[]` for missing 5W1H node groups.
- Every node must include `tag_start`, `tag_end`, and `evidence`; use `null` offsets only when the text was summarized or OCR-damaged and exact offsets cannot be recovered.
