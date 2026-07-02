# 安装教程

语言：中文 | [English](INSTALL.en.md)

## 方式一：手动安装

1. 下载或 clone 本仓库。
2. 找到仓库中的 `5w1h-extractor/` 文件夹。
3. 将该文件夹复制到 Codex 的 skills 目录。

Windows PowerShell：

```powershell
Copy-Item -Recurse .\5w1h-extractor "$env:USERPROFILE\.codex\skills\"
```

macOS / Linux：

```bash
cp -R ./5w1h-extractor ~/.codex/skills/
```

4. 新开一个 Codex 线程。
5. 输入：

```text
$5w1h-extractor 抽取下面文本的事件 5W1H 知识超图：
...
```

## 方式二：让 AI 自动安装

如果你正在使用 Codex、Claude Code、Cursor、Trae 或其他本地 AI 编程工具，可以打开：

```text
prompts/install-with-ai.zh.md
```

把里面的提示词发给 AI。AI 应该完成：

1. 定位本仓库中的 `5w1h-extractor/` 文件夹。
2. 复制到当前用户的 `.codex/skills/` 目录。
3. 检查 `SKILL.md` 是否存在。
4. 提示你新开线程使用 `$5w1h-extractor`。

## 检查安装是否成功

安装后，目标路径应类似：

Windows：

```text
C:\Users\你的用户名\.codex\skills\5w1h-extractor\SKILL.md
```

macOS / Linux：

```text
~/.codex/skills/5w1h-extractor/SKILL.md
```

如果新线程里能识别 `$5w1h-extractor`，说明安装成功。

## 验证输出格式

仓库中包含一个输出校验脚本：

```bash
python 5w1h-extractor/scripts/validate_output.py examples/minimal-output.json
```

期望结果：

```text
VALID: 2 node(s), 1 hyperedge(s)
```
