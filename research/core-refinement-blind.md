# 지침을 가린 답변 비교

입력 사실과 독자의 이해 부담을 기준으로 A·B·C를 비교한다. 조건 이름·지침·usage·시간은 제외하였다. 답변은 실제 생성 결과이며 문구와 문단을 편집하지 않았다.

대표 비교는 사전에 정한 각 과제의 첫 repeat인 T1·T6·T7이다. T2–T5는 같은 coding 과제의 추가 반복이다. 비교 간 A·B·C가 같은 조건을 뜻하지 않는다.

## T1 — Coding 보고 · repeat 1

### 입력

> 동료에게 보낼 작업 결과를 4문장 이내로 작성해줘.
> Android pose timestamp가 20 ms grid에 snap되었다. label noise가 발생했을 가능성이
> 있지만 regression dilution이 원인인지는 미확인이다. Replay에서 p95 error가
> 2.4 m에서 1.8 m로 감소했다. 전체 150 session 중 성공한 135 session만 집계했고
> 실패한 15 session은 제외했다. 같은 data로 threshold도 선택하여 independent
> holdout이 아니다. iOS와 현장 실기는 미검증이다. 다음 행동은 전체 session을 포함한
> 별도 holdout 평가를 제안하는 것이며 확정된 계획은 아니다.

### A

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다. Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외한 결과입니다.
> 
> 같은 data로 threshold도 선택했으므로 independent holdout 평가가 아니며, 개선 효과를 일반화하기에는 한계가 있습니다. iOS와 현장 실기는 미검증이며, 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하지만 확정된 계획은 아닙니다.

### B

> Android pose timestamp가 20 ms grid에 snap되었으며, label noise가 발생했을 가능성은 있지만 regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했지만, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다.
> 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 아직 확정된 계획은 아닙니다.
> threshold도 같은 data로 선택했으므로 independent holdout이 아니고 iOS와 현장 실기도 미검증이라, 관찰된 개선을 일반화하기에는 한계가 있습니다.

### C

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다.
> 같은 data로 threshold도 선택해 independent holdout이 아니므로, 전체 session을 포함한 별도 holdout 평가를 제안하며 아직 확정된 계획은 아닙니다.
> iOS와 현장 실기는 미검증이며, 현재 결과를 전체 session의 성능 개선으로 일반화하기에는 한계가 있습니다.

## T6 — API 문서 · repeat 1

### 입력

> 다음 사실로 API 사용 문서를 4문장 이내로 작성해줘.
> Caller가 같은 job_id로 요청하면 server는 처음 성공한 결과를 반환한다.
> 같은 job_id로 payload가 바뀌면 HTTP 409를 반환한다. 결과 보관 기간은 24 h이며,
> 그 이후 또는 다른 region에서는 중복 실행 방지를 보장하지 않는다.
> Client timeout은 server의 실행 실패를 뜻하지 않는다. Timeout 뒤 재시도에는
> 같은 job_id를 사용하도록 안내한다. Unit test 12개가 통과했지만 production 검증은
> 수행하지 않았다.

### A

> Caller가 같은 `job_id`로 요청하면 server는 처음 성공한 결과를 반환하며, 같은 `job_id`의 payload가 바뀌면 HTTP 409를 반환합니다.
> Client timeout은 server의 실행 실패를 뜻하지 않으므로, timeout 뒤 재시도에는 같은 `job_id`를 사용하세요.
> 
> 결과 보관 기간은 24 h이며, 그 이후 또는 다른 region에서는 중복 실행 방지를 보장하지 않습니다.
> Unit test 12개는 통과했지만 production 검증은 수행하지 않았습니다.

### B

> Caller가 같은 `job_id`로 요청하면 server는 처음 성공한 결과를 반환하며, 같은 `job_id`로 `payload`가 바뀌면 HTTP 409를 반환한다.
> Client timeout은 server의 실행 실패를 뜻하지 않으므로, timeout 뒤 재시도에는 같은 `job_id`를 사용한다.
> Unit test 12개가 통과했지만 production 검증은 수행하지 않았다.
> 결과 보관 기간은 24 h이며, 그 이후 또는 다른 region에서는 중복 실행 방지를 보장하지 않는다.

### C

> Caller가 같은 `job_id`로 요청하면 server는 처음 성공한 결과를 반환하며, 같은 `job_id`로 payload가 바뀌면 HTTP 409를 반환한다.
> Client timeout은 server의 실행 실패를 뜻하지 않으므로, timeout 뒤 재시도에는 같은 `job_id`를 사용한다.
> 결과 보관 기간은 24 h이며, 그 이후 또는 다른 region에서는 중복 실행 방지를 보장하지 않는다.
> Unit test 12개가 통과했지만 production 검증은 수행하지 않았다.

