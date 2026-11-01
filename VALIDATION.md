# 작성 원칙의 검증 기록

검증일: 2026-10-27.

## 1. 검증 목적과 한계

논문 분석의 근거 범위와 manifest의 적용 가능성을 확인하였다. 원문을 독립적으로 검토한 agent 1개와 작성 과제를 수행한 agent 2개를 사용하였다. Agent들은 root의 대화 이력을 전달받지 않았다. 두 작성 agent의 결과는 아래에 원문 그대로 기록하였다.

이 검증은 사람을 대상으로 한 독해 실험이 아니다. 작성 agent의 단일 baseline·적용 확인이며 model별 반복 sample, 읽기 시간, 이해도 정답률을 측정하지 않았다. 따라서 개선 효과나 통계적 유의성을 산출하지 않는다.

## 2. 작성 과제

두 agent에게 동일하게 다음 세 과제를 부여하였다.

1. Android pose timestamp가 10 ms grid에 snap된 사실과 label noise 가능성을 바탕으로 동료에게 전달할 짧은 보고를 작성한다. Regression dilution은 미확인이다. Replay의 median error는 1.4 m → 1.1 m이며 120 session 중 성공한 96 session만 집계하고 실패 24 session은 제외하였다. 같은 data로 threshold를 선택하여 independent holdout은 아니다. iOS·현장 실기는 미검증이다. 다음 행동은 성공·실패 전체 session을 포함한 새 holdout 측정이다. 보고는 5문장 이내로 요청하였다.
2. `holdout regression dilution mitigation gate`를 동료가 이해할 제목으로 개정한다.
3. 영어 corpus의 feature 관찰과 작은 model의 length-penalty 실험을 한 문장으로 설명한다. Frontier model의 실제 훈련 원인과 한국어 독해 개선 효과는 미검증이라는 사실을 함께 제공하였다.

Baseline agent에는 새 manifest나 논문을 읽지 않도록 하였다. 적용 agent에는 manifest를 읽고 같은 요청을 수행하도록 하였다. Manifest에는 첫 과제와 같은 가상 측정 예시가 포함되어 있으므로, 이 과제는 예시와 다른 상황으로의 일반화 검증이 아니다.

적용 agent에는 다음 문장만으로 상태 보고를 작성하는 별도 과제도 부여하였다. 이 문장은 manifest의 예시에 포함되지 않았다.

```text
iOS fallback relocalization timeout carryover path regression gate가 probe freshness debt를 먹어서 candidate release parity를 닫았다.
```

평가 기준은 수치·단위·분모·제외 대상·불확실성·검증 범위·다음 행동의 보존, 불명확한 관계에 대한 사실 추가 여부이다. 마지막 과제에는 의미가 정의되지 않은 표현이 있으므로 그럴듯한 성공·실패 상태를 확정하지 않는지 확인하였다. 문장별 금칙어 개수는 평가 기준으로 사용하지 않았다.

## 3. Baseline 산출물

아래는 agent가 반환한 원문이다. 인용의 어체와 표기를 보존하였다.

> Android pose timestamp가 10 ms grid에 snap돼 label에 noise가 들어갔을 가능성이 있으나, regression dilution이 실제 원인인지는 아직 확인되지 않았습니다. Replay에서 median error는 1.4 m에서 1.1 m로 줄었지만, 전체 120 session 중 성공한 96 session만 포함했고 실패한 24 session은 제외했습니다. 같은 replay data로 threshold도 선택했으므로 independent holdout 결과로 볼 수 없습니다. iOS와 현장 실기는 미검증이며, 다음에는 성공·실패 전체 session을 포함한 새 holdout을 측정하겠습니다.
>
> 제목: 새 holdout에서 위치 오차 개선 효과 확인
>
> 논문 요지: 영어 corpus에서 difficulty와 관련된 feature가 관찰됐고 작은 model의 length penalty 실험에서 일부 짧은 문법 형태에 대한 preference가 강화됐으며, frontier model의 실제 훈련 원인과 한국어 독해 개선 효과는 미검증입니다.

**판정:** 보고의 의미 보존 기준을 충족하였다. 논문 요지도 관찰·작은 model의 실험·미검증 범위를 보존하였다. 제목은 원문의 `mitigation gate` 관계가 무엇인지 명시적으로 검토하지 않았지만, 성공·실패 조건을 새로 확정하지도 않았다. 이 결과에서 정보 누락 실패를 관찰하였다고 주장하지 않는다.

## 4. Manifest 적용 산출물

