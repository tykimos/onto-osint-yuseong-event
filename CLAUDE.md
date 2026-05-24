# Onto-OSINT-Yuseong-Event — 유성구 어린이·가족 이벤트 일일 모니터

## Project Purpose
대전 유성구(특히 용산동·전민동·관평동·문지동·신성동·도룡동 일대)에서 매일 새로 공지되거나 진행되는 어린이·가족 동반 이벤트를 자동으로 수집·구조화·요약한다.
`onto-osint`의 6단계 파이프라인(수집→추출→온톨로지→그래프→보고서→발행)을 그대로 사용하되, 도메인 특화 설정(`config/osint-config.json`)으로 지역 행사용 온톨로지를 시드한다.

## Domain Snapshot

| 항목 | 값 |
|------|-----|
| 지리적 중심 (anchor) | **대전광역시 유성구 용성로 20** — 모든 이벤트는 이 지점으로부터의 거리(ring)에 따라 우선순위를 받는다 |
| 동심원 우선순위 | 0.5km(도보 5분) > 1km(도보 15분) > 2km(자전거) > 5km(차량 10분) |
| 핵심 지역 | 유성구 — 용산동, 전민동, 관평동, 문지동, 신성동, 도룡동 (1차 타겟) |
| 보조 지역 | 노은동, 어은동, 구암동, 지족동, 반석동 (인접 — 가족 이동 반경) |
| 핵심 대상 | 영유아 / 유아 / 초등저학년 / 초등고학년 / 가족 전연령 |
| 추적 대상 종류 | (1) 가족·어린이 이벤트 (2) 가게(카페·식당·키즈카페·공방·학원) 신규오픈/프로모션/팝업 (3) 공공기관 행사(행정복지센터·보건소·복지관·도서관·우체국·경찰서·소방서·주민자치) |
| 핵심 출처 | 유성구청, 유성구 도서관(관평·노은·진잠·전민), 국립중앙과학관, 대전시민천문대, 유성구 평생학습관·가족센터, 대전관광공사, 용산/전민/관평 행정복지센터, 유성구 보건소·복지관, Naver/Kakao Place, Instagram 지역 해시태그 |
| 보고서 언어 | 한국어 (`report_language: ko`) |
| 룩백 기간 | 14일 (이전 보고서 대비 신규/후속 판별) |

## Pipeline Architecture

```
Phase 1        Phase 2         Phase 3          Phase 4        Phase 5          Phase 6
수집(Collect) → 추출(Extract) → 온톨로지(Onto) → 그래프(Graph) → 보고서(Report) → 발행(Publish)
    │              │               │                │              │                │
    ▼              ▼               ▼                ▼              ▼                ▼
search-        index.json      ontology/        kg/            YYYY-MM-DD.md    Git + Wiki
results.json   items/          schema.json      YYYY-MM-DD     (KG 시각화 포함)
                               instances.json   .json
```

## Directory Structure

```
config/
└── osint-config.json          # 유성구 이벤트용 설정 (이 파일만 수정)

ontology/
├── schema.json                # 클래스(Event/Venue/Organization/Activity/AgeGroup/Dong) + 관계
├── instances.json             # 알려진 장소·기관·동 인스턴스 누적
├── kg/
│   ├── YYYY-MM-DD.json        # 일별 KG 스냅샷 (LLM 산출)
│   ├── YYYY-MM-DD.ttl         # 일별 KG RDF Turtle (post-step 자동 생성)
│   ├── cumulative.json        # 누적 KG
│   └── cumulative.ttl         # 누적 KG RDF Turtle (post-step 자동 생성)
└── reasoning-log.md           # 추론 로그

scripts/
├── kg_to_ttl.py               # KG JSON → RDF Turtle 변환 (의존성 없음)
└── publish_wiki.sh            # 보고서 + TTL을 GitHub Wiki에 동기화

sources/YYYY-MM-DD/
├── search-results.json        # Phase 1
├── index.json                 # Phase 2
├── items/src-XXX.json         # Phase 2
├── entities.json              # Phase 2
├── analysis.md                # Phase 3
└── report-basis.md            # Phase 4

reports/YYYY/MM/
└── YYYY-MM-DD.md              # 최종 일일 이벤트 다이제스트
```

