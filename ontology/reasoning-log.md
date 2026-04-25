# 온톨로지 추론 로그

이 파일은 온톨로지 추론 엔진이 생성한 추론 결과를 기록한다.
각 엔트리는 추론 규칙, 입력 트리플, 추론된 트리플, 신뢰도를 포함한다.

## 2026-04-25 추론 결과

### 추론 #1: same_dong_combo (도룡동 방문 조합)
- **입력:** (ent-evt-001 hostsAt ent-venue-001), (ent-evt-006 hostsAt ent-venue-006), (ent-venue-001 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-001 visitCombo ent-evt-006)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 사이언스페스티벌(종료) + 천문대 관측 = 도룡동 당일 연계 가능

### 추론 #2: same_dong_combo (도룡동 오후-야간 연계)
- **입력:** (ent-evt-004 hostsAt ent-venue-004), (ent-evt-006 hostsAt ent-venue-006), (ent-venue-004 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-004 visitCombo ent-evt-006)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** K-사이언스(주간) → 천문대(야간) 시간대 자연 연계

### 추론 #3: operator_kid_friendliness (K-사이언스 가산)
- **입력:** (ent-org-005 operates ent-venue-004), (ent-org-005 orgType 과학관), (ent-evt-004 hostsAt ent-venue-004)
- **추론:** (ent-evt-004 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정

### 추론 #4: operator_kid_friendliness (북스타트 가산)
- **입력:** (ent-org-004 operates ent-venue-003), (ent-org-004 orgType 도서관), (ent-evt-003 hostsAt ent-venue-003)
- **추론:** (ent-evt-003 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정

### 추론 #5: indoor_rainy_fallback (천문대 = 페스티벌 우천 대체)
- **입력:** (ent-evt-001 indoor_outdoor 야외+실내), (ent-evt-006 indoor_outdoor 실내+야외), (ent-venue-001 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-006 rainyFallbackFor ent-evt-001)
- **신뢰도:** 0.75
- **상태:** 확정

### 추론 #6: proximity (도룡동 과학벨트)
- **입력:** (ent-venue-001 locatedIn dong-doryong), (ent-venue-004 locatedIn dong-doryong)
- **추론:** (ent-venue-001 nearby ent-venue-004), (ent-venue-004 nearby ent-venue-005)
- **신뢰도:** 0.90 / 0.95
- **상태:** 확정
- **비고:** 엑스포공원 → 어린이과학관 → 중앙과학관 도보 연계 가능

### 추론 #7: same_dong_combo (노은동 어린이회관 + 도서관)
- **입력:** (ent-evt-009 hostsAt ent-venue-011), (ent-evt-007 관련 ent-venue-008), (ent-venue-011 locatedIn dong-noeun), (ent-venue-008 locatedIn dong-noeun)
- **추론:** (ent-evt-009 visitCombo ent-evt-007)
- **신뢰도:** 0.70
- **상태:** 잠정 (신뢰도 < 0.7 경계)
- **비고:** 노은동 어린이회관 + 노은도서관 = 묶음 방문 가능. 단, 도서관 프로그램 일정 확인 필요

### 추론 #8: operator_kid_friendliness (어린이회관 가산)
- **입력:** (ent-org-010 operates ent-venue-011), (ent-evt-009 hostsAt ent-venue-011)
- **추론:** (ent-evt-009 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 어린이 전용 시설 — 기본 친화도가 높음
