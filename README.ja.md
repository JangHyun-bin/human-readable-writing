<p align="center">
  <img src="assets/readme-header.svg" alt="Human-readable writing" width="100%">
</p>

<p align="center">
  <strong>エージェント向けの文章作成スキル。</strong><br>
  Claude Code、Codex、OpenCode、Pi、oh-my-pi を対応対象としています。検証範囲はツールごとに異なります。
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.ko.md">한국어</a> · <a href="README.fr.md">Français</a> · <a href="README.zh-CN.md">中文（简体）</a> · <strong>日本語</strong>
</p>

<p align="center">
  <a href="#クイックスタート">クイックスタート</a> ·
  <a href="skills/human-readable-writing/MANIFEST.md">執筆の原則</a> ·
  <a href="#インストール">インストール</a> ·
  <a href="#対応言語">対応言語</a> ·
  <a href="#根拠と限界">根拠</a>
</p>

---

研究の解釈、財務分析、設備投資の検討、政策評価、設計判断の記録など、専門的な実務文書を対象にしています。プルリクエストの説明や障害報告にも使えます。誰が何をしたのか、その条件と根拠、実務上の意味を読み手が追えるようにするための指針です。

## 同じ事実を、より読み取りやすく

[記録として残されている韓国語の文章編集例](research/structure-layout-responses.json)をもとにした説明用の例です。新たな測定結果でも、英語の文章に対する好みを調べた試験でもありません。

**編集前**

> evaluator は、全80セッションからタイムアウトした12セッションを除いた68セッションで、誤差の中央値が0.8 mだったと報告した。タイムアウトしたセッションの誤差は算出していない。

**編集後**

> 全80セッションのうち、12セッションがタイムアウトした。evaluator は、残りの68セッションで誤差の中央値が0.8 mだったと報告した。
>
> タイムアウトした12セッションの誤差は算出していない。

数値や結果の適用範囲を変えずに、測定の対象となった群と除外された群を明確にしています。

## クイックスタート

スキルをインストールしたら、呼び出し時に編集したい文章を添えてください。

**Codex**

```text
$human-readable-writing このプルリクエストの説明を、メンテナーが読みやすいように編集してください。
専門用語、事実、条件、不確実性はそのまま保ってください。
```

**Claude Code**

```text
/human-readable-writing この障害の状況報告をわかりやすくしてください。
観測された事実、考えられる原因、未検証の主張を明確に区別してください。
```

このスキルは呼び出された際に [MANIFEST.md](skills/human-readable-writing/MANIFEST.md) を読み、すでにコンテキストにある指針は再利用します。出力には指定された言語を使います。文章の編集では、翻訳を依頼されない限り原文の言語を保ちます。

## どこを改善するか

| 確認する箇所 | 改善の方針 |
|---|---|
| 名詞が密集した表現 | 誰が何をするのか、要素同士がどう関係するのかを明示する。 |
| 文の途中の挿入や入れ子になった条件 | 主な主張を追いやすくし、関連する条件をまとめる。 |
| 複数の条件にわたる比較 | 比較が明確になる場合は表を使い、単位、範囲、留意点を保つ。 |
| 運用上の案内 | 現状と必要な判断・行動を先に示し、その理由を説明する。 |
| 研究結果の解釈 | 観測結果を、そこから導く判断とその限界につなげる。 |

**変えずに保つもの：** 専門的な名称、識別子、数値、単位、除外条件、否定、不確実性が何にかかるかとその程度。原文から裏づけられない関係は、未解決のまま残します。

段落は論理の流れと指定された形式に合わせて構成します。言語や文書の種類を問わず、1段落を1文にする方針を一律に適用するものではありません。

## インストール

`skills` CLI には Node.js 22.20 以降と `npx` が必要です。現在のプロジェクトにインストールするには、そのプロジェクトのディレクトリで次のコマンドを実行します。

```sh
npx skills add JangHyun-bin/human-readable-writing --skill human-readable-writing -a codex -a claude-code
```

使わない実行環境の `-a` オプションは削除してください。ユーザー単位でインストールし、すべてのプロジェクトで使えるようにするには、`-g` を追加します。この CLI はインストール時のテレメトリを収集します。無効にするには、コマンドの前に `DISABLE_TELEMETRY=1` を付けてください。