아래는 agent가 반환한 원문이다.

> 성공한 96 session의 replay에서 median error가 1.4 m에서 1.1 m로 감소했습니다. 다만 전체 120 session 중 실패한 24 session을 제외했고, 같은 replay data로 threshold를 선택했으므로 independent holdout 결과는 아닙니다. Android pose timestamp가 10 ms grid에 snap되어 label에 noise가 생겼을 가능성이 있으나, regression dilution이 실제 원인인지는 아직 확인하지 못했습니다. iOS와 현장 실기는 미검증이며, 다음에는 성공·실패 전체 session을 포함한 새 holdout을 측정하겠습니다.
>
> 제목: **holdout 측정 결과와 regression dilution 가설** — gate의 진행 조건은 확인이 필요합니다.
>
> 논문은 영어 corpus에서 difficulty와 관련된 feature를 관찰하고 작은 model의 length penalty 실험에서 일부 짧은 문법 형태에 대한 preference가 강화됨을 보였지만, frontier model의 실제 훈련 원인과 한국어 독해 개선 효과는 확인하지 않았습니다.
>
> 원문만으로는 iOS fallback relocalization의 timeout carryover path에서 무엇이 달라졌고 probe freshness debt가 regression gate에 어떤 영향을 줬는지 불명확해, candidate release parity의 달성 여부는 확인이 필요합니다.

**판정:** 보고의 의미 보존 기준을 충족하였다. 제목에서는 정의되지 않은 gate 조건을 확인 대상으로 표시하였다. 추가 문장에서는 성공이나 실패를 확정하는 대신 의미 확인이 필요하다고 응답하였다. 다만 마지막 문장 자체가 여전히 길고 명사 연쇄를 포함한다. 불명확한 내용을 추측하지 않는 동작은 확인하였지만, 그 한 문장만으로 가독성 개선을 입증할 수는 없다.

두 agent의 보고는 모두 4문장이며 수치·분모·제외 대상·미검증 범위를 유지하였다. 핵심 차이는 적용 산출물이 결과부터 제시하고 제목의 모호한 조건을 명시한 점이다. 단일 관찰이고 예시와 겹치는 과제를 사용하였으므로 manifest의 인과 효과로 해석하지 않는다.

## 5. 독립 검토와 보완

원문 근거 검토자는 본문·appendix·figure를 대조하고 [evidence-review.md](research/evidence-review.md)에 결과를 기록하였다. 이어 [ANALYSIS.md](ANALYSIS.md)와 [MANIFEST.md](MANIFEST.md)를 검토하였다.

검토 후 두 부분을 보완하였다.

- Trained alternation의 지표를 `정답으로 판정된 sampled output 중 short 비율`로 명확히 하였다.
- Manifest의 예시에서 새 holdout 측정을 이미 정한 계획처럼 서술한 부분을 `후속 측정 제안`으로 표시하였다. 원문 사실과 새로 제안한 행동의 경계를 보존하였다.

핵심 논문 해석은 두 trained `that` alternation의 >98% 범위, forced-choice transfer와 실제 산출 비율의 구분, human baseline이 없는 panel, 다른 translator·pivot 검토의 word-count 범위를 유지하였다.

## 6. 산출물 확인

Korean report style 검사에는 `--loanwords english`를 지정하고 morphology 검사도 포함하였다. Markdown 4개 모두 finding 0, 미수행 검사 0으로 통과하였다. Local link 35개의 대상이 존재함을 확인하였고, corpus 수량·RL 조합 수·예시 odds 계산도 확인하였다. 이 검사는 내용의 과학적 타당성이나 인간 독해 효과를 보장하지 않는다.

분석에 사용한 `acl_latex.tex`는 778 lines이며 SHA-256은 다음과 같다. Official arXiv source와의 byte-level 일치를 확인한 hash는 아니며, 이번에 읽은 local source의 식별값이다.

```text
f300288c906d7e6cdaf285c9fda5b6894dadd20dab8ee7eeb2dcecf13bd504cc
```

Global instruction, 기존 skill, repository 설정, 원문 source는 변경하지 않았다. 새 dependency 설치·training·원문 통계 재현·human reader 평가는 수행하지 않았다.

## 7. 전역 skill 배포 추가

최초 분석 이후 2026-10-27 사용자 요청에 따라 전역 discovery를 추가하였다. 앞 절의 원문 검토와 작성 평가 결과는 해당 분석 시점의 기록으로 유지한다.