## T7 — Incident 경과 · repeat 1

### 입력

> 다음 사실로 장애 경과를 동료에게 4문장 이내로 설명해줘.
> 14:00 배포 후 14:02에 HTTP 503 비율이 1.2%에서 8.6%로 증가했다.
> 14:09 app version을 rollback했고 14:12에 1.5%로 측정되었다.
> DB schema는 변경하지 않았다. DB connection pool 지표는 수집하지 않아 원인은
> 미확인이다. Rollback과 비율 감소의 인과관계도 확정하지 않았다.
> 다음 행동으로 별도 부하 test와 pool 지표 수집을 제안하지만 실행은 미정이다.

### A

> 14:00 배포 후 14:02에 HTTP 503 비율이 1.2%에서 8.6%로 증가했다.
> 14:09에 app version을 rollback했고 14:12에는 1.5%로 측정되었으며, DB schema는 변경하지 않았다.
> 다음 행동으로 별도 부하 test와 DB connection pool 지표 수집을 제안하지만 실행 여부는 미정이다.
> DB connection pool 지표를 수집하지 않아 원인은 미확인이며, rollback과 비율 감소의 인과관계도 확정하지 않았다.

### B

> 14:00 배포 후 14:02에 HTTP 503 비율이 1.2%에서 8.6%로 증가했다.
> 14:09에 app version을 rollback했고 14:12에 비율이 1.5%로 측정됐으며, DB schema는 변경하지 않았다.
> 다음 행동으로 별도 부하 test와 pool 지표 수집을 제안하지만 실행 여부는 미정이다.
> DB connection pool 지표를 수집하지 않아 원인은 미확인이며, rollback과 비율 감소의 인과관계도 확정하지 않았다.

### C

> 14:00 배포 후 14:02에 HTTP 503 비율이 1.2%에서 8.6%로 증가했다.
> 14:09에 app version을 rollback했고, 14:12에는 HTTP 503 비율이 1.5%로 측정되었다.
> 별도 부하 test와 DB connection pool 지표 수집을 다음 행동으로 제안하지만, 실행 여부는 미정이다.
> DB schema는 변경하지 않았으며, DB connection pool 지표를 수집하지 않아 원인은 미확인이고 rollback과 비율 감소의 인과관계도 확정하지 않았다.

## T2 — Coding 보고 · repeat 2

### 입력

> 동료에게 보낼 작업 결과를 4문장 이내로 작성해줘.
> Android pose timestamp가 20 ms grid에 snap되었다. label noise가 발생했을 가능성이
> 있지만 regression dilution이 원인인지는 미확인이다. Replay에서 p95 error가
> 2.4 m에서 1.8 m로 감소했다. 전체 150 session 중 성공한 135 session만 집계했고
> 실패한 15 session은 제외했다. 같은 data로 threshold도 선택하여 independent
> holdout이 아니다. iOS와 현장 실기는 미검증이다. 다음 행동은 전체 session을 포함한
> 별도 holdout 평가를 제안하는 것이며 확정된 계획은 아니다.

### A

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다.
> 같은 data로 threshold도 선택했으므로 independent holdout 평가가 아니며, iOS와 현장 실기도 미검증입니다.
> 다음 행동으로 실패한 session까지 전체 session을 포함한 별도 holdout 평가를 제안하며, 아직 확정된 계획은 아닙니다.

### B

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인이다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계했고 실패한 15 session은 제외했다.
> 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 확정된 계획은 아니다.
> 같은 data로 threshold도 선택했으므로 independent holdout이 아니며, iOS와 현장 실기도 미검증이어서 관찰된 개선을 일반화하기 어렵다.

### C

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다.
> 같은 data로 threshold도 선택해 independent holdout이 아니므로, 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며 확정된 계획은 아닙니다.
> iOS와 현장 실기는 미검증이며, 실패 session 제외와 data 재사용으로 현재 결과의 일반화 여부는 확인되지 않았습니다.

## T3 — Coding 보고 · repeat 3

### 입력

> 동료에게 보낼 작업 결과를 4문장 이내로 작성해줘.
> Android pose timestamp가 20 ms grid에 snap되었다. label noise가 발생했을 가능성이
> 있지만 regression dilution이 원인인지는 미확인이다. Replay에서 p95 error가
> 2.4 m에서 1.8 m로 감소했다. 전체 150 session 중 성공한 135 session만 집계했고
> 실패한 15 session은 제외했다. 같은 data로 threshold도 선택하여 independent
> holdout이 아니다. iOS와 현장 실기는 미검증이다. 다음 행동은 전체 session을 포함한
> 별도 holdout 평가를 제안하는 것이며 확정된 계획은 아니다.

