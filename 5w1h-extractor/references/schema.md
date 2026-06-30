# Event-5W1H Hypergraph Schema

Use this schema by default.

```json
{
  "schema_version": "event-5w1h-hypergraph-v1",
  "text": "original input text",
  "sentences": {},
  "nodes": [],
  "hyperedges": []
}
```

## Meaning

- `nodes`: extracted 5W1H nodes.
- `hyperedges`: event hyperedges.
- `hyperedges[].nodes`: the 5W1H nodes connected by that event hyperedge.

One event equals one hyperedge. The 5W1H fillers are nodes connected by that hyperedge.

```text
HE1 = event(trigger, who_nodes, what_nodes, when_nodes, where_nodes, why_nodes, how_nodes)
```

## Top-Level Fields

```json
{
  "schema_version": "event-5w1h-hypergraph-v1",
  "text": "original input text",
  "sentences": {
    "S1": {
      "text": "source sentence",
      "tag_start": 0,
      "tag_end": 20
    }
  },
  "nodes": [],
  "hyperedges": []
}
```

`text` should preserve the original input used for offset calculation. If the input is too long and the user did not ask for the full text, `text` may be omitted only when every node still has reliable offsets relative to the provided text chunk.

## Node Object

Each extracted 5W1H span becomes one node.

```json
{
  "id": "N1",
  "text": "source span",
  "node_type": "who|what|when|where|why|how",
  "entity_type": "ORG|PERSON|COUNTRY|WEAPON|SYSTEM|PLATFORM|TIME|PLACE|CAUSE|PURPOSE|METHOD|CAPABILITY|CLAIM|QUANTITY|OTHER",
  "tag_start": 0,
  "tag_end": 0,
  "evidence": ["S1"],
  "confidence": 0.0
}
```

Rules:

- `node_type` must be one of `who`, `what`, `when`, `where`, `why`, `how`.
- `tag_start` is the zero-based character offset of the first character in `text`.
- `tag_end` is the zero-based exclusive end offset.
- `text == original_text[tag_start:tag_end]` should hold whenever offsets are available.
- Use `null` for `tag_start` and `tag_end` only when exact offsets cannot be recovered.
- Do not create nodes for side events.

## Hyperedge Object

Each center event becomes one hyperedge.

```json
{
  "id": "HE1",
  "event_type": "disclosure|deployment|test|construction|exhibition|casualty|announcement|capability|briefing|risk_demonstration|other",
  "trigger": {
    "text": "source trigger",
    "tag_start": 0,
    "tag_end": 0
  },
  "summary": "one concise event sentence",
  "nodes": {
    "who": ["N1"],
    "what": ["N2"],
    "when": ["N3"],
    "where": [],
    "why": [],
    "how": ["N4"]
  },
  "evidence": ["S1"],
  "confidence": 0.0
}
```

Rules:

- Use `nodes`, not `roles`, for the 5W1H connections inside a hyperedge.
- Each ID in `hyperedges[].nodes.*` must exist in top-level `nodes`.
- The same node may connect to multiple hyperedges only when the source text truly reuses the same 5W1H filler for multiple independent events.
- Empty 5W1H groups must be `[]`.
- Do not put explanatory labels or role schemas in output.

## Optional Metadata

Use these fields only when useful:

```json
{
  "document_id": "D1",
  "discarded": [
    {
      "text": "side event span",
      "reason": "side_event|background|unsupported|wrong_event",
      "tag_start": 0,
      "tag_end": 0
    }
  ]
}
```

Keep optional metadata short. The core output is `nodes + hyperedges`.
