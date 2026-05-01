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

## 2026-04-29 추론 결과

### 추론 #1: age_group_overlap (나무랑 놀꾸야 → 유아·초등저학년 타겟)
- **입력:** (ent-evt-020 featuresActivity ent-act-004), (ent-act-004 sub_programs "16종 목공체험")
- **추론:** (ent-act-004 targetsAgeGroup age-toddler), (ent-act-004 targetsAgeGroup age-elem-low)
- **신뢰도:** 0.85 / 0.90
- **상태:** 확정
- **비고:** 나무 도마·자동차·독서대 등은 유아~초등저학년에 적합. 초등저학년이 가장 높은 적합도.

### 추론 #2: age_group_overlap (과학체험 6종 → 초등저학년·고학년)
- **입력:** (ent-evt-020 featuresActivity ent-act-006), (ent-act-006 sub_programs "진공실험·배터리시계·망원경·3D펜·모루인형")
- **추론:** (ent-act-006 targetsAgeGroup age-elem-low), (ent-act-006 targetsAgeGroup age-elem-high)
- **신뢰도:** 0.95 / 0.90
- **상태:** 확정
- **비고:** 밀가루 배터리 시계·진공 실험 = 초등 과학 교과와 연계. 3D펜은 초등고학년에도 적합.

### 추론 #3: ticket_scarcity_alert (티니핑 참여권 조기 소진 예상)
- **입력:** (ent-act-001 ticketDistribution "선착순 50명×2회"), (ent-act-001 kid_friendly_score 0.95), (ent-evt-021 visitor_estimate "대규모 축제")
- **추론:** (ent-act-001 scarcityAlert true)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 인기 유아 IP(티니핑) + 선착순 50명 = 참여권 조기 소진 높음. 1회차 12시 배부 → 11시 현장 도착 권장.

### 추론 #4: program_detail_confidence_boost (어린이 한마당 프로그램 확정)
- **입력:** (ent-evt-020 featuresActivity ent-act-004~007), (4개 카테고리: 목공·공연·과학·안전)
- **추론:** (ent-evt-020 kidFriendlyScore 확정 0.95)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 프로그램 구성이 4개 카테고리로 구체화됨에 따라 기존 kid_friendly_score 0.95를 확정 유지. 안전 캠페인(지문등록·감염병) 포함으로 공공 신뢰도 가산.

### 추론 #5: temporal_sequence (D-3 → D-6 골든위크 카운트다운)
- **입력:** (ent-evt-021 D-3), (ent-evt-020 D-6), (ent-evt-021 end_date 5/4), (ent-evt-020 start_date 5/5)
- **추론:** 골든위크 5일 연속 가족 행사 루트 확정 — 5/2~4 온천축제 → 5/5 어린이 한마당
- **신뢰도:** 0.85
- **상태:** 확정

## 2026-04-30 추론 결과

### 추론 #1: same_venue_series (국립중앙과학관 5월 가정의 달 시리즈)
- **입력:** (ent-evt-024 hostsAt ent-venue-005), (ent-evt-025 hostsAt ent-venue-005), (ent-evt-026 hostsAt ent-venue-005), (ent-evt-027 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), (ent-evt-024~028 organizedBy ent-org-006)
- **추론:** (ent-evt-024 partOfSeries 과학관-가정의달), (ent-evt-025 partOfSeries 과학관-가정의달), (ent-evt-026 partOfSeries 과학관-가정의달), (ent-evt-027 partOfSeries 과학관-가정의달), (ent-evt-028 partOfSeries 과학관-가정의달)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 동일 장소(국립중앙과학관) + 동일 주최 + 5월 연속 배치 → 가정의 달 시리즈 확정. 매주 1~2건 행사가 5월 전체를 커버.

### 추론 #2: same_dong_combo (동심 로그인 → 어린이 한마당 연계)
- **입력:** (ent-evt-024 hostsAt ent-venue-005), (ent-evt-020 hostsAt ent-venue-005), (ent-venue-005 locatedIn dong-doryong), (ent-evt-024 end_date 5/3), (ent-evt-020 start_date 5/5)
- **추론:** (ent-evt-024 visitCombo ent-evt-020)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 5/1~3 동심 로그인과 5/5 어린이 한마당이 동일 장소에서 2일 간격으로 이어짐 — 과학관 연속 방문 패턴.

