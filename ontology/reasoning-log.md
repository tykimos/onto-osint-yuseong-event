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

### 추론 #8: operator_kid_friendliness (어린이회��� 가산)
- **입력:** (ent-org-010 operates ent-venue-011), (ent-evt-009 hostsAt ent-venue-011)
- **추론:** (ent-evt-009 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **��고:** 어린이 전용 시설 — 기본 친화도가 높음

## 2026-04-26 추론 결과

### 추론 #1: proximity (도룡동 아쿠아리움 ↔ 엑스포과학공원)
- **입력:** (ent-venue-012 locatedIn dong-doryong), (ent-venue-001 locatedIn dong-doryong)
- **추론:** (ent-venue-012 nearby ent-venue-001)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 아쿠아리움은 신세계 Art&Science B1(엑스포로 1)에 위치, 엑스포과학공원과 같은 엑스포 권역 내 도보 연계 가능

### 추��� #2: proximity (아쿠아리움 ↔ 국립어린이과학관)
- **입력:** (ent-venue-012 locatedIn dong-doryong), (ent-venue-004 locatedIn dong-doryong)
- **추론:** (ent-venue-012 nearby ent-venue-004)
- **��뢰도:** 0.85
- **상태:** 확정
- **비고:** 도룡동 엑스포 권역 내 근접 시설

### 추론 #3: same_dong_combo (아쿠아리움 + K-사이언스)
- **���력:** (ent-evt-011 hostsAt ent-venue-012), (ent-evt-004 hostsAt ent-venue-004), (ent-venue-012 locatedIn dong-doryong), (ent-venue-004 locatedIn dong-doryong)
- **추론:** (ent-evt-011 visitCombo ent-evt-004)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 아쿠아리움(예약 불필요, 상시 운영) + K-사이언스(사전신청) 당일 연계 ��능

### 추론 #4: same_dong_combo (아쿠아리움 + 천문대)
- **입력:** (ent-evt-011 hostsAt ent-venue-012), (ent-evt-006 hostsAt ent-venue-006), (ent-venue-012 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-011 visitCombo ent-evt-006)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 아쿠아리움(주간 ~19:00) → 천문대(야간 14:00~22:00) 시간대 자연 연계

### 추론 #5: operator_kid_friendliness (평생학습센터 원데이클래스)
- **입력:** (ent-org-013 operates ent-venue-014), (ent-org-013 orgType 평생학습관), (ent-evt-012 hostsAt ent-venue-014)
- **추론:** (ent-evt-012 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 평생학습관 운영 프로그램 → 공공기관 가산. 다만 전체 프로그램 중 어린이 대상 비율은 확인 필요

### 추론 #6: public_institution_kid_event (청소년수련관)
- **입력:** (ent-org-014 orgType 복지관), (ent-evt-013 organizedBy ent-org-014)
- **��론:** (ent-evt-013 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **��태:** 확정
- **비고:** 공공기관 주최 청소년 프로그램 → 신뢰도 가산. 초등고학년 이상 대상

### 추론 #7: proximity (구암동 평생학습센터 ↔ 청소년수련관)
- **입력:** (ent-venue-013 locatedIn dong-guam), (ent-venue-015 locatedIn dong-guam)
- **추론:** (ent-venue-013 nearby ent-venue-015)
- **신뢰도:** 0.75
- **���태:** 확정
- **비고:** 둘 다 구암동 소재 공공시설, 묶음 방문 가능

### 추론 #8: same_dong_combo (사이언스데이 + 아쿠아리움)
- **입력:** (ent-evt-014 hostsAt ent-venue-005), (ent-evt-011 hostsAt ent-venue-012), (ent-venue-005 locatedIn dong-doryong), (ent-venue-012 locatedIn dong-doryong)
- **추론:** (ent-evt-014 visitCombo ent-evt-011)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 사이언스데이(국립중앙과학관) + 아쿠아리움(신세계 B1) = 도룡동 당일 과학+해양 연계 체험

### 추론 #9: operator_kid_friendliness (탐이꿈이 실험실)
- **입력:** (ent-org-005 operates ent-venue-004), (ent-org-005 orgType 과학관), (ent-evt-015 hostsAt ent-venue-004)
- **추론:** (ent-evt-015 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정

### 추론 #10: operator_kid_friendliness (아가맘 행복교실)
- **입력:** (ent-org-004 orgType 도서관), (ent-evt-017 organizedBy ent-org-004)
- **추론:** (ent-evt-017 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 도서관 운영 영유아 프로그램 — 기본 친화도 높음

### 추론 #11: public_institution_kid_event (유성소방서 이동안전체험)
- **입력:** (ent-org-015 orgType 소방서), (ent-evt-018 organizedBy ent-org-015), (ent-evt-018 targetsAgeGroup 유아|초등)
- **추론:** (ent-evt-018 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 소방서 주최 어린이 안전교육 — 공공 신뢰도 가산

### 추론 #12: public_institution_kid_event (119시민체험센터)
- **입력:** (ent-org-015 orgType 소방서), (ent-evt-019 organizedBy ent-org-015)
- **추론:** (ent-evt-019 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정

### 추론 #13: proximity (아가랑도서관 ↔ 평생학습센터 전민센터)
- **입력:** (ent-venue-016 locatedIn dong-jeonmin), (ent-venue-014 locatedIn dong-jeonmin)
- **추론:** (ent-venue-016 nearby ent-venue-014)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 전민동 내 도서관 + 평생학습센터 묶음 방문 가능. 용성로20 도보권(ring-stroll) 내 공공 프로그램 클러스터 형성

## 2026-04-27 추론 결과

### 추론 #1: public_institution_kid_event (유성 어린이 한마당)
- **입력:** (ent-org-001 orgType 구청), (ent-evt-020 organizedBy ent-org-001), (ent-evt-020 targetsAgeGroup 유아|초등저학년|초등고학년|전연령가족)
- **추론:** (ent-evt-020 publicTrustBoost +0.15)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 유성구청 주최 어린이날 행사 — 최고 수준 공공 신뢰도. 무료·사전신청 불필요.

### 추론 #2: same_dong_combo (어린이 한마당 + 사이언스데이)
- **입력:** (ent-evt-020 hostsAt ent-venue-005), (ent-evt-014 hostsAt ent-venue-005)
- **추론:** (ent-evt-020 visitCombo ent-evt-014)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 같은 국립중앙과학관에서 열리는 행사. 사이언스데이(4/17~19, 종료)와 어린이 한마당(5/5)은 시기가 다르지만, 동일 venue에서 유성구가 반복 개최하는 시리즈로 볼 수 있음.

### 추론 #3: same_dong_combo (어린이 한마당 + 아쿠아리움)
- **입력:** (ent-evt-020 hostsAt ent-venue-005), (ent-evt-011 hostsAt ent-venue-012), (ent-venue-005 locatedIn dong-doryong), (ent-venue-012 locatedIn dong-doryong)
- **추론:** (ent-evt-020 visitCombo ent-evt-011)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 어린이날(5/5) 어린이 한마당(국립중앙과학관) + 아쿠아리움(신세계 B1) 도룡동 당일 연계

### 추론 #4: public_institution_kid_event (가정의 달 소방안전체험)
- **입력:** (ent-org-015 orgType 소방서), (ent-evt-022 organizedBy ent-org-015)
- **추론:** (ent-evt-022 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 소방서 주최 가정의 달 확대 운영 — 기존 이동안전체험(ent-evt-018)의 후속

### 추론 #5: temporal_sequence (유성온천문화축제 → 어린이 한마당)
- **입력:** (ent-evt-021 start_date 2026-05-02), (ent-evt-021 end_date 2026-05-04), (ent-evt-020 start_date 2026-05-05)
- **추론:** (ent-evt-021 visitCombo ent-evt-020)
- **신뢰도:** 0.75
- **상태:** 확정
- **비고:** 유성온천문화축제(5/2~4) 직후 어린이 한마당(5/5) = 5일 연속 가족 행사. 다만 장소가 봉명동 → 도룡동으로 이동이 필요하므로 신뢰도 0.75.

### 추론 #6: operator_kid_friendliness (어린이 한마당)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-020 hostsAt ent-venue-005)
- **추론:** (ent-evt-020 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 국립중앙과학관이 운영하는 장소에서 개최 → 어린이 친화도 가산

## 2026-04-28 추론 결과

### 추론 #1: age_group_overlap (캐치! 티니핑 → 유아 타겟)
- **입력:** (ent-evt-021 featuresActivity ent-act-001), (ent-act-001 target_age 유아·초등저학년)
- **추론:** (ent-act-001 targetsAgeGroup age-toddler)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 캐치! 티니핑은 유아·초등저학년 핵심 IP. 축제 전체의 어린이 집객력을 크게 높이는 프로그램.

### 추론 #2: proximity (너티차일드 ↔ 아쿠아리움)
- **입력:** (ent-shop-005 shopLocatedIn dong-doryong), (ent-venue-012 locatedIn dong-doryong)
- **추론:** (ent-shop-005 nearby ent-venue-012)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 너티차일드(엑스포로151번길)와 아쿠아리움(엑스포로1, 신세계 B1) 모두 도룡동 엑스포 권역. 도보 15분 이내 추정. 어린이날 실내 연계 루트로 활용 가능.

### 추론 #3: proximity (너티차일드 ↔ 국립중앙과학관)
- **입력:** (ent-shop-005 shopLocatedIn dong-doryong), (ent-venue-005 locatedIn dong-doryong)
- **추론:** (ent-shop-005 nearby ent-venue-005)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 어린이 한마당(5/5, 국립중앙과학관) 후 너티차일드에서 실내 놀이 가능. 우천 시 대체 루트.

### 추론 #4: kid_program_boost (유성온천문화축제 어린이 친화도 상향)
- **입력:** (ent-evt-021 featuresActivity ent-act-001), (ent-act-001 kid_friendly_score 0.95), (ent-evt-021 기존 kid_friendly_score 0.7)
- **추론:** (ent-evt-021 kidFriendlyBoost +0.1)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 캐치! 티니핑(유아 IP) + 물총 스플래쉬(초등) 프로그램 확정으로 축제 전체의 어린이 친화도를 0.7→0.8으로 상향 조정할 근거 확보. DJ파티·7080 등 성인 프로그램도 혼재하여 0.8이 적정.
