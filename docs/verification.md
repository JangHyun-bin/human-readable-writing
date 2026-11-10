# Distribution verification

Checked on 2026-11-10. This record concerns `skills/human-readable-writing`, not the old root-level layout. The machine-readable [commands, outputs, package hashes, failures, and checks](../verification/public-readiness-20261110.json) accompany this summary. Historical [2026-11-02 evidence](../research/runtime-validation-20261102.json) remains unchanged.

## What worked

- Node.js 24.4.1 and `skills` CLI 1.7.6 installed the package into isolated project and user-level directories for Codex and Claude Code.
- Actual CLI updates replaced changed content and removed obsolete fixture files. After the final updates, both scopes matched all seven files of the final package byte for byte. Targeted CLI removal removed this skill while preserving unrelated fixture skills.
- The shell blocks in the [English installation guide](install.md) exercised manual installation from an existing checkout, removal, root-link migration, a safe migration rerun, and refusal to replace a foreign symlink or regular directory. The [Korean guide](install.ko.md) has the same executable shell commands.
- The two existing user-level symlinks that pointed exactly to this checkout's root were migrated to its installable subdirectory. No shared skills directory was deleted.
- The final English and Korean README first-use requests were exercised through Claude Code. The source text replaced the documented paste placeholder; the request wording and slash command matched the final documents.
- All 23 existing research-utility tests passed. All 61 tracked historical research, analysis, and validation files remained byte-identical. The five moved guidance/metadata files matched their prior contents after normalizing link destinations and the moved language-reference label.
- Active local documentation links, anchors, package-relative links, legal-copy identity, and shell syntax were checked. Both issue forms parsed as YAML and passed checks for required top-level fields, unique field IDs, and a required privacy confirmation.

## Runtime observations

These are small compatibility checks, not writing-quality measurements. Each successful language case used a fresh process. No credentials were committed. Installer telemetry was disabled.

| Runtime | Configuration | Observed result |
|---|---|---|
| Claude Code 2.1.321 | `claude-sonnet-5-5`; CLI project and user-level installations | English and Korean explicit invocation loaded the manifest; Korean also loaded its reference. One uninvoked English control per scope did not load the skill. English and Korean README first-use requests also loaded the guidance. |
| Pi 1.4.0 | `openai-codex/gpt-6-astra`; independent project copy | English and Korean invocation loaded the manifest; Korean also loaded its reference. The uninvoked English control did not load the skill. Authentication used an in-memory token referenced from a disposable model configuration, not a change to user settings. |
| oh-my-pi 18.18.6 | `anthropic/claude-sonnet-5-5`; independent `.omp/skills` project copy | Both language cases loaded the manifest and Korean loaded its reference. The uninvoked control did not load the skill. The Korean output included an English fact checklist before its revision, violating the requested output format. |
| Codex CLI 0.167.0 | Native CLI with the test ChatGPT account | Blocked before skill loading. `gpt-6-astra` was rejected with “requires a newer version of Codex”; an additional `gpt-6.1-sol` probe was rejected as unsupported for this ChatGPT account. Neither is a pass. |
| OpenCode | Not rerun in this task | The historical partial-support failures remain. Packaging does not establish a fix. |

The native Codex errors are not evidence that reference resolution failed. They also do not verify the new package in native Codex. At the time of checking, both npm and the official GitHub latest release identified Codex 0.167.0, so this task did not silently upgrade the user's CLI, spoof its version, or claim an available upgrade solved the rejection. Pi's successful `openai-codex` provider check is not a substitute for a native Codex pass.

Pi's first Anthropic-provider attempt returned an extra-usage billing error despite exit code zero. It produced no edited text and was not counted as successful. The later authorized OpenAI Codex-provider cases used the same skill package and are recorded separately. Claude's first user-scope harness attempt excluded user settings sources and failed to discover the global skill; including the isolated user source corrected the harness without changing the skill.

## Source fidelity and output limits

The successful incident revisions retained the checked time window, 240 total requests, 18 HTTP 503 responses, 222 successes, excluded retries and their unknown outcomes, zero-limit retry condition, unestablished causation, 820 ms successful-request p95, unmeasured failed-request latency, and proposed but unapproved replay.

