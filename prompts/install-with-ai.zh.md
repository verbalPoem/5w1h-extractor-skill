# 让 AI 自动安装本 Skill 的提示词

请帮我把当前仓库里的 Codex skill 安装到本机。

要求：

1. 找到当前仓库中的 `5w1h-extractor/` 文件夹。
2. 确认该文件夹中存在 `SKILL.md`。
3. 将整个 `5w1h-extractor/` 文件夹复制到当前用户的 Codex skills 目录：
   - Windows: `%USERPROFILE%\.codex\skills\`
   - macOS/Linux: `~/.codex/skills/`
4. 复制后检查目标路径中是否存在：
   - `5w1h-extractor/SKILL.md`
   - `5w1h-extractor/references/schema.md`
   - `5w1h-extractor/scripts/validate_output.py`
5. 不要删除或覆盖其他 skill。
6. 如果目标目录中已经存在 `5w1h-extractor/`，请先告诉我，再覆盖安装。
7. 安装完成后，告诉我应该新开一个 Codex 线程，并用下面的方式调用：

```text
$5w1h-extractor 抽取下面文本的事件 5W1H 知识超图：
...
```

请直接执行安装，并在最后给出安装路径和检查结果。
