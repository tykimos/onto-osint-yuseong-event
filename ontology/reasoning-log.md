# 온톨로지 추론 로그

이 파일은 온톨로지 추론 엔진이 생성한 추론 결과를 기록한다.
각 엔트리는 추론 규칙, 입력 트리플, 추론된 트리플, 신뢰도를 포함한다.

---

## 2026-04-25 추론 결과

### 추론 #1: same_dong_combo
- **입력:** (ent-evt-001 hostsAt ent-venue-001), (ent-evt-006 hostsAt ent-venue-006), (ent-venue-001 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-001 visitCombo ent-evt-006)
- **신뢰도:** 0.85
- **상태:** 확정
- **의미:** 대전사이언스페스티벌과 시민천문대 관측 프로그램은 도룡동에서 같은 날 이용 가능 — 함께 방문 추천

### 추론 #2: same_dong_combo
- **입력:** (ent-evt-004 hostsAt ent-venue-004), (ent-evt-006 hostsAt ent-venue-006), (ent-venue-004 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-004 visitCombo ent-evt-006)
- **신뢰도:** 0.85
- **상태:** 확정
- **의미:** K-사이언스 교육 프로그램과 천문대 야간 관측을 도룡동 내에서 연이어 방문 가능

### 추론 #3: operator_kid_friendliness
- **입력:** (ent-org-005 operates ent-venue-004), (ent-org-005 orgType 과학관), (ent-evt-004 hostsAt ent-venue-004)
- **추론:** (ent-evt-004 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **의미:** 국립어린이과학관이 운영하는 K-사이언스 프로그램은 어린이 친화도 가산점 적용

### 추론 #4: operator_kid_friendliness
- **입력:** (ent-org-004 operates ent-venue-003), (ent-org-004 orgType 도서관), (ent-evt-003 hostsAt ent-venue-003)
- **추론:** (ent-evt-003 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **의미:** 유성구통합도서관이 운영하는 북스타트 책놀이는 어린이 친화도 가산점 적용

### 추론 #5: indoor_rainy_fallback
- **입력:** (ent-evt-001 indoor_outdoor 야외+실내), (ent-evt-006 indoor_outdoor 실내+야외), (ent-venue-001 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-006 rainyFallbackFor ent-evt-001)
- **신뢰도:** 0.75
- **상태:** 확정
- **의미:** 야외 과학축제 우천 시, 같은 동의 천문대 실내 프로그램으로 대체 가능

### 추론 #6: proximity (도룡동 과학벨트)
- **입력:** (ent-venue-001 locatedIn dong-doryong), (ent-venue-004 locatedIn dong-doryong), (ent-venue-005 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-venue-001 nearby ent-venue-004), (ent-venue-001 nearby ent-venue-006), (ent-venue-004 nearby ent-venue-005)
- **신뢰도:** 0.90~0.95
- **상태:** 확정
- **의미:** 도룡동 과학벨트 — 엑스포공원·어린이과학관·중앙과학관·천문대가 밀집, 도보 연계 가능

### 온톨로지 변경 요약 (2026-04-25)
- 스키마: seed 클래스/관계로 초기화 (변경 없음)
- 인스턴스: 26개 신규 엔티티 추가 (Event 8, Venue 10, Organization 8)
- 트리플: 41개 명시적 + 8개 추론 = 총 49개
