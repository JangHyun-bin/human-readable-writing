# Human-readable Writing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. 현재 요청은 계획 수립까지다. 기능 구현을 시작하라는 후속 요청을 받은 뒤 실행한다.

**Goal:** 기존 Agent Skill을 유지하면서 작업·언어·개인 선호를 분리하고, 원문 비교·반복 평가·설치 진단을 재현 가능하게 만든다.

**Architecture:** 공통 Core와 작업별 참조를 필요한 범위만 읽는다. Python 보조 모듈은 읽기 전용 문서 검사, 새 디렉터리에 기록하는 평가 실행, 파일·버전 진단을 제공한다. 기존 `research/`는 보존하고 새 계약·평가 자료를 별도 경로에서 관리한다.

**Tech Stack:** Python 3.11+, standard library, unittest, Markdown/JSON, GitHub Actions. 첫 모델 어댑터는 Codex app-server의 실행 시점 지원 API를 확인하여 연결한다. 사용자용 스킬에는 Python 실행을 필수로 만들지 않는다.

**Spec:** [2026-11-02-writing-stack-design.md](../specs/2026-11-02-writing-stack-design.md)

## 계획의 상태와 범위

- MIT와 여섯 구성의 개발 계획은 사용자 요청이다. 세부 인터페이스와 평가 규모는 설계자의 제안이다.
- 이번 변경: LICENSE, NOTICE, 다섯 README의 라이선스 안내, 설계와 계획 문서.
- 이후 구현: 아래 Task 1–8. 현재 기능·지원·성능으로 안내하지 않는다.
- 구현 단위는 세 개다: A=지침·계약(Task 1–2), B=검사·평가(Task 3–5), C=배포·채택(Task 6–8). B는 A의 계약을, C는 A/B의 결과를 사용하므로 순서대로 수행한다.

## Global Constraints

- Python 3.11 이상, 런타임 외부 의존성 없음, 테스트는 기존 `unittest`를 유지한다. CLI를 설치하지 않아도 Markdown 스킬을 사용할 수 있다.
- `research/`의 프로토콜·어댑터·출력·감사·실행 코드는 과거 실험의 일부다. 새 구현 때문에 바꾸거나 재명명하지 않는다.
- 명시적 스킬 호출을 유지한다. Core를 전역 설정에 자동 삽입하지 않는다.
- 프로필이 지정되지 않으면 개인 선호를 적용하지 않는다.
- 조건별 로드 파일 목록과 SHA-256을 고정한다. 한 실험 안에서는 언어·요청·원문·모델·effort·길이 조건을 동일하게 유지하고 실행 순서를 기록된 seed로 섞는다.
- 결과 디렉터리는 새로 생성한다. 중단 전 데이터는 보존하며 기존 결과를 덮어쓰지 않는다. unknown과 0을 구분한다.
- 외부 모델 호출은 일반 PR CI에서 실행하지 않는다. 실제 생성은 별도 `--execute`와 양수 호출 상한을 필요로 한다.
- 기계 검사 통과를 의미 보존·이해도 향상으로 표시하지 않는다. 오류·미평가·불확실은 구분한다.
- 사용자 전역 파일·기존 설치·원문을 자동 수정하지 않는다. 제3자 자료의 라이선스를 MIT로 덮어쓰지 않는다.

## Review Focus

1. 혼용 한글·영문, 결합문자, CRLF, backtick과 단위 표기: 원문 byte와 보호 문자열을 임의 정규화하지 않는다. Task 1/3의 fixture로 확인한다.
2. 원문 속 명령·개인 프로필 충돌·선택 영역: 데이터가 실행 지침을 덮어쓰지 않고 요청 범위를 지킨다. Task 2의 사례와 Task 3의 읽기 전용 검사로 확인한다.
3. stale 의미 검토: 같은 case ID라도 원문 또는 출력이 바뀌면 이전 검토를 적용하지 않는다. Task 3에서 해시 불일치를 실패시킨다.
4. 모델 timeout·부분 출력·알 수 없는 usage·예기치 않은 도구 호출: 증거를 남기고 중단하며 재시도·0 비용 추정을 하지 않는다. Task 4/5에서 fake transport로 확인한다.
5. symlink·중복 설치·stale 배포본·깨진 참조: 올바른 실경로와 제한된 검사 범위를 표시하고 기존 설치를 변경하지 않는다. Task 6/7에서 임시 경로와 패키지 검사로 확인한다.

