# 5W1H Event Knowledge Hypergraph Extractor Skill

Language: [中文](README.md) | English

This repository contains a Codex skill for extracting **event-centric 5W1H knowledge hypergraphs** from news, military reports, policy text, incident briefings, and technical reports.

Core idea:

```text
one center event = one hyperedge
Who / What / When / Where / Why / How = nodes connected by that hyperedge
```

Default output:

```json
{
  "schema_version": "event-5w1h-hypergraph-v1",
  "text": "original input text",
  "sentences": {},
  "nodes": [],
  "hyperedges": []
}
```

## Features

- Center-event first: identify the essential event or center claim before extracting 5W1H.
- Event as hyperedge: each event is represented as one hyperedge.
- 5W1H as nodes: `who`, `what`, `when`, `where`, `why`, and `how` are nodes connected to the event hyperedge.
- Span offsets: every normal node includes `tag_start` and `tag_end`.
- Evidence traceability: nodes and hyperedges can point back to source sentences.
- Skill-guided extraction: a finite-state controller and Trigger/Action micro-skill library reduce noisy side-event extraction.

## Repository Layout

```text
.
├── 5w1h-extractor/          # installable Codex skill
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── examples/
│   └── minimal-output.json
├── prompts/
│   ├── install-with-ai.zh.md
│   └── install-with-ai.en.md
├── docs/
│   ├── INSTALL.md
│   └── INSTALL.en.md
├── README.md
├── README.en.md
└── LICENSE
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

Node:

```json
{
  "id": "N1",
  "text": "U.S. Department of State",
  "node_type": "who",
  "entity_type": "ORG",
  "tag_start": 0,
  "tag_end": 24,
  "evidence": ["S1"],
  "confidence": 0.95
}
```

Event hyperedge:

```json
{
  "id": "HE1",
  "event_type": "disclosure",
  "trigger": {
    "text": "disclosed",
    "tag_start": 25,
    "tag_end": 34
  },
  "summary": "The U.S. Department of State disclosed system details.",
  "nodes": {
    "who": ["N1"],
    "what": ["N2"],
    "when": [],
    "where": [],
    "why": [],
    "how": []
  },
  "evidence": ["S1"],
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
VALID: 2 node(s), 1 hyperedge(s)
```

## License

MIT License. See [LICENSE](LICENSE).
