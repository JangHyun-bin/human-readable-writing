# Korean finance correction review

Status: accepted after explicit review feedback. Reviewer: integration owner, not the separate agent that reviewed the first attempt.

- [Unchanged original](../../../examples/professional/finance/before.ko.md)
- [First failed review](../../../examples/professional/finance/review.md)
- [Feedback](feedback.md), [actual correction request](finance/ko/request.md), [raw corrected output](finance/ko/output.md), and [capture metadata](finance/ko/attempt.json)
- [Fact-by-fact correction review](review.json)

The first revision joined two independent assumptions with “가정했기 때문이다”, adding a causal explanation absent from the original. The separate correction states them independently:

> 그 밖의 조정 합계는 설계상 0이다. 또한 인수·환산·제각·재분류 또는 그 밖의 비현금 변동이 위 잔액 증감에 영향을 주지 않는다고 가정했다.

The full corrected document was compared with F01–F10 and the original Korean text. Periods, units, balances, adjustment signs, both cash-flow reconciliations, the change bridge, and unknown-versus-zero boundaries remain intact. F07 no longer introduces the unsupported cause.

The correction ran in a fresh native session with the same source, package hashes, Claude Code 2.1.322 and `claude-sonnet-5-5`. It was not an automatic retry or a manual edit of the model output. The original failed output and review remain unchanged. This acceptance is a textual source-fidelity review, not a measure of readability or general model reliability.
