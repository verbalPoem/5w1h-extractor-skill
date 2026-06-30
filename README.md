# 5W1H 事件知识超图抽取 Skill

语言：中文 | [English](README.en.md)

这是一个面向 Codex 的 5W1H 抽取 skill，用于从新闻、军事报道、政策文本、事件通报和技术报告中抽取 **以事件为超边、以 5W1H 为节点** 的知识超图结构。

核心思想：

```text
一个中心事件 = 一条超边
Who / What / When / Where / Why / How = 这条超边连接的节点
```

默认输出：

```json
{
  "schema_version": "event-5w1h-hypergraph-v1",
  "text": "原始输入文本",
  "sentences": {},
  "nodes": [],
  "hyperedges": []
}
```

## 特点

- 中心事件优先：先确定 essential event / center claim，再抽取 5W1H。
- 事件即超边：每个事件用一条 hyperedge 表示。
- 5W1H 即节点：`who`、`what`、`when`、`where`、`why`、`how` 都作为节点连接到事件超边。
- 支持 span 偏移：节点包含 `tag_start` 和 `tag_end`，便于训练、评估和人工复查。
- 证据可追溯：节点和超边都能通过 `evidence` 回到原文句子。
- 面向复杂报道：内置有限状态机和 Trigger/Action 微技能库，减少旁支事件乱抽取。

## 仓库结构

```text
.
├── 5w1h-extractor/          # 可安装的 Codex skill
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

真正需要安装的是 `5w1h-extractor/` 文件夹。

## 快速安装

Windows PowerShell：

```powershell
Copy-Item -Recurse .\5w1h-extractor "$env:USERPROFILE\.codex\skills\"
```

macOS / Linux：

```bash
cp -R ./5w1h-extractor ~/.codex/skills/
```

然后新开一个 Codex 线程，输入：

```text
$5w1h-extractor 抽取下面文本的事件 5W1H 知识超图：
...
```

更详细的安装说明见：[docs/INSTALL.md](docs/INSTALL.md)

## 让 AI 自动安装

如果你正在使用 Codex、Claude Code、Cursor、Trae 或其他能读写本地文件的 AI 编程工具，可以把下面的提示词发给它：

[prompts/install-with-ai.zh.md](prompts/install-with-ai.zh.md)

AI 会根据提示把 `5w1h-extractor/` 放到你的 `.codex/skills/` 目录，并检查 `SKILL.md` 是否存在。

## 输出结构示例

节点：

```json
{
  "id": "N1",
  "text": "美国国务院",
  "node_type": "who",
  "entity_type": "ORG",
  "tag_start": 0,
  "tag_end": 5,
  "evidence": ["S1"],
  "confidence": 0.95
}
```

事件超边：

```json
{
  "id": "HE1",
  "event_type": "disclosure",
  "trigger": {
    "text": "公开",
    "tag_start": 5,
    "tag_end": 7
  },
  "summary": "美国国务院公开细节。",
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

`tag_start` 是原文中的起始字符位置，`tag_end` 是结束字符位置，采用左闭右开的 Python 切片风格。

## 验证输出

```bash
python 5w1h-extractor/scripts/validate_output.py examples/minimal-output.json
```

期望输出：

```text
VALID: 2 node(s), 1 hyperedge(s)
```

## 方法定位

本 skill 不是普通的 5W1H 标签抽取器，而是一个事件中心的知识超图构建器：

```text
Text -> Center Event -> 5W1H Nodes -> Event Hyperedge -> Knowledge Hypergraph
```

它适合用于：

- 事件抽取
- 5W1H 数据标注
- 知识图谱 / 知识超图构建
- 新闻与军事情报结构化
- LLM 抽取框架实验
- 论文方法设计与消融实验

## License

MIT License. See [LICENSE](LICENSE).
