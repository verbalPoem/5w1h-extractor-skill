# 5W1H Event Knowledge Hypergraph Extractor Skill

Language: [中文](README.md) | English

This repository contains Codex skills for extracting **event-centric and clustered-event 5W1H knowledge hypergraphs** from news, military reports, policy text, incident briefings, and technical reports.

It currently includes two installable skills:

- `5w1h-extractor`: single center-event 5W1H hypergraph extraction.
- `ceh-5w1h`: Clustered Event Hypergraph for 5W1H Extraction, with event clusters, event-level 5W1H hyperedges, and event-to-event relation hyperedges.

Core idea:

```text
one center event = one event hyperedge
related events = one event cluster
Who / What / When / Where / Why / How = nodes connected by event hyperedges
event-to-event links = relation_hyperedges
S1 / S2 = evidence sentence IDs
N1 / N2 = 5W1H node IDs
```

Default output:

```json
{
  "schema_version": "event-5w1h-hypergraph-v3",
  "sentences": {},
  "nodes": {},
  "hyperedges": []
}
```

Clustered-event output:

```json
{
  "schema_version": "ceh-5w1h-v1",
  "sentences": {},
  "nodes": {},
  "events": {},
  "event_hyperedges": {},
  "relation_hyperedges": {},
  "event_clusters": {}
}
```

## Features

- Center-event first: identify the essential event or center claim before extracting 5W1H.
- Event as hyperedge: each center event is represented as one `hyperedge`.
- 5W1H as nodes: `who`, `what`, `when`, `where`, `why`, and `how` are node groups.
- Indexed traceability: `S1/S2` preserve sentence evidence, and `N1/N2` preserve node references.
- Span offsets: normal nodes and triggers include `tag_start` and `tag_end`.
- Noise control: a finite-state controller and Trigger/Action micro-skill library reduce side-event extraction.

## Repository Layout

```text
.
|-- 5w1h-extractor/          # single center-event 5W1H skill
|   |-- SKILL.md
|   |-- agents/
|   |-- references/
|   `-- scripts/
|-- ceh-5w1h/                # clustered event 5W1H hypergraph skill
|   |-- SKILL.md
|   |-- agents/
|   |-- references/
|   `-- scripts/
|-- examples/
|   |-- minimal-output.json
|   `-- ceh-minimal-output.json
|-- prompts/
|   |-- install-with-ai.zh.md
|   `-- install-with-ai.en.md
|-- docs/
|   |-- INSTALL.md
|   `-- INSTALL.en.md
|-- README.md
|-- README.en.md
`-- LICENSE
```

Install `5w1h-extractor/` for single-event extraction, or `ceh-5w1h/` for clustered event hypergraph extraction.

## Quick Install

Windows PowerShell:

```powershell
Copy-Item -Recurse .\5w1h-extractor "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\ceh-5w1h "$env:USERPROFILE\.codex\skills\"
```

macOS / Linux:

```bash
cp -R ./5w1h-extractor ~/.codex/skills/
cp -R ./ceh-5w1h ~/.codex/skills/
```

Then start a new Codex thread and invoke:

```text
$5w1h-extractor extract the event 5W1H knowledge hypergraph from the following text:
...
```

Clustered-event skill:

```text
$ceh-5w1h extract clustered event 5W1H hypergraphs from the following text and draw a Mermaid diagram:
...
```

For detailed installation instructions, see [docs/INSTALL.en.md](docs/INSTALL.en.md).

## AI-Assisted Install

If you are using Codex, Claude Code, Cursor, Trae, or another coding agent that can read and write local files, copy this prompt to let the agent install the skill for you:

[prompts/install-with-ai.en.md](prompts/install-with-ai.en.md)

## Output Example

Sentence index:

```json
{
  "S1": {
    "text": "U.S. State Department disclosed nuclear delivery system details on Dec. 1.",
    "tag_start": 0,
    "tag_end": 74
  }
}
```

Node index:

```json
{
  "N1": {
    "node_type": "who",
    "text": "U.S. State Department",
    "entity_type": "ORG",
    "tag_start": 0,
    "tag_end": 21,
    "evidence": ["S1"],
    "confidence": 0.95
  }
}
```

Event hyperedge:

```json
{
  "id": "HE1",
  "event_type": "disclosure",
  "trigger": {
    "text": "disclosed",
    "tag_start": 22,
    "tag_end": 31
  },
  "summary": "U.S. State Department disclosed nuclear delivery system details on Dec. 1.",
  "nodes": {
    "who": ["N1"],
    "what": ["N2"],
    "when": ["N3"],
    "where": [],
    "why": [],
    "how": []
  },
  "evidence": ["S1"],
  "missing": ["where", "why", "how"],
  "confidence": 0.92
}
```

`tag_start` is the zero-based start character offset in the original text. `tag_end` is exclusive.

## Validate Output

```bash
python 5w1h-extractor/scripts/validate_output.py examples/minimal-output.json
python ceh-5w1h/scripts/validate_ceh_output.py examples/ceh-minimal-output.json
```

Expected:

```text
VALID: 1 sentence(s), 3 node(s), 1 hyperedge(s)
VALID: 1 cluster(s), 2 event(s), 2 event hyperedge(s), 1 relation hyperedge(s)
```

## License

MIT License. See [LICENSE](LICENSE).
