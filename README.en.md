# 5W1H Event Knowledge Hypergraph Extractor Skill

Language: [中文](README.md) | English

This repository contains a Codex skill for extracting **event-centric 5W1H knowledge hypergraphs** from news, military reports, policy text, incident briefings, and technical reports.

Core idea:

```text
one center event = one hyperedge
Who / What / When / Where / Why / How = nodes connected by that hyperedge
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
|-- 5w1h-extractor/          # installable Codex skill
|   |-- SKILL.md
|   |-- agents/
|   |-- references/
|   `-- scripts/
|-- examples/
|   `-- minimal-output.json
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

The installable skill is the `5w1h-extractor/` folder.

## Quick Install

Windows PowerShell:

```powershell
Copy-Item -Recurse .\5w1h-extractor "$env:USERPROFILE\.codex\skills\"
```

macOS / Linux:

```bash
cp -R ./5w1h-extractor ~/.codex/skills/
```

Then start a new Codex thread and invoke:

```text
$5w1h-extractor extract the event 5W1H knowledge hypergraph from the following text:
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
```

Expected:

```text
VALID: 1 sentence(s), 3 node(s), 1 hyperedge(s)
```

## License

MIT License. See [LICENSE](LICENSE).