That does not mean every output followed every instruction. The oh-my-pi Korean response added a preface despite the requested format. The English README first-use output also added claims about in-flight requests completing and responses being discarded that the source did not explicitly establish. These are recorded limitations, not accepted examples or evidence of improved writing quality. Users must compare revisions with their sources.

## Installation transport and isolation

The source was a disposable Git repository containing the current package, served on loopback. It was not an unpublished revision claimed to exist on GitHub. Global update tracking required an owner/repository-shaped SSH source; a per-process Git URL rewrite routed it to the same local Git daemon. No external repository, release, or tag was created or changed.

The initial dumb-HTTP fixture could not serve the installer's shallow clone. Verification switched to an actual Git daemon. The first generic `git://` global source was not tracked by the installer and its update exited zero without changing content; that was rejected as update proof. The tracked-source update subsequently replaced the actual package contents. Material file checks, not exit codes alone, determined success.

A manual-check assertion also needed canonical paths because macOS resolves `/tmp` to `/private/tmp`. No writing-rule change was used to make these harness failures pass. Final static checks corrected two archive links and restored an unintended wording change in the optional language-support reference. The current writing principles remain unchanged apart from moved links; successful model cases were not rerun merely to obtain preferred wording.

Native processes used disposable project/home/state directories, restricted tools, disabled hooks/extensions where supported, and existing authentication without committing credentials. Other fixture skills survived lifecycle operations. Personal configuration snapshots and internal review transcripts are not part of the public verification record.

## Repeating the bounded checks

1. Install only this named skill into a disposable project and user scope with telemetry disabled. Record Node, installer, runtime, model, and source revision.
2. Confirm all seven package files are present and research logs are absent. Test an independent copy, not just a symlink to the source checkout.
3. Send the recorded English and Korean incident requests with the runtime's explicit invocation, then an English control without the command. Inspect actual manifest/reference reads and the full final output. Check provider errors even when a process exits zero.
4. Follow the final README request with its example source. Compare quantities, conditions, exclusions, negation, uncertainty, and output format separately from whether the skill loaded.
5. Advance a disposable Git source, run the real updater, and check changed bytes and obsolete-file removal. Remove only this skill and verify unrelated sentinel skills survive.
6. Run the documented manual migration against a root link, a rerun, a foreign link, and a regular directory. Preserve the latter two.
7. Check current document links and package closure, legal-copy identity, and the historical-file hashes. Do not rewrite old results as verification of a new revision.

These local checks were performed before publishing a PR. Public GitHub installation commands fetch the revision actually on the default branch; testing a local mirror is not proof that an unpublished revision can be installed from that public URL.

## 한국어 요약

현재 실제 호출을 확인한 첫 사용 경로는 Claude Code 2.1.321입니다. 프로젝트·사용자 전역 설치에서 한·영 명시적 호출과 필요한 참조 읽기를 확인했고, 최종 한·영 README의 첫 요청도 실행했습니다. Pi와 oh-my-pi도 제한된 프로젝트 검사를 수행했습니다. 호출하지 않은 비교 요청에서는 대상 스킬을 읽지 않았습니다.

Codex 0.167.0은 테스트 계정에서 모델 제공자가 버전·계정 오류로 거부해 네이티브 호출을 확인하지 못했습니다. 당시 npm과 GitHub의 최신 공개 버전도 0.167.0이었습니다. Pi의 Codex-provider 성공을 네이티브 Codex 성공으로 대신하지 않았습니다. OpenCode의 과거 실패도 그대로 구분합니다.

CLI 설치·실제 변경을 반영하는 업데이트·대상 스킬만 삭제하는 절차와 수동 설치·삭제·기존 링크 이전을 격리된 환경에서 시험했습니다. 원격 저장소에 게시하지 않은 변경을 GitHub에서 설치했다고 주장하지 않습니다. 기존 테스트 23개는 통과했고 과거 자료 61개는 원본을 보존했습니다.

로딩 성공과 출력 품질은 다릅니다. oh-my-pi 한국어 출력은 요청하지 않은 서문을 붙였고, 영어 첫 사용 출력에는 원문에 명시되지 않은 요청 완료·응답 폐기 표현이 추가됐습니다. 이해도나 품질 향상을 입증한 결과로 사용하지 않으며, 사용자는 개정문을 원문과 대조해야 합니다.
