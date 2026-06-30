# Event-5W1H-HG Finite-State Controller

Use this controller for every non-trivial extraction. The goal is to construct event hyperedges that connect 5W1H nodes.

```text
S0_SEGMENT
  -> S1_CENTER_SCORE
  -> S2_SKELETON
  -> S3_NODE_EXTRACT
  -> S4_SKILL_APPLY
  -> S5_HYPEREDGE
  -> S6_VALIDATE
  -> S7_FEEDBACK
```

## State Duties

### S0_SEGMENT

Decide whether the input is a single document or a batch of independent snippets.

Split only at strong boundaries:

- blank lines between unrelated news briefs
- headline/source changes
- major actor/event shifts
- user-provided list items

Do not split every sentence.

### S1_CENTER_SCORE

Create candidate center events and score them:

```text
salience = trigger_strength + first_sentence_weight + argument_density + repetition + user_focus - side_event_penalty
```

Select one center event per snippet. If two candidates compete, choose the event that best explains the paragraph's essential content.

### S2_SKELETON

Build the coarse event skeleton:

```text
WHO / source / actor -> PREDICATE(trigger) -> WHAT / object / claim
```

Do not attach time, place, reason, or method yet.

### S3_NODE_EXTRACT

Extract 5W1H spans as nodes. Every normal node must have `tag_start` and `tag_end`.

Attach a node only if it passes the center-lock test:

```text
has_evidence && fits_5w1h_node_type && attaches_to_center_event && improves_hyperedge
```

### S4_SKILL_APPLY

Check `skill-library.md` for trigger/action micro-skills. Apply only skills whose trigger is explicit in the source.

Examples:

- inventory disclosure
- risk demonstration
- exhibition capability
- operational test
- construction deadline
- casualty report

### S5_HYPEREDGE

Project the accepted event frame into one event hyperedge:

```text
HE(event, who, what, when, where, why, how)
```

Keep one hyperedge per center event. Use `hyperedges[].nodes`, not `roles`, to connect the six 5W1H node groups.

### S6_VALIDATE

Run quality checks:

- exactly one center event per hyperedge
- every node has evidence
- every normal node has `tag_start` and `tag_end`
- no side event is promoted
- why/how are separated
- output follows schema

### S7_FEEDBACK

Record:

- applied micro-skills
- missing node groups
- discarded high-risk side candidates
- unstable cues that may need future skill updates

## Rollback Rules

- If `what` does not match the trigger, go back to `S1_CENTER_SCORE`.
- If `who` is only a news outlet but reporting is not the event, repair `who`.
- If `why` is actually a result, move it to `what` or discard it.
- If `how` is actually a motive, move it to `why`.
- If a technical detail creates a new event, discard it unless the snippet's center changes.

## Main Event Selection Priority

1. User-specified target event.
2. First-sentence or headline event.
3. Repeated central claim.
4. Event with the densest valid 5W1H attachments.
5. Event that best supports one coherent hyperedge.
