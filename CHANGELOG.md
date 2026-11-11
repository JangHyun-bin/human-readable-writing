# Changelog

This file lists changes that affect people who install or maintain the skill. No version has been released yet. Earlier work is in the git history and the research records.

## Unreleased

### Added

- Links to the English and Korean website at the top of every README and in the GitHub repository's About panel.
- The material written for this project is available under the [MIT License](LICENSE). [NOTICE.md](NOTICE.md) lists third-party sources and their licenses, and explains how the license applies to model outputs kept in the research records. The installed package includes copies of both files.
- Installation with the [`skills` CLI](https://github.com/vercel-labs/skills), for the current project by default or for the user account with `-g`.
- An [installation guide](docs/install.md) and a [Korean installation guide](docs/install.ko.md) for manual installation, updates, removal, and migration.
- A [verification record](docs/verification.md) for the new package layout and install commands.
- English and Korean [examples](examples/README.md) that show the request, source, revision, and kept facts.
- A [contributing guide](CONTRIBUTING.md) and issue forms for install or invocation problems and for changed source meaning.
- English and Korean static [landing pages](site/README.md), with illustrative edits, installation instructions, and dated runtime coverage. The site includes a shared design catalog and token check. GitHub Pages deployment requires a manual request on `main`.
- The Korean landing uses locally served SUIT Variable and Paperlogy Bold. The official font files retain their original OFL 1.1 licenses and copyright notices separately from the site's MIT license.
- The [English landing](https://human-readable-writing.vercel.app/) and [Korean landing](https://human-readable-writing.vercel.app/ko/) are hosted on Vercel. CLI deployment is manual and excludes research records, the installable skill, and repository tooling.
- Five [professional example packets](examples/professional/README.md) in English and Korean: research interpretation, financial analysis, capital investment, policy evaluation, and architecture decisions. Originals, fact ledgers, sources and rights are separate from unchanged native outputs.
- A [2026-11-11 execution and source-fidelity record](verification/professional-examples-20261111/README.md): ten initial native calls, nine accepted first revisions, one retained failure, and a separately requested Korean finance correction. Accepted examples and review provenance are indexed without rewriting failed records.
- The English and Korean landing pages display all five professional genres directly, with accessible genre selection, complete-text comparison, and local source/execution records. A dependency-free publisher and deployment freshness check keep the pages aligned with the accepted revisions. Pull-request CI runs capture-parser, example and design checks without deployment or model calls.

### Changed

- The skill package moved to `skills/human-readable-writing/`. `SKILL.md`, `MANIFEST.md`, `references/korean.md`, and `agents/openai.yaml` now live there.
- `docs/language-support.md` moved to `skills/human-readable-writing/references/language-support.md`, which is now its only copy.
- The English and Korean READMEs describe the CLI installation, how to call the skill, the limits of the evidence, and how to report problems. The French, Chinese, and Japanese READMEs link to the new paths.
- Product descriptions and runtime guidance name Claude Code, Codex, OpenCode, Pi, and oh-my-pi as support targets, separately from their current verification status. OpenCode's partial-support limitations remain explicit.
- The English and Korean landing pages use shorter example captions and support summaries, and go directly from the example to installation. Writing principles remain linked in the footer. Detailed checks and limitations remain in the linked documentation.
- Both landing pages use descriptive language, including setup instructions and clipboard error messages. The headings are "A writing skill for your agent." and "글쓰기를 위한 에이전트 스킬". Introductions and search descriptions do not restrict writing to technical documents or Markdown output.
- README and installed-skill introductions describe professional prose rather than only software-engineering documents. The writing-principles body, Korean guidance, license/notice files and explicit-invocation policy remain unchanged.

### Fixed

- The native example runner withholds output after any outside-project read, even when malformed events, provider errors, or process failures change the capture status. The privacy decision now uses the observed read independently of the failure label.

### Removed

- The repository-root copies of `SKILL.md`, `MANIFEST.md`, `references/korean.md`, and `agents/openai.yaml`, and the old `docs/language-support.md`. Nothing redirects from the old paths.

### Migration

- A link from a skills directory to the repository root no longer reaches `SKILL.md`. Replace it with a CLI installation or with a link to `skills/human-readable-writing`, as the [installation guide](docs/install.md) and the [Korean installation guide](docs/install.ko.md) describe.
