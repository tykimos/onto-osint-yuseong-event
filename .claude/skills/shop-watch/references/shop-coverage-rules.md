# Shop Coverage Rules — 보고서 의무 커버 검증·patch 규칙

## 목차
- [3종 의무 커버 정의](#3종-의무-커버-정의)
- [윈도우 노출 의무](#윈도우-노출-의무)
- [누락 검출 알고리즘](#누락-검출-알고리즘)
- [Patch 템플릿](#patch-템플릿)
- [coverage-audit.json 스키마](#coverage-auditjson-스키마)
- [심각도 등급](#심각도-등급)

## 3종 의무 커버 정의

CLAUDE.md의 "추적 대상 3종 의무 커버" 규칙을 자동 검증한다.

| 카테고리 | 보고서에서 확인할 섹션 | 충족 조건 |
|---------|---------------------|----------|
| (a) 어린이·가족 이벤트 | "신규 이벤트", "오늘의 추천", "마감 임박", "동심원별 묶음" | 위 섹션 중 1개 이상에 Event 항목 1건 이상 |
| (b) 신규 오픈 가게·팝업 | "신규 오픈 가게·팝업·프로모션" | shop-roster.json의 active_shops와 동일 개수 또는 "금일 신규 없음" 명시 |
| (c) 공공기관 행사 | "공공기관 주최 행사" | Organization with org_type ∈ {행정복지센터·보건소·복지관·도서관·우체국·경찰서·소방서·주민자치회} 1건 이상 또는 "금일 없음" 명시 |

**한 카테고리라도 0건 + "없음" 명시도 없음 → WARNING.**

## 윈도우 노출 의무

shop-roster.json의 `active_shops` 목록과 보고서를 교차 비교한다.

| 가게 상태 | 보고서 노출 위치 | 누락 시 |
|----------|----------------|--------|
| `active` (윈도우 활성) | "신규 오픈 가게·팝업·프로모션" 본문 표 | **CRITICAL** — 30일 동안 매일 의무 노출 |
| `recent` (윈도우 종료 직후) | "최근 오픈 (참고)" 보조 섹션 | WARNING |
| `suspected_closed` | "확인 필요" 보조 섹션 | INFO (제외 가능) |
| `archived` | 보고서 노출 안 함 | — |
| `manual_seeds.status: pending` | "조사 진행 중" 보조 섹션 | WARNING — 사용자가 자신의 제보 처리 현황을 알아야 함 |
| `manual_seeds.status: gave_up` | "찾지 못함 — 사용자 확인 요청" 섹션 | WARNING |

## 누락 검출 알고리즘

### Step 1 — 보고서에서 가게 언급 추출

보고서 markdown을 파싱하여 다음 패턴으로 가게명 추출:

- "신규 오픈 가게·팝업·프로모션" 섹션 내 표의 가게 이름 컬럼
- 본문 내 `**가게명**` 굵게 표시
- "기존 Shop 현황" 표

추출된 가게명 집합을 `mentioned_shops` 변수에 저장.

### Step 2 — roster와 교차 비교

```python
# 의사코드
active_in_roster = {shop["name"] for shop in roster["active_shops"]}
mentioned = extract_shop_mentions(report_markdown)

missing_active = active_in_roster - mentioned  # 누락
unexpected = mentioned - (active_in_roster | recent | archived_names)  # roster에 없는데 보고서에 있음

for shop_name in missing_active:
    record_finding(severity="CRITICAL", category="missing_active_window",
                   shop_name=shop_name)
```

### Step 3 — manual_seeds 가시성 검사

```python
for seed in roster["manual_seeds"]:
    if seed["status"] in ("pending", "gave_up"):
        if not report_has_section("사용자 제보 처리 현황"):
            record_finding(severity="WARNING", category="manual_seed_invisibility")
            break
```

### Step 4 — 3종 의무 커버 검사

```python
for category, sec_keywords in CATEGORIES.items():
    section_text = extract_section(report_markdown, sec_keywords)
    if not section_text:
        record_finding(severity="WARNING", category=f"missing_section_{category}")
        continue
    if has_no_items(section_text) and not has_explicit_empty_message(section_text):
        record_finding(severity="WARNING", category=f"empty_without_message_{category}")
```

### Step 5 — 모순 검사

```python
if report_is_empty_mode(report_markdown) and len(active_in_roster) > 0:
    record_finding(severity="CRITICAL", category="contradiction_empty_with_active",
                   detail="보고서는 '특이사항 없음' 모드인데 active 가게가 존재")
```

## Patch 템플릿

`audit_mode: patch`일 때, 누락된 가게를 보고서에 자동 추가한다.

### 누락된 active 가게 추가

"신규 오픈 가게·팝업·프로모션" 섹션이 비어있거나 "발견 없음" 메시지를 포함하면 다음 표로 교체. 섹션이 있고 표가 있으면 표에 행 추가:

```markdown
| 가게 | 유형 | 동 | 거리 | 오픈일 | 윈도우 만료 | 프로모션 | 출처 |
|------|------|----|------|--------|-------------|---------|------|
| **엉클부대찌개 관평동점** | 식당 | 관평동 | ~2.5km (ring-bike) | 2026-05-15 (추정) | 2026-06-14 | 오픈 기념 10% 할인 (~5/31) | [Naver](URL), [Instagram](URL) |
```

### 누락된 manual_seeds 가시화

"신규 오픈 가게·팝업·프로모션" 섹션 하단에 추가:

```markdown
### 사용자 제보 처리 현황

| 제보 가게 | 등록일 | 상태 | 결과 |
|----------|-------|------|------|
| {seed_name} | {added_on} | {status} | {resolved_to or "다음 사이클 재시도" or "3회 시도 후 미발견"} |
```

### 검증 로그 (patch 사실 명시)

보고서 최하단에 추가 — 투명성을 위해 patch가 일어났음을 사용자가 알 수 있어야 함:

```markdown
---

## 검증 로그 (shop-coverage-auditor)

- **검증 시각:** 2026-05-24T22:35:00+09:00
- **CRITICAL:** 1건 (관평동 엉클부대찌개 누락 → patch로 보강)
- **WARNING:** 1건 (manual_seeds 가시화 누락 → patch로 보강)
- **자동 patch 적용:** 2건
- **상세:** `sources/2026-05-24/coverage-audit.json`
```

## coverage-audit.json 스키마

```json
{
  "audit_date": "2026-05-24",
  "audited_at": "ISO8601",
  "report_path": "reports/2026/05/2026-05-24.md",
  "roster_snapshot_date": "2026-05-24",
  "summary": {
    "critical": 1,
    "warning": 1,
    "info": 0,
    "patches_applied": 2,
    "active_shops_in_roster": 3,
    "active_shops_mentioned": 3,
    "missing_active_shops": 0,
    "category_coverage": {
      "event": true,
      "shop": true,
      "public_institution": true
    }
  },
  "findings": [
    {
      "severity": "CRITICAL",
      "category": "missing_active_window",
      "shop_id": "shop-001",
      "shop_name": "엉클부대찌개 관평동점",
      "detail": "active 가게 (윈도우 expires 2026-06-14)이 보고서에 0회 언급",
      "patched": true,
      "patch_location": "신규 오픈 가게·팝업·프로모션 섹션 표 추가"
    }
  ],
  "post_patch_recheck": {
    "performed": true,
    "remaining_critical": 0,
    "remaining_warning": 0
  }
}
```

## 심각도 등급

| 등급 | 의미 | 처리 |
|------|------|------|
| CRITICAL | 30일 윈도우 의무 위반 — 사용자가 약속받은 노출이 누락됨 | patch 모드에서 강제 보강. exit 1 |
| WARNING | 권장 노출 누락 (recent, manual_seeds 가시화, 3종 커버) | patch 모드에서 보강 시도. exit 0 |
| INFO | 참고 사항 (suspected_closed 미노출 등) | patch 안 함. 로그만 |

**exit code 정책:**
- 0: 모든 검증 통과 또는 WARNING만 존재
- 1: CRITICAL 존재 (patch 적용 여부와 무관) — GHA 워크플로우가 사용자에게 알림
