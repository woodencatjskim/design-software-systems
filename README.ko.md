# Design Software Systems

[English](README.md) · [평가 기록](evals/README.md) · [출처](docs/sources.md)

요구사항을 검토 가능한 설계로 바꾸는 Agent Skill입니다. **새 시스템 설계, 기존 시스템 개선, 아키텍처 검토**에 사용합니다.

## 설치

```bash
npx skills add woodencatjskim/design-software-systems --skill design-software-systems
```

설치 도구에서 사용할 agent를 선택합니다. 특정 대상으로 설치하려면 `-a codex`, `-a claude-code`, `-a cursor` 등을 사용합니다. CLI에 필요한 Node.js 버전은 [현재 설치 문서](https://github.com/vercel-labs/skills)를 확인하세요. skill 자체에는 별도 실행 환경이나 API 키가 필요하지 않습니다.

수동 설치 시 `skills/design-software-systems/` 폴더 전체를 agent의 공식 skill 경로로 복사하세요. [호환성 문서](docs/compatibility.md)는 설치 검증과 실제 실행 검증을 구분합니다.

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

[작은 서비스](examples/small-document-catalog.md), [예약](examples/hotel-booking.md), [메시징 검토](examples/messaging-review.md) 예시와 [평가 과제](evals/prompts.json)를 제공합니다. 예시는 교육용이며 실제 운영 성능을 입증하지 않습니다.

## 출처와 기여

Hayk Simonyan의 [Design Software Systems Like a Senior Engineer – Complete Course](https://www.youtube.com/watch?v=soTfFFIQQ8U), freeCodeCamp.org 공개 강의를 참고해 제작했습니다. 강의 분석 과정에서 필요한 기술 보완을 반영하고, 다른 공개 skill의 강점도 검토했습니다. 자세한 내용은 [출처](docs/sources.md)와 [한국어 분석 문서](docs/system-design-course-analysis.ko.md)를 참고하세요. 원본 자막 전체나 영상 자료는 재배포하지 않습니다.

[기여 방법](CONTRIBUTING.md) · [MIT 라이선스](LICENSE)
