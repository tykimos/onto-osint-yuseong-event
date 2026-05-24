---
name: shop-watch
description: "용성로20 인근 신규 오픈 가게·팝업·프로모션을 50일 윈도우 동안 의무 노출하고, 누락된 가게(예: 사용자 제보 '관평동 엉클부대찌개')를 backfill하는 가게 모니터링 하네스. onto-osint-report 파이프라인의 Phase 1.5/2.5/4.5에 hook으로 결합되며, 3명의 에이전트(shop-scout, shop-curator, shop-coverage-auditor)가 팀으로 협업한다. '신규 오픈 가게', '가게 누락', '엉클부대찌개', '50일 윈도우', 'shop-watch', '가게 backfill', '신규 오픈 보강', '팝업 추적' 요청 시 사용."
---

# Shop Watch — 신규 오픈 가게 50일 윈도우 모니터링 하네스

이 하네스는 용성로20 인근에 새로 오픈한 가게/팝업/프로모션을 50일 동안 보고서에 의무 노출하고, 사용자가 제보한 누락 가게를 backfill한다. 3개 에이전트가 **에이전트 팀**으로 협업하며 결정적 스크립트가 시간 기반 전이를 처리한다.

## 실행 모드
**에이전트 팀** — `shop-scout`, `shop-curator`, `shop-coverage-auditor`가 SendMessage로 상호 통신하며, 결정적 스크립트(`shop_roster_prune.py`, `shop_roster_backfill.py`)가 윈도우 만료·backfill 같은 결정적 작업을 처리한다. 메인 오케스트레이터(onto-osint-report)가 hook으로 호출한다.

## 호출 모드

| 모드 | 트리거 | 동작 |
|------|--------|------|
| `daily` (기본) | onto-osint-report Phase 1.5에서 자동 hook | 매일 신규 가게 탐색 + 윈도우 갱신 + 보고서 검증 |
| `backfill` | 사용자가 `/shop-watch backfill <가게명>` 직접 호출 | manual_seeds에 즉시 추가 + shop-scout가 1회 단발 조사 |
| `audit_only` | 사용자가 `/shop-watch audit <YYYY-MM-DD>` 호출 | 기존 보고서 검증만 수행, 새 탐색 없음 |
| `prune` | GHA post-step 자동 실행 | 시간 기반 윈도우 만료만 처리, LLM 미사용 |

## 실행 흐름

### Phase 0: 준비
1. `config/osint-config.json`의 `shop_watch` 섹션을 읽어 윈도우 기간(`window_days`, 기본 30), 탐색 채널(`discovery_sources`), audit 모드(`audit_mode: report|patch`)를 결정
2. `ontology/shop-roster.json`이 없으면 빈 초기 구조로 생성:
   ```json
   {
     "version": "1.0.0",
     "last_updated": "YYYY-MM-DD",
     "window_days": 50,
     "active_shops": [],
     "recent_shops": [],
     "archived_shops": [],
     "manual_seeds": []
   }
   ```
3. **자동 prune**: `scripts/shop_roster_prune.py <YYYY-MM-DD>` 실행 — 만료된 active를 recent로, recent를 archived로 결정적 이동

### Phase 1: 팀 구성 및 시드 주입
1. `TeamCreate` 또는 메인 오케스트레이터가 3명의 에이전트를 차례로 호출
2. shop-roster.json의 `manual_seeds`에서 미해결 항목을 shop-scout에게 우선 작업으로 전달

### Phase 2: 가게 탐색 (shop-scout)
**에이전트:** `.claude/agents/shop-scout.md`
**입력:** `config/osint-config.json` (shop_watch.discovery_sources), `ontology/shop-roster.json` (manual_seeds + active_shops 재검증 대상)
**산출물:** `sources/YYYY-MM-DD/shop-candidates.json`

### Phase 3: 윈도우 lifecycle 관리 (shop-curator)
**에이전트:** `.claude/agents/shop-curator.md`
**입력:** `sources/YYYY-MM-DD/shop-candidates.json`, `ontology/shop-roster.json`, `ontology/instances.json`
**산출물:**
- `ontology/shop-roster.json` (갱신 — backup `.bak` 자동 생성)
- `ontology/instances.json` (Shop 인스턴스 동기화 — `window_status`, `window_expires_on` 필드 추가)
- `sources/YYYY-MM-DD/shop-roster-diff.json` (이번 사이클의 신규/만료/재발견 가게 요약)

### Phase 4: 보고서 커버리지 검증 (shop-coverage-auditor)
**에이전트:** `.claude/agents/shop-coverage-auditor.md`
**입력:** `reports/YYYY/MM/YYYY-MM-DD.md` (osint-reporter 산출물), `ontology/shop-roster.json`, `sources/YYYY-MM-DD/shop-roster-diff.json`
**산출물:**
- `sources/YYYY-MM-DD/coverage-audit.json`
- (patch 모드일 때) `reports/YYYY/MM/YYYY-MM-DD.md`에 누락 가게 추가 + "검증 로그" 섹션 부착

