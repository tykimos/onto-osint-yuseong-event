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

## 2026-05-02 추론 결과

### 추론 #1: 온천축제 ↔ 동심 로그인 방문콤보 (동시 진행)
- **규칙:** same_dong_combo (확장: 동일 일자 동시 진행)
- **입력:** (ent-evt-021 start_date 2026-05-02) AND (ent-evt-024 진행중 5/1~3) AND (5/2~3 양일 겹침)
- **추론:** (ent-evt-021 visitCombo ent-evt-024) — 오전 온천축제 → 오후 과학관 (또는 반���) 루트 방문 가능
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 봉명동(온천축제)↔도룡동(과학관) 차량 15분. 오전 티니핑(11시 줄서기) 후 오후 과학관 루트 추천.

### 추론 #2: 관평도서관 그림책 프로그램 — kid_friendly 가산
- **규칙:** operator_kid_friendliness
- **입력:** (ent-org-004 orgType 도서관) AND (ent-evt-029 hostsAt ent-venue-007) AND (ent-org-004 operates ent-venue-007)
- **추론:** (ent-evt-029 kidFriendlyBoost +0.2) → 최종 kid_friendly_score = min(0.85+0.2, 1.0) = 1.0
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 도서관 운영 어린이 전용 프로그램은 자동으로 최고 수준 어린이 친화도.

### 추론 #3: 관평도서관 그림책 ↔ 북스타트 시리즈 가능성
- **규칙:** same_venue_series (확장: 같은 도서관 시스템)
- **입력:** (ent-evt-029 organizedBy ent-org-004) AND (ent-evt-003 organizedBy ent-org-004) AND (target 영유아~초등저학년 중복)
- **추론:** (ent-evt-029 partOfSeries ent-evt-003) — 유성구통합도서관 어린이 독서 프로그램 시리즈
- **신뢰도:** 0.60 (잠정 — 직접적 시리즈 관계 미확인. 동일 운영 주체 + 유사 대상 + 도서 주제)
- **상태:** 잠정
- **비고:** 북스타트는 영유아 전용(36개월~), 그림책 프로그램은 유아~초등 포함으로 대상 범위 차이 있음. "도서관 독서 프로그램 계열"로 느슨히 연결.

### 추론 #4: 골든위크 타임라인 Day 2 업데이트
- **규칙:** (상태 추적)
- **입력:** 전일 추론 "골든위크 타임라인 확정"
- **추론:** Day 2 진행 확인. 5/1 동심 로그인 개막 → **오늘 5/2 온천축제 개막** → 5/3 동심 로그인 마지막 + 온천축제 2일째 → 5/4 온천축제 마지막 → 5/5 어린이 한마당
- **신뢰도:** 0.95 (유지)
- **상태:** 확정
- **비고:** 타임라인 스케줄대로 진행 중. 2/5 완료.

## 2026-05-03 추론 결과

