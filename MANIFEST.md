# Human-readable technical writing

## 작성 목표

독자가 결론과 근거를 연결하고 다음 행동을 판단할 수 있도록 작성한다. 의미를 확정한 뒤 불필요한 내용을 제거한다.

## 적용 범위

기술 설명·PR 설명·진행 보고·연구 해석·agent 지시의 자연어를 작성하거나 개정할 때 사용한다. 기존 용어·문서 형식·사용자 요청을 유지한다. Code, 식별자, 경로, command, API 이름, 원문 인용은 원형을 보존한다. 정착한 전문 용어는 읽는 사람에게 필요한 경우 처음 한 번 설명한다.

## 실행 원칙

1. **판단에 필요한 사실을 먼저 확정한다.** 누가 무엇을 하였고, 무엇을 관찰하였으며, 무엇이 아직 미검증인지 구분한다. 원인·대상·조건의 관계가 원문에 없으면 확인이 필요한 부분으로 표시한다.
2. **이름은 보존하고 관계는 풀어 쓴다.** 낯선 명사 연쇄는 조사·전치사·동사로 연결한다. `guard`, `gate`, `holdout`, `regression dilution` 같은 검색 가능한 이름은 유지한다. 기존 식별자와 임의로 만든 문장 표현을 구분한다.
3. **핵심 서술을 가까이 배치한다.** 주어와 동작 사이의 긴 수식, 여러 조건이 중첩된 문장, 지시 대상이 불분명한 `이것`을 검토한다. 필요하면 문장을 분리하고 조건·이유·결과를 연결하는 말을 명시한다.
4. **현상과 행동을 구체적으로 쓴다.** 은유나 새 용법의 동사가 실제 현상을 숨기면, 무엇이 실패·변화·차단되는지 기재한다. 정착한 기술 용어는 그대로 사용한다.
5. **근거의 강도를 보존한다.** 관찰·가능한 설명·확인한 인과를 구분한다. 수치와 단위, 분모·제외 대상, 조건·부정·예외, 검증 범위를 해당 주장 곁에 둔다.
6. **독자의 다음 판단 순서로 배치한다.** 결과를 보고하는 글은 결론에서 시작하고, 그 결론을 뒷받침하는 근거와 제한 조건을 이어 쓴다. Agent 지시는 행동과 완료 조건을 명시한다. 필요한 예시 하나로 관계를 설명하고 반복을 제거한다.

## 마지막 확인

최종 문장만 읽고 다음 질문에 답한다.

- 무엇이 달라졌고, 그 판단은 어떤 근거에 의존하는가?
- 누구 또는 무엇이 작용하며, 어떤 조건에서 결과가 성립하는가?
- 원문과 비교할 때 수치·부정·조건·불확실성·검증 범위가 보존되었는가?
- 다음 행동이 필요하다면 누가 무엇을 확인하거나 수행해야 하는가?

답이 불분명한 부분만 다시 쓴다. 원문에 없는 관계는 추측으로 보충하지 않는다. 단어 수·문장 길이·명사 개수는 검토 단서이며 합격 기준이 아니다.

## 적용 예시

아래 문장은 가상 예시이며 프로젝트의 실제 측정 결과가 아니다.

### 1. 압축된 제목의 관계 명시

원문: `holdout regression dilution mitigation gate`

**관계를 모를 때:** `holdout`에서 무엇을 측정하고 어떤 조건으로 진행을 허용하는지 확인이 필요하다. 제목만으로는 `mitigation`을 수행하였는지 알 수 없다.

**원문 설명에서 “독립 holdout으로 label noise 영향을 다시 측정한 뒤 진행”이라는 뜻이 확인된 경우:**

> 독립 holdout의 label noise 영향 재측정과 진행 조건

관계를 확인한 뒤 제목을 바꾸었다. 어색한 제목을 자연스럽게 만드는 과정에서 새로운 기술적 의미를 만들지 않는다.

### 2. 짧은 보고의 조건 보존

원문:

> timestamp snap이 label noise를 먹여 holdout regression dilution gate를 흔들었다. median error 1.4 m → 1.1 m, 개선 확인.