### Phase 5: 종료
- 검증 결과 요약을 stdout 출력
- CRITICAL이 있으면 exit code 1 (GHA에서 보고서 commit은 진행하되 워크플로우 결과는 warning으로 표시)

## onto-osint-report 파이프라인과의 연결

| onto-osint-report Phase | shop-watch hook | 실행 순서 |
|------------------------|-----------------|----------|
| Phase 0 (준비) | shop-watch Phase 0 (prune 포함) | 직렬, prune은 결정적 |
| Phase 1 (Collect) | shop-watch Phase 2 (shop-scout) | **병렬** — collector와 동시 실행 가능 |
| Phase 2 (Extract) | — | shop-scout 결과는 extractor 산출물과 별도로 보존 |
| Phase 3 (Ontology) | shop-watch Phase 3 (shop-curator) | 직렬 — reasoner 종료 후 curator가 instances.json 동기화 |
| Phase 4 (Report) | — | reporter가 shop-roster.json을 읽어 "신규 오픈" 섹션 작성 |
| Phase 5 (Publish) 직전 | shop-watch Phase 4 (auditor) | 직렬 — patch는 commit 이전에 |
| Phase 5 post | shop-watch prune (다음날 대비) | 결정적 |

## 데이터 전달

| 파일 | 생성자 | 소비자 | 비고 |
|------|--------|--------|------|
| `ontology/shop-roster.json` | curator | scout, reporter, auditor | source of truth |
| `sources/<날짜>/shop-candidates.json` | scout | curator | 일별 raw 후보 |
| `sources/<날짜>/shop-roster-diff.json` | curator | auditor, reporter | 일별 변경 요약 |
| `sources/<날짜>/coverage-audit.json` | auditor | 사용자, GHA | 검증 결과 |
| `ontology/instances.json` (Shop 인스턴스) | curator | reasoner, reporter | 동기화 필드 |

## 에러 핸들링

| 단계 | 에러 | 전략 |
|------|------|------|
| 0 | shop-roster.json 없음 | 빈 초기 구조 생성 후 진행 |
| 0 | prune 스크립트 실패 | 윈도우 만료 미수행, daily 계속 진행하되 auditor가 경고 |
| 2 | shop-scout 0건 발견 + manual_seeds 미해결 | 기존 roster 유지, auditor가 사용자에게 "이번 사이클 신규 0건" 명시 |
| 3 | curator의 dedupe 모호 | 두 인스턴스 모두 보존 + `dedupe_conflict: true` 플래그, 사용자 확인 요청 |
| 4 | auditor가 CRITICAL 발견 + patch 모드 | 보고서에 누락 가게 표 추가 + "검증 로그" 섹션 + exit 1 |
| 4 | auditor가 CRITICAL 발견 + report 모드 | exit 1, patch 없이 보고서 그대로 commit (사용자 결정 대기) |

## 팀 크기 가이드라인 적용

- 3명 (scout, curator, auditor) — 중규모 작업에 적합
- 팀원당 작업 수: scout 1~10개 후보, curator 동일 + dedupe, auditor 1개 보고서 검증
- 의존성: scout → curator → auditor (직선)
- 통신 빈도: scout↔curator (manual_seeds 협의), curator↔auditor (roster 최신성 확인) — 사이클당 0~3회 메시지

## 테스트 시나리오

### 정상 흐름 1 — daily 모드
1. shop-roster.json에 active 5건, manual_seeds 1건 ("관평동 엉클부대찌개")
2. shop-watch daily 실행
3. shop-scout가 엉클부대찌개를 Naver Place에서 발견, opened_date 2026-05-15 추정
4. shop-curator가 active_shops에 추가 (window_expires_on: 2026-06-14)
5. osint-reporter가 보고서 작성 후, shop-coverage-auditor가 "신규 오픈" 섹션에 엉클부대찌개 노출 확인 (CRITICAL 0건)
6. 검증 통과

### 정상 흐름 2 — backfill 모드
1. 사용자가 `/shop-watch backfill 전민동 새로운카페이름` 실행
2. `scripts/shop_roster_backfill.py`가 manual_seeds에 즉시 추가
3. shop-scout 단발 호출 — 즉시 조사 (24시간 내 다음 daily에서 처리)
4. 사용자가 다음날 보고서에서 결과 확인

### 에러 흐름 1 — 발견 실패
1. manual_seeds에 "허위 가게이름" 등록
2. shop-scout 3일간 0건 발견
3. shop-curator가 `status: gave_up`으로 전환
4. auditor가 보고서에 "다음 가게를 찾지 못함: 허위 가게이름 (3회 시도)" 명시 → 사용자가 정정 가능

### 에러 흐름 2 — 윈도우 만료
1. active_shops에 opened_date 2026-04-20 가게 (윈도우 5/20 만료)
2. 2026-05-21 prune 실행 → active → recent 이동
3. 2026-05-21 보고서의 "신규 오픈" 본문 섹션에서 제거되되, "최근 오픈 (참고)" 보조 섹션에 노출
4. 2026-06-20 prune → recent → archived, 보고서 노출 종료
