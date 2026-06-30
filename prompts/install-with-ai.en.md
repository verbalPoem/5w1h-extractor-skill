# AI-Assisted Install Prompt

Please install the Codex skill in this repository on my local machine.

Requirements:

1. Locate the `5w1h-extractor/` folder in the current repository.
2. Confirm that `SKILL.md` exists inside that folder.
3. Copy the entire `5w1h-extractor/` folder into the current user's Codex skills directory:
   - Windows: `%USERPROFILE%\.codex\skills\`
   - macOS/Linux: `~/.codex/skills/`
4. After copying, check that these files exist in the target path:
   - `5w1h-extractor/SKILL.md`
   - `5w1h-extractor/references/schema.md`
   - `5w1h-extractor/scripts/validate_output.py`
5. Do not delete or overwrite any other skill.
6. If `5w1h-extractor/` already exists in the target directory, tell me before overwriting it.
7. After installation, tell me to start a new Codex thread and invoke:

```text
$5w1h-extractor extract the event 5W1H knowledge hypergraph from the following text:
...
```

Please perform the installation and report the final install path and verification result.