### A

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인이다. Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계했고 실패한 15 session은 제외했다. 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 확정된 계획은 아니다.
> 같은 data로 threshold도 선택했으므로 이번 평가는 independent holdout이 아니며, iOS와 현장 실기는 미검증이다.

### B

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계했고 실패한 15 session은 제외했습니다.
> 같은 data로 threshold도 선택했으므로 independent holdout이 아니며, 이 결과만으로 전체 session의 개선을 판단하기는 어렵습니다.
> iOS와 현장 실기는 미검증이며, 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하지만 확정된 계획은 아닙니다.

### C

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외한 결과입니다.
> 같은 data로 threshold도 선택했으므로 independent holdout이 아니며, iOS와 현장 실기는 미검증입니다.
> 이러한 평가 조건 때문에 전체 session에서의 성능 개선을 확정하기 어려워, 전체 session을 포함한 별도 holdout 평가를 다음 행동으로 제안하며 아직 확정된 계획은 아닙니다.

## T4 — Coding 보고 · repeat 4

### 입력

> 동료에게 보낼 작업 결과를 4문장 이내로 작성해줘.
> Android pose timestamp가 20 ms grid에 snap되었다. label noise가 발생했을 가능성이
> 있지만 regression dilution이 원인인지는 미확인이다. Replay에서 p95 error가
> 2.4 m에서 1.8 m로 감소했다. 전체 150 session 중 성공한 135 session만 집계했고
> 실패한 15 session은 제외했다. 같은 data로 threshold도 선택하여 independent
> holdout이 아니다. iOS와 현장 실기는 미검증이다. 다음 행동은 전체 session을 포함한
> 별도 holdout 평가를 제안하는 것이며 확정된 계획은 아니다.

### A

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다. Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다. 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 확정된 계획은 아닙니다.
> 
> 같은 data로 threshold도 선택했으므로 independent holdout이 아니며, iOS와 현장 실기도 미검증이어서 결과를 일반화하는 데 한계가 있습니다.

### B

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다. Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다. 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 확정된 계획은 아닙니다.
> 
> 같은 data로 threshold도 선택해 independent holdout이 아니고 iOS와 현장 실기는 미검증이므로, 개선 결과의 일반화 여부는 확인되지 않았습니다.

### C

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성은 있지만, regression dilution이 원인인지는 미확인이다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했다.
> 같은 data로 threshold도 선택했으므로 independent holdout 평가가 아니며, 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하지만 확정된 계획은 아니다.
> iOS와 현장 실기는 미검증이며, 현재 결과만으로 전체 session이나 다른 환경에서도 error가 감소한다고 판단할 수는 없다.

## T5 — Coding 보고 · repeat 5

### 입력

> 동료에게 보낼 작업 결과를 4문장 이내로 작성해줘.
> Android pose timestamp가 20 ms grid에 snap되었다. label noise가 발생했을 가능성이
> 있지만 regression dilution이 원인인지는 미확인이다. Replay에서 p95 error가
> 2.4 m에서 1.8 m로 감소했다. 전체 150 session 중 성공한 135 session만 집계했고
> 실패한 15 session은 제외했다. 같은 data로 threshold도 선택하여 independent
> holdout이 아니다. iOS와 현장 실기는 미검증이다. 다음 행동은 전체 session을 포함한
> 별도 holdout 평가를 제안하는 것이며 확정된 계획은 아니다.

### A

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다.
> 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 아직 확정된 계획은 아닙니다.
> 같은 data로 threshold도 선택했으므로 independent holdout이 아니고, iOS와 현장 실기도 미검증이어서 이번 개선을 전체 session과 실제 환경에 일반화할 근거는 아직 부족합니다.

### B

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인이다. Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했다. 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며, 확정된 계획은 아니다.
> 
> 같은 data로 threshold도 선택했으므로 independent holdout 결과가 아니며, iOS와 현장 실기는 미검증이어서 성능 개선을 일반화하기에는 한계가 있다.

### C

> Android pose timestamp가 20 ms grid에 snap되어 label noise가 발생했을 가능성이 있지만, regression dilution이 원인인지는 미확인입니다.
> Replay에서 p95 error는 2.4 m에서 1.8 m로 감소했으나, 전체 150 session 중 성공한 135 session만 집계하고 실패한 15 session은 제외했습니다.
> 같은 data로 threshold도 선택해 independent holdout이 아니므로, 다음 행동으로 전체 session을 포함한 별도 holdout 평가를 제안하며 아직 확정된 계획은 아닙니다.
> iOS와 현장 실기는 미검증이며, 실패 session 제외와 threshold 선택에 사용한 data 재사용으로 성능이 실제보다 좋게 평가됐을 수 있습니다.

