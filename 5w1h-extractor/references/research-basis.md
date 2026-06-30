# Research Basis

This skill is designed as an original 5W1H-to-knowledge-hypergraph workflow, not a dataset-specific prompt.

## External Ideas Used as Inspiration

Hyper-KGGen argues that knowledge hypergraph generation benefits from:

- Coarse-to-fine extraction rather than direct one-shot generation.
- Skill-driven extraction rules.
- A feedback loop that captures unstable extractions and turns them into reusable skills.
- Hyperedges that preserve n-ary relations instead of flattening everything into binary triples.

This skill adapts those ideas to event-as-hyperedge 5W1H extraction.

## Original Method: Event-5W1H-HG

Event-5W1H-HG has four layers:

1. **Center-event controller**: choose the essential event or claim before extracting nodes.
2. **Span-to-node extractor**: extract 5W1H source spans as nodes with `tag_start` and `tag_end`.
3. **Trigger/action micro-skill library**: apply domain rules such as inventory disclosure, risk demonstration, exhibition capability, test evaluation, construction deadline, casualty report, and first deployment.
4. **Event hyperedge projection**: connect the 5W1H nodes through one event hyperedge.

## Why This Is Not Just Span Tagging

Traditional span tagging can identify 5W1H mentions, but it does not guarantee that all mentions attach to the same center event.

Event-5W1H-HG adds:

- Center-event locking.
- Node attachment tests.
- Side-event rejection.
- Event-as-hyperedge output.
- Micro-skill feedback for repeated failure patterns.

## Paper Angle

Potential paper contribution:

```text
We propose Event-5W1H-HG, a skill-guided framework for event-centric knowledge hypergraph generation. The method represents each center event as a hyperedge and extracts Who, What, When, Where, Why, and How as connected nodes with source offsets. Compared with generic prompting, it reduces side-event drift and produces auditable n-ary hypergraph structures.
```

## References

- Hyper-KGGen: https://arxiv.org/html/2602.19543
- Hyper-Extract: https://github.com/yifanfeng97/Hyper-Extract
