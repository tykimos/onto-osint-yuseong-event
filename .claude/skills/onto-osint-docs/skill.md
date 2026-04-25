---
name: onto-osint-docs
description: "onto-osint 프로젝트의 README 및 알고리즘 문서를 설계, 작성, 시각화, 검증하는 문서 파이프라인. 'README 개선', '문서 업데이트', 'docs 다시 써줘', '알고리즘 설명 추가' 요청 시 사용."
---

# Onto-OSINT Docs — 문서 파이프라인 오케스트레이터

3개 에이전트를 순차적으로 연결하여 README를 생성/개선한다.

## 실행 모드
서브 에이전트 파이프라인 — 산출물이 단일 README.md이므로 순차 정제가 적합.

## 실행 흐름

### Phase 1: 구조 설계 & 본문 작성
**에이전트:** `.claude/agents/doc-architect.md`
**입력:** 현재 README.md, config/, .claude/agents/, .claude/skills/
**산출물:** `_workspace/01_doc_draft.md`

### Phase 2: 다이어그램 생성
**에이전트:** `.claude/agents/diagram-specialist.md`
**입력:** `_workspace/01_doc_draft.md`
**산출물:** `_workspace/02_diagrams.md`
→ 다이어그램을 본문 초안에 통합하여 `_workspace/01_doc_draft.md` 업데이트

### Phase 3: 초보자 검증
**에이전트:** `.claude/agents/beginner-reviewer.md`
**입력:** 통합된 `_workspace/01_doc_draft.md`
**산출물:** `_workspace/03_review.md`
→ 리뷰 결과를 반영하여 최종 README.md 생성

### Phase 4: 최종 출력
리뷰 피드백을 반영하여 `README.md`를 최종 업데이트한다.

## 에러 핸들링
| Phase | 에러 | 전략 |
|-------|------|------|
| 1 | 현재 README 없음 | 처음부터 새로 작성 |
| 2 | 다이어그램 렌더링 이슈 | 단순한 형태로 폴백 |
| 3 | 리뷰어 피드백 없음 | Phase 2 결과를 최종으로 사용 |

## 테스트 시나리오

### 정상 흐름
1. "README 개선해줘" 요청
2. 3단계 파이프라인 실행
3. _workspace/에 중간 산출물 3개 생성 확인
4. README.md 최종 업데이트 확인

### 부분 업데이트
1. "다이어그램만 개선해줘" 요청
2. Phase 2만 실행하여 다이어그램 교체
