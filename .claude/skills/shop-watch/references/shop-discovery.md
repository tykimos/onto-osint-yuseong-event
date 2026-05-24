# Shop Discovery — 신규 오픈 가게 탐색 전략

## 목차
- [탐색 채널](#탐색-채널) — Naver Place, Kakao Map, Instagram, 블로그, 일반 검색
- [opened_date 추정 휴리스틱](#opened_date-추정-휴리스틱)
- [거리 추정 휴리스틱](#거리-추정-휴리스틱)
- [kid_friendly 판단 단서](#kid_friendly-판단-단서)
- [출력 스키마](#출력-스키마-shop-candidatesjson)

## 탐색 채널

각 채널은 신뢰도가 다르며, 두 채널 이상 교차할 때 최종 신뢰도가 올라간다. 단일 채널만으로는 0.6을 넘기지 않는다.

### Channel 1 — Naver Place (1차 출처)

신뢰도 기본값 0.7 (공식 등록 정보이므로 높음).

```bash
# 동·키워드 결합 검색 (예: "관평동 신규 오픈")
node $CHELIPED_CLI '[
  {"cmd":"goto","args":["https://map.naver.com/p/search/관평동%20신규%20오픈"]},
  {"cmd":"wait","args":["3000"]},
  {"cmd":"extract","args":["all"]},
  {"cmd":"close"}
]'
```

**탐색 키워드 조합 (config의 dong 목록 × suffix):**
- `<동명> 신규 오픈`, `<동명> 새로 생긴`, `<동명> 그랜드 오픈`
- `<동명> 카페 신규`, `<동명> 식당 오픈`, `<동명> 키즈카페`
- `용성로 오픈`, `용성로 카페`, `용성로 새로`

**추출 단서:**
- 가게 상세 페이지의 "오픈일" 또는 "방문자 리뷰 첫 등록일"을 opened_date 후보로
- "팝업"/"한정"/"오픈 기념" 같은 배지 → is_new 신호
- 영업시간·전화번호 → instances.json 매칭 키

### Channel 2 — Kakao Map (교차검증 출처)

신뢰도 0.6. Naver와 교차하면 0.85 가능.

```bash
node $CHELIPED_CLI '[
  {"cmd":"goto","args":["https://map.kakao.com/?q=관평동%20신규"]},
  {"cmd":"wait","args":["3000"]},
  {"cmd":"extract","args":["all"]},
  {"cmd":"close"}
]'
```

**Naver와 차이점 검증:**
- 영업시간 차이 → 운영 변경 가능성, `last_verified` 날짜만 갱신
- 정기휴무 차이 → Kakao 우선 (보통 더 최신)
- 한 쪽에만 있음 → 단일 채널 신뢰도(0.6)로 기록

### Channel 3 — Instagram 지역 해시태그 (보조 출처, 신선도 우수)

신뢰도 기본 0.5 — SNS 단독 사용 시 0.6 상한. CLAUDE.md의 "SNS 출처 신뢰도" 규칙 적용.

**해시태그 패턴 (config의 dong + suffix):**
- `#용성로` `#용성로카페` `#용성로맛집`
- `#용산동맛집` `#전민동카페` `#관평동키즈카페` `#관평동맛집`
- `#유성구신규` `#유성구가볼만한곳`

```bash
node $CHELIPED_CLI '[
  {"cmd":"goto","args":["https://www.instagram.com/explore/tags/관평동맛집/"]},
  {"cmd":"wait","args":["4000"]},
  {"cmd":"extract","args":["all"]},
  {"cmd":"close"}
]'
```

**opened_date 추정:**
- 가게 공식 계정의 첫 게시일이 가장 강한 단서 → opened_date 후보
- "오픈했어요"/"드디어 오픈"/"오픈 이벤트" 캡션 → 게시일 ± 14일을 opened_date 범위로

### Channel 4 — 네이버 블로그 첫 후기 (보조)

신뢰도 0.5. 후기 글의 작성일이 강한 신호.

**검색 패턴:**
```
"엉클부대찌개" "관평동" site:blog.naver.com
"관평동" "오픈" "후기" site:blog.naver.com
```

**추출 단서:**
- "오픈한지 며칠 안 된" / "갓 오픈한" / "그랜드 오픈" 같은 표현 → 작성일 - 7일을 opened_date 후보로
- 동일 가게에 대한 여러 블로그 후기 → 가장 이른 작성일을 opened_date_min, 가장 늦은 작성일을 last_seen으로

### Channel 5 — WebSearch (백업, 누락 보강)

위 채널이 모두 실패하면 일반 WebSearch로 폴백. 신뢰도 0.4 상한.

**키워드:**
- `"<가게명>" "<동명>" 오픈`
- `"<가게명>" 대전 유성구`
- 가게명에 영문이 포함되면 영문 검색도 병행

### Channel 6 — 유성구청 공지 (공식 출처)

가끔 구청 새소식에 신규 오픈/허가 발급이 공지됨. config의 `custom_sites.yuseong-gu`를 사용.

## opened_date 추정 휴리스틱

여러 단서가 충돌하면 **가장 이른 날짜를 채택** (보수적 — 윈도우를 늦게 끝내는 게 누락보다 낫다).

| 단서 | 신뢰도 | 처리 |
|------|--------|------|
| 가게 공식 SNS 첫 게시 + "오픈" 캡션 | 0.85 | opened_date 직접 사용 |
| Naver Place 등록일 | 0.75 | opened_date 후보, 단 등록일이 실제 오픈일보다 늦을 수 있음 |
| 첫 블로그 후기 작성일 - 7일 | 0.6 | 추정 (방문 후 1주 내 작성 가정) |
| "그랜드 오픈" 공지 날짜 | 0.8 | 공지일 = opened_date |
| 정확한 단서 없음 | 0.3 | `opened_date_estimated: true`, first_seen을 임시 사용, 다음 사이클 재조사 |

추정 시 항상 `opened_date_min`과 `opened_date_max` 범위도 함께 기록한다 (windowing의 보수적 처리를 위함).

## 거리 추정 휴리스틱

용성로20(대전광역시 유성구 용성로 20)을 기준으로 직선거리를 추정한다.

| 동 | 용성로20 대비 거리 추정 | 기본 ring |
|----|----------------------|----------|
| 전민동 (테크노밸리 인접) | 0.5~1.5km | ring-stroll/bike |
| 용산동 | 1.5~2.5km | ring-bike |
| 관평동 | 2.0~3.0km | ring-bike |
| 문지동 | 2.5~3.5km | ring-bike/car |
| 신성동 | 3.0~4.5km | ring-car |
| 도룡동 | 3.0~4.0km | ring-car |
| 노은동 | 4.0~6.0km | ring-car |
| 봉명동 (보조) | 4.5~5.5km | ring-car |

**조정 단서:**
- 같은 동 안에서 큰 거리 차이는 도로명·랜드마크로 보정
- "테크노 X로", "엑스포로", "갑동" 같은 키워드는 용성로20 인근일 확률 ↑
- 정확한 주소가 있으면 향후 결정적 거리 계산 스크립트(별도 작업)로 대체 가능

## kid_friendly 판단 단서

| 단서 | 판단 |
|------|------|
| "키즈존" / "키즈카페" / "놀이방" | true |
| "유아 의자 보유" / "수유실" | true |
| "베이비 메뉴" / "어린이 메뉴" | true |
| "노키즈존" / "성인 전용" | false (보고서에서 제외) |
| "주류 전문" / "와인바" / "이자카야" | 보통 false, 가족 동반 어려움 → 신뢰도 0.7 미만이면 제외 |
| 단서 없음 | "unknown" — 보수적으로 false 처리, 다음 사이클 재조사 |

부대찌개·삼겹살 같은 식당은 기본적으로 가족 동반 가능 → `kid_friendly: true`. 다만 영업 시간이 저녁뿐(예: 17:00~02:00)이면 어린이 동반 부적합으로 판단.

## 출력 스키마: shop-candidates.json

```json
{
  "date": "YYYY-MM-DD",
  "collected_at": "ISO8601",
  "manual_seeds_processed": [
    {
      "seed_name": "관평동 엉클부대찌개",
      "found": true,
      "candidate_id": "cand-001"
    }
  ],
  "candidates": [
    {
      "id": "cand-001",
      "name": "엉클부대찌개 관평동점",
      "shop_type": "식당",
      "dong": "관평동",
      "address_estimated": "대전 유성구 테크노로 ...",
      "distance_from_anchor_m_estimated": 2500,
      "ring": "ring-bike",
      "kid_friendly": true,
      "opened_date": "2026-05-15",
      "opened_date_estimated": true,
      "opened_date_min": "2026-05-10",
      "opened_date_max": "2026-05-20",
      "is_new": true,
      "promotions": ["오픈 기념 10% 할인 (~5/31)"],
      "open_hours": "11:00~22:00",
      "phone": "042-...",
      "discovery_channels": ["naver-place", "instagram"],
      "source_urls": [
        "https://map.naver.com/p/entry/place/...",
        "https://www.instagram.com/p/..."
      ],
      "confidence": 0.8,
      "scout_notes": "Naver Place 등록일 2026-05-15. 인스타 첫 게시 5/14 '드디어 오픈' 캡션. 교차 일치.",
      "status": "found"
    },
    {
      "id": "cand-002",
      "name": "허위가게이름",
      "status": "not_found",
      "search_attempts": 1,
      "channels_tried": ["naver-place", "kakao-map", "instagram", "websearch"],
      "scout_notes": "4개 채널에서 0건. 가게명 정확성 재확인 필요."
    }
  ],
  "stats": {
    "total_candidates": 2,
    "found": 1,
    "not_found": 1,
    "manual_seeds_resolved": 1,
    "manual_seeds_unresolved": 0
  }
}
```
