#!/usr/bin/env python3
"""shop_roster_prune.py — 결정적 윈도우 만료 처리

shop-roster.json의 active_shops / recent_shops에서 만료 조건을 충족하는
가게를 다음 단계로 이동시킨다. LLM이 처리하면 변동성이 생기므로 결정적
스크립트로 분리한다.

사용:
    python3 scripts/shop_roster_prune.py [YYYY-MM-DD]

기본 동작:
- active_shops: window_expires_on < target_date → recent_shops로 이동
- recent_shops: window_started_on + recent_window_days < target_date → archived_shops로 이동
- suspected_closed: status 진입 후 30일 경과 → archived_shops로 이동
- promotions: valid_until < target_date → 제거 (가게 자체는 유지)

backup:
- 변경 전 shop-roster.json.bak에 백업 저장 (1회만, 가장 최근 상태 보존)
"""

from __future__ import annotations

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROSTER_PATH = Path("ontology/shop-roster.json")
BACKUP_PATH = Path("ontology/shop-roster.json.bak")


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def add_days(d: date, n: int) -> date:
    return d + timedelta(days=n)


def empty_roster() -> dict:
    return {
        "version": "1.0.0",
        "last_updated": date.today().isoformat(),
        "window_days": 50,
        "recent_window_days": 50,
        "_policy": "strict 50일 cap — opened_date+50일 경과 시 즉시 archived",
        "active_shops": [],
        "recent_shops": [],
        "archived_shops": [],
        "suspected_closed_shops": [],
        "manual_seeds": [],
    }


def load_roster() -> dict:
    if not ROSTER_PATH.exists():
        roster = empty_roster()
        ROSTER_PATH.parent.mkdir(parents=True, exist_ok=True)
        ROSTER_PATH.write_text(
            json.dumps(roster, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return roster
    return json.loads(ROSTER_PATH.read_text(encoding="utf-8"))


def save_roster(roster: dict) -> None:
    BACKUP_PATH.write_text(
        ROSTER_PATH.read_text(encoding="utf-8") if ROSTER_PATH.exists() else "",
        encoding="utf-8",
    )
    ROSTER_PATH.write_text(
        json.dumps(roster, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def prune(roster: dict, target: date) -> dict:
    window_days = int(roster.get("window_days", 50))
    recent_window_days = int(roster.get("recent_window_days", 50))
    # strict 50일 정책: window_days == recent_window_days면 active → archived 직행 (recent grace 없음)
    strict_cap = recent_window_days <= window_days

    moved_to_recent: list[dict] = []
    moved_to_archived: list[dict] = []

    # active → (archived if strict_cap else recent)
    new_active: list[dict] = []
    for shop in roster.get("active_shops", []):
        expires = parse_date(shop.get("window_expires_on"))
        started = parse_date(shop.get("window_started_on")) or parse_date(
            shop.get("opened_date")
        )
        if expires is None and started is not None:
            expires = add_days(started, window_days)
            shop["window_expires_on"] = expires.isoformat()
        if expires is not None and target > expires:
            if strict_cap:
                shop["window_status"] = "archived"
                shop["archived_on"] = target.isoformat()
                shop["archive_reason"] = "strict_50day_cap_expired"
                moved_to_archived.append(shop)
            else:
                shop["window_status"] = "recent"
                shop["recent_started_on"] = target.isoformat()
                moved_to_recent.append(shop)
        else:
            new_active.append(shop)
    roster["active_shops"] = new_active

    # recent → archived (only runs when strict_cap == false)
    new_recent: list[dict] = []
    for shop in roster.get("recent_shops", []) + moved_to_recent:
        started = parse_date(shop.get("window_started_on")) or parse_date(
            shop.get("opened_date")
        )
        if started is None:
            new_recent.append(shop)
            continue
        archive_threshold = add_days(started, recent_window_days)
        if target > archive_threshold:
            shop["window_status"] = "archived"
            shop["archived_on"] = target.isoformat()
            moved_to_archived.append(shop)
        else:
            new_recent.append(shop)
    roster["recent_shops"] = new_recent

    # suspected_closed → archived (after 30 days)
    new_suspected: list[dict] = []
    for shop in roster.get("suspected_closed_shops", []):
        flagged_on = parse_date(shop.get("suspected_closed_on"))
        if flagged_on is None:
            new_suspected.append(shop)
            continue
        if target > add_days(flagged_on, 30):
            shop["window_status"] = "archived"
            shop["archived_on"] = target.isoformat()
            shop["archive_reason"] = "suspected_closed_unverified"
            moved_to_archived.append(shop)
        else:
            new_suspected.append(shop)
    roster["suspected_closed_shops"] = new_suspected

    roster["archived_shops"] = roster.get("archived_shops", []) + moved_to_archived

    # Expire promotions in-place
    for shop in roster["active_shops"] + roster["recent_shops"]:
        valid_promos: list[dict] = []
        for promo in shop.get("promotions", []) or []:
            valid_until = parse_date(promo.get("valid_until"))
            if valid_until is None or target <= valid_until:
                valid_promos.append(promo)
        shop["promotions"] = valid_promos

    roster["last_updated"] = target.isoformat()
    roster["_last_prune"] = {
        "ran_on": datetime.now(timezone.utc).isoformat(),
        "target_date": target.isoformat(),
        "moved_to_recent": [s.get("id") for s in moved_to_recent],
        "moved_to_archived": [s.get("id") for s in moved_to_archived],
    }
    return roster


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        target = parse_date(argv[1])
        if target is None:
            print(f"invalid date: {argv[1]}", file=sys.stderr)
            return 2
    else:
        target = date.today()

    roster = load_roster()
    roster = prune(roster, target)
    save_roster(roster)

    last = roster.get("_last_prune", {})
    print(
        "prune complete:",
        json.dumps(
            {
                "target_date": last.get("target_date"),
                "moved_to_recent": len(last.get("moved_to_recent", [])),
                "moved_to_archived": len(last.get("moved_to_archived", [])),
                "active_remaining": len(roster.get("active_shops", [])),
                "recent_remaining": len(roster.get("recent_shops", [])),
            },
            ensure_ascii=False,
        ),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