手動でインストールする場合は、このリポジトリにアクセスできるアカウントでクローンしてください。リンク先となる2つのスキルパスがどちらも存在しないことを確認し、**リポジトリのルートディレクトリで**リンク作成コマンドを実行します。

```sh
git clone https://github.com/JangHyun-bin/human-readable-writing.git
cd human-readable-writing

skill="$PWD/skills/human-readable-writing"
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
ln -s "$skill" "$HOME/.agents/skills/human-readable-writing"
ln -s "$skill" "$HOME/.claude/skills/human-readable-writing"
```

両方の実行環境が、チェックアウト内の同じ `skills/human-readable-writing` ディレクトリを読み込みます。このディレクトリは丸ごと残してください。すでにクローン済みの場合は、そのディレクトリで `skill=` の行から実行してください。以前の手順で作成したリンクはリポジトリのルートを指していますが、ルートはもうスキルではありません。このリンクの移行、更新、削除の手順は[インストールガイド](docs/install.md)（英語）を参照してください。

<details>
<summary><strong>実行環境の設定と明示的な呼び出し</strong></summary>

| 実行環境 | 手動インストール時の読み込み先 | 呼び出し方針 |
|---|---|---|
| Codex | `~/.agents/skills/human-readable-writing/SKILL.md` | `agents/openai.yaml` に `allow_implicit_invocation: false` を設定済み。 |
| Claude Code | `~/.claude/skills/human-readable-writing/SKILL.md` | `SKILL.md`: `disable-model-invocation: true`. |

共通の `SKILL.md` に `disable-model-invocation: true` を設定済みです。検証した Claude Code のバージョンでは `skillOverrides` の追加は不要です。ほかの既存設定は維持してください。