## Agents & Skills

### Main pipeline (onto-osint-report)

| 에이전트 | 참조 스킬 | Phase |
|----------|----------|-------|
| `.claude/agents/osint-collector.md` | `references/search-strategy.md` | 1 |
| `.claude/agents/osint-extractor.md` | `references/extraction-rules.md` | 2 |
| `.claude/agents/osint-reasoner.md` | `references/ontology-reasoning.md` | 3-4 |
| `.claude/agents/osint-reporter.md` | `references/report-format.md` | 5 |

오케스트레이터: `.claude/skills/onto-osint-report/skill.md`

### Shop Watch 보조 하네스 (30일 윈도우 유지 + 누락 보강)

| 에이전트 | 참조 스킬 | Hook Phase |
|----------|----------|-----------|
| `.claude/agents/shop-scout.md` | `shop-watch/references/shop-discovery.md` | 1.5 (병렬) |
| `.claude/agents/shop-curator.md` | `shop-watch/references/shop-roster-mgmt.md` | 3.5 (reasoner 직후) |
| `.claude/agents/shop-coverage-auditor.md` | `shop-watch/references/shop-coverage-rules.md` | 4.5 (reporter 직후) |

오케스트레이터: `.claude/skills/shop-watch/skill.md` (main pipeline이 hook으로 호출)
결정적 스크립트: `scripts/shop_roster_prune.py`, `scripts/shop_roster_backfill.py`
Source of truth: `ontology/shop-roster.json`

## Domain Rules (이 프로젝트 특수 규칙)

