<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center">
  <strong>让技术文字清晰、准确的写作技能。</strong><br>
  适用于 Codex 和 Claude Code。
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <strong>中文（简体）</strong> · <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <a href="#快速上手">快速上手</a> ·
  <a href="MANIFEST.md">写作原则</a> ·
  <a href="#安装">安装</a> ·
  <a href="#语言支持">语言支持</a> ·
  <a href="#证据与局限">证据</a>
</p>

---

写清谁做了什么、在什么条件下发生，以及证据支持什么结论。这个技能适用于拉取请求说明、事故进展通报、研究笔记和操作指引。

## 事实不变，更容易读懂

以下示例改编自[保留的韩语写作案例](research/structure-layout-responses.json)，用于说明改写方式，并非新的测量结果或针对英语写作的偏好测试。

**改写前**

> 在全部 80 个会话中，evaluator 排除了超时的 12 个会话，报告其余 68 个会话的误差中位数为 0.8 m；超时会话的误差未计算。

**改写后**

> 全部 80 个会话中，有 12 个超时。evaluator 报告其余 68 个会话的误差中位数为 0.8 m。
>
> 超时的 12 个会话未计算误差。

改写明确区分了纳入测量和被排除的两组会话，同时完整保留了数值和限制。

## 快速上手

安装后，显式调用技能，并附上需要改写的文字。

**Codex**

```text
$human-readable-writing 请面向项目维护者改写这段拉取请求说明。
保留技术术语、事实、条件和不确定性。
```

**Claude Code**

```text
/human-readable-writing 请把这段事故进展通报写得更清楚。
区分已观察到的情况、可能的原因和未经验证的说法。
```

调用时，技能会读取 [MANIFEST.md](MANIFEST.md)，并复用上下文中已有的指引。输出使用你要求的语言；编辑时保留原文语言，除非你要求翻译。

## 它会改进什么

| 检查重点 | 改进方式 |
|---|---|
| 密集堆叠的名词 | 写清主体、动作及其相互关系。 |
| 打断主线的插入语和层层嵌套的条件 | 让主句易于理解，把相关条件放在一起。 |
| 多种条件之间的比较 | 在有助于比较时使用表格，同时保留单位、范围和限定说明。 |
| 操作指引 | 先说明当前状态以及需要做出的决策或采取的行动，再解释原因。 |
| 研究解读 | 说明观察结果如何支持判断，以及判断的局限。 |

**完整保留的内容：**技术名称、标识符、数量、单位、排除项、否定含义，以及不确定性针对的对象和程度。原文没有交代清楚的关系，在找到来源依据前不自行补全。

分段遵循论述思路和要求的格式，不会对所有语言和文档类型一律采用“一句一段”的偏好。

## 安装

