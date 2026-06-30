# Evaluation Plan

Use this file when the user wants to turn the skill into an experiment, report, or paper section.

## Baselines

Compare Event-5W1H-HG against:

1. Generic direct 5W1H prompt.
2. Few-shot 5W1H prompt.
3. Event extraction prompt without hyperedge projection.
4. Event-5W1H-HG without micro-skill library.
5. Event-5W1H-HG without center-lock validation.

## Metrics

### Center Event Accuracy

Whether the extracted center event matches the document's essential event or claim.

Suggested labels:

- correct
- partially correct
- side event
- over-split
- missed

### Node-Type F1

Compute precision, recall, and F1 for `who`, `what`, `when`, `where`, `why`, and `how`.

Use relaxed semantic matching when exact span offsets are not the objective.

### Hyperedge Quality

Evaluate whether the output forms one coherent event hyperedge:

- predicate correctness
- node-type correctness
- node attachment correctness
- no side-event nodes
- offset correctness
- readable event text

### Noise Rate

Measure side-event drift:

```text
noise_rate = invalid_or_side_event_nodes / all_extracted_nodes
```

### Compactness

Measure whether the output is usable for downstream graph construction:

```text
compactness = useful_event_nodes / total_json_fields
```

This is not a standard metric; use it as an analysis signal, not the main result.

### Stability

Run the same inputs across multiple LLMs or temperatures.

Report:

- center event agreement
- node-type agreement
- hyperedge predicate agreement
- invalid JSON rate

## Ablation Table

Recommended ablations:

| Method | Center Lock | Micro-Skills | Hyperedge Projection | Expected Weakness |
|---|---|---|---|---|
| Direct Prompt | No | No | No | noisy spans, side events |
| Few-shot Prompt | Partial | No | No | dataset overfit |
| FSM Only | Yes | No | Partial | misses domain-specific cues |
| Skill Library Only | No | Yes | Partial | applies rules to wrong event |
| Event-5W1H-HG | Yes | Yes | Yes | full method |

## Error Taxonomy

Track these errors:

- center-event drift
- over-splitting one event into many hyperedges
- attribution confusion
- inventory explosion
- why/how confusion
- background promoted as event
- unsupported node
- wrong tag_start/tag_end
- unreadable hyperedge

## Suggested Paper Section Names

- Method: Center-Event Skill-Guided 5W1H Hypergraph Extraction
- Finite-State Extraction Controller
- Trigger/Action Micro-Skill Library
- Hyperedge Projection Schema
- Experiments and Ablations