- Root의 `SKILL.md`가 기존 `MANIFEST.md`를 읽는 진입점이다. 새 작성 규칙이나 이해도 개선 주장을 추가하지 않았다.
- `agents/openai.yaml`에 이름·설명·기본 호출 예시를 추가하고 implicit invocation을 허용하였다.
- `~/.agents/skills/human-readable-writing`과 `~/.claude/skills/human-readable-writing`이 같은 repository를 가리키도록 연결하였다. 두 경로에서 같은 `SKILL.md`·`MANIFEST.md`를 읽는 것을 확인하였다.
- `~/.agents/TERMINOLOGY.md`에 적용 시점을 추가하였다. Codex의 global `AGENTS.md`는 이 정본을 가리키는 symlink이며, Claude Code의 global `CLAUDE.md`도 이 정본을 읽도록 이미 설정되어 있다.
- Skill validator가 통과하였고 implicit-invocation metadata, local link 46개, 두 runtime의 진입점, global instruction의 연결을 확인하였다. Repository 문서와 관련 global 지침에 credential 원문과 token pattern이 포함되지 않았음을 확인하였다.
- Private GitHub의 `db72849` commit을 bundled `skill-installer`로 임시 directory에 설치하였다. 설치한 `SKILL.md`·`MANIFEST.md`·`agents/openai.yaml`이 local 원본과 byte 단위로 일치하고 skill validator도 통과하였다. 첫 download에서는 local Python의 CA 설정으로 TLS 검증에 실패하였으며, 해당 child process에 설치된 `certifi` CA bundle을 지정한 뒤 통과하였다. TLS 검증과 전역 Python 설정은 유지하였다.

README는 `korean-report-style`의 `SKILL.md` §1.4에 따라 평서체로 작성하였다. 해당 skill의 morphology 규칙에는 `README.md`를 합니다체로 요구하는 고정 설정이 있어 filename 기준 검사에서 문체 지적 1건이 발생하였다. 작성 지침의 명시 규칙을 유지하고 README의 본문 검사는 stdin으로 수행한다. 검사기 자체는 변경하지 않았다.

이 검증은 설치 경로·metadata·참조의 정합성 확인이다. 새 model session에서 자동 선택될 확률이나 인간 독해 효과를 측정한 결과는 아니다. Local skill directory를 읽지 않는 cloud runtime은 별도 설치가 필요하다.

## 8. 명시적 호출 전환과 비용 비교

이후 사용자 요청에 따라 기본 경로·전체 지침 읽기·축약 지침 추가의 세 조건을 비교하였다. 가상 과제 세 개에서 총 9회 실행하였으며, 원본 usage·시간·실제 답변과 한계는 [비용 비교](research/invocation-cost.md)에 기록하였다.

세 조건 모두 핵심 사실 보존 검토를 통과하였다. 축약 지침의 추가 효과가 이 sample에서 확인되지 않아 상시 추가하지 않았다. 전역 지침의 자동 읽기 절을 제거하고, Codex의 implicit invocation과 Claude Code의 자동 호출을 해제하였다. 이전 절의 implicit invocation 허용 기록은 최초 배포 상태이며 현재 설정과 구분한다.

Timing 집계의 commentary 제외, 동결한 reference 반환, baseline의 예상하지 않은 reference 호출 차단을 확인하는 세 test가 통과하였다. 누적 input 사용량 차이는 관찰하였지만 cache 상태와 reasoning·output이 조건별로 달라 일정한 속도 개선을 주장하지 않는다.

배포 후 Codex의 실제 기본 prompt에서 이 skill의 목록 항목과 description이 제외되고, `skills/list`에는 활성 등록으로 유지되는 것을 확인하였다. Claude의 명시적 호출용 setting도 확인하였다. 기존 benchmark output을 지정하면 덮어쓰지 않고 종료하는 동작과 원본 hash 보존도 확인하였다. 독립 review에서 중요 finding은 없었다.

## 9. 같은 token budget의 core 고도화 비교

기존 축약 core와 후보를 `o200k_base` 기준 각각 61 tokens로 고정하고, baseline을 포함한 21개 답변을 생성하였다. Coding 과제는 조건별 5회, 새 API 문서·incident 과제는 조건별 1회 실행하였다. Model·effort는 `gpt-6-astra/high`로 고정하였다. [설계·계측·판단](research/core-refinement.md), [실제 답변의 blind 비교](research/core-refinement-blind.md), [원본 기록](research/core-refinement.jsonl)을 보존하였다.