## Task 0: MIT와 계획 기록 — 이번 변경

**Files:** Create `LICENSE`, 이 계획, 연결된 설계. Modify `NOTICE.md`, `README.md`, `README.ko.md`, `README.fr.md`, `README.ja.md`, `README.zh-CN.md`.

- [x] 표준 MIT 본문에 `Copyright (c) 2026 Hyunbin Jang`을 사용한다. 표준 조건은 수정하지 않는다.
- [x] 제3자 자료의 기존 조건과 프로젝트 자체의 MIT 적용 범위를 구분한다.
- [x] 다섯 README의 미지정 라이선스 문구를 일치시킨다. 한·영 README에 계획 링크와 미구현 상태를 표시한다.
- [x] LICENSE 본문·새 링크·변경 범위를 확인하고 기존 테스트 23개가 통과함을 확인했다. 이 변경은 검토용 PR로 제공한다.

이 작업은 문서·라이선스 변경이므로 이를 그대로 흉내 내는 새 단위 테스트는 만들지 않는다.

## Task 1: 공통 계약·사례·기준 snapshot

**Files:** Create `hrw/__init__.py`, `hrw/contracts.py`, `evals/README.md`, `evals/schemas.md`, `evals/cases/development/*.json`, `evals/cases/holdout/*.json`, `evals/baselines/1ab42a0/`, `tests/test_contracts.py`.

**Interfaces:**
- `load_case(path: Path) -> Case`, `load_profile(path: Path) -> Profile`, `load_review(path: Path) -> Review`; frozen dataclasses의 필드는 설계의 v1 표와 동일하다. Case에 `file_sha256: str` 읽기 메타데이터를 추가한다.
- `ValidationError(ValueError)`; 모든 계약 오류는 이 타입과 필드 경로를 포함한다.
- `sha256_file(path: Path) -> str`; 원본 byte 기준이다.

- [ ] 테스트 `test_case_preserves_unicode_and_line_endings`는 UTF-8 원본, JSON 안의 CRLF·결합문자·backtick·`0.8 m`를 로드하여 문자열과 file_sha256이 변하지 않음을 확인한다. `test_invalid_contract_rejected`는 unknown field, 중복 id 검사 헬퍼, enum 오류, 빈 보호 문자열, 음수 max_characters를 거부한다.
- [ ] `python -m unittest discover -s tests -p 'test_contracts.py' -v`를 실행해 아직 없는 계약 모듈로 실패하는지 확인한다.
- [ ] 계약을 구현한다. Case의 source/request는 문자열, required_facts/forbidden_claims는 문자열 배열, protected는 객체 배열로 검사한다. 일반 파일 로드는 명시적으로 전달한 경로만 허용한다.
- [ ] 개발 사례 24개를 고정한다: 언어별 edit 4, restructure 3, explain 3, draft 2. 좋은 원문 유지, 조건·역할·부정·수치·분모·혼용 문체·긴 글·원문 속 지시문을 포함한다. 정답 문장 대신 보존 사실과 금지 주장을 기록한다.
- [ ] 보류 사례 8개를 별도로 작성·해시 고정한다. 언어별 작업당 1개다. 생성·검토 담당자는 이를 지침 수정 근거로 사용하지 않는다. 조정에 사용한 사례는 development로 전환하고 새 사례를 확보한다.
- [ ] 기존 commit `1ab42a098e2adec546da7b1942713f530c3706a6`의 SKILL.md, MANIFEST.md, references/korean.md를 baseline 디렉터리에 byte 그대로 보존하고 provenance.json에 원본 경로·commit·SHA-256을 기록한다. 기존 지침의 추가 필수 참조는 실제 로딩 경로를 확인하여 포함한다. 문서의 역사적 외부 링크를 실행 입력으로 자동 로드하지 않는다.
- [ ] 위 테스트와 기존 `python -m unittest discover -s research -p 'test_*.py' -v`를 실행한다. 기존 23개와 새 계약 검사가 통과해야 한다.
- [ ] Commit: `feat: define writing cases and preserve evaluation baseline`.

