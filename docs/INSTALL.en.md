# Installation

Language: [中文](INSTALL.md) | English

## Option 1: Manual Install

1. Download or clone this repository.
2. Locate the `5w1h-extractor/` or `ceh-5w1h/` folder.
3. Copy the skill folder you need into your Codex skills directory.

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

4. Start a new Codex thread.
5. Invoke:

```text
$5w1h-extractor extract the event 5W1H knowledge hypergraph from the following text:
...
```

Clustered-event skill:

```text
$ceh-5w1h extract clustered event 5W1H hypergraphs from the following text:
...
```

## Option 2: AI-Assisted Install

If you are using Codex, Claude Code, Cursor, Trae, or another local coding agent, open:

```text
prompts/install-with-ai.en.md
```

Send the prompt to the agent. It should:

1. Locate the `5w1h-extractor/` and/or `ceh-5w1h/` folder in this repository.
2. Copy it into the current user's `.codex/skills/` directory.
3. Check whether `SKILL.md` exists.
4. Tell you to start a new thread and invoke `$5w1h-extractor`.

## Check Installation

The final path should look like:

Windows:

```text
C:\Users\YOUR_NAME\.codex\skills\5w1h-extractor\SKILL.md
C:\Users\YOUR_NAME\.codex\skills\ceh-5w1h\SKILL.md
```

macOS / Linux:

```text
~/.codex/skills/5w1h-extractor/SKILL.md
~/.codex/skills/ceh-5w1h/SKILL.md
```

If a new Codex thread recognizes `$5w1h-extractor` or `$ceh-5w1h`, the installation is successful.

## Validate Output

This repository includes a JSON validator:

```bash
python 5w1h-extractor/scripts/validate_output.py examples/minimal-output.json
python ceh-5w1h/scripts/validate_ceh_output.py examples/ceh-minimal-output.json
```

Expected:

```text
VALID: 1 sentence(s), 3 node(s), 1 hyperedge(s)
VALID: 1 cluster(s), 2 event(s), 2 event hyperedge(s), 1 relation hyperedge(s)
```