추가로 확인한 사실:

> Android timestamp는 10 ms grid에 snap되었다. regression dilution은 가설이다. 120 session 중 성공한 96 session만 집계하였고 실패 24 session은 제외하였다. 같은 replay data로 threshold를 선택하였다. iOS·현장 실기는 미검증이다.

개정:

> 성공한 96 session의 replay에서 median error가 1.4 m에서 1.1 m로 감소하였다. 전체 120 session 중 실패한 24 session은 집계에서 제외하였고, 같은 data로 threshold도 선택하여 independent holdout 결과로 볼 수 없다.
>
> Android timestamp가 10 ms grid에 snap되어 label에 noise가 추가되었을 가능성이 있다. regression dilution이 원인인지는 확인하지 않았다. iOS·현장 실기는 미검증이다. 후속 측정으로 성공·실패 전체 session을 포함한 새 holdout 평가를 제안한다.

원문만으로 복원할 수 없는 사실은 추가 근거가 확보된 뒤 포함하였다. 마지막 문장은 원문 사실에 근거한 후속 측정 제안이며, 합의된 계획이나 수행한 검증으로 표시하지 않았다.

### 3. 논문 해석의 범위 보존

과도한 결론:

> Reasoning training이 AI 문장을 어렵게 만들기 때문에 문장을 길게 쓰면 해결된다.

개정:

> 논문은 영어 AI output에서 읽기 어려움과 관련된 언어적 특성을 관찰하였다. 작은 model의 통제 실험에서는 length penalty가 일부 짧은 문법 형태에 대한 preference를 강화하였다. Frontier model의 실제 훈련 원인과 한국어 독해 개선 효과는 확인하지 않았다.

관찰과 제한된 실험 결과를 구분하였다. 해결책의 효과까지 입증한 것처럼 서술하지 않는다.

## 다른 지시와의 관계

사용자가 정한 용어와 문서 목적을 따른다. 한국어·영어 code-switching에서는 technical term의 표기를 유지하고 주변의 관계를 자연스러운 한국어로 작성한다. 영어 commit message에는 같은 명료성 원칙을 영어로 적용한다. 글의 내용을 기술적으로 바꾸거나 과거 증거 문서를 개정하는 권한은 이 manifest에서 부여하지 않는다.

## 재사용

현재 작업에 적용하려면 다음과 같이 요청한다.

> `/Users/janghyunbin/dev/human-readable-writing/MANIFEST.md`를 읽고 이 설명에 적용해줘. 원문에 없는 관계와 미검증 조건은 보존해.

Repository에 채택할 때는 manifest를 해당 repository의 문서 위치에 복사하고, 그 repository의 `AGENTS.md`에 다음처럼 짧은 pointer를 연결할 수 있다. 아래 상대 경로는 배치 예시이다.

```markdown
문장 개선·문서 검토를 명시적으로 요청받으면
docs/WRITING_MANIFEST.md를 읽고 적용한다.
```

최초 분석에서는 global instruction·기존 repository·skill 등록을 변경하지 않았다. 이후 사용자 요청에 따라 [SKILL.md](SKILL.md)를 전역 설치하였고, 누적 비용을 줄이기 위해 명시적으로 호출하는 검토용으로 전환하였다. 상세 작성 원칙의 정본은 이 manifest로 유지한다. 평소 답변은 기존 기본 instructions로 바로 작성한다. 설치 경로와 사용법은 [README.md](README.md)를 참조한다.

## 근거와 상태

근거는 [Why is AI-generated language so hard to understand?](https://arxiv.org/abs/2610.29162v1)이다. 위 원칙과 한국어 적용 예시는 논문의 저자들이 검증한 writing intervention이 아니라 실무 제안이다. 이 연구는 인간의 이해도를 직접 측정하지 않았다. Manifest 적용에 따른 독해 개선 효과도 미측정이다. [상세 분석](ANALYSIS.md) · [검증 기록](VALIDATION.md).

원논문의 license는 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)이며, 저자와 변경 내역은 [NOTICE.md](NOTICE.md)에 명시하였다.