## Task 2: Core·작업·언어·프로필 분리

**Files:** Create `CORE.md`, `references/tasks/{edit,restructure,explain,draft}.md`, `references/english.md`, `profiles/{neutral,maintainer-ko}.json`, `hrw/instructions.py`, `tests/test_instructions.py`. Modify `SKILL.md`, `MANIFEST.md`, `references/korean.md`, 한·영 README, `docs/language-support.md`.

**Interfaces:**
- `resolve_instruction_paths(root: Path, *, task: str, language: str, profile_id: str | None, detailed: bool) -> list[Path]`.
- 순서: CORE.md, 작업 파일, 해당 언어 파일, 명시적 profile 파일(있을 때), MANIFEST.md(detailed=True일 때). 허용 ID 밖의 profile/path traversal은 ValidationError다.
- `snapshot_instructions(paths: list[Path]) -> list[dict[str, str]]`; 각 원소는 `path`, `sha256`, `content`를 가진다. 경로는 root 기준 상대 경로로 보존한다.

- [ ] `test_minimal_edit_loads_only_core_task_language`는 profile=None/detailed=False일 때 정확히 3개 파일을 기대한다. `test_personal_profile_is_opt_in`은 지정할 때만 maintainer-ko가 포함됨을 확인한다. `test_path_escape_and_conflicting_profile_rejected`는 `../` 및 복수 프로필 입력을 거부한다.
- [ ] `python -m unittest discover -s tests -p 'test_instructions.py' -v`로 실패를 확인한다.
- [ ] 공통 원칙을 CORE.md에 짧게 정리하고 상세 설명은 MANIFEST에 남긴다. 새 core가 과거 61-token core와 같은 버전이라는 표현은 쓰지 않는다. 공통 규칙의 독립 사본을 작업·프로필 파일에 복제하지 않는다.
- [ ] 작업별 허용 범위와 상세 지침 로딩 조건을 설계대로 구현한다. 한국어의 개인 문단 취향은 opt-in maintainer-ko로 옮기며 언어 일반 규칙과 분리한다. neutral은 문체 null, 용어 객체 비어 있음, layout_notes 비어 있음이다.
- [ ] Case의 원문과 요청은 지침과 구분해 전달한다. 원문 안의 `ignore previous instructions` 등은 인용 데이터로 다룬다. 사용자 요청과 프로필이 충돌하면 요청이 우선이며 중요한 불명확성만 확인하도록 문서화한다.
- [ ] 위 단위 테스트와 development 사례의 계약 검사를 실행한다. 원문 유지·제한 영역·초안의 누락 정보 사례를 사람 또는 별도 검토자가 읽고 기대 행동을 확인한다. 아직 모델 품질 개선을 선언하지 않는다.
- [ ] Commit: `feat: separate writing core tasks and optional profiles`.

## Task 3: 읽기 전용 문서 검사와 의미 검토 연결

**Files:** Create `hrw/checks.py`, `hrw/cli.py`, `hrw/__main__.py`, `tests/test_checks.py`, `tests/test_cli_check.py`.

**Interfaces:**
- `check_output(case: Case, output: str, *, output_sha256: str, review: Review | None = None) -> CheckReport`.
- `check_exit_code(report: CheckReport, *, require_semantic_review: bool) -> int`.
- `main(argv: list[str] | None = None) -> int`; `python -m hrw check --case CASE --output TEXT --json [--review REVIEW] [--require-semantic-review]`.