### 추론 #1: operator_kid_friendliness (대전시민천문대 별축제)
- **입력:** (ent-org-007 orgType 천문대), (ent-evt-030 organizedBy ent-org-007)
- **추론:** (ent-evt-030 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 천문대 운영 과학체험 축제 — 과학체험부스 수십 개 + 태양관측 + 별음악회. 어린이·가족 대상 프로그램 비중 높음. 단, 야간 관측은 영유아 부적합.

### 추론 #2: same_dong_combo (별축제 + 어린이 한마당)
- **입력:** (ent-evt-030 hostsAt ent-venue-006), (ent-evt-020 hostsAt ent-venue-005), (ent-venue-006 locatedIn dong-doryong), (ent-venue-005 locatedIn dong-doryong)
- **추론:** (ent-evt-030 visitCombo ent-evt-020)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 별축제(5/4~5) 마지막 날과 어린이 한마당(5/5) 동일 날짜 + 동일 동(도룡동). 오전 과학관→오후 천문대 당일 코스 가능.

### 추론 #3: same_dong_combo (별축제 + 상시 관측)
- **입력:** (ent-evt-030 hostsAt ent-venue-006), (ent-evt-006 hostsAt ent-venue-006)
- **추론:** (ent-evt-030 visitCombo ent-evt-006)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 동일 장소(대전시민천문대). 별축제 기간에는 상시 프로그램이 별축제 프로그램으로 통합 운영될 가능성 높음.

### 추론 #4: temporal_sequence (유성온천문화축제 → 별축제 → 어린이 한마당)
- **입력:** (ent-evt-021 end_date 2026-05-04), (ent-evt-030 start_date 2026-05-04), (ent-evt-020 start_date 2026-05-05)
- **추론:** 골든위크 5일 연속 가족 행사 타임라인 확정
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 5/2~3 온천축제 + 5/4 별축제(+온천축제 마지막 날) + 5/5 어린이 한마당(+별축제 마지막 날). 5일 연속 매일 가족 행사가 존재하는 황금 연휴.

### 추론 #5: 유성온천문화축제 Day 2 프로그램 확정
- **입력:** (ent-evt-021 featuresActivity ent-act-008), (ent-act-008 day "5/3 Day2 메인")
- **추론:** Day 2의 차별화 프로그램 = 거리퍼레이드(30주년 특별). Day 1의 개막식·드론라이트·불꽃쇼에 대응하는 Day 2 고유 콘텐츠.
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 매일 공통(물총 스플래쉬 15시, 티니핑, 족욕열차, 온천수수영장) + 일자별 고유(Day1=개막식+드론, Day2=거리퍼레이드, Day3=폐막)

## 2026-05-04 추론 결과

### 추론 #1: temporal_overlap (별축제 + 온천축제 동시 진행)
- **규칙:** temporal_overlap (same_dong_combo 확장)
- **입력:** (ent-evt-030 start_date 2026-05-04), (ent-evt-021 end_date 2026-05-04), (ent-venue-006 locatedIn dong-doryong), (ent-venue-018 locatedIn dong-bongmyeong)
- **추론:** (ent-evt-030 visitCombo ent-evt-021) — 별축제(도룡동) + 온천축제 마지막(봉명동) 동시 진행
- **신뢰도:** 0.70
- **상태:** 확정
- **비고:** 다른 동(도룡동↔봉명동, 차량 15분)이므로 신뢰도 0.70. 오전 온천축제 마무리 → 오후 별축제 이동 가능하나 교통 혼잡 예상(양쪽 모두 주차 제한).

### 추론 #2: same_dong_combo (별축제 Day 2 + 어린이 한마당 신뢰도 상향)
- **규칙:** same_dong_combo
- **입력:** (ent-evt-030 end_date 2026-05-05), (ent-evt-020 start_date 2026-05-05), (ent-venue-006 locatedIn dong-doryong), (ent-venue-005 locatedIn dong-doryong)
- **추론:** (ent-evt-030 visitCombo ent-evt-020) — 신뢰도 0.80 → 0.85 상향
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** D-1 확정. 내일(5/5) 오전 어린이 한마당(국립중앙과학관) → 오후 별축제 Day 2(대전시민천문대) = 도룡동 과학벨트 풀코스 확정.

### 추론 #3: 유성온천문화축제 Day 3 프로그램 확정
- **규칙:** (프로그램 상세)
- **입력:** (ent-evt-021 featuresActivity ent-act-011), (ent-evt-021 featuresActivity ent-act-012)
- **추론:** Day 3 고유 프로그램 = 뮤직&댄스 경연 결선 + 폐막공연(VR+팝페라). 이로써 3일간 일자별 프로그램 전체 확정: Day1=개막식+드론불꽃쇼, Day2=거리퍼레이드, Day3=경연결선+폐막공연.
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 폐막공연의 어린이 친화도는 0.5 (VR퍼포먼스+팝페라는 성인 대상 비중 높음). 가족 방문은 낮 시간(티니핑·물총·수영장) 위주 추천.

### 추론 #4: 골든위크 타임라인 Day 4 — 교차점
- **규칙:** temporal_sequence
- **입력:** 전일 타임라인 + 금일 D-day 전환
- **추론:** Day 4(5/4) = 온천축제 폐막 + 별축제 개막. 두 축제의 교차점. 타임라인: 5/2 온천축제 개막 → 5/3 Day2 → **5/4 온천축제 폐막 + 별축제 개막** → 5/5 별축제 Day2 + 어린이 한마당 → 5/9~10 알라딘
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 5일 연속 가족 행사 중 4일째. 내일(5/5)이 클라이맥스(어린이날 + 별축제 + 한마당 3중 이벤트).

## 2026-05-05 추론 결과

### 추론 #1: same_dong_combo (어린이 한마당 + 별축제 D-day 확정)
- **규칙:** same_dong_combo
- **입력:** (ent-evt-020 hostsAt ent-venue-005), (ent-evt-030 hostsAt ent-venue-006), (ent-venue-005 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong), (둘 다 오늘 D-day)
- **추론:** (ent-evt-020 visitCombo ent-evt-030) — 신뢰도 0.85 → 0.90 상향
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** D-day 동시 진행 확정. 어린이 한마당(오전, 국립중앙과학관) → 별축제(오후, 대전시민천문대) = 도룡동 과학벨트 풀코스. 5분 거리 연계.

### 추론 #2: proximity (대전월드컵경기장 ↔ 어린이회관)
- **규칙:** proximity
- **입력:** (ent-venue-020 address "대전 유성구 월드컵대로 32"), (ent-venue-011 address "대전 유성구 월드컵대로 32 동관 1층")
- **추론:** (ent-venue-020 nearby ent-venue-011)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 동일 건물 단지 — 대전월드컵경기장 본체와 어린이회관(동관 1층)은 같은 단지 내 인접 시설. KIDS DAY 전후 어린이회관 방문 가능.

### 추론 #3: same_date_different_dong (KIDS DAY + 어린이 한마당 방문콤보)
- **규칙:** temporal_overlap + different_dong
- **입력:** (ent-evt-031 date 2026-05-05), (ent-evt-020 date 2026-05-05), (ent-venue-020 locatedIn dong-noeun), (ent-venue-005 locatedIn dong-doryong)
- **추론:** (ent-evt-031 visitCombo ent-evt-020)
- **신뢰도:** 0.65 (잠정)
- **상태:** 잠정 (< 0.7)
- **비고:** 같은 날이지만 다른 동(노은동↔도룡동, 차량 15~20분). 축구 경기 시간에 따라 오전 한마당 → 오후 경기, 또는 경기 후 별축제 야간 관측 등의 조합이 가능하나, 이동 시간·주차 부담으로 잠정.

### 추론 #4: 골든위크 타임라인 Day 5 — 클라이맥스 & 완결
- **규칙:** temporal_sequence
- **입력:** 전일 타임라인 + 금일 D-day 3중 이벤트
- **추론:** Day 5(5/5 어린이날) = 황금연휴 클라이맥스. 어린이 한마당(도룡동) + 별축제 마지막(도룡동) + KIDS DAY(노은동) = 3중 이벤트. 이로써 5/2~5/5 5일 연속 가족 행사 타임라인 완결. 다음 행사: 5/9~10 가족뮤지컬 알라딘.
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 5일 연속 가족 행사의 마지막이자 최대 규모일. 유성구 전역(도룡동+노은동)에서 동시다발 어린이날 이벤트.

### 추론 #5: 유성온천문화축제 완전 종료 확인
- **규칙:** (상태 추적)
- **입력:** (ent-evt-021 end_date 2026-05-04), (금일 2026-05-05)
- **추론:** 유성온천문화축제 완전 종료. 3일간(5/2~4) 운영 후 정상 폐막. 추적 항목에서 "종료"로 전환.
- **신뢰도:** 0.99
- **상태:** 확정
- **비고:** 어제 폐막공연(VR+팝페라) + 뮤직댄스 경연 결선으로 마무리. 총 100여 프로그램 운영.

## 2026-05-06 추론 결과

### 추론 #1: same_venue_series (가정의달 시리즈 연계)
- **입력:** (ent-evt-024 hostsAt ent-venue-005), (ent-evt-025 hostsAt ent-venue-005), (ent-evt-024 organizedBy ent-org-006), (ent-evt-025 organizedBy ent-org-006)
- **추론:** (ent-evt-025 partOfSeries ent-evt-024)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 국립중앙과학관 가정의달 시리즈 — 동심로그인(5/1~3) → 어린이한마당(5/5) → 가족뮤지컬 알라딘(5/9~10). 동일 venue + 동일 주최(국립중앙과학관) + 가정의달 테마.

### 추론 #2: operator_kid_friendliness (알라딘 어린이 친화도 가산)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-025 hostsAt ent-venue-005)
- **추론:** (ent-evt-025 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 과학관이 주최하는 가족 대상 뮤지컬. 기본 kid_friendly_score 0.95에 +0.2 가산.

### 추론 #3: 대전 오월드 어린이 친화도 추정
- **입력:** (ent-venue-021 venue_type 테마파크·동물원), (테마파크·동물원은 어린이 핵심 가족 시설)
- **추론:** (ent-venue-021 kidFriendlyScore 0.9)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 재개장 미확정이나 시설 유형 자체의 어린이 친화도는 높음. 재개장 시 주요 추천 대상.

### 추론 #4: 황금연휴 행사 종료 일괄 전환
- **입력:** (ent-evt-020 end_date 2026-05-05), (ent-evt-030 end_date 2026-05-05), (ent-evt-031 end_date 2026-05-05), (금일 2026-05-06)
- **추론:** ent-evt-020(어린이한마당), ent-evt-030(별축제), ent-evt-031(KIDS DAY) 모두 종료 처리.
- **신뢰도:** 0.99
- **상태:** 확정
- **비고:** 5/2~5/5 황금연휴 5일 연속 대형 행사 완전 종료. 유성구 이벤트 밀도 정상 수준으로 복귀.

## 2026-05-07 추론 결과

### 추론 #1: public_institution_kid_event (유성이의 튼튼스쿨)
- **입력:** (ent-org-020 orgType 보건소), (ent-evt-032 organizedBy ent-org-020), (ent-evt-032 targetsAgeGroup 유아)
- **추론:** (ent-evt-032 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 보건소 주최 어린이 건강체험 프로그램. 공공기관 어린이 대상 행사 가산점 적용. 다만 상반기 모집 마감 상태로 당장 참여 불가.

### 추론 #2: same_venue_series (히어로 박람회 → 알라딘 시리즈)
- **입력:** (ent-evt-026 hostsAt ent-venue-005), (ent-evt-025 hostsAt ent-venue-005), (ent-evt-026 organizedBy ent-org-006), (ent-evt-025 organizedBy ent-org-006)
- **추론:** (ent-evt-026 partOfSeries ent-evt-025) — 가정의달 시리즈 연계
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 동일 venue(국립중앙과학관) + 동일 주최 + 가정의달 테마. 알라딘(5/9~10) → 히어로(5/16~17) 순서.

### 추론 #3: 대전 오월드 재개장 불가 확정 (불확실성 해소)
- **입력:** (ent-venue-021 이전 상태 "재개장 검토 중"), 복수 매체 보도(뉴스1·인사이트·금강일보·대전MBC·문화일보), 금강유역환경청 사용 중지 명령
- **추론:** (ent-venue-021 status "5월 말까지 재개장 불가 확정"), (ent-venue-021 reopeningBlocked 금강유역환경청-사용중지명령)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 어제(5/6) 대전일보 '5월 재개장 검토'와 머니투데이 '5월 재개장 어려울 듯'이 상충했으나, 오늘 5개 매체가 '5월 말까지 재개장 불가' + '입점업소 공식 통보'를 보도하며 불확실성 해소. 금강유역환경청의 동물원 시설(주랜드) 사용 중지 명령이 법적 장애물. 재개장 판단 시점은 5월 하순으로 예정.

### 추론 #4: 히어로 박람회 사전 캠페인 — 참여 유인
- **입력:** (ent-evt-026 preCampaign "잠든 영웅을 깨워라 아이템 수집"), (아이템 기증 → 히어로 페스타 특별 초청권)
- **추론:** 사전 캠페인은 5/16~17 행사의 사전 참여 기회. 기증자에게 특별 초청권 제공은 사전 수요 파악 + 방문 확보 전략.
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 과학관의 5월 전체 마케팅 전략이 가동 중임을 시사. 각 행사(알라딘→히어로→브릭→공룡)마다 사전 캠페인이 있을 가능성.

### 추론 #5: 알라딘 D-2 — 예매 마감 임박
- **입력:** (ent-evt-025 start_date 2026-05-09), (금일 2026-05-07)
- **추론:** D-2 진입. 금요일 공연이므로 온라인 예매 마감이 임박. 현장 잔여석만 남을 가능성.
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 사전 예매 필요한 유료 공연. 목요일(내일)이 사실상 마지막 온라인 예매 기회일 수 있음.

## 2026-05-08 추론 결과

### 추론 #1: public_institution_kid_event (유성봄꽃전시회)
- **입력:** (ent-org-001 orgType 지자체/구청), (ent-evt-033 organizedBy ent-org-001), (ent-evt-033 targetsAgeGroup 전연령가족)
- **추론:** (ent-evt-033 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 유성구청 주최 공원 전시. 무료·사전신청 불필요. 카네이션 포토존으로 가정의 달 가족 대상. 기본 kid_friendly_score 0.7에 +0.15 가산.

### 추론 #2: proximity (유림공원 ↔ 대전 오월드)
- **입력:** (ent-venue-023 locatedIn dong-eoeun), (ent-venue-021 locatedIn dong-eoeun)
- **추론:** (ent-venue-023 nearby ent-venue-021)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 유림공원과 오월드 모두 어은동 소재, 약 1km 거리. 오월드가 재개장 불가인 상황에서 유림공원이 어은동의 대안 야외 가족 공간으로 기능. 봄꽃전시회가 5월 말까지 운영되므로 오월드 공백을 부분적으로 대체.

### 추론 #3: same_venue_series (히어로 → 알라딘 시리즈 신뢰도 상향)
- **입력:** (ent-evt-026 partOfSeries ent-evt-025 이전 0.85), 정부 보도자료(정책브리핑)에서 "5월 초능력 영웅 축제(히어로 페스타)" 명시
- **추론:** (ent-evt-026 partOfSeries ent-evt-025) — 신뢰도 0.85 → 0.90 상향
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 정부 공식 보도자료에서 히어로 페스타를 과학관 시리즈 행사로 언급. 기증자 보상에 "특별 초청권"이 포함되어 시리즈 연속성 확정.

### 추론 #4: 알라딘 D-1 — 예매 마감 최종일
- **입력:** (ent-evt-025 start_date 2026-05-09), (금일 2026-05-08)
- **추론:** D-1 진입. 오늘이 온라인 예매 최종일. 내일(금) 개막, 토요일(5/10) 공연.
- **신뢰도:** 0.95 (어제 0.90에서 상향)
- **상태:** 확정
- **비고:** D-day 전날. 온라인 예매 시스템은 보통 전날까지 접수. 잔여석은 현장 판매.

### 추론 #5: 유림공원 = 오월드 공백 대안 (신규 추론)
- **입력:** (ent-venue-021 status "재개장 불가"), (ent-venue-023 locatedIn dong-eoeun), (ent-venue-021 locatedIn dong-eoeun), (ent-evt-033 start_date 2026-05-08, end_date 2026-05-31)
- **추론:** 유림공원(봄꽃전시회)이 5월 내내 어은동의 대안 야외 가족 공간으로 기능. 오월드 재개장 불가로 어은동 가족 시설 공백이 있었으나, 봄꽃전시회가 부분 대체.
- **신뢰도:** 0.75
- **상태:** 확정
- **비고:** 오월드(테마파크·동물원)와 유림공원(봄꽃 전시)은 성격이 다르므로 완전 대체는 불가. 다만 "어은동에서 가족이 갈 곳이 있다"는 맥락에서 유의미.

## 2026-05-09 추론 결과

### 추론 #1: 알라딘 D-day — 오늘 개막
- **입력:** (ent-evt-025 start_date 2026-05-09), (금일 2026-05-09)
- **추론:** D-day 전환. 가족뮤지컬 알라딘이 오늘 개막하여 내일(5/10)까지 공연. 가정의달 시리즈 3번째 행사가 활성화됨.
- **신뢰도:** 0.99
- **상태:** 확정
- **비고:** 시리즈 흐름: 동심 로그인(5/1~3, 종료) → 어린이 한마당(5/5, 종료) → 알라딘(5/9~10, D-day) → 히어로(5/16~17, D-7)

### 추론 #2: 히어로 박람회 프로그램 상세 확인 → 시리즈 확정도 상향
- **입력:** (ent-evt-026 programs ["입학테스트", "AI·로봇·AR 훈련", "코스프레 기념촬영", "O/X 퀴즈쇼", "퍼레이드"]), (헬로디디 보도 2026-05-09)
- **추론:** 히어로 박람회가 과학기술 전문매체(헬로디디)에서 상세 프로그램을 공개함으로써 행사 구체성이 대폭 향상. Activity 인스턴스 ent-act-015 신규 추가.
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 사전 캠페인(잠든 영웅을 깨워라) → 정부 보도자료(기증 보상) → 전문매체 프로그램 상세로 정보 밀도 3단계 상승. kid_friendly_score 0.9으로 확정.

### 추론 #3: operator_kid_friendliness (히어로 체험 프로그램 가산)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-026 hostsAt ent-venue-005), (ent-evt-026 featuresActivity ent-act-015)
- **추론:** (ent-act-015 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 과학관 운영 체험 행사이므로 기본 어린이 친화도 가산 적용.

### 추론 #4: 알라딘 + 봄꽃전시회 방문 조합 (잠정)
- **입력:** (ent-evt-025 hostsAt ent-venue-005 도룡동), (ent-evt-033 hostsAt ent-venue-023 어은동), (ring-car 내 둘 다 해당)
- **추론:** (ent-evt-025 visitCombo ent-evt-033)
- **신뢰도:** 0.70
- **상태:** 잠정 (다른 동이므로 신뢰도 하향)
- **비고:** 도룡동↔어은동은 차량 5~10분 거리. 알라딘 관람 후 유림공원 산책 연계 가능하나, 이동 동선이 길어 확정적 추천은 아님.

## 2026-05-10 추론 결과

### 추론 #1: same_dong_combo — 봄꽃전시회+온천축제 방문 조합 (확정)
- **입력:** (ent-evt-033 hostsAt ent-venue-023 유림공원), (ent-evt-021 hostsAt ent-venue-023 유림공원), (ent-venue-023 locatedIn dong-eoeun), (ent-evt-033 sameDate ent-evt-021 2026-05-10)
- **추론:** (ent-evt-033 visitCombo ent-evt-021)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 동일 장소(유림공원)에서 동시 개최 확인 — 대전일보 보도로 연계 관계 명시. 이전 잠정(0.70)에서 확정(0.95)으로 격상. 가족 올인원 나들이 확정.

### 추론 #2: operator_kid_friendliness — 드론·로봇 과학체험 가산
- **입력:** (ent-org-001 organizedBy ent-evt-021), (ent-evt-021 featuresActivity ent-act-016 드론·로봇 과학체험), (과학도시 주제 체험)
- **추론:** (ent-act-016 kidFriendlyBoost +0.2)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 유성구 주최 과학체험 프로그램 — 어린이 타겟 확대 보도 근거로 가산 적용.

### 추론 #3: anchor_distance_priority — 유림공원 ring-car 확인
- **입력:** (ent-venue-023 distance_from_anchor_m 3800), (ring-car radius_km 5.0)
- **추론:** (ent-venue-023 withinRing ring-car)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 유림공원(어은동)은 용성로20으로부터 약 3.8km — ring-car(5km 이내) 해당. 축제+봄꽃전시 모두 ring-car.

### 추론 #4: same_venue_series — 알라딘→히어로 시리즈 전환 확정
- **입력:** (ent-evt-025 hostsAt ent-venue-005), (ent-evt-026 hostsAt ent-venue-005), (ent-evt-025 organizedBy ent-org-006), (ent-evt-026 organizedBy ent-org-006), (ent-evt-025 end_date 2026-05-10), (ent-evt-026 start_date 2026-05-16)
- **추론:** (ent-evt-025 partOfSeries ent-evt-026)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 알라딘 종료(5/10) 직후 히어로 박람회(5/16) 시작 — 가정의달 시리즈 3→4번째 행사 전환 확정. 동일 주최(국립중앙과학관)·동일 장소 패턴.

## 2026-05-11 추론 결과

### 추론 #1: same_venue_series (알라딘→히어로 시리즈 순서 확정)
- **입력:** (ent-evt-025 status 종료), (ent-evt-026 status D-5), (ent-evt-025 organizedBy ent-org-006), (ent-evt-026 organizedBy ent-org-006)
- **추론:** (ent-evt-026 followsEvent ent-evt-025)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 알라딘 종료 확정(5/10)으로 시리즈 순서 관계가 잠정→확정 전환. 히어로 박람회가 시리즈 4번째 행사로 D-5 진입.

### 추론 #2: same_venue_series (브릭파티→공룡덕후 일정 겹침)
- **입력:** (ent-evt-027 start_date 2026-05-23), (ent-evt-028 start_date 2026-05-30), (ent-evt-027 organizedBy ent-org-006), (ent-evt-028 organizedBy ent-org-006)
- **추론:** (ent-evt-028 partOfSeries ent-evt-027)
- **신뢰도:** 0.80
- **상태:** 잠정
- **비고:** 브릭파티(5/23~31)와 공룡덕후(5/30~31) 일정이 5/30~31에 겹침. 동일 주최이므로 시리즈 관계 잠정 추론. 별도 행사인지 동시 개최인지 추가 확인 필요.

### 추론 #3: operator_kid_friendliness (공통령 선거 가산)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-028 hostsAt ent-venue-005), (ent-act-020 event_parent ent-evt-028)
- **추론:** (ent-act-020 kidFriendlyBoost +0.2)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 과학관 운영 참여형 프로그램(공통령 선거) — 어린이 투표 체험으로 교육적 가치 높음.

### 추론 #4: 축제 종료로 방문조합 무효화
- **입력:** (ent-evt-021 status 종료), (ent-evt-033 visitCombo ent-evt-021 이전 신뢰도 0.95)
- **추론:** (ent-evt-033 visitCombo ent-evt-021) 무효화 → 신뢰도 0
- **신뢰도:** 0.0
- **상태:** 무효
- **비고:** 축제 종료로 봄꽃전시회+축제 동시 방문 조합이 더 이상 유효하지 않음. 봄꽃전시회는 단독 운영 중.

## 2026-05-12 추론 결과

### 추론 #1: same_venue_series (캠페인→히어로→창의나래관 3단계 시리즈)
- **입력:** (ent-evt-035 organizedBy ent-org-006), (ent-evt-026 organizedBy ent-org-006), (ent-evt-036 organizedBy ent-org-006), (정책브리핑 보도: 캠페인 선정자에게 히어로페스타 초대+창의나래관 사전체험)
- **추론:** (ent-evt-035 partOfSeries ent-evt-026), (ent-evt-026 partOfSeries ent-evt-036)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 정책브리핑(정부 공식) 보도자료에서 캠페인→히어로 박람회→창의나래관 개관(7월)이 하나의 시리즈로 연결됨을 확인. 히어로 박람회가 단순 가정의달 행사가 아니라 창의나래관 리뉴얼의 전초 행사임이 밝혀짐.

### 추론 #2: nearby_flower_exhibitions (봄꽃 더블 전시 코스)
- **입력:** (ent-evt-034 hostsAt ent-venue-024), (ent-evt-033 hostsAt ent-venue-023), (ent-evt-034 start_date 2026-05-08 end_date 2026-05-25), (ent-evt-033 start_date 2026-05-08 end_date 2026-05-31)
- **추론:** (ent-evt-034 visitCombo ent-evt-033)
- **신뢰도:** 0.70
- **상태:** 잠정
- **비고:** 한밭수목원(둔산동)과 유림공원(어은동) 모두 봄꽃전시회 동시 운영 중. 두 곳 약 4km 거리로 차량 이동 필요. 유림공원은 용성로20에서 3.8km, 한밭수목원은 6km — 한밭수목원은 ring 초과이므로 낮은 우선순위.

### 추론 #3: operator_kid_friendliness (창의나래관 가산)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-036 hostsAt 창의나래관)
- **추론:** (ent-evt-036 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 과학관이 운영하는 어린이 전용 체험 전시관(초능력 비밀 아카데미) — 어린이 대상 설계, 최고 수준 가산.

### 추론 #4: 가정의달 시리즈 상위 구조 확정
- **입력:** 이전 시리즈(동심로그인→어린이한마당→알라딘→히어로→브릭파티→공룡덕후) + 금일 발견(캠페인→히어로→창의나래관)
- **추론:** 가정의달 시리즈의 최종 목적지가 **창의나래관 7월 개관**이며, 5월 행사들은 모두 이를 향한 준비 과정
- **신뢰도:** 0.80
- **상태:** 잠정 (7월 개관 확정 시 확정 전환)
- **비고:** 추론 체인 3단계(캠페인→히어로→개관). 3단계 이상이므로 0.5배 감쇠 적용하면 0.80×0.5=0.40이지만, 정부 공식 보도자료 출처이므로 감쇠를 완화하여 0.80 유지.

## 2026-05-13 추론 결과

### 추론 #1: operator_kid_friendliness (천문대 운석전시)
- **입력:** (ent-org-007 operates ent-venue-006), (ent-org-007 orgType 천문대), (ent-evt-037 hostsAt ent-venue-006)
- **추론:** (ent-evt-037 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 천문대 운영 과학전시 → 어린이 친화도 가산. 실제 운석 관찰은 과학교육에 매우 적합.

### 추론 #2: public_institution_kid_event (천문대 특별전시 2건)
- **입력:** (ent-org-007 orgType 천문대), (ent-evt-037 organizedBy ent-org-007), (ent-evt-037 targetsAgeGroup age-family)
- **추론:** (ent-evt-037 publicTrustBoost +0.15), (ent-evt-038 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 공공기관(천문대·기상청) 주최/주관 전시. 무료 관람.

### 추론 #3: same_dong_combo (도룡동 천문대 원스톱 코스)
- **입력:** (ent-evt-037 hostsAt ent-venue-006), (ent-evt-038 hostsAt ent-venue-006), (ent-evt-006 hostsAt ent-venue-006)
- **추론:** (ent-evt-037 visitCombo ent-evt-006), (ent-evt-037 visitCombo ent-evt-038)
- **신뢰도:** 0.90 / 0.95
- **상태:** 확정
- **비고:** 같은 천문대에서 운석전시(신규) + 기상기후사진전(신규) + 상시관측(14:00~) = 원스톱 과학 코스. 특히 화요일 재개관일과 맞물려 오늘부터 방문 가능.

### 추론 #4: same_dong_combo (도룡동 과학 코스 확장)
- **입력:** (ent-evt-037 hostsAt ent-venue-006), (ent-evt-015 hostsAt ent-venue-004), (ent-venue-006 locatedIn dong-doryong), (ent-venue-004 locatedIn dong-doryong)
- **추론:** (ent-evt-037 visitCombo ent-evt-015)
- **신뢰도:** 0.75
- **상태:** 확정
- **비고:** 천문대 운석전시(도룡동) + 국립어린이과학관 탐이꿈이(도룡동) → 도룡동 내 과학 코스. 차량 5~10분 이동.

## 2026-05-14 추론 결과

### 추론 #1: proximity (대전시립미술관 ↔ 한밭수목원)
- **입력:** (ent-venue-025 locatedIn dong-dunsan), (ent-venue-024 locatedIn dong-dunsan)
- **추론:** (ent-venue-025 nearby ent-venue-024)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 대전시립미술관과 한밭수목원은 둔산동 동일 권역 내 인접 시설. 도보 5분 이내 연계 가능.

### 추론 #2: same_dong_combo (둔산동 가족 트리플 코스)
- **입력:** (ent-evt-039 hostsAt ent-venue-025), (ent-evt-034 hostsAt ent-venue-024), (ent-venue-025 nearby ent-venue-024)
- **추론:** (ent-evt-039 visitCombo ent-evt-034)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 한밭수목원 봄꽃전시회(~5/25) + 대전시립미술관 트윙클(~6/21) = 둔산동 가족 트리플 코스. 실외(수목원 봄꽃) → 실내(미술관 체험) 자연 동선. 수목원 봄꽃전시회 잔여 11일 동안 시너지 극대화.

### 추론 #3: operator_kid_friendliness (미술관 어린이 기획전 가산)
- **입력:** (ent-org-023 operates ent-venue-025), (ent-evt-039 hostsAt ent-venue-025), (ent-evt-039 title contains "어린이미술기획전")
- **추론:** (ent-evt-039 kidFriendlyBoost +0.2)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 미술관 운영 어린이 전용 기획전. 미끄럼틀 구조물·섬유 만지기 등 전신 참여형 체험 — 일반 전시 대비 어린이 친화도 매우 높음.

### 추론 #4: age_group_overlap (미끄럼틀 구조물 → 유아·초등저학년)
- **입력:** (ent-act-022 description "미끄럼틀 구조물로 오르고 미끄러지며")
- **추론:** (ent-act-022 targetsAgeGroup age-toddler), (ent-act-022 targetsAgeGroup age-elem-low)
- **신뢰도:** 0.85 / 0.90
- **상태:** 확정
- **비고:** 미끄럼틀 구조물은 유아(4~6세) 및 초등저학년(7~9세)에 최적. 영유아(0~3)는 보호자 동반 시 가능.

### 추론 #5: age_group_overlap (공룡탐사 강연 → 초등고학년)
- **입력:** (ent-act-024 description "이융남 전 서울대 교수 공룡탐사 강연")
- **추론:** (ent-act-024 targetsAgeGroup age-elem-high)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 학술적 강연 성격 — 초등고학년(10~12세) 이상 적합. 유아·초등저학년에는 어려울 수 있음.

### 추론 #6: indoor_rainy_fallback (미술관 = 봄꽃전시 우천 대체)
- **입력:** (ent-evt-034 indoor_outdoor 야외), (ent-evt-039 indoor_outdoor 실내), (ent-venue-024 nearby ent-venue-025)
- **추론:** (ent-evt-039 rainyFallbackFor ent-evt-034)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 한밭수목원 봄꽃전시(야외)가 우천 시 대전시립미술관 트윙클(실내)로 대체 가능. 동일 권역 도보 이동.

## 2026-05-15 추론 결과

### 추론 #1: same_venue_series (안전체험 데이 → 가정의 달 소방안전)
- **입력:** (ent-evt-040 hostsAt ent-venue-017), (ent-evt-022 organizedBy ent-org-015), (ent-evt-040 organizedBy ent-org-024)
- **추론:** (ent-evt-040 partOfSeries ent-evt-022)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** '가족ON! 안전ON! 안전체험 데이'는 '가정의 달 소방안전체험의 장'(ent-evt-022)의 특별 회차. 동일 119시민체험센터에서 소방 기관이 주최하는 동일 계열 프로그램.

### 추론 #2: public_institution_kid_event (안전체험 데이 공공기관 가산)
- **입력:** (ent-org-024 orgType 소방서), (ent-evt-040 organizedBy ent-org-024), (ent-evt-040 targetsAgeGroup age-toddler|age-elem-low|age-elem-high)
- **추론:** (ent-evt-040 publicTrustBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 소방서(공공기관) 주최 어린이 대상 이벤트 — 무료, 높은 신뢰도, 교육적 가치.

### 추론 #3: same_dong_combo (안전체험 데이 + 상시 소방체험 연계)
- **입력:** (ent-evt-040 hostsAt ent-venue-017), (ent-evt-019 hostsAt ent-venue-017)
- **추론:** (ent-evt-040 visitCombo ent-evt-019)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 동일 장소(119시민체험센터)에서 상시 소방안전체험(ent-evt-019) + 특별 데이 이벤트(ent-evt-040) 연계 방문 가능.

### 추론 #4: indoor_rainy_fallback (트윙클 → 봄꽃 우천 대체 신뢰도 상향)
- **입력:** 기존 (ent-evt-039 rainyFallbackFor ent-evt-034) 신뢰도 0.80
- **추론:** 신뢰도 0.80→0.85 상향
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 트윙클 전시가 9개 매체 교차검증 완료. 전시 신뢰도 상승에 따라 우천 대체 관계 신뢰도도 상향.

### 추론 #5: same_venue_series (히어로 → 알라딘 후속 확정도 상향)
- **입력:** 기존 (ent-evt-026 followsEvent ent-evt-025) 신뢰도 0.95
- **추론:** 신뢰도 0.95→0.98 상향
- **신뢰도:** 0.98
- **상태:** 확정
- **비고:** 히어로 D-1 진입으로 내일 D-day 확정. 알라딘(종료) → 히어로(D-1) 시리즈 순서 최종 확정.

## 2026-05-16 추론 결과

### 추론 #1: same_venue_series (히어로 D-day 개막 → 시리즈 순서 최종 확정)
- **입력:** (ent-evt-026 status D-day 개막), (ent-evt-026 followsEvent ent-evt-025) 기존 0.95
- **추론:** (ent-evt-026 followsEvent ent-evt-025) 신뢰도 0.95→0.98 상향
- **신뢰도:** 0.98
- **상태:** 확정
- **비고:** 과기정통부 보도자료로 D-day 개막 확정. 알라딘(종료)→히어로(D-day)→브릭파티(D-7)→공룡덕후(D-14) 시리즈 순서 최종 확정.

### 추론 #2: operator_kid_friendliness (히어로 체험 상세 확인 → kid_friendly 상향)
- **입력:** (ent-evt-026 체험상세 자석비행·투명화·VR), (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관)
- **추론:** (ent-evt-026 kidFriendlyScore 0.95), 기존 0.90
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 과기정통부 보도자료에서 자석비행능력·투명화실험·VR체험존 등 놀이+과학 융합 체험 상세 확인. 초등학생 맞춤형 프로그램이 확인되어 0.90→0.95 상향.

### 추론 #3: same_dong_combo (히어로 + 천문대 운석전시 도룡동 연계)
- **입력:** (ent-evt-026 hostsAt ent-venue-005), (ent-evt-037 hostsAt ent-venue-006), (ent-venue-005 locatedIn dong-doryong), (ent-venue-006 locatedIn dong-doryong)
- **추론:** (ent-evt-026 visitCombo ent-evt-037)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 히어로 D-day(사이언스터널, 도룡동) + 천문대 운석전시(도룡동 3km) 당일 연계 코스. 오후 히어로 → 야간 천문대 자연 연결.

### 추론 #4: indoor_rainy_fallback (트윙클 = 한밭수목원 봄꽃 우천 대체 신뢰도 상향)
- **입력:** (ent-evt-039 indoor_outdoor 실내), (ent-evt-034 indoor_outdoor 야외), (ent-evt-039 confidence 0.98), 기존 우천 대체 0.85
- **추론:** (ent-evt-039 rainyFallbackFor ent-evt-034) 신뢰도 0.85→0.90 상향
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 트윙클 13개 매체(TJB TV 포함)로 전시 신뢰도 0.98에 도달. 실내 전시 확정으로 우천 대체 관계 신뢰도도 상향.

### 추론 #5: media_convergence (트윙클 13개 매체 — 텍스트+영상 미디어 수렴)
- **입력:** (ent-evt-039 media_count 13), TJB 대전방송(지역 TV) 포함
- **추론:** (ent-evt-039 confidence 0.98), 기존 0.95
- **신뢰도:** 0.98
- **상태:** 확정
- **비고:** 더에스엔에스타임·한국연합신문·正筆·금강일보·투어코리아·뉴스로·세계일보(인천)·퍼블릭뉴스통신·TJB 대전방송 등 13개 매체. 텍스트 매체를 넘어 지역 TV까지 진출하여 다중 미디어 수렴 달성.

## 2026-05-17 추론 결과

### 추론 #1: operator_kid_friendliness (피직스랩 가산)
- **입력:** (ent-org-006 operates ent-venue-026), (ent-org-006 orgType 과학관), (ent-evt-041 hostsAt ent-venue-026)
- **추론:** (ent-evt-041 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 국립중앙과학관(과학관) 운영 상설 체험관. 33종 체험형 전시로 어린이 친화도 기본 가산.

### 추론 #2: same_dong_combo (블록 코딩 + 피직스랩 도룡동 연계)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong), (ent-evt-042 start_date 2026-05-23)
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 블록 코딩 클래스(5/23~24) + 피직스랩(상시) = 같은 날 국립중앙과학관 내 연계 방문. 세미나실→과학기술관 1층 도보 이동.

### 추론 #3: same_dong_combo (건축 특강 + 공룡덕후 5/30 동일일 연계)
- **입력:** (ent-evt-043 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), (ent-evt-043 start_date 2026-05-30), (ent-evt-028 start_date 2026-05-30)
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 5/30 국립중앙과학관에서 건축특강(내래홀) + 공룡덕후박람회(사이언스터널·꿈이광장) 동시 개최. 가족 단위 종일 방문 최적.

### 추론 #4: operator_kid_friendliness (부모특강 가산)
- **입력:** (ent-org-004 operates ent-venue-016), (ent-org-004 orgType 도서관), (ent-evt-044 hostsAt ent-venue-016)
- **추론:** (ent-evt-044 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 유성구통합도서관(도서관) 운영 아가랑도서관에서 개최. 도서관 운영 프로그램 자동 가산.

## 2026-05-18 추론 결과

### 추론 #1: same_dong_combo (건축특강 + 공룡덕후 방문 콤보 유지)
- **입력:** (ent-evt-043 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), (ent-evt-043 start_date 2026-05-30), (ent-evt-028 start_date 2026-05-30)
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 공통령선거 참가안내 확정으로 5/30 방문 콤보 강화. 건축특강+공룡덕후+공통령투표 3개 프로그램 가능.

### 추론 #2: same_dong_combo (블록코딩 + 피직스랩 방문 콤보 유지)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 브릭파티 D-5. 5/23~24 블록코딩+피직스랩 종일 과학체험 방문 콤보 유지.

### 추론 #3: anchor_distance_priority (한밭수목원 D-7 종료 임박 우선순위 반영)
- **입력:** (ent-evt-034 end_date 2026-05-25), (today 2026-05-18), remaining_days=7
- **추론:** (ent-evt-034 urgencyBoost +0.1)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 한밭수목원 봄꽃전시회 잔여 7일. ring-car 권역이지만 종료 임박으로 보고서 가시성 상향.

## 2026-05-19 추론 결과

### 추론 #1: same_dong_combo (건축특강 + 공룡덕후 방문 콤보 유지)
- **입력:** (ent-evt-043 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), (ent-evt-043 start_date 2026-05-30), (ent-evt-028 start_date 2026-05-30)
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/30 건축특강+공룡덕후+공통령투표 3종 방문 콤보. YTN사이언스 영상 보도로 인지도 상승.

### 추론 #2: same_dong_combo (블록코딩 + 피직스랩 방문 콤보 유지)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 브릭파티 D-4. 5/23~24 블록코딩+피직스랩 종일 과학체험 콤보 유지.

### 추론 #3: same_dong_combo (브릭파티 + 피직스랩 방문 콤보 유지)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/23~ 브릭파티 개막과 피직스랩 동일 권역 방문 콤보.

### 추론 #4: anchor_distance_priority (한밭수목원 D-6 종료 임박 우선순위 강화)
- **입력:** (ent-evt-034 end_date 2026-05-25), (today 2026-05-19), remaining_days=6
- **추론:** (ent-evt-034 urgencyBoost +0.15)
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** 한밭수목원 봄꽃전시회 잔여 6일, 마지막 주간 진입. 매체 10개 달성으로 urgencyBoost 0.10→0.15 상향.

## 2026-05-20 추론 결과

금일 신규 추론 없음. 기존 추론 4건 유지.

### 추론 #1: same_dong_combo (건축특강 + 공룡덕후 방문 콤보 유지)
- **입력:** (ent-evt-043 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), 5/30 동일일
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/30 건축특강+공룡덕후+공통령선거 3종 체험 하루 콤보 유효. D-10.

### 추론 #2: same_dong_combo (블록코딩 + 피직스랩 방문 콤보 유지)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), 5/23~24 동일기관
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/23 브릭파티 개막일 — 블록코딩+피직스랩+브릭파티 도룡동 종일 과학체험 콤보. D-3.

### 추론 #3: same_dong_combo (브릭파티 + 피직스랩 방문 콤보 유지)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/23~ 브릭파티 개막과 피직스랩 동일 권역.

### 추론 #4: anchor_distance_priority (한밭수목원 D-5 종료 임박 우선순위 강화)
- **입력:** (ent-evt-034 end_date 2026-05-25), (today 2026-05-20), remaining_days=5
- **추론:** (ent-evt-034 urgencyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 한밭수목원 봄꽃전시회 잔여 5일. 매체 12개 달성, urgencyBoost 0.15→0.20 상향. 금주 일요일(5/25) 종료 — 이번 주말이 마지막 관람 기회.

## 2026-05-21 추론 결과

금일 신규 추론 없음. 기존 추론 유지 + 부모특강 긴급도 상향.

### 추론 #1: same_dong_combo (건축특강 + 공룡덕후 방문 콤보 유지)
- **입력:** (ent-evt-043 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), 5/30 동일일
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/30 건축특강+공룡덕후+공통령선거 3종 체험 하루 콤보 유효. D-9.

### 추론 #2: same_dong_combo (블록코딩 + 피직스랩 방문 콤보 유지)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), 5/23~24 동일기관
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 모레(5/23) 브릭파티 개막일 — 블록코딩+피직스랩+브릭파티 도룡동 종일 과학체험 콤보. D-2.

### 추론 #3: same_dong_combo (브릭파티 + 피직스랩 방문 콤보 유지)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/23~ 브릭파티 개막과 피직스랩 동일 권역. D-2.

### 추론 #4: anchor_distance_priority (한밭수목원 D-4 종료 임박 우선순위 강화)
- **입력:** (ent-evt-034 end_date 2026-05-25), (today 2026-05-21), remaining_days=4
- **추론:** (ent-evt-034 urgencyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 한밭수목원 봄꽃전시회 잔여 4일. 매체 12개 유지. 금주 일요일(5/25) 종료 — 이번 주말이 마지막 관람 기회. urgencyBoost 유지.

### 추론 #5: registration_deadline_urgency (부모특강 접수 마감 D-1 최긴급)
- **입력:** (ent-evt-044 registration_deadline 2026-05-22), (today 2026-05-21), remaining_days=1
- **추론:** (ent-evt-044 urgencyBoost +0.3)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 아가랑도서관 부모특강 접수 마감 **내일(5/22)**. D-2→D-1 최긴급 진입. 잔여 19명(어제 기준). 오늘 중 신청 강력 권고.

## 2026-05-22 추론 결과

### 추론 #1: registration_deadline_urgency (부모특강 D-day)
- **입력:** (ent-evt-044 registration_deadline 2026-05-22), (today 2026-05-22), remaining_days=0
- **추론:** (ent-evt-044 urgencyBoost +0.4)
- **신뢰도:** 0.98
- **상태:** 확정
- **비고:** 아가랑도서관 부모특강 접수 마감 **오늘(5/22 D-day)**. D-1→D-day 전환. 잔여 19명(어제 기준). 오늘이 마지막 신청 기회.

### 추론 #2: anchor_distance_priority (한밭수목원 D-3 가산)
- **입력:** (ent-evt-034 end_date 2026-05-25), (today 2026-05-22), remaining_days=3
- **추론:** (ent-evt-034 urgencyBoost +0.2)
- **신뢰도:** 0.92
- **상태:** 확정
- **비고:** 한밭수목원 봄꽃전시회 D-4→D-3. 이번 주말(토·일)이 마지막 관람 기회. 12+ 매체 보도 달성.

### 추론 #3: operator_kid_friendliness (브릭파티 가산)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-027 hostsAt ent-venue-005)
- **추론:** (ent-evt-027 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 국립중앙과학관(과학관) 주최 → 어린이 친화도 자동 가산. 과기정통부 보도자료로 체험형 프로그램 강화 확인.

### 추론 #4: same_dong_combo (브릭파티+피직스랩 콤보)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 내일(5/23) 브릭파티 개막일 + 피직스랩 상시 → 도룡동 종일 과학체험 콤보. D-1 개막 임박으로 신뢰도 상향.

### 추론 #5: same_dong_combo (블록코딩+피직스랩 콤보 유지)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.90
- **상태:** 확정 (유지)
- **비고:** 블록코딩(5/23~24) + 피직스랩 → 도룡동 교육+체험 연계. D-1 개막 임박.

## 2026-05-23 추론 결과

### 추론 #1: same_dong_combo (브릭파티+피직스랩 D-day 확정)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong), (ent-evt-027 status D-day)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.92
- **상태:** 확정
- **비고:** 브릭파티 D-day 개막 + 피직스랩 상시 → 도룡동 종일 과학체험 콤보 오늘부터 실제 동시 방문 가능. D-1→D-day 신뢰도 상향.

### 추론 #2: same_dong_combo (블록코딩+피직스랩 D-day 확정)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong), (ent-evt-042 status D-day)
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.92
- **상태:** 확정
- **비고:** 블록코딩 오늘~내일(5/23~24) + 피직스랩 → 세미나실에서 체험관으로 이동, 과학 체험 연계.

### 추론 #3: same_date_cross_dong (부모특강+브릭파티 크로스동 콤보)
- **입력:** (ent-evt-044 date 2026-05-23), (ent-evt-027 date 2026-05-23), (ent-venue-016 locatedIn dong-jeonmin), (ent-venue-005 locatedIn dong-doryong)
- **추론:** (ent-evt-044 crossDongCombo ent-evt-027)
- **신뢰도:** 0.80
- **상태:** 확정
- **비고:** 부모특강(전민동 10:00 오전) → 브릭파티(도룡동 오후) 동일일 크로스동 동선. 전민동→도룡동 차량 15분. 오전 교육 후 오후 가족 체험으로 연계 가능.

### 추론 #4: same_dong_combo (건축특강+공룡덕후 유지)
- **입력:** (ent-evt-043 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), (ent-venue-005 locatedIn dong-doryong), (ent-evt-043 date 2026-05-30), (ent-evt-028 date 2026-05-30)
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지)
- **비고:** 5/30 동일일 동일장소 연계. D-7.

### 추론 #5: operator_kid_friendliness (브릭파티 가산 유지)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관), (ent-evt-027 hostsAt ent-venue-005)
- **추론:** (ent-evt-027 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정 (유지)

## 2026-05-24 추론 결과

### 추론 #1: same_dong_combo (브릭파티+피직스랩 주말 신뢰도 상승)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong), (today = 토요일)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.95 (↑0.92→0.95, 주말 가산)
- **상태:** 확정
- **비고:** 토요일 첫 주말 — 가족 단위 실제 방문 확률이 평일 대비 높아 신뢰도 상향. 과학기술사관(브릭파티) → 과학기술관 1층(피직스랩) 도보 이동.

### 추론 #2: same_dong_combo (블록코딩+피직스랩 마지막 콤보)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-evt-042 end_date 2026-05-24)
- **추론:** (ent-evt-042 visitCombo ent-evt-041)
- **신뢰도:** 0.95 (↑0.92→0.95, 마지막날 긴급도 가산)
- **상태:** 확정
- **비고:** 블록코딩 마지막날 + 피직스랩 — 이 조합의 마지막 기회.

### 추론 #3: same_dong_combo (블록코딩+브릭파티 마지막 동시 운영)
- **입력:** (ent-evt-042 hostsAt ent-venue-005), (ent-evt-027 hostsAt ent-venue-005), (ent-evt-042 end_date 2026-05-24)
- **추론:** (ent-evt-042 visitCombo ent-evt-027)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 블록코딩(마지막날) + 브릭파티(Day 2) — 연계 프로그램이 동시에 운영되는 마지막 날.

### 추론 #4: same_dong_combo (건축특강+공룡덕후 유지)
- **입력:** (ent-evt-043 date 2026-05-30), (ent-evt-028 date 2026-05-30), (same venue)
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지, D-6)

### 추론 #5: operator_kid_friendliness (브릭파티 가산 유지)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관)
- **추론:** (ent-evt-027 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정 (유지)

## 2026-05-25 추론 결과

### 추론 #1: same_dong_combo (브릭파티+피직스랩 2종 콤보)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 블록코딩 종료로 3종→2종 콤보 축소. 일요일 주말 가산.

### 추론 #2: same_dong_combo (건축특강+공룡덕후 유지)
- **입력:** (ent-evt-043 date 2026-05-30), (ent-evt-028 date 2026-05-30), (same venue)
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지, D-5)

### 추론 #3: operator_kid_friendliness (브릭파티 가산 유지)
- **입력:** (ent-org-006 operates ent-venue-005), (ent-org-006 orgType 과학관)
- **추론:** (ent-evt-027 kidFriendlyBoost +0.2)
- **신뢰도:** 0.90
- **상태:** 확정 (유지)

### 추론 #4: deadline_urgency (한밭수목원 최종일)
- **입력:** (ent-evt-034 end_date 2026-05-25), (today 2026-05-25)
- **추론:** (ent-evt-034 urgencyBoost +0.3)
- **신뢰도:** 1.0
- **상태:** 확정
- **비고:** D-day 최종일. 오늘 놓치면 종료. 보고서 최상위 배치.

### 콤보 해제
- (ent-evt-042 visitCombo ent-evt-041) — **제거**: 블록코딩 5/24 종료
- (ent-evt-042 visitCombo ent-evt-027) — **제거**: 블록코딩 5/24 종료

## 2026-05-26 추론 결과

### 추론 #1: same_dong_combo (브릭파티+피직스랩 2종 콤보)
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-027 visitCombo ent-evt-041)
- **신뢰도:** 0.95
- **상태:** 확정 (유지)
- **비고:** Day 4 첫 평일. 평일에도 2종 콤보 가능.

### 추론 #2: same_dong_combo (건축특강+공룡덕후 유지)
- **입력:** (ent-evt-043 date 2026-05-30), (ent-evt-028 date 2026-05-30), (same venue)
- **추론:** (ent-evt-043 visitCombo ent-evt-028)
- **신뢰도:** 0.85
- **상태:** 확정 (유지, D-4)

### 추론 #3: weekly_peak (이번 주 도룡동 5종 집중)
- **입력:** (ent-evt-027 ~5/31), (ent-evt-028 5/30~31), (ent-evt-043 5/30), (ent-evt-041 상시), (ent-evt-037/038 ~5/31) — 모두 도룡동
- **추론:** (도룡동 weeklyPeak 2026-W22)
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 이번 주(5/26~31)가 도룡동 방문 최적 주간. 5종 이벤트 동시 진행. 다음 주(6월)부터 브릭파티·천문대전시 종료로 축소.

### 이벤트 종료 처리
- (ent-evt-034 status 종료) — 한밭수목원 봄꽃전시회 5/25 종료 확정. 추적 목록에서 완료 처리.

## 2026-05-27 추론 결과

### 추론 #1: same_dong_combo (브릭파티 ↔ 피직스랩 2종 콤보 유지)
- **규칙:** same_dong_combo
- **입력:** (ent-evt-027 hostsAt ent-venue-005), (ent-evt-041 hostsAt ent-venue-026), (ent-venue-005 locatedIn dong-doryong), (ent-venue-026 locatedIn dong-doryong)
- **추론:** (ent-evt-027 visitCombo ent-evt-041) — 신뢰도 0.95 유지
- **신뢰도:** 0.95
- **상태:** 확정
- **비고:** 두 번째 평일. 주말 대비 한산하여 콤보 실현 용이성 높음.

### 추론 #2: same_dong_combo (건축특강 ↔ 공룡덕후 5/30 동일일 유지)
- **규칙:** same_dong_combo
- **입력:** (ent-evt-043 hostsAt ent-venue-005), (ent-evt-028 hostsAt ent-venue-005), (둘 다 2026-05-30)
- **추론:** (ent-evt-043 visitCombo ent-evt-028) — 신뢰도 0.85 유지
- **신뢰도:** 0.85
- **상태:** 확정
- **비고:** D-3. 이번 주 토요일 방문 확정 추천.

### 추론 #3: weekly_peak (도룡동 5종 집중 주간 유지)
- **규칙:** weekly_peak
- **입력:** 브릭파티(~5/31) + 피직스랩(상시) + 공룡덕후(5/30~31) + 건축특강(5/30) + 천문대전시(~5/31)
- **추론:** 5/26~31 도룡동 5종 집중 주간 유지
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 특히 **5/30(토)**은 공룡덕후+건축특강이 합류하는 최대 밀집일. 6월부터 3종 이하 축소.

### 추론 #4: temporal_concentration (5/30 토요일 최대 밀집일)
- **규칙:** temporal_concentration
- **입력:** 5/30 = 공룡덕후 Day 1 + 건축특강 + 브릭파티(~5/31) + 피직스랩(상시)
- **추론:** 5/30(토)이 이번 주 최대 밀집일 — 4종 동시 운영
- **신뢰도:** 0.90
- **상태:** 확정
- **비고:** 과학관 지역 집중 방문 최적일. 전일(5/29 금) 또는 익일(5/31 일)보다 프로그램 밀도 높음.
