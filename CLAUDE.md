# Onto-OSINT-Yuseong-Event — 유성구 어린이·가족 이벤트 일일 모니터

## Project Purpose
대전 유성구(특히 용산동·전민동·관평동·문지동·신성동·도룡동 일대)에서 매일 새로 공지되거나 진행되는 어린이·가족 동반 이벤트를 자동으로 수집·구조화·요약한다.
`onto-osint`의 6단계 파이프라인(수집→추출→온톨로지→그래프→보고서→발행)을 그대로 사용하되, 도메인 특화 설정(`config/osint-config.json`)으로 지역 행사용 온톨로지를 시드한다.

## Domain Snapshot

| 항목 | 값 |
|------|-----|
| 핵심 지역 | 유성구 — 용산동, 전민동, 관평동, 문지동, 신성동, 도룡동 (1차 타겟) |
| 보조 지역 | 노은동, 어은동, 구암동, 지족동, 반석동 (인접 — 가족 이동 반경) |
| 핵심 대상 | 영유아 / 유아 / 초등저학년 / 초등고학년 / 가족 전연령 |
| 핵심 출처 | 유성구청, 유성구 도서관(관평·노은·진잠·전민), 국립중앙과학관, 대전시민천문대, 유성구 평생학습관·가족센터, 대전관광공사 |
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
│   ├── YYYY-MM-DD.json        # 일별 KG 스냅샷
│   └── cumulative.json        # 누적 KG
└── reasoning-log.md           # 추론 로그

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

| 에이전트 | 참조 스킬 | Phase |
|----------|----------|-------|
| `.claude/agents/osint-collector.md` | `references/search-strategy.md` | 1 |
| `.claude/agents/osint-extractor.md` | `references/extraction-rules.md` | 2 |
| `.claude/agents/osint-reasoner.md` | `references/ontology-reasoning.md` | 3-4 |
| `.claude/agents/osint-reporter.md` | `references/report-format.md` | 5 |

오케스트레이터: `.claude/skills/onto-osint-report/skill.md`

## Domain Rules (이 프로젝트 특수 규칙)

- **kid_friendly_score 의무 산출**: 모든 Event 인스턴스는 어린이 친화도 점수(0~1)를 추정해 기록한다. 산정 근거를 `entities.json`에 함께 남긴다.
- **타겟 동 우선**: 1차 타겟 동(용산/전민/관평/문지/신성/도룡)에 위치한 이벤트는 보고서 상단에 우선 배치한다.
- **사전신청 마감 표시**: 사전신청이 필요한 이벤트는 보고서에서 D-day 표기한다 (`D-3 이내`는 별도 "마감 임박" 섹션).
- **연령 매칭 주의**: 모집 대상이 명확하지 않으면 보수적으로 분류하고 `AgeGroup` 매핑에 신뢰도 0.5 미만으로 기록.
- **유료/무료 명시**: `fee` 필드는 무료/유료 구분과 금액을 함께 기록 (예: "무료", "5,000원/1인").
- **실내·야외 구분**: `indoor_outdoor` 필드는 우천 시 대체 추천에 사용된다 — 누락하지 않는다.
- **scope.exclude 엄격 적용**: 성인 전용·주류·정치 행사는 자동 제외한다 (`config/osint-config.json` `scope.exclude` 참조).

## Commit Convention
- 보고서 커밋: `report: daily yuseong event update (YYYY-MM-DD)`
- 온톨로지 변경: `ontology: expand schema/instances (YYYY-MM-DD)`
- 구조/설정 변경: `chore: 설명`
- `git add sources/ reports/ ontology/`

## Rules
- 출처 URL 없는 이벤트는 보고서에 포함하지 않는다 (구청 공지, 시설 페이지, 언론 기사 중 1개 이상 필수)
- 동일 이벤트가 여러 매체에서 보도된 경우 대표 1개를 본문에, 나머지는 출처 목록에 모두 기재한다
- 보고서가 비어있더라도 파일은 생성한다 ("금일 유성구 일대 어린이·가족 동반 신규 이벤트 특이사항 없음")
- 파이프라인 중간 산출물은 항상 생성한다
- 온톨로지 변경은 반드시 근거(reasoning-log)를 남긴다
- 지식그래프 시각화는 Mermaid 다이어그램으로 보고서에 포함한다
