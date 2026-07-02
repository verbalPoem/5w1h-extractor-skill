# 5W1H 事件知识超图抽取 Skill

语言：中文 | [English](README.en.md)

这是一个面向 Codex 的 5W1H 与事件知识超图抽取 skill 仓库，用于从新闻、军事报道、政策文本、事故通报和技术报告中抽取**以事件为超边、以 5W1H 为节点**的结构化知识。

仓库现在包含两个可安装 skill：

- `5w1h-extractor`：单中心事件 5W1H 超图抽取。
- `ceh-5w1h`：Clustered Event Hypergraph for 5W1H Extraction，先抽事件簇，再抽事件 5W1H，并建模事件间关系。

核心思想：

```text
一个中心事件 = 一条事件超边
多个相关事件 = 一个事件簇
Who / What / When / Where / Why / How = 事件超边连接的节点
事件之间 = relation_hyperedges
S1 / S2 = 证据句编号
N1 / N2 = 5W1H 节点编号
```

默认输出：

```json
{
  "schema_version": "event-5w1h-hypergraph-v3",
  "sentences": {},
  "nodes": {},
  "hyperedges": []
}
```

事件簇版输出：

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

## 特点

- 中心事件优先：先确定 essential event / center claim，再抽取 5W1H。
- 事件即超边：每个中心事件用一条 `hyperedge` 表示。
- 5W1H 即节点：`who`、`what`、`when`、`where`、`why`、`how` 都是节点组。
- 保留跳转编号：`S1/S2` 用于证据句追溯，`N1/N2` 用于超边连接节点。
- 支持 span 偏移：节点和触发词包含 `tag_start` 与 `tag_end`，便于训练、评估和人工复查。
- 减少乱抽取：内置有限状态机和 Trigger/Action 微技能库，避免把旁支事件全部枚举出来。

## 仓库结构

```text
.
|-- 5w1h-extractor/          # 单中心事件 5W1H skill
|   |-- SKILL.md
|   |-- agents/
|   |-- references/
|   `-- scripts/
|-- ceh-5w1h/                # 事件簇 5W1H 知识超图 skill
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

真正需要安装的是 `5w1h-extractor/` 或 `ceh-5w1h/` 文件夹。普通中心事件抽取用前者，多事件簇知识超图抽取用后者。

## 快速安装

Windows PowerShell：

```powershell
Copy-Item -Recurse .\5w1h-extractor "$env:USERPROFILE\.codex\skills\"
Copy-Item -Recurse .\ceh-5w1h "$env:USERPROFILE\.codex\skills\"
```

macOS / Linux：

```bash
cp -R ./5w1h-extractor ~/.codex/skills/
cp -R ./ceh-5w1h ~/.codex/skills/
```

然后新开一个 Codex 线程，输入：

```text
$5w1h-extractor 抽取下面文本的事件 5W1H 知识超图：
...
```

事件簇版：

```text
$ceh-5w1h 把下面文本抽成事件簇 5W1H 知识超图，并画 Mermaid 图：
...
```

更详细的安装说明见：[docs/INSTALL.md](docs/INSTALL.md)

## 让 AI 自动安装

如果你正在使用 Codex、Claude Code、Cursor、Trae 或其他能读写本地文件的 AI 编程工具，可以把下面的提示词发给它：

[prompts/install-with-ai.zh.md](prompts/install-with-ai.zh.md)

AI 会把 `5w1h-extractor/` 放到你的 `.codex/skills/` 目录，并检查 `SKILL.md` 是否存在。
如需事件簇版本，也让 AI 同时安装 `ceh-5w1h/`。

## 输出结构示例

证据句索引：

```json
{
  "S1": {
    "text": "U.S. State Department disclosed nuclear delivery system details on Dec. 1.",
    "tag_start": 0,
    "tag_end": 74
  }
}
```

节点索引：

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

事件超边：

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

`tag_start` 是原文中的起始字符位置，`tag_end` 是结束字符位置，采用左闭右开的 Python 切片风格。

## 验证输出

```bash
python 5w1h-extractor/scripts/validate_output.py examples/minimal-output.json
python ceh-5w1h/scripts/validate_ceh_output.py examples/ceh-minimal-output.json
```

期望输出：

```text
VALID: 1 sentence(s), 3 node(s), 1 hyperedge(s)
VALID: 1 cluster(s), 2 event(s), 2 event hyperedge(s), 1 relation hyperedge(s)
```

## 方法定位

这个仓库不是普通的 5W1H 标签器，而是事件中心与事件簇中心的知识超图构建器：

```text
Text -> Center Event -> 5W1H Nodes -> Event Hyperedge -> Knowledge Hypergraph
Text -> Event Clusters -> Events -> 5W1H Event Hyperedges -> Relation Hyperedges
```

适合用于：

- 事件抽取
- 5W1H 数据标注
- 知识图谱 / 知识超图构建
- 新闻与军事情报结构化
- LLM 抽取框架实验
- 论文方法设计与消融实验

## License

MIT License. See [LICENSE](LICENSE).
