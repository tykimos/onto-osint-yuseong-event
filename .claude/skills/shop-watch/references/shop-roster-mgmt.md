# Shop Roster Management — 30일 윈도우 lifecycle

## 목차
- [shop-roster.json 스키마](#shop-rosterjson-스키마)
- [윈도우 상태 머신](#윈도우-상태-머신)
- [Dedupe 알고리즘](#dedupe-알고리즘)
- [manual_seeds 처리 절차](#manual_seeds-처리-절차)
- [instances.json 동기화](#instancesjson-동기화)

## shop-roster.json 스키마

```json
{
  "version": "1.0.0",
  "last_updated": "YYYY-MM-DD",
  "window_days": 30,
  "recent_window_days": 60,
  "active_shops": [
    {
      "id": "shop-001",
      "name": "엉클부대찌개 관평동점",
      "shop_type": "식당",
      "dong": "관평동",
      "address": "대전 유성구 ...",
      "distance_from_anchor_m": 2500,
      "ring": "ring-bike",
      "kid_friendly": true,
      "phone": "042-...",
      "open_hours": "11:00~22:00",
      "opened_date": "2026-05-15",
      "opened_date_estimated": true,
      "opened_date_min": "2026-05-10",
      "opened_date_max": "2026-05-20",
      "window_status": "active",
      "window_started_on": "2026-05-15",
      "window_expires_on": "2026-06-14",
      "promotions": [
        { "text": "오픈 기념 10% 할인", "valid_until": "2026-05-31" }
      ],
      "discovery_channels": ["naver-place", "instagram"],
      "source_urls": ["https://...", "https://..."],
      "confidence": 0.8,
      "first_seen": "2026-05-24",
      "last_verified": "2026-05-24",
      "re_discovered_on": null,
      "opened_date_history": [
        { "value": "2026-05-15", "set_on": "2026-05-24", "set_by": "shop-scout", "confidence": 0.8 }
      ],
      "dedupe_conflict": false,
      "notes": "사용자 제보로 발견"
    }
  ],
  "recent_shops": [],
  "archived_shops": [],
  "suspected_closed_shops": [],
  "manual_seeds": [
    {
      "seed_name": "관평동 엉클부대찌개",
      "added_on": "2026-05-24",
      "added_by": "user",
      "note": "사용자가 5/24 대화에서 제보",
      "status": "pending",
      "search_attempts": 0,
      "resolved_to": null
    }
  ]
}
```

**필드 의미:**
- `window_status`: `active` | `recent` | `archived` | `suspected_closed`
- `window_started_on`: opened_date와 동일 (단 미상 시 first_seen)
- `window_expires_on`: window_started_on + window_days
- `re_discovered_on`: archived 가게가 새 출처에서 다시 발견된 날짜 (윈도우는 재시작하지 않음)
- `dedupe_conflict`: 자동 dedupe가 모호하여 사람 확인이 필요한 상태

## 윈도우 상태 머신

```
        [신규 발견]
            ▼
       ┌─────────┐ (오픈일 + window_days 경과)
       │ active  │ ─────────────────────────┐
       └────┬────┘                          ▼
            │                          ┌─────────┐
            │ (폐업 의심)              │ recent  │
            ▼                          └────┬────┘
       ┌──────────────────┐                 │ (recent_window_days 경과)
       │ suspected_closed │                 ▼
       └────────┬─────────┘            ┌──────────┐
                │ (재확인)             │ archived │ ◀── [재발견 시 re_discovered_on 갱신, 윈도우 재시작 X]
                ▼                      └──────────┘
       ┌─────────────┐
       │ archived    │
       └─────────────┘
```

**전이 규칙:**

| 현재 상태 | 트리거 | 다음 상태 | 처리자 |
|----------|--------|----------|--------|
| (없음) | shop-scout가 신규 발견 + opened_date 추정 가능 | active | curator |
| active | 오늘 > window_expires_on | recent | prune script |
| recent | 오늘 > window_started_on + recent_window_days | archived | prune script |
| active/recent | 폐업 의심 단서 (인스타 6개월 미게시 등) | suspected_closed | scout/curator |
| suspected_closed | 30일 내 재확인 안 됨 | archived | prune script |
| archived | 새 출처에서 재발견 | archived (re_discovered_on 갱신) | curator |

**왜 윈도우를 재시작하지 않는가:** 이미 알려진 가게가 다시 화제가 되었다고 해서 "신규 오픈"으로 분류하면 사용자에게 오해를 준다. 단, `re_discovered_on`을 기록하여 reporter가 "재조명" 같은 별도 섹션을 만들 수 있게 한다.

## Dedupe 알고리즘

shop-scout 후보(`shop-candidates.json`)와 기존 roster + instances.json의 Shop 인스턴스를 비교한다.

**우선순위 매칭 키:**

1. **전화번호 일치** → 동일 가게 확정 (신뢰도 1.0)
2. **주소 + 상호 부분일치 (Levenshtein 80%+)** → 동일 가게 (신뢰도 0.9)
3. **상호 + 동 + shop_type 일치** → 동일 가게 후보 (신뢰도 0.7)
4. **상호만 일치 + 동 다름** → 다른 지점, 별도 인스턴스 (예: "엉클부대찌개 관평동점" vs "엉클부대찌개 도룡동점")
5. **부분 매칭만 60~70%** → `dedupe_conflict: true`, 두 인스턴스 모두 보존 + auditor가 사용자 확인 요청

**병합 규칙 (동일 가게로 판정 시):**

- `opened_date`: 더 이른 날짜 채택, 변경 사실은 `opened_date_history`에 기록
- `confidence`: 두 인스턴스의 max
- `source_urls`: 합집합
- `promotions`: 합집합 (valid_until 기준 만료 자동 제거는 prune이 처리)
- `last_verified`: 더 최신 날짜
- `first_seen`: 더 이른 날짜

## manual_seeds 처리 절차

### 등록 (3가지 경로)

1. **사용자 직접**: `scripts/shop_roster_backfill.py add "<가게명>" --dong "<동>" --note "사용자 제보"` 또는 사용자가 대화에서 제보 시 curator가 직접 추가
2. **auditor 발견**: 보고서 검증 중 사용자가 댓글/PR에서 누락 가게를 언급하면 manual_seeds로 등록
3. **재조사 큐**: opened_date 추정 실패한 active 가게가 7일 후에도 확정 안 되면 자동으로 manual_seeds에 재등록 (조사 강도 ↑)

### 처리 사이클

```
[등록] → status: pending, search_attempts: 0
  ↓
[shop-scout 시도] → search_attempts += 1
  ├─ 발견 → resolved_to: shop-XXX, status: resolved, active_shops에 추가, manual_seeds에서 제거
  └─ 미발견 → status 유지
       ├─ search_attempts < 3 → 다음 사이클 재시도
       └─ search_attempts >= 3 → status: gave_up, auditor가 보고서에 "찾지 못함" 명시
```

### 사용자 가시성

매일 보고서의 "신규 오픈 가게·팝업·프로모션" 섹션 하단에 manual_seeds 처리 현황을 표시한다 (auditor가 patch):

```markdown
### 사용자 제보 처리 현황

| 제보 가게 | 등록일 | 상태 | 결과 |
|----------|-------|------|------|
| 관평동 엉클부대찌개 | 2026-05-24 | resolved | → shop-001 (active 목록에 추가됨) |
| 전민동 새로운카페 | 2026-05-20 | pending (2회 시도) | 다음 사이클 재시도 |
| 허위가게이름 | 2026-05-15 | gave_up | 3회 시도 후 미발견 — 가게명 재확인 필요 |
```

이 표가 있으면 사용자는 자신의 제보가 시스템에 반영되었음을 매일 확인할 수 있고, 가게명 오타 같은 입력 오류를 빨리 정정할 수 있다.

## instances.json 동기화

shop-roster.json이 source of truth지만, 기존 파이프라인(reasoner, reporter)이 instances.json을 읽으므로 Shop 인스턴스는 양쪽에 동기화한다.

**동기화 규칙:**

- roster의 `active_shops` + `recent_shops` → instances.json의 Shop 인스턴스로 upsert
- `window_status`, `window_expires_on`, `promotions` 같은 새 필드는 instances.json의 `properties` 안에 중첩
- `archived_shops`도 instances.json에 보존 (history)
- 충돌 시 roster 우선 — 다만 reasoner가 추가한 관계(`shopHosts` 등)는 보존

**예시 — instances.json 내 Shop:**

```json
{
  "id": "shop-001",
  "type": "Shop",
  "name": "엉클부대찌개 관평동점",
  "properties": {
    "shop_type": "식당",
    "dong": "관평동",
    "address": "대전 유성구 ...",
    "distance_from_anchor_m": 2500,
    "ring": "ring-bike",
    "kid_friendly": true,
    "opened_date": "2026-05-15",
    "is_new": true,
    "window_status": "active",
    "window_expires_on": "2026-06-14",
    "promotions": [
      { "text": "오픈 기념 10% 할인", "valid_until": "2026-05-31" }
    ]
  },
  "first_seen": "2026-05-24",
  "last_seen": "2026-05-24",
  "mention_count": 1
}
```

reasoner가 `new_shop_event_combo` 같은 추론 규칙을 적용할 때 `is_new` + `window_status: active`를 결합해서 사용한다.