- [ ] `test_missing_protected_quantity_fails_mechanical`는 `0.8 m` 누락을 error로 확인한다. `test_mechanical_pass_is_not_semantic_pass`는 모든 문자열이 있어도 semantic_status가 not_reviewed임을 확인한다. `test_review_binding_rejects_changed_source_or_output`은 case_id·case_sha256·output_sha256의 어느 불일치도 오류로 처리한다.
- [ ] `test_boundary_and_role_changes_require_review`는 보호 문자열만 남긴 잘못된 조건문도 자동 semantic pass가 되지 않음을 확인한다. `test_check_does_not_modify_inputs`는 CRLF 원문·출력 파일과 주변 파일의 byte/mtime가 동일함을 확인한다. `test_cli_exit_codes`는 설계의 0/1/2와 require-semantic-review를 확인한다.
- [ ] 두 테스트 파일을 `python -m unittest discover -s tests -p 'test_*check*.py' -v`로 실행해 실패를 확인한다.
- [ ] exact 보호 문자열, code point 길이, heading 조건, unified diff와 required_facts/forbidden_claims 검토 항목을 구현한다. Markdown heading은 ATX `#` 형식만 첫 버전에서 검사하며 코드 fence 안은 제외한다. 이 범위를 문서에 표시한다.
- [ ] 기계 검사와 별도 review 상태를 조합하되 단일 품질 점수를 만들지 않는다. JSON 출력은 stdout, 진단은 stderr로 분리한다. 데이터 파일 내용을 명령으로 실행하거나 외부로 보내지 않는다.
- [ ] CLI를 임시 fixture에서 실행한다. 보호 항목이 빠지면 exit 1, 잘못된 JSON은 exit 2, 정상 기계 검사만 통과하면 exit 0이며 semantic_status는 not_reviewed여야 한다. 모든 관련 테스트를 통과시킨다.
- [ ] Commit: `feat: add read-only fidelity checks and review binding`.

## Task 4: 모델 호출 없는 평가 실행기

**Files:** Create `hrw/evaluation.py`, `hrw/providers/__init__.py`, `hrw/providers/fixture.py`, `evals/protocols/pilot.json`, `tests/test_evaluation.py`; extend contracts.py/cli.py.

**Interfaces:**
- `Protocol`: schema_version, id, model, effort, provider, seed, repeats, max_calls, timeout_seconds, cases(list[Path]), arms(dict[str,list[Path]]), profile_id(str|null), isolation_required(bool). arm ID는 baseline/core/current/candidate다.
- `GenerationRequest`: case_id, prompt, instruction_snapshot, model, effort, timeout_seconds. `GenerationResult`: output, observed_model(str|null), observed_effort(str|null), usage(dict|null), elapsed_ms, ttft_ms(float|null), events(list[dict]).
- `Provider.preflight(protocol: Protocol) -> dict`, `Provider.generate(request: GenerationRequest) -> GenerationResult`, `Provider.close() -> None`.
- `plan_run(protocol_path: Path) -> RunPlan`, `run_evaluation(plan: RunPlan, provider: Provider, output: Path) -> RunSummary`.
- RunPlan은 protocol hash, case 파일·지침 snapshot, 고정된 trial 순서, calls_planned를 가진다. RunSummary는 completed, attempted, stopped_reason, output_dir를 가진다.

- [ ] `test_dry_run_never_initializes_provider`는 기본 eval이 파일 계약과 계획만 확인함을 검증한다. `test_seed_reproduces_order`는 같은 seed에서 동일한 case/arm/repeat 순서를 확인한다. `test_budget_counts_failed_attempts`는 실패한 호출도 상한에 포함하고 초과 전에 중단함을 검증한다.
- [ ] `test_existing_results_are_not_overwritten`, `test_partial_failure_retains_outputs`, `test_unknown_usage_is_null`, `test_isolation_failure_prevents_generation`을 작성한다. fixture provider는 성공·timeout·부분 출력·예기치 않은 tool·미확인 설정 시나리오를 반환한다.
- [ ] `python -m unittest discover -s tests -p 'test_evaluation.py' -v`에서 실패를 확인한다.
- [ ] 프로토콜·snapshot·순서를 먼저 고정하고 결과 디렉터리를 exclusive 생성한다. 실제 생성은 --execute일 때만 수행한다. 자동 재시도 없이 실패·중단 event를 flush하고 provider.close를 finally에서 호출한다.
- [ ] 결과는 protocol.json, snapshots.json, results.jsonl, events.jsonl, summary.json으로 분리한다. 시도 전에 trial_start를 기록하고 결과·실패 직후 flush한다. 오류 원문·인증정보 대신 허용한 메타데이터를 남긴다.
- [ ] 8개 development 사례 × 4조건 × 2회, max_calls=64, timeout_seconds=180, seed=20261102의 pilot 프로토콜을 만든다. 모델·effort는 실행자가 명시하고 preflight에서 기록한다. 빈 모델은 --execute 시 오류다. 비어 있으면 dry-run에서 unresolved로 표시한다.
- [ ] fixture 실행으로 최대 64회 일정·중단·재실행 차단을 확인하고 모든 관련 테스트를 통과시킨다. 이 결과는 모델 품질 기록에 섞지 않는다.
- [ ] Commit: `feat: add reproducible bounded evaluation runner`.

