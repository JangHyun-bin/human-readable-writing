# Changelog

This file lists changes that affect people who install or maintain the skill. No version has been released yet. Earlier work is in the git history and the research records.

## Unreleased

### Added

- The material written for this project is available under the [MIT License](LICENSE). [NOTICE.md](NOTICE.md) lists third-party sources and their licenses, and explains how the license applies to model outputs kept in the research records. The installed package includes copies of both files.
- Installation with the [`skills` CLI](https://github.com/vercel-labs/skills), for the current project by default or for the user account with `-g`.
- An [installation guide](docs/install.md) and a [Korean installation guide](docs/install.ko.md) for manual installation, updates, removal, and migration.
- A [verification record](docs/verification.md) for the new package layout and install commands.
- English and Korean [examples](examples/README.md) that show the request, source, revision, and kept facts.
- A [contributing guide](CONTRIBUTING.md) and issue forms for install or invocation problems and for changed source meaning.

### Changed

- The skill package moved to `skills/human-readable-writing/`. `SKILL.md`, `MANIFEST.md`, `references/korean.md`, and `agents/openai.yaml` now live there.
- `docs/language-support.md` moved to `skills/human-readable-writing/references/language-support.md`, which is now its only copy.
- The English and Korean READMEs describe the CLI installation, how to call the skill, the limits of the evidence, and how to report problems. The French, Chinese, and Japanese READMEs link to the new paths.
- Product descriptions and runtime guidance name Claude Code, Codex, OpenCode, Pi, and oh-my-pi as support targets, separately from their current verification status. OpenCode's partial-support limitations remain explicit.

### Removed

- The repository-root copies of `SKILL.md`, `MANIFEST.md`, `references/korean.md`, and `agents/openai.yaml`, and the old `docs/language-support.md`. Nothing redirects from the old paths.

### Migration

- A link from a skills directory to the repository root no longer reaches `SKILL.md`. Replace it with a CLI installation or with a link to `skills/human-readable-writing`, as the [installation guide](docs/install.md) and the [Korean installation guide](docs/install.ko.md) describe.
