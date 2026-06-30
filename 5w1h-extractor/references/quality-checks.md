# Quality Checks

## Top-Level Checks

- Default JSON contains `schema_version`, `sentences`, `nodes`, and `hyperedges`.
- `schema_version` is `event-5w1h-hypergraph-v3`.
- Keep `sentences` and `nodes`; they are required for evidence tracing and graph construction.
- Do not include the full original text unless the user asks for audit mode.

## Sentence Checks

- Sentence IDs use `S1`, `S2`, ...
- Every sentence object has `text`, `tag_start`, and `tag_end`.
- Every sentence referenced by a node or hyperedge exists in `sentences`.
- Do not create unused sentence entries.

## Node Checks

- Node IDs use `N1`, `N2`, ...
- Every node has `node_type`, `text`, `entity_type`, `tag_start`, `tag_end`, `evidence`, and `confidence`.
- `node_type` is one of `who`, `what`, `when`, `where`, `why`, `how`.
- `tag_start` and `tag_end` are zero-based offsets; `tag_end` is exclusive.
- Every evidence ID in a node exists in `sentences`.
- Do not create nodes for background facts or side events.

## Hyperedge Checks

- Exactly one event hyperedge exists for each independent center event.
- `hyperedges[].summary` is short, factual, and event-like.
- `hyperedges[].trigger.text` appears in the source text when offsets are available.
- `hyperedges[].nodes` contains exactly six keys: `who`, `what`, `when`, `where`, `why`, `how`.
- Every node ID referenced by a hyperedge exists in top-level `nodes`.
- Every hyperedge evidence ID exists in `sentences`.
- Side events are not promoted unless the input is a true batch.

## Role Semantics

- `who` is not a news outlet unless reporting is the event.
- `what` is the central object, action, claim, system, or grouped quantity.
- `when` scopes the event time.
- `where` scopes the event location.
- `why` is cause or purpose, not consequence.
- `how` is method or mechanism, not motive.

## Readability

- Use indexed `nodes`, not repeated embedded node objects.
- Use sentence IDs like `S1`, not repeated long evidence strings inside every node.
- Repeated technical counts should be grouped into a few high-value `what` nodes.
- If a field is missing, use `[]` in the node group and list the group name in `missing`.

## Failure Patterns

Common bad outputs:

- Removing `N1/N2` node IDs or `S1/S2` evidence IDs.
- Enumerating every weapon model as its own event hyperedge.
- Treating background future plans as the center event.
- Filling `why` with a result or capability advantage.
- Filling `how` with a motivation.
- Omitting offsets for normal source spans.
- Using any alternative field name instead of `nodes` in a hyperedge.