使用有权访问此仓库的账号克隆。**在仓库根目录下**运行链接命令，并确保两个目标技能路径均未被占用。

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$PWD" "$HOME/.agents/skills/human-readable-writing"
ln -s "$PWD" "$HOME/.claude/skills/human-readable-writing"
```

两个运行环境会读取同一份仓库工作副本。如果已经克隆，只需在该目录下运行 `mkdir` 和 `ln` 命令。

<details>
<summary><strong>运行环境设置与显式调用</strong></summary>

| 运行环境 | 入口 | 调用规则 |
|---|---|---|
| Codex | `~/.agents/skills/human-readable-writing/SKILL.md` | `agents/openai.yaml` 中包含 `allow_implicit_invocation: false`，禁止隐式调用。 |
| Claude Code | `~/.claude/skills/human-readable-writing/SKILL.md` | 将下面的 `skillOverrides` 设置合并到现有设置文件中，使技能仅可由用户显式调用。 |

向 `~/.claude/settings.json` 添加以下内容时，保留其他已有设置：

```json
{
  "skillOverrides": {
    "human-readable-writing": "user-invocable-only"
  }
}
```

无法读取本地技能目录的云端会话需要单独安装。请参阅 [Codex](https://learn.chatgpt.com/docs/build-skills) 和 [Claude Code](https://code.claude.com/docs/en/skills) 的个人技能指南。

</details>

<details>
<summary><strong>维护者单独开展的全局核心规则试用</strong></summary>

维护者的个人环境还在全局指令中使用了一份早期的精简韩语核心规则。安装上述符号链接不会安装这份核心规则。

这份核心规则于 2026-10-29 在 `~/.agents/TERMINOLOGY.md` 中启用，通过 Codex 和 Claude Code 已有的指令路径生效，至今保持不变。其 61 个 token 的大小是使用 `o200k_base` 得到的参考计数，并不代表请求总用量。

[原始试用记录](research/native-pilot.md)以韩语记录了本地安装经过和撤销命令。此技能是独立的一层，需要显式调用。

</details>

## 语言支持

**韩语和英语是同等优先的主要支持语言。** [韩语 README](README.ko.md) 和[英语 README](README.md) 同步维护安装、使用、支持范围和验证结果；示例可以根据各自语言的表达习惯调整。

共用指令仍保存在一份英语写作原则文件中。输出始终以用户要求的语言为准；没有翻译要求时，编辑会保留原文语言。

| 语言 | 当前范围 |
|---|---|
| 韩语和英语 | 主要文档、示例和已记录的有限检查。尚未完成普遍适用的写作质量验证。 |
| 简体中文 | 提供本翻译指南，尚未验证简体中文输出质量。不代表已覆盖中文的所有书写形式。 |
| 法语 | 提供[翻译指南](README.fr.md)，尚未验证法语输出质量。 |
| 日语 | 提供[翻译指南](README.ja.md)，尚未验证日语输出质量。 |

三种翻译指南的语言之间不设开发先后顺序。后续工作取决于实际需求及相应语言的审阅条件。提供翻译文档不等于已验证输出具有母语水平。

详见[语言政策与验证记录](docs/language-support.md)。OpenCode 2、Pi 和 oh-my-pi 仍在评估中；[工具兼容性说明](docs/tool-support.md) 区分了文档核查与尚未开展的实际运行检查。

## 证据与局限

**这是一个仍在演进的个人写作工具。** 指引结合了从文献中得到的思路和已记录的编辑偏好，目前尚未证实它能提高人的理解程度或缩短阅读时间。

| 证据 | 能支持的结论 |
|---|---|
| [以英语为主的工作流程检查](docs/language-support.md#workflow-check)（英语） | 对语言选择、要求的格式和原文忠实度进行了有限检查，不能证明质量达到母语水平。 |
| [五篇韩语文档的改写比较](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | 一位用户对段落、表格和信息顺序的偏好。 |
| [12 次版式生成](research/layout-generation-pilot.md)（韩语） | 发现没有依据的验证声明和不确定性表达的变化后，暂缓采用。 |
| [四次生成结果的原文忠实度检查](research/source-fidelity-pilot.md)（韩语） | 两个实验组均通过检查，未能证明修订版更优。 |
| [六个修订核心规则案例](research/source-fidelity-six-audit.json)（韩语） | 六个案例均满足智能体的语义和格式标准，但没有同期对照组。 |

早期生成研究使用的是韩语技术文字。其中用于实验的修订核心规则为 93 个 token，与 61 个 token 的全局核心规则及完整写作原则均不相同。这些研究的结果不能验证当前版本的技能。

## 延伸阅读

| 用途 | 文档 |
|---|---|
| 共用写作指引 | [写作原则](MANIFEST.md) · [技能入口](SKILL.md) |
| 各语言的专用指引 | [韩语](references/korean.md) · [覆盖范围与验证（英语）](docs/language-support.md) |
| 原论文分析，韩语 | [分析](ANALYSIS.md) · [证据评述](research/evidence-review.md) |
| 相关文献与应用，韩语 | [文献笔记](research/related-literature.md) · [两篇论文的应用](research/two-paper-application.md) |
| 早期成本与耗时研究，韩语 | [调用成本](research/invocation-cost.md) · [固定预算比较](research/core-refinement.md) · [隐去实验组别的输出](research/core-refinement-blind.md) |
| 历史验证与偏好记录，韩语 | [验证记录](VALIDATION.md) · [版式偏好](research/structure-layout-pilot.md) |

即使指令不需要额外读取文件，也会消耗输入 token。早期的 token 和延迟测量并未衡量本次修订的成本。

---

本项目始于对 Thomas Hikaru Clark、Matias B. Martin 和 Kyle Mahowald 的论文 [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1) 的分析。这里的写作指引和示例是独立的实践建议，并非经论文作者验证或认可的干预措施。

原论文采用 CC BY 4.0 许可。[署名与来源记录](NOTICE.md)以韩语列出各项来源及其各自的许可证。**本仓库尚无单独的分发许可证。**