- **용성로20 동심원 우선순위 (최상위 규칙)**: 모든 Venue/Shop은 `config.project.geo_focus.center_address`(대전광역시 유성구 용성로 20)로부터의 직선거리를 추정하여 ring(walk/stroll/bike/car) 중 하나로 분류한다. 보고서 첫 섹션은 `ring-walk`(0.5km 이내)에서 시작한다. 거리 추정 근거(주소·동·랜드마크)를 `entities.json`에 기록한다.
- **추적 대상 3종 의무 커버**: 매 사이클마다 (a) 어린이·가족 이벤트, (b) 가게(Shop) — 신규 오픈/프로모션/팝업/원데이클래스, (c) 공공기관(Organization with org_type ∈ {행정복지센터·보건소·복지관·도서관·우체국·경찰서·소방서·주민자치회}) 주최 행사 — 세 카테고리 모두 검색·수집한다. 한 카테고리라도 0건이면 보고서에 "금일 신규 없음" 명시. **shop-coverage-auditor가 매일 검증**한다.
- **신규 오픈 50일 strict cap (Shop Watch 규칙)**: opened_date 기준 50일 이내 가게만 `window_status: active`로 분류되며 매일 보고서의 "신규 오픈 가게·팝업·프로모션" 본문 표에 **의무 노출된다**. **50일 초과 시 즉시 `archived` — recent grace 없음, 보고서 노출 종료.** 팝업의 경우 `popup_close_date`가 윈도우 만료일을 대체한다. 50일 이전 오픈 가게는 manual_seed로 제보되어도 `resolved_not_new`로 분류되고 active_shops에 등록되지 않는다. lifecycle은 `ontology/shop-roster.json`이 source of truth이며 `scripts/shop_roster_prune.py`가 결정적으로 윈도우 전이를 처리한다. 누락된 가게는 `scripts/shop_roster_backfill.py add "<가게명>" --dong <동> --note <사유>` 또는 사용자 대화 제보로 manual_seeds에 등록 → 다음 사이클에서 shop-scout가 우선 조사.
- **Shop 인스턴스 필수 필드**: 가게는 `name, shop_type, dong, address, distance_from_anchor_m, open_hours, kid_friendly, source_url`을 최소 채운다. `is_new=true`(개점 50일 이내) 가게만 보고서 "신규 오픈" 섹션에 노출. shop-curator가 `window_status`, `window_expires_on`, `promotions` 필드를 추가로 동기화한다.
- **공공기관 행사 가산점**: 공공기관(특히 어린이 대상)은 `publicTrustBoost +0.15` 자동 적용 — 신뢰도가 높고 무료/저비용일 가능성이 크기 때문.
- **kid_friendly_score 의무 산출**: 모든 Event 인스턴스는 어린이 친화도 점수(0~1)를 추정해 기록한다. 산정 근거를 `entities.json`에 함께 남긴다.
- **타겟 동 우선**: 1차 타겟 동(용산/전민/관평/문지/신성/도룡)에 위치한 이벤트는 보고서 상단에 우선 배치한다 — 단, ring-walk가 다른 동에 있다면 ring 우선순위가 동 우선순위를 이긴다.
- **사전신청 마감 표시**: 사전신청이 필요한 이벤트는 보고서에서 D-day 표기한다 (`D-3 이내`는 별도 "마감 임박" 섹션).
- **연령 매칭 주의**: 모집 대상이 명확하지 않으면 보수적으로 분류하고 `AgeGroup` 매핑에 신뢰도 0.5 미만으로 기록.
- **유료/무료 명시**: `fee` 필드는 무료/유료 구분과 금액을 함께 기록 (예: "무료", "5,000원/1인").
- **실내·야외 구분**: `indoor_outdoor` 필드는 우천 시 대체 추천에 사용된다 — 누락하지 않는다.
- **SNS 출처 신뢰도**: Instagram 등 SNS 출처는 단독 사용 시 신뢰도 0.6 이하로 기록. 가능하면 Naver Place / 가게 공식 채널과 교차검증.
- **scope.exclude 엄격 적용**: 성인 전용·주류·정치 행사는 자동 제외한다 (`config/osint-config.json` `scope.exclude` 참조).

## Commit Convention
- 보고서 커밋: `report: daily yuseong event update (YYYY-MM-DD)`
- 온톨로지 변경: `ontology: expand schema/instances (YYYY-MM-DD)`
- TTL 스냅샷 (post-step 자동): `ontology: TTL snapshot (YYYY-MM-DD)`
- Wiki 발행 (post-step 자동, wiki repo): `report+kg: YYYY-MM-DD`
- Shop roster 갱신: `shop-watch: roster update (YYYY-MM-DD)` — `ontology/shop-roster.json` 변경 시
- 구조/설정 변경: `chore: 설명`
- `git add sources/ reports/ ontology/`

## Rules
- 출처 URL 없는 이벤트는 보고서에 포함하지 않는다 (구청 공지, 시설 페이지, 언론 기사 중 1개 이상 필수)
- 동일 이벤트가 여러 매체에서 보도된 경우 대표 1개를 본문에, 나머지는 출처 목록에 모두 기재한다
- 보고서가 비어있더라도 파일은 생성한다 ("금일 유성구 일대 어린이·가족 동반 신규 이벤트 특이사항 없음")
- 파이프라인 중간 산출물은 항상 생성한다
- 온톨로지 변경은 반드시 근거(reasoning-log)를 남긴다
- 지식그래프 시각화는 Mermaid 다이어그램으로 보고서에 포함한다
- 매일 GHA 실행 시 KG의 TTL(RDF Turtle) 직렬화를 자동 생성한다 — 일별(`ontology/kg/YYYY-MM-DD.ttl`) + 누적(`ontology/kg/cumulative.ttl`)
- Wiki 발행은 `scripts/publish_wiki.sh`가 결정적으로 수행한다 — Home/Sidebar/Monthly/KG-Index 페이지를 멱등 갱신하고 TTL도 함께 게시
