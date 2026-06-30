# Quality Checks

## Hyperedge Checks

- Exactly one event hyperedge exists for each independent center event.
- `hyperedges[].summary` is short, factual, and event-like.
- `hyperedges[].trigger.text` appears in the original text when offsets are available.
- `hyperedges[].nodes` contains exactly six keys: `who`, `what`, `when`, `where`, `why`, `how`.
- Every node ID referenced by a hyperedge exists in top-level `nodes`.
- Side events are not promoted unless the input is a true batch.

## Node Checks

- Every extracted 5W1H span is represented as a node.
- Every node has `id`, `text`, `node_type`, `entity_type`, `tag_start`, `tag_end`, `evidence`, and `confidence`.
- `node_type` is one of `who`, `what`, `when`, `where`, `why`, `how`.
- `tag_start` and `tag_end` are zero-based offsets; `tag_end` is exclusive.
- When original `text` is present, `node.text == text[tag_start:tag_end]`.
- Do not create nodes for background facts or side events.

## Role Semantics

- `who` is not a news outlet unless reporting is the event.
- `what` is the central object, action, claim, system, or quantity.
- `when` scopes the event time.
- `where` scopes the event location.
- `why` is cause or purpose, not consequence.
- `how` is method or mechanism, not motive.

## Readability

- Default JSON is `text + sentences + nodes + hyperedges`.
- Use `nodes`, not `roles`, inside each hyperedge.
- Do not output explanatory labels, role schemas, or bulky graph-import tables by default.
- Repeated technical counts are grouped where possible.
- Optional `discarded` should explain only important rejected side facts.

## Failure Patterns

Common bad outputs:

- Enumerating every weapon model as its own event hyperedge.
- Treating background future plans as the center event.
- Filling `why` with a result or capability advantage.
- Filling `how` with a motivation.
- Omitting offsets for normal source spans.
- Using `roles` instead of `nodes` in a hyperedge.