전체 일곱 block에서 두 core의 실제 input usage가 같고 baseline보다 정확히 61 tokens 많으며, reference tool 왕복이 0임을 확인하였다. 이 counter만으로 builtin tool 사용 부재까지 입증하지는 않는다. 작성자가 전체 21개 답변의 필수 사실과 불확실성을 입력에 대조하였다. 별도 agent가 조건을 모르는 상태에서 수행한 사실 보존 검토에서도 중대한 누락이나 모순은 보고되지 않았다. 읽기 선호는 agent 판단으로 구분하며 사용자 평가나 인간 독해 측정으로 취급하지 않는다.

후보 지침이 기존 core에 덧붙지 않고 교체되며 baseline에는 포함되지 않는지 확인하는 test를 추가하였다. 전체 네 test가 통과하였고, 새 runner도 기존 output 경로를 지정하면 model 요청 전에 종료하여 원본을 보존하는지 별도 sentinel로 확인하였다. Blind file의 각 답변과 원본 output이 일치하고, 조건 대응표의 label과 원본 hash가 일치하는지 확인하였다.

후보의 일관된 개선 근거가 확보되지 않아 새 core의 전역 적용은 수행하지 않았다. 기존의 명시적 skill 호출 설정과 기본 응답 경로를 유지하였다.

별도 code·method review에서 Critical·Important finding은 없었다. 조건별 중앙값의 집계 설명 한 곳을 바로잡고, reference tool counter의 계측 범위를 명시하였다. 실제 model 요청을 반복 실행하지 않고 원본 usage·계측 표·blind mapping과 output 일치 여부를 대조하였다.


## 2026-10-29 Source fidelity 후속 확인

[고정된 4회→6회 확인](research/source-fidelity-pilot.md)을 완료하였다. 4회에서는 current·revised의 N2·E2가 모두 pass였고, 동일 revised core를 사용한 후속 6개 사례도 agent의 의미·Formal·문단 형식 기준을 모두 충족하였다. [Six-case audit](research/source-fidelity-six-audit.json)에 원본 hash·전송 조건·판정 근거와 runtime 기록 한계를 보존하였다. Core를 직접 전달한 known-case 확인이며 full MANIFEST 적용 효과·global core 개선·human comprehension 측정은 아니다.

별도 context의 agent가 기존 SKILL·MANIFEST를 적용한 N2·E2도 의미를 보존하였다. 작성 규칙을 추가하지 않고 manifest의 재사용 안내에 현재 pilot 상태를 기재하였다. 전역 61-token core와 명시적 skill 호출 정책은 유지하였다. Offline unit test 23개와 skill 구조 검사는 통과하였다.


## 2026-10-30 개인 선호를 상세 지침에 반영

[실제 문서 다섯 쌍의 편집 선호](research/native-pilot.md#2026-10-30-다섯-편집-비교의-최종-집계)를 A·B·B·B·A로 기록한 뒤, 사용자가 진행을 승인하여 MANIFEST의 원칙 3·5·6에 반영하였다. 짧은 기술 설명·사용 안내의 문단 구분, 여러 조건의 수치를 비교할 때의 표 사용, 실행 안내와 연구 해석의 정보 순서를 구체화하였다. 기존의 모든 결과 보고를 결론부터 시작한다는 규칙은 목적별 순서로 바꾸었다.

Fresh-context reviewer `manifest_preference_review`는 변경 전후 문서와 사용자 선택을 read-only로 비교하였다. Critical·Important finding은 없었으며, 두 Minor 제안을 반영하였다. 표 사용 조건을 단순히 수치가 여러 개인 경우가 아닌 나란히 비교하는 경우로 좁혔고, 관찰·통제 실험·미확인 범위를 설명하는 기존 예시 세 문장의 문구는 유지하면서 문단만 나누었다.

의미 보존 원칙·사용자 지정 형식·technical term 유지 규칙은 보존하였다. Source code·SKILL.md·호출 설정·전역 core는 변경하지 않았다. Codex와 Claude Code의 설치 경로가 이 checkout을 가리키는지, 해당 경로에서 최종 MANIFEST를 읽을 수 있는지 확인하였다. 별도 benchmark나 추가 사용자 A/B 평가는 실행하지 않았다. 기존 Python test는 이 문서 동작을 검증하지 않으므로 이번 문서 변경을 위해 재실행하지 않았다.

이는 개인 선호를 문서에 반영하고 문서의 범위·충돌을 확인한 결과다. 변경 후 새 session의 실제 출력 준수율·읽기 시간·이해도 개선이나 core의 인과 효과는 측정하지 않았다.