## Task 5: 실제 모델 어댑터와 통제 조건 검사

**Files:** Create `hrw/providers/codex.py`, `tests/fixtures/codex_app_server.py`, `tests/test_codex_provider.py`, `docs/evaluation.md`; extend cli.py.

**Interfaces:**
- `CodexProvider`는 Task 4의 Provider 계약을 구현한다. 생성자 `CodexProvider(command: list[str], *, work_dir: Path)`; 요청 모델·effort와 관찰된 설정을 각각 기록한다.
- preflight 결과 필수 필드: runtime_version, model_requested, model_observed, effort_requested, effort_observed, input_hashes, isolation_status(`verified`/`failed`/`unknown`), reasons. isolation_required=True일 때 verified 외에는 실행하지 않는다.

- [ ] 구현 시점 로컬 CLI 문서/지원 API와 기존 benchmark_writing.py의 이벤트 처리를 비교한다. 현재 계정·호스트에서 전역 설정을 수정하지 않고 대상 core/다른 스킬 개입을 배제할 수 있는지 읽기 전용으로 조사한다. 확인 불가하면 어댑터를 unsupported 상태로 제공하고 통제 평가를 차단한다.
- [ ] `test_final_without_delta_keeps_unknown_ttft`, `test_eof_and_timeout_preserve_partial_records`, `test_unexpected_tool_stops_run`, `test_missing_isolation_evidence_blocks_baseline`, `test_sensitive_error_body_is_not_logged`를 작성한다. 프로세스 시작·종료는 fake server로 검사한다.
- [ ] `python -m unittest discover -s tests -p 'test_codex_provider.py' -v`에서 실패를 확인한다.
- [ ] 실제 지원 API에 맞는 어댑터를 구현한다. 새로운 context를 조건마다 사용하고 원문·공통 요청·조건별 지침을 별도로 기록한다. 기존 research 모듈을 수정하거나 새로운 런타임에서 frozen 연구를 재작성하지 않는다.
- [ ] fake server 테스트를 통과시킨다. `--execute` 없는 실제 CLI dry-run이 모델 생성을 하지 않는지 확인한다. 유료 생성과 native skill discovery 검증을 구분해 문서화한다.
- [ ] 첫 실제 실행은 사용자가 요청한 범위에서 별도 새 디렉터리와 호출 상한으로 수행한다. 실제 설정을 관찰할 수 없는 필드는 unknown으로 남기고 통제 비교를 통과시키지 않는다.
- [ ] Commit: `feat: add isolated Codex evaluation adapter`.

## Task 6: 설치 진단·버전·배포물

**Files:** Create `hrw/doctor.py`, `hrw/release.py`, `VERSION`, `release/references.json`, `tests/test_doctor.py`, `tests/test_release.py`, `docs/releases.md`; extend cli.py and 한·영 README. `release-manifest.json`은 ZIP 안에서 생성하는 산출물이며 Git에 체크인하지 않는다.

**Interfaces:**
- `inspect_installation(skill_root: Path, runtime: str, *, expected_manifest: Path | None = None) -> DoctorReport`.
- DoctorReport: schema_version, requested_path, resolved_path, runtime, scope, file_checks, static_status, runtime_status, findings. runtime_status는 이 명령에서 항상 not_tested다.
- `build_skill_archive(root: Path, destination: Path, *, version: str, source_commit: str) -> Path`; 새 ZIP 파일만 생성하고 설계 allowlist·SHA-256을 사용한다. source_commit의 입력 파일과 작업 트리 bytes가 다르면 오류다.
- CLI: `python -m hrw doctor --skill-root PATH --runtime codex --json`; `python -m hrw package --output NEW.zip --version VERSION --source-commit SHA`.

