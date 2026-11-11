# Contributing

[한국어 요약](#한국어-요약)

This project accepts problem reports, evidence from real use, and small pull requests. Read the [README](README.md) first for installation, use, and the limits of the current evidence.

## Report a problem

Open an issue with one of the two forms:

- Use the [install or invocation form](https://github.com/JangHyun-bin/human-readable-writing/issues/new?template=install-problem.yml) when the CLI, a manual link, or a runtime does not find or load the skill.
- Use the [changed source meaning form](https://github.com/JangHyun-bin/human-readable-writing/issues/new?template=source-meaning-change.yml) when an edit changed a number, a condition, a negation, an exclusion, or the strength of a claim. Use it also when an edit added a relationship that the source did not state.

Issues are public. Remove credentials, personal data, and confidential text first. A short made-up source that shows the same change is enough. You can write in English or Korean.

## Find the right file

- `skills/human-readable-writing/` is the package that users install. `SKILL.md` is the entry point, and `MANIFEST.md` holds the shared writing principles. `references/` holds the Korean guidance and the language-support policy, and `agents/openai.yaml` holds Codex's invocation policy.
- `README.md` and `README.ko.md` are the English and Korean guides. `README.fr.md`, `README.zh-CN.md`, and `README.ja.md` are translations.
- `docs/` holds the English and Korean installation guides, tool support, and verification. `examples/` holds the English and Korean examples.
- `examples/professional/` holds fact-ledger-based cases and source/rights notes. Its [catalog](examples/professional/catalog.json) selects the exact recorded revision for each language; the dated [assembly script](verification/professional-examples-20261111/assemble.py) checks source/request/output hashes and review coverage before generating the indexes.
- `site/` holds the English and Korean static landing pages and their shared design catalog. [Preview, design checks, and manual deployment](site/README.md) describe how to maintain them without changing the installed skill.
- `site/build-examples.py` publishes the reviewed cases into both landing pages and the design catalog, with public provenance downloads. After changing a displayed example, generation and its `--check` must pass; editing the repository example index alone does not update the visitor-facing page. The read-only `.github/workflows/validate.yml` runs parser, publication and design checks on PRs and `main` without deploying.
- `ANALYSIS.md`, `VALIDATION.md`, and `research/` are historical records. Do not edit them. Add a new dated record instead.

## Change the instructions

- Keep the shared principles in `MANIFEST.md`. Add language-specific guidance only when it changes a concrete writing decision.
- Keep every file that `SKILL.md` reads inside the package, and use relative links, so that an installed copy works on its own.
- Keep `disable-model-invocation: true` in `SKILL.md` and `allow_implicit_invocation: false` in `agents/openai.yaml`, so that the skill loads only when someone calls it by name.
- After you change the instructions or the package layout, repeat the checks described in [docs/verification.md](docs/verification.md). Record the date, runtime versions, models, commands, and outputs. Earlier records do not cover changed instructions.
- `verification/run_professional_examples.py` captures explicit native calls in disposable project copies. An outside-project read blocks output storage independently of other execution or parsing failures. Capture is not a fidelity pass: each accepted output also needs a fact-by-fact review tied to its hash. Corrections get separate attempts and reviews; initial failures stay unchanged. The [professional-example record](verification/professional-examples-20261111/README.md) describes this protocol.

## Change the documentation

- When installation, invocation, support status, or evidence changes, update the English and Korean versions together in the same pull request. That means `README.md` and `README.ko.md`, and `docs/install.md` and `docs/install.ko.md` when the change affects them. Wording and examples can differ to suit each language.
- Correct the same shared facts and paths in the translations.
- Label each example as an illustration or a recorded output. Copy a recorded output unchanged and link its record.
- Do not claim gains in comprehension, reading time, or writing quality unless a measurement supports the claim.

## Open a pull request

Keep one topic per pull request. Describe what changed, why, and what you checked. If you could not run a check, say so.

## License

The project uses the [MIT License](LICENSE), and contributions are accepted under it. Add third-party text only if its license allows it, and record the source and license in [NOTICE.md](NOTICE.md). The repository root and the package each have a copy of `LICENSE` and `NOTICE.md`. Keep the two copies identical.

## 한국어 요약

- 설치·호출 문제와 원문 의미 변경은 각각의 issue 양식으로 알려 주세요. Issue는 공개되므로 인증정보, 개인정보, 기밀 문서를 지우고, 같은 변경을 보여 주는 짧은 가상 원문을 사용해 주세요. 영어나 한국어로 작성하실 수 있습니다.
- 사용자가 설치하는 패키지는 `skills/human-readable-writing/`입니다. 공통 원칙은 `MANIFEST.md` 한 곳에 두고, 언어별 지침은 구체적인 작성 판단을 바꿀 때만 추가합니다. `SKILL.md`가 읽는 파일은 모두 패키지 안에 두고 상대 경로로 연결합니다.
- `site/`에는 한·영 정적 랜딩과 공통 디자인 기준이 있습니다. [미리보기·디자인 검사·수동 배포 안내](site/README.md)를 따르고, 설치되는 스킬과 과거 연구 기록은 변경하지 마세요.
- `ANALYSIS.md`, `VALIDATION.md`, `research/`는 과거 기록이므로 수정하지 말고, 날짜를 적은 새 기록을 추가해 주세요.
- 지침이나 패키지 구조를 바꾸면 [docs/verification.md](docs/verification.md)의 검사를 다시 수행하고 날짜, 도구 버전, 모델, 명령, 출력을 기록해 주세요.
- 설치, 호출, 지원 상태, 검증 근거가 바뀌면 `README.md`와 `README.ko.md`를 같은 pull request에서 함께 고쳐 주세요. 변경이 설치 안내에 영향을 주면 `docs/install.md`와 `docs/install.ko.md`도 함께 고쳐 주세요. 번역 문서도 공통 사실과 경로를 맞춰 주세요.
- 예시에는 설명용 예시인지 기록된 출력인지 표시하고, 기록된 출력은 고치지 않고 원래 기록에 연결해 주세요. 측정 근거 없이 이해도·읽기 시간·글쓰기 품질 향상을 주장하지 마세요.
- 기여는 MIT License로 받습니다. 제3자 글은 license가 허용할 때만 추가하고, 출처와 license를 `NOTICE.md`에 기록해 주세요. 루트와 패키지의 `LICENSE`, `NOTICE.md`는 같은 내용으로 유지해 주세요.
