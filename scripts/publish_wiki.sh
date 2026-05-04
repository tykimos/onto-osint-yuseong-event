#!/usr/bin/env bash
# publish_wiki.sh — 일별 보고서 + KG TTL을 GitHub Wiki로 동기화한다.
#
# 사용법:
#   GITHUB_TOKEN=... GITHUB_REPOSITORY=owner/repo \
#     bash scripts/publish_wiki.sh <YYYY-MM-DD>
#
# 동작:
#   1. <repo>.wiki.git 을 /tmp/wiki 로 clone (없으면 init)
#   2. reports/YYYY/MM/<date>.md → /tmp/wiki/<date>.md  (frontmatter 제거)
#   3. ontology/kg/<date>.ttl → /tmp/wiki/kg/<date>.ttl
#      ontology/kg/cumulative.ttl → /tmp/wiki/kg/cumulative.ttl
#   4. Home.md (최신 14일 링크) / _Sidebar.md / Monthly-YYYY-MM.md / KG-Index.md 갱신
#   5. commit & push
#
# 멱등: 같은 날짜를 다시 실행해도 새 콘텐츠로 덮어쓰고 사이드바 중복은 dedup.
set -euo pipefail

DATE="${1:-}"
if [[ -z "$DATE" ]]; then
  echo "Usage: $0 <YYYY-MM-DD>" >&2
  exit 1
fi
if [[ ! "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Invalid date: $DATE" >&2
  exit 1
fi

YEAR="${DATE%%-*}"
MONTH="$(echo "$DATE" | cut -d- -f2)"
REPO="${GITHUB_REPOSITORY:-}"
TOKEN="${GITHUB_TOKEN:-}"
if [[ -z "$REPO" || -z "$TOKEN" ]]; then
  echo "GITHUB_REPOSITORY and GITHUB_TOKEN must be set" >&2
  exit 1
fi

WIKI_DIR="/tmp/wiki"
REPORT_SRC="reports/${YEAR}/${MONTH}/${DATE}.md"
DAILY_TTL_SRC="ontology/kg/${DATE}.ttl"
CUM_TTL_SRC="ontology/kg/cumulative.ttl"

if [[ ! -f "$REPORT_SRC" ]]; then
  echo "[publish_wiki] report not found: $REPORT_SRC — skipping" >&2
  exit 0
fi

rm -rf "$WIKI_DIR"
WIKI_URL="https://x-access-token:${TOKEN}@github.com/${REPO}.wiki.git"
if ! git clone --quiet "$WIKI_URL" "$WIKI_DIR" 2>/tmp/wiki-clone.err; then
  echo "[publish_wiki] wiki clone failed; bootstrapping fresh wiki:" >&2
  cat /tmp/wiki-clone.err >&2 || true
  mkdir -p "$WIKI_DIR"
  (cd "$WIKI_DIR" && git init -q && git remote add origin "$WIKI_URL")
fi

cd "$WIKI_DIR"
git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

# 1. report → wiki page (frontmatter strip)
mkdir -p kg
awk 'BEGIN{f=0} NR==1 && /^---$/ {f=1; next} f==1 && /^---$/ {f=0; next} f==0 {print}' \
  "$OLDPWD/$REPORT_SRC" > "${DATE}.md"

# 2. TTL files
if [[ -f "$OLDPWD/$DAILY_TTL_SRC" ]]; then
  cp "$OLDPWD/$DAILY_TTL_SRC" "kg/${DATE}.ttl"
fi
if [[ -f "$OLDPWD/$CUM_TTL_SRC" ]]; then
  cp "$OLDPWD/$CUM_TTL_SRC" "kg/cumulative.ttl"
fi

# 3. Home.md (최신 14일 링크 + KG 인덱스 링크)
cat > Home.md <<EOF
# Onto-OSINT-Yuseong-Event Wiki

대전 유성구 어린이·가족 이벤트 OSINT 일일 보고서 모음.

- 최신 보고서: [[${DATE}]]
- 지식그래프 인덱스: [[KG-Index]]
- 이번 달 인덱스: [[Monthly-${YEAR}-${MONTH}]]

## 최근 14일

EOF

ls -1 [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md 2>/dev/null \
  | sort -r | head -14 \
  | while read -r f; do
      d="${f%.md}"
      echo "- [[${d}]]" >> Home.md
    done

# 4. _Sidebar.md (최근 14일)
{
  echo "**Onto-OSINT-Yuseong**"
  echo
  echo "- [[Home]]"
  echo "- [[KG-Index]]"
  echo
  echo "**최근 보고서**"
  echo
  ls -1 [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md 2>/dev/null \
    | sort -r | head -14 \
    | while read -r f; do
        d="${f%.md}"
        echo "- [[${d}]]"
      done
} > _Sidebar.md

# 5. Monthly-YYYY-MM.md
MONTHLY="Monthly-${YEAR}-${MONTH}.md"
{
  echo "# ${YEAR}년 ${MONTH}월 보고서"
  echo
  ls -1 "${YEAR}-${MONTH}"-[0-9][0-9].md 2>/dev/null \
    | sort \
    | while read -r f; do
        d="${f%.md}"
        echo "- [[${d}]]"
      done
} > "$MONTHLY"

# 6. KG-Index.md
{
  echo "# 지식그래프 (Turtle/RDF)"
  echo
  echo "유성구 이벤트 온톨로지의 RDF Turtle 직렬화."
  echo
  echo "## 누적 그래프"
  echo
  echo "- [cumulative.ttl](kg/cumulative.ttl) — 전체 누적 KG (스키마 + 인스턴스 + 전체 트리플)"
  echo
  echo "## 일별 스냅샷"
  echo
  if compgen -G "kg/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].ttl" > /dev/null; then
    ls -1 kg/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].ttl 2>/dev/null \
      | sort -r \
      | while read -r f; do
          d="$(basename "$f" .ttl)"
          echo "- [${d}.ttl](${f}) — ${d} 일자 신규/업데이트/추론 트리플"
        done
  fi
} > KG-Index.md

# 7. commit & push
git add -A
if git diff --cached --quiet; then
  echo "[publish_wiki] no changes to commit"
else
  git commit -q -m "report+kg: ${DATE}"
  if ! git push -q origin HEAD:master 2>/tmp/wiki-push.err; then
    if grep -q "src refspec" /tmp/wiki-push.err; then
      git push -q -u origin HEAD:master
    else
      cat /tmp/wiki-push.err >&2
      exit 1
    fi
  fi
  echo "[publish_wiki] pushed wiki for ${DATE}"
fi