- [ ] `test_symlink_reports_actual_root_without_mutation`, `test_missing_reference_and_stale_hash_fail`, `test_static_success_is_not_runtime_support`를 작성한다. 입력은 지정한 root와 manifest뿐이며 사용자 홈 전체 탐색을 하지 않는다.
- [ ] `test_archive_is_reproducible`, `test_archive_excludes_research_and_personal_files`, `test_missing_runtime_reference_prevents_packaging`, `test_dirty_source_and_unknown_links_rejected`를 작성한다. 같은 입력/version/commit이면 정렬·ZIP timestamp를 고정하여 동일한 archive SHA-256을 기대한다. ZIP에 manifest가 있고 hrw/는 없음을 확인한다.
- [ ] `python -m unittest discover -s tests -p 'test_doctor.py' -v`와 `python -m unittest discover -s tests -p 'test_release.py' -v`에서 실패를 확인한다.
- [ ] doctor·패키지를 구현한다. references.json은 파일별 링크를 필수 runtime 참조/읽기용 문서로 분류한다. 필수 참조는 포함된 로컬 파일이어야 하고, 읽기용 참조는 source_commit의 repository URL로 변환하며 unknown 링크는 실패한다. 원본 문서는 변경하지 않는다. 변환 후 bytes를 생성 manifest의 files에 기록하고 manifest 자신은 해시 목록에서 제외한다.
- [ ] CLI는 버전을 지정한 Git checkout의 root에서 `python -m hrw`로 실행하도록 안내한다. PyPI 패키지·전역 설치는 제공하지 않는다. Markdown ZIP에는 CLI가 없고 생성 manifest가 포함된다. doctor의 checkout 검사와 package manifest 검사를 구분한다.
- [ ] 첫 기능 버전은 `0.1.0-dev`로 시작한다. 검증 완료 전 stable tag를 만들지 않는다. 업데이트·제거·rollback은 기존 경로 확인과 버전 선택을 포함한 문서 절차로 제공하며 자동 덮어쓰기를 구현하지 않는다.
- [ ] 임시 설치 root·symlink·깨진 참조·다른 버전으로 doctor를 실행하고 패키지 재현성 테스트를 통과시킨다.
- [ ] Commit: `feat: add installation diagnostics and versioned skill packages`.

## Task 7: CI와 네이티브 호출 확인

**Files:** Create `.github/workflows/ci.yml`, `tests/test_repository_integrity.py`, `tests/fixtures/research-hashes.json`, `evals/runtime-smoke/protocol.json`, `docs/contributing.md`; modify docs/tool-support.md and docs/releases.md.

**Interfaces:**
- 런타임 smoke 기록 필드: schema_version, runtime/version/model, skill_version, installation_scope, requested_root, resolved_root, requested_files, observed_files, explicit_case, uninvoked_control, output_sha256, verdict, limits.
- supported 선언은 runtime+version+model+scope+skill hash 조합에 한정한다. 결과 파일이 없거나 unknown이면 기존 지원 범위를 확대하지 않는다.

- [ ] `test_research_blobs_unchanged`는 기준 commit의 연구 파일 SHA-256 목록과 작업 트리를 비교한다. `test_required_skill_links_resolve`, `test_license_and_language_policy_consistent`는 배포 필수 참조·정책 메타데이터를 검사한다. 문구 전체 snapshot 대신 실제 계약만 검사한다.
- [ ] 새 integrity 테스트를 실행해 fixture/필수 파일 누락에서 실패함을 확인한 뒤 기준 목록과 검사를 완성한다.
- [ ] Ubuntu/macOS × Python 3.11/3.13 CI에서 `python -m unittest discover -s research -p 'test_*.py' -v`와 `python -m unittest discover -s tests -p 'test_*.py' -v`를 실행한다. 일반 PR CI에는 credentials와 실제 모델 호출을 넣지 않는다.
- [ ] Codex·Claude 각각 프로젝트 설치와 사용자 설치 scope에 대해 영어·한국어 명시 호출, 참조 로딩, 호출 없는 대조군을 확인할 프로토콜을 고정한다. 실제 지원 경로·실행 명령은 실행 당시 공식 문서와 설치된 CLI를 확인한다.
- [ ] 사용자 요청 범위에서 smoke를 수행한다. 임시 목적지를 지원하지 않는 사용자 scope는 기존 설치의 읽기 전용 확인과 fresh session을 이용하거나 untested로 남긴다. 다른 스킬이 개입하면 효과 측정으로 사용하지 않는다.
- [ ] 실제 검사한 조합만 docs/tool-support.md에 기록한다. 기존 raw evidence는 수정하지 않는다. 기여자의 신규 자료에도 MIT 적용 권한과 제3자 출처 표기를 확인하도록 CONTRIBUTING 안내를 작성한다.
- [ ] Commit: `ci: gate integrity and record scoped runtime support`.

