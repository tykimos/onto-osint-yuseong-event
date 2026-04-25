# Onto-OSINT-Yuseong-Event

> 대전 유성구 일대(용산동·전민동·관평동·문지동·신성동·도룡동 등)에서 진행되는 **어린이·가족 동반 이벤트**를 매일 자동으로 수집·구조화·요약하는 OSINT 시스템.
> [`onto-osint`](https://github.com/tykimos/onto-osint) 시스템을 포크하여 유성구 가족 이벤트 도메인에 맞게 설정한 인스턴스다.

---

## 1. 무엇을 해주는가

매일 아침 출근/등교 전, 다음 한 장의 보고서가 자동으로 갱신된다 — `reports/YYYY/MM/YYYY-MM-DD.md`.

| 섹션 | 내용 |
|------|------|
| 오늘의 추천 (가족 동반 Top 5) | 어린이 친화도·접근성·날씨 적합도 종합 |
| 신규 이벤트 | 어제 이후 새로 공지된 행사 |
| 마감 임박 | 사전신청 D-3 이내, 정원 마감 임박 |
| 동(洞)별 묶음 | 용산동·전민동·관평동·문지동·신성동·도룡동 등 동 단위로 그룹핑 |
| 연령대별 묶음 | 영유아 / 유아 / 초등저학년 / 초등고학년 / 가족전연령 |
| 시리즈/정기 프로그램 | 같은 장소·주최가 반복하는 시리즈의 다음 회차 알림 |
| 지식그래프 시각화 | 이벤트–장소–주최–활동의 관계망 (Mermaid) |
| 출처 목록 | 모든 이벤트의 원문 URL |

---

## 2. 모니터링 범위

### 1차 타겟 동 (우선순위 상)

용산동, 전민동, 관평동, 문지동, 신성동, 도룡동

### 2차 인접 동 (가족 이동 반경)

노은동, 어은동, 구암동, 지족동, 반석동

### 핵심 출처 (custom_sites)

| 출처 | 다루는 내용 |
|------|------------|
| 유성구청 | 구 단위 공식 행사·축제·교육 프로그램 |
| 유성구 도서관 (관평·노은·진잠·전민) | 어린이 독서·체험, 가족 영화상영, 인형극 |
| 국립중앙과학관 (도룡동) | 어린이과학관·창의나래관·자기부상열차·특별전 |
| 대전시민천문대 (도룡동) | 야간 관측회, 가족 천문교실 |
| 대전엑스포과학공원 일원 | 도룡동 일대 야외 가족 행사 |
| 유성구 평생학습관·가족센터 | 주말 가족 강좌, 부모-자녀 만들기 |
| KAIST·출연연 공개 행사 | 신성동·도룡동 권역 가족 대상 과학 행사 |
| 대전관광공사 | 구 단위 축제 통합 캘린더 |

---

## 3. 도메인 온톨로지 시드

`config/osint-config.json` → `ontology.seed_classes`에 다음이 정의되어 있다.

```
Entity
├── Event         — name, start_date, venue, host, fee, target_age_group, kid_friendly_score, indoor_outdoor, ...
├── Venue         — name, dong, address, venue_type, parking, stroller_accessible, kids_zone, ...
├── Organization  — name, org_type (구청/도서관/과학관/평생학습관/박물관/가족센터)
├── Activity      — name, category (체험/전시/공연/강연/축제/스포츠)
├── AgeGroup      — label, min_age, max_age
└── Dong          — name, is_primary_target
```

핵심 관계:

```
Event   --hostsAt-->         Venue
Event   --organizedBy-->     Organization
Venue   --locatedIn-->       Dong
Event   --featuresActivity--> Activity
Event   --targetsAgeGroup--> AgeGroup
Event   --partOfSeries-->    Event   (추론 결과)
Venue   --nearby-->          Venue   (같은 동 내)
```

도메인 추론 규칙(`reasoning_rules`):

- `same_venue_series` — 같은 장소·주최가 반복하면 시리즈로 인식
- `same_dong_combo` — 같은 동, 같은 날 이벤트는 한 번에 묶어 방문 후보
- `age_group_overlap` — 같은 연령대 이벤트는 후보군 형성
- `operator_kid_friendliness` — 도서관/과학관/평생학습관/가족센터 운영 이벤트는 어린이 친화도 가산점
- `indoor_rainy_fallback` — 같은 동 실내 이벤트는 우천 시 야외 이벤트 대체 후보

---

## 4. 실행 방법

### 로컬 (Claude Code CLI)

```bash
cd onto-osint-yuseong-event
claude "오늘 날짜로 유성구 어린이·가족 이벤트 OSINT 보고서를 생성해줘"
```

Claude Code가 `CLAUDE.md`를 읽고, `.claude/skills/onto-osint-report/skill.md` 오케스트레이터를 따라 6단계 파이프라인을 실행한다.

### GitHub Actions (자동)

`.github/workflows/daily-osint-report.yml`이 매일 KST 07:00에 실행된다.

1. 이 리포지토리를 Fork
2. Settings → Secrets에 `CLAUDE_CODE_OAUTH_TOKEN` 추가
3. Actions → "Daily OSINT Report" → Run workflow (수동 테스트)

---

## 5. 디렉토리 구조

```
onto-osint-yuseong-event/
├── config/
│   └── osint-config.json          # 유성구 이벤트 도메인 설정 (이것만 수정하면 다른 지역으로 포팅 가능)
├── ontology/
│   ├── schema.json                # 자동 진화하는 스키마
│   ├── instances.json             # 누적되는 장소·기관·동 인스턴스
│   ├── kg/
│   │   ├── YYYY-MM-DD.json        # 일별 KG 스냅샷
│   │   └── cumulative.json        # 누적 KG
│   └── reasoning-log.md
├── sources/YYYY-MM-DD/            # 파이프라인 중간 산출물
│   ├── search-results.json
│   ├── index.json
│   ├── items/src-XXX.json
│   ├── entities.json
│   ├── analysis.md
│   └── report-basis.md
├── reports/YYYY/MM/
│   └── YYYY-MM-DD.md              # 일일 이벤트 다이제스트 (최종 산출물)
├── .claude/
│   ├── agents/                    # 4개 에이전트 역할 정의 (collector/extractor/reasoner/reporter)
│   └── skills/onto-osint-report/  # 오케스트레이터
├── .github/workflows/
│   └── daily-osint-report.yml
├── CLAUDE.md
└── README.md
```

---

## 6. 베이스 시스템에 대한 설명

이 프로젝트의 파이프라인·에이전트·추론 엔진 구조는 [`onto-osint`](https://github.com/tykimos/onto-osint) 본가에서 그대로 가져왔다.
온톨로지 진화·지식그래프 추론·에이전트 분리 등 일반 메커니즘에 대한 자세한 설명은 본가 README를 참고하라.

이 포크에서 손댄 것은 단 두 파일이다:

- `config/osint-config.json` — 도메인 시드(주제/지역/연령/장소/온톨로지)
- `CLAUDE.md` — 도메인 규칙(어린이 친화도, 마감 임박, 실내·야외 구분)

---

## License

MIT
