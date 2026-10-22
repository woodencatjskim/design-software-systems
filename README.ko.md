# Design Software Systems

[English](README.md) · [평가 기록](evals/README.md) · [출처](docs/sources.md)

요구사항을 검토 가능한 설계로 바꾸는 Agent Skill입니다. **새 시스템 설계, 기존 시스템 개선, 아키텍처 검토**에 사용합니다.

## 설치

```bash
npx skills add woodencatjskim/design-software-systems --skill design-software-systems
```

설치 도구에서 사용할 agent를 선택합니다. 특정 대상으로 설치하려면 `-a codex`, `-a claude-code`, `-a cursor` 등을 사용합니다. CLI에 필요한 Node.js 버전은 [현재 설치 문서](https://github.com/vercel-labs/skills)를 확인하세요. skill 자체에는 별도 실행 환경이나 API 키가 필요하지 않습니다.

수동 설치 시 `skills/design-software-systems/` 폴더 전체를 agent의 공식 skill 경로로 복사하세요. [호환성 문서](docs/compatibility.md)는 설치 검증과 실제 실행 검증을 구분합니다.

[릴리스 페이지](https://github.com/woodencatjskim/design-software-systems/releases)에서 skill 전용 ZIP과 SHA-256 체크섬도 받을 수 있습니다.

## 사용 예시

각 agent에서 skill을 선택한 다음 요청합니다. Codex에서는 `$design-software-systems`로 호출할 수 있습니다.

```text
$design-software-systems 호텔 예약 서비스를 설계해줘.
동일 요청 재전송, 마지막 객실 동시 예약, 결제 타임아웃과
점유 만료 후 늦게 도착한 결제 결과를 포함해줘.
```

```text
design-software-systems로 이 메시징 설계를 검토해줘.
성공 응답 직후 서버가 종료되거나 Redis 알림을 놓쳐도
메시지를 복구할 수 있는지 확인해줘.
```

핵심 지침은 영어로 작성되었으며 결과는 사용자의 언어로 제공합니다. 작은 결정은 짧게, 복잡한 작업은 설계 문서로 정리합니다.

## 얻을 수 있는 결과

- 요구사항·가정·미해결 질문, 단위가 명확한 용량 추정
- 데이터 모델과 API, 구성 요소별 책임, 정상·실패 흐름
- 정합성·멱등성·영속성 검토와 기술 선택의 대가
- 기존 시스템의 호환성·이행·되돌림 계획
- 구현 후 확인할 구체적인 검증 조건

저장소 검토에서는 다른 쓰기 경로와 응답 필드까지 추적하고, 구체적인 실패 순서를 만든 뒤 DB 제약·상위 권한 검사 같은 보호 장치가 그 순서를 막는지 확인합니다. 실제 결함, 조건부 위험, 근거 부족을 구분하며 정상 경로에는 결함이 없다고 답할 수 있습니다. [검토 절차](skills/design-software-systems/references/repository-review.md)와 [신뢰 경계 지침](skills/design-software-systems/references/security-and-trust-boundaries.md)은 관련 작업에서만 읽습니다.

[작은 서비스](examples/small-document-catalog.md), [예약](examples/hotel-booking.md), [메시징 검토](examples/messaging-review.md) 예시와 [평가 과제](evals/prompts.json)를 제공합니다. 예시는 교육용이며 실제 운영 성능을 입증하지 않습니다.

## 검증 범위

패키지 검사와 단위 테스트 7개가 Python 3.11·3.13 CI에서 통과했고, GitHub에서 Codex·Claude Code·Cursor 대상으로 설치한 10개 파일의 일치를 확인했습니다. 각 앱의 자동 호출과 실제 시스템 성능은 검증하지 않았습니다.

위 설치 기록은 v0.1.0 기준입니다. 현재 개발 버전에는 [저장소 검토 평가](evals/repository-review/README.md)용 정상·결함 쌍 3개와 근거 부족 사례 1개, 그 동작을 확인하는 테스트 7개가 추가되어 전체 테스트는 14개입니다. 코드의 실제 동작 검사와 agent 답변 평가는 구분합니다.

개발 버전 비교 실행은 subagent 사용 한도로 중단됐습니다. 14회 계획 중 8개 응답이 완료됐고, 2회는 실행 오류, 4회는 미실행입니다. 완료 답변과 미완료 상태를 [평가 기록](evals/results/2026-10-22-repository-review/README.md)에 보존했으며 개선 우위를 주장하지 않습니다.

8개 과제를 세 조건에서 비교한 결과, 주요 설계 기준은 모두 충족했지만 **기본 agent나 비교 skill보다 품질이 높다는 근거는 얻지 못했습니다.** 새 skill 답변에는 두 문단 요청 앞에 라벨을 덧붙인 형식 문제가 하나 있었습니다. 원문과 기준별 판단을 [평가 기록](evals/README.md)에 공개합니다.

## 출처와 기여

Hayk Simonyan의 [Design Software Systems Like a Senior Engineer – Complete Course](https://www.youtube.com/watch?v=soTfFFIQQ8U), freeCodeCamp.org 공개 강의를 참고해 제작했습니다. 강의 분석 과정에서 필요한 기술 보완을 반영하고, 다른 공개 skill의 강점도 검토했습니다. 자세한 내용은 [출처](docs/sources.md)와 [한국어 분석 문서](docs/system-design-course-analysis.ko.md)를 참고하세요. 원본 자막 전체나 영상 자료는 재배포하지 않습니다.

[기여 방법](CONTRIBUTING.md) · [MIT 라이선스](LICENSE)