## Task 8: 한정된 품질 비교와 첫 안정 버전

**Files:** Create `evals/protocols/holdout.json`, `evals/reports/REPORT_ID/`, `CHANGELOG.md`; modify VERSION, 한·영 README, docs/language-support.md, docs/releases.md. 패키지 manifest는 source commit 확정 후 다시 생성한다.

**Interfaces:**
- 선호 기록: comparison_id, case_id, output_hashes, hidden_label_mapping, presentation_order, choice(`A`/`B`/`tie`), reason(str|null), comprehension(dict|null), reedit_seconds(float|null), disclosed_before_choice(bool).
- 평가 report는 source fidelity, format, preference, comprehension, reedit_seconds, latency, tokens를 별도 항목으로 표시한다. 전체 품질 단일 점수는 만들지 않는다.

- [ ] Task 4의 개발 pilot를 명시적으로 실행하고 모든 실패·미평가를 포함해 보고한다. 중대한 의미 변경은 새 기본 지침 채택을 차단한다. 원인 수정에 사용한 사례를 holdout이라고 부르지 않는다.
- [ ] 문제가 해결되면 별도 요청 범위에서 보류 사례 8 × 4조건 × 3회, max_calls=96, seed=20261103, timeout_seconds=180 프로토콜을 고정한다. 같은 모델·effort·snapshot을 사용하고 결과를 본 뒤 유리한 출력만 고르지 않는다.
- [ ] 조건명을 가리고 위치를 섞은 비교에서 선호와 동률을 기록한다. 의미 검토자는 원문과 출력 해시를 확인한다. 읽기 이해·재편집 시간은 실제로 측정한 경우만 기록하고 나머지는 null이다.
- [ ] 사용자에게 관찰 범위와 실패·비용을 함께 제시한다. 단순 core가 더 적합한 작업에는 상세 지침을 기본으로 강제하지 않는다. 기본 지침 선택은 이 결과를 검토한 뒤 결정한다.
- [ ] cheap CI, 검사·평가의 오류 경로, 패키지 재현성, 주장과 실제 증거의 일치를 확인한다. 동작을 못 확인한 runtime/scope는 명시적으로 제한한다.
- [ ] 첫 안정 기능 버전 `0.1.0`의 CHANGELOG·파일 해시·검증 기록을 고정한다. 실제 release/tag 게시가 요청되었을 때 패키지를 게시한다. 안정 버전이라는 명칭은 일반적인 이해도 우위나 무오류 보증이 아니다.
- [ ] Commit: `release: document bounded evidence for writing stack 0.1.0`.

## 완료 판단과 후속 범위

첫 릴리스에서 사용자는 기존 에이전트로 스킬을 호출하고, 작업별 지침과 선택한 프로필을 사용하며, CLI로 원문 대비 보호 항목·형식·설치 버전을 확인할 수 있어야 한다. 유지관리자는 같은 snapshot과 사례로 평가를 재실행하고 실패·unknown·개인 선호를 구분할 수 있어야 한다.

Vale·Promptfoo 통합, 더 많은 모델 어댑터, summary 작업, 자동 패치, 웹 UI, 추가 언어별 품질 검증은 이 기반을 실제로 사용한 뒤 별도 요구로 다룬다. 첫 구현에서는 실제로 필요한 경계와 증거를 유지하는 데 집중한다.