ローカルのスキルディレクトリを読み込めないクラウドセッションでは、別途インストールが必要です。[Codex](https://learn.chatgpt.com/docs/build-skills) と [Claude Code](https://code.claude.com/docs/en/skills) の個人用スキルに関する案内を参照してください。

</details>

<details>
<summary><strong>メンテナーが別途試行しているグローバルコア</strong></summary>

メンテナー個人の環境では、以前に作成した短い韓国語のコア指示も、グローバルな指示に含めています。上記の方法でインストールしても、このコアはインストールされません。

このコアは2026-10-29に `~/.agents/TERMINOLOGY.md` で有効化され、既存の Codex と Claude Code の指示読み込み経路を通じて適用されています。内容は変更していません。61トークンというサイズは `o200k_base` で数えた参考値であり、リクエスト全体のトークン消費量を保証するものではありません。

[当初の試行記録](research/native-pilot.md)には、ローカルへの導入履歴と元に戻すためのコマンドが韓国語で記載されています。このスキルは、それとは別に、明示的な呼び出しによって使うものです。

</details>

## 対応言語

スキルは指定された言語に従い、利用できる言語を特定の一覧に限定しません。**韓国語と英語は、文書の整備と検証で同等に優先します。** [韓国語 README](README.ko.md) と[英語 README](README.md) のインストール手順、使い方、対応範囲、検証状況を合わせて更新します。例文は、それぞれの言語に自然な形で作成します。

共通の指示は引き続き一つの英語の方針文書で管理します。出力には利用者が指定した言語を使い、翻訳の依頼がなければ原文の言語を保ちます。

| 言語 | 現在の対応範囲 |
|---|---|
| 韓国語・英語 | 主要ドキュメント、例文、記録済みの限定的な確認。一般的な文章品質の検証は未完了。 |
| 日本語 | この翻訳ガイドを公開済み。日本語の出力品質は未検証。 |
| フランス語 | [翻訳ガイド](README.fr.md) を公開済み。フランス語の出力品質は未検証。 |
| 簡体字中国語 | [翻訳ガイド](README.zh-CN.md) を公開済み。簡体字中国語の出力品質は未検証。 |

三つの翻訳ガイドの言語間に開発順位は設けません。今後の作業は実際の需要と各言語のレビュー体制に応じて決めます。文書の翻訳は、母語話者に相当する出力品質の検証を意味しません。

詳細は[言語方針](skills/human-readable-writing/references/language-support.md)を参照してください。2026-11-02に、リポジトリのルートをスキルとして使う以前の構成で、Codex、Claude Code、Pi、oh-my-pi は限定的な英語・韓国語の動作確認を通過しました。OpenCode 2 は一部のみ確認でき、失敗もあります。[互換性の記録](docs/tool-support.md)にバージョン、検証したパス、制約を記載しています。日本語の出力品質を検証した結果ではありません。新しい構成の確認については、[現在の検証記録](docs/verification.md)を参照してください。

2026-11-10の配布構成の検証では、Claude Codeのネイティブな初回利用手順を確認しました。Codex 0.167.0のネイティブ呼び出しは提供元のバージョンまたはアカウントのエラーで停止しており、成功として扱いません。

[英語・韓国語の専門実務例](examples/professional/README.md)は、2026-11-11に隔離したプロジェクトのコピーでClaude Code 2.1.322と`claude-sonnet-5-5`を使って実行しました。[記録](verification/professional-examples-20261111/README.md)では初回の修正と、検証での指摘を受けた再修正を区別しています。日本語の出力や他の実行環境を検証したものではありません。

## 根拠と限界

**これは、継続的に改善している個人用の文章作成ツールです。** 文献から得た考え方と、記録された編集上の好みを組み合わせて指針を作っています。人間の理解度や読了時間が改善することは、確認されていません。

| 根拠 | そこから言えること |
|---|---|
| [英語を主軸とするワークフローの確認](skills/human-readable-writing/references/language-support.md#workflow-check)（英語） | 言語の選択、指定された形式、原文への忠実さに関する限定的な確認。母語話者に相当する品質の証明ではない。 |
| [韓国語文書5件の比較](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계) | 段落、表、情報の順序に関する、1人の利用者の好み。 |
| [12件のレイアウト生成](research/layout-generation-pilot.md) | 裏づけがないのに検証済みとする主張や、不確実性の変化が見つかったため、採用を見送った。 |
| [原文への忠実さの検証（計4回の生成）](research/source-fidelity-pilot.md) | 両条件とも基準を満たしたが、改訂版の優位性は確認されなかった。 |
| [改訂コアを用いた6件の事例](research/source-fidelity-six-audit.json) | 6件すべてが、エージェントによる意味と形式の判定基準を満たした。同時に実施した比較条件はなかった。 |

以前の生成実験では、韓国語の技術文書を使っています。その実験用の93トークンの改訂コアは、61トークンのグローバルコアとも、完全版の執筆方針とも異なります。これらの実験結果によって、現在のスキルが検証されたわけではありません。

## 関連資料

| 目的 | 資料 |
|---|---|
| 共通の執筆指針 | [執筆方針](skills/human-readable-writing/MANIFEST.md) · [スキルの読み込み先](skills/human-readable-writing/SKILL.md) |
| 言語固有の指針 | [韓国語](skills/human-readable-writing/references/korean.md) · [対応範囲と検証](skills/human-readable-writing/references/language-support.md)（英語） |
| 元論文の分析（韓国語） | [分析](ANALYSIS.md) · [根拠の検討](research/evidence-review.md) |
| 関連文献と応用（韓国語） | [文献ノート](research/related-literature.md) · [2本の論文の応用](research/two-paper-application.md) |
| 以前のコスト・所要時間の調査（韓国語） | [呼び出しコスト](research/invocation-cost.md) · [固定予算での比較](research/core-refinement.md) · [条件を伏せた出力](research/core-refinement-blind.md) |
| 過去の検証と編集上の好み（韓国語） | [検証記録](VALIDATION.md) · [レイアウトの好み](research/structure-layout-pilot.md) |

ファイルを追加で読み込まなくても、指示文は入力トークンを消費します。以前のトークン数や応答時間の測定は、今回の改訂にかかるコストを測ったものではありません。

---

このプロジェクトは、Thomas Hikaru Clark、Matias B. Martin、Kyle Mahowald による [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1) の分析から始まりました。ここで示す執筆指針と例は、独立した実践上の提案であり、論文の著者らが検証したり推奨したりした介入方法ではありません。

元論文は CC BY 4.0 で公開されています。このプロジェクトのために作成した内容は [MIT ライセンス](LICENSE)で提供します。このライセンスは、第三者の著作物からの引用にも、引用元の論文にも適用されません。英語と韓国語の[出典・権利表記](NOTICE.md)に、各出典とそれぞれのライセンス、記録したモデル出力へのライセンスの適用範囲を記載しています。