### 추론 #3: operator_kid_friendliness (과학관 운영 가산)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-024~028 hostsAt ent-venue-005)
- **추론:** (ent-evt-024 kidFriendlyBoost +0.2), (ent-evt-025 kidFriendlyBoost +0.2), (ent-evt-026 kidFriendlyBoost +0.2), (ent-evt-027 kidFriendlyBoost +0.2), (ent-evt-028 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정

### 추론 #4: temporal_sequence (골든위크 타임라인 확장 5/1~10)
- **입력:** (ent-evt-024 start_date 5/1), (ent-evt-021 start_date 5/2), (ent-evt-020 start_date 5/5), (ent-evt-025 start_date 5/9)
- **추론:** 골든위크 행사가 5/1부터 시작하여 5/10까지 이어지는 확장 타임라인 확인
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 이전 타임라인(5/2~5) → 확장 타임라인(5/1~10). 과학관 동심 로그인(5/1~3)이 온천축제(5/2~4)와 겹쳐 선택지 다양화.

### 추론 #5: public_institution_kid_event (과학관 = 공공기관 가산)
- **입력:** (ent-org-006 orgType 과학관), (ent-evt-024~028 organizedBy ent-org-006), 과학관 ∈ operator_kid_friendliness 대상
- **추론:** (ent-evt-024~028 publicTrustBoost +0.15)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 국립중앙과학관은 국립기관으로 공공 신뢰도 최고 수준. 5건 모두 publicTrustBoost 적용.

## 2026-05-01 추론 결과

### 추론 #1: 골든위크 타임라인 확정 (D-day 전환)
- **입력:** (ent-evt-024 start_date 2026-05-01), (ent-evt-021 start_date 2026-05-02), (ent-evt-020 start_date 2026-05-05), (ent-evt-025 start_date 2026-05-09)
- **추론:** 골든위크 타임라인이 실제 개막으로 확정됨: 5/1 동심 로그인 → 5/2~4 온천축제 → 5/5 어린이 한마당 → 5/9~10 알라딘
- **신뢰도:** 0.95 (어제 0.85에서 상향 — 개막 실현)
- **상태:** 확정
- **비고:** 전일 추론한 골든위크 확장 타임라인이 D-day 도래로 확정. 더 이상 "예측"이 아닌 "진행 중".

### 추론 #2: 가정의 달 공공기관 시즌 시작 (신규 추론)
- **규칙:** public_institution_kid_event (확장)
- **입력:** (ent-evt-024 start_date 2026-05-01 + organizedBy 국립중앙과학관), (ent-evt-022 start_date 2026-05-01 + organizedBy 유성소방서), (ent-evt-023 start_date 2026-05-01 + organizedBy 유성구통합도서관)
- **추론:** 3개 공공기관(과학관·소방서·도서관)이 동시에 5/1 시작 → "가정의 달 공공기관 시즌"으로 묶을 수 있음
- **신뢰도:** 0.80
- **상태:** 잠정
- **비고:** 우연의 일치(5월 1일이 가정의 달 시작이므로 당연)일 수 있으나, 3기관 동시 시작은 보고서에서 묶어 안내할 가치가 있음.

### 추론 #3: 동심 로그인 ↔ 어린이 한마당 방문 콤보 강화
- **규칙:** same_venue_series
- **입력:** (ent-evt-024 hostsAt ent-venue-005) AND (ent-evt-020 hostsAt ent-venue-005) AND (ent-evt-024 end_date 5/3) AND (ent-evt-020 start_date 5/5)
- **추론:** (ent-evt-024 visitCombo ent-evt-020) — 같은 장소, 2일 간격
- **신뢰도:** 0.85 (전일 0.80에서 상향 — 동심 로그인 개막 확인)
- **상태:** 확정
