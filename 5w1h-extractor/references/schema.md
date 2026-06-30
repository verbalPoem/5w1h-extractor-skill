# Event-5W1H Hypergraph Schema

Use this indexed schema by default.

```json
{
  "schema_version": "event-5w1h-hypergraph-v3",
  "sentences": {},
  "nodes": {},
  "hyperedges": []
}
```

## Meaning

- One center event equals one hyperedge.
- `sentences` stores evidence sentences as `S1`, `S2`, ...
- `nodes` stores 5W1H nodes as `N1`, `N2`, ...
- `hyperedges[].nodes` connects each 5W1H group to node IDs.

```text
HE1 = event(trigger, who[N*], what[N*], when[N*], where[N*], why[N*], how[N*])
```

## Sentence Object

```json
{
  "S1": {
    "text": "source sentence",
    "tag_start": 0,
    "tag_end": 20
  }
}
```

Rules:

- Sentence IDs must be stable and compact: `S1`, `S2`, ...
- `tag_start` and `tag_end` are offsets in the original user-provided text.
- Keep sentences only when they support at least one node or hyperedge.

## Node Object

`nodes` is an object keyed by node ID:

```json
{
  "N1": {
    "node_type": "who|what|when|where|why|how",
    "text": "source span",
    "entity_type": "ORG|PERSON|COUNTRY|WEAPON|SYSTEM|PLATFORM|TIME|PLACE|CAUSE|PURPOSE|METHOD|CAPABILITY|CLAIM|QUANTITY|OTHER",
    "tag_start": 0,
    "tag_end": 0,
    "evidence": ["S1"],
    "confidence": 0.0
  }
}
```

Rules:

- Node IDs must be stable and compact: `N1`, `N2`, ...
- `node_type` must be one of `who`, `what`, `when`, `where`, `why`, `how`.
- `tag_start` is the zero-based character offset of the first character in the original input text.
- `tag_end` is the zero-based exclusive end offset.
- `evidence` must reference sentence IDs from `sentences`.
- Use `null` for `tag_start` and `tag_end` only when exact offsets cannot be recovered.

## Hyperedge Object

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
    "how": []
  },
  "evidence": ["S1"],
  "missing": [],
  "confidence": 0.0
}
```

Rules:

- Use `nodes` as the only field name for 5W1H connections.
- Values inside `hyperedges[].nodes.*` must be node IDs from top-level `nodes`.
- `hyperedges[].evidence` must reference sentence IDs from `sentences`.
- Empty 5W1H groups must be `[]`.
- List missing 5W1H groups in `missing`.

## Readability Rules

- Keep `sentences` short: only evidence sentences, not the whole document split into every possible fragment.
- Keep `nodes` grouped by compact IDs, not as a long array with repeated `id` fields.
- Merge long inventories into grouped `what` nodes when possible.
- Do not output explanatory labels, auxiliary schemas, or graph-database tables by default.
- Do not create side-event hyperedges unless the text contains independent snippets.
