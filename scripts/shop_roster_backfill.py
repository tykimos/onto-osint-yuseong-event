#!/usr/bin/env python3
"""shop_roster_backfill.py — 누락 가게 manual_seed 등록 도우미

사용자가 발견한 누락 가게(예: "관평동 엉클부대찌개")를 shop-roster.json의
manual_seeds에 즉시 추가한다. 이후 다음 파이프라인 사이클에서 shop-scout가
이 시드를 우선 조사하여 active_shops로 승격한다.

사용:
    # 시드 추가
    python3 scripts/shop_roster_backfill.py add "엉클부대찌개" --dong 관평동 \\
        --note "사용자 5/24 제보"

    # 시드 목록 보기
    python3 scripts/shop_roster_backfill.py list

    # 처리 안 된 시드 제거
    python3 scripts/shop_roster_backfill.py remove "엉클부대찌개"

    # 강제로 resolved 처리 (수동으로 가게 정보를 다 안다면)
    python3 scripts/shop_roster_backfill.py resolve "엉클부대찌개" \\
        --shop-id shop-099 --opened-date 2026-05-15
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


ROSTER_PATH = Path("ontology/shop-roster.json")


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
        ROSTER_PATH.parent.mkdir(parents=True, exist_ok=True)
        roster = empty_roster()
        ROSTER_PATH.write_text(
            json.dumps(roster, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return roster
    return json.loads(ROSTER_PATH.read_text(encoding="utf-8"))


def save_roster(roster: dict) -> None:
    roster["last_updated"] = date.today().isoformat()
    ROSTER_PATH.write_text(
        json.dumps(roster, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def cmd_add(args: argparse.Namespace) -> int:
    roster = load_roster()
    seeds = roster.setdefault("manual_seeds", [])
    name = args.name.strip()

    for s in seeds:
        if s.get("seed_name", "").strip() == name and s.get("status") == "pending":
            print(f"이미 등록된 pending 시드: {name}", file=sys.stderr)
            return 1

    seed = {
        "seed_name": name,
        "dong_hint": args.dong,
        "shop_type_hint": args.shop_type,
        "added_on": date.today().isoformat(),
        "added_by": args.added_by,
        "note": args.note or "",
        "status": "pending",
        "search_attempts": 0,
        "resolved_to": None,
    }
    seeds.append(seed)
    save_roster(roster)
    print(f"manual_seed 등록 완료: {name} (dong={args.dong})")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    roster = load_roster()
    seeds = roster.get("manual_seeds", [])
    if not seeds:
        print("등록된 manual_seeds가 없습니다.")
        return 0
    print(f"{'STATUS':<10} {'ATTEMPTS':<8} {'ADDED':<12} {'NAME'}")
    for s in seeds:
        print(
            f"{s.get('status','?'):<10} {s.get('search_attempts',0):<8} "
            f"{s.get('added_on',''):<12} {s.get('seed_name','')}"
        )
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    roster = load_roster()
    seeds = roster.get("manual_seeds", [])
    name = args.name.strip()
    new_seeds = [s for s in seeds if s.get("seed_name", "").strip() != name]
    if len(new_seeds) == len(seeds):
        print(f"제거할 시드 없음: {name}", file=sys.stderr)
        return 1
    roster["manual_seeds"] = new_seeds
    save_roster(roster)
    print(f"시드 제거: {name}")
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    roster = load_roster()
    seeds = roster.get("manual_seeds", [])
    name = args.name.strip()

    opened = datetime.strptime(args.opened_date, "%Y-%m-%d").date()
    window_days = int(roster.get("window_days", 50))
    expires = opened + timedelta(days=window_days)

    shop = {
        "id": args.shop_id,
        "name": name,
        "shop_type": args.shop_type or "기타",
        "dong": args.dong or "",
        "address": args.address or "",
        "distance_from_anchor_m": args.distance_m or None,
        "ring": args.ring or "",
        "kid_friendly": args.kid_friendly,
        "opened_date": opened.isoformat(),
        "opened_date_estimated": False,
        "window_status": "active",
        "window_started_on": opened.isoformat(),
        "window_expires_on": expires.isoformat(),
        "promotions": [],
        "discovery_channels": ["manual_resolve"],
        "source_urls": args.source_url or [],
        "confidence": 0.95,
        "first_seen": date.today().isoformat(),
        "last_verified": date.today().isoformat(),
        "notes": "수동 resolve",
    }
    roster.setdefault("active_shops", []).append(shop)

    # remove from manual_seeds (or mark resolved)
    remaining: list[dict] = []
    for s in seeds:
        if s.get("seed_name", "").strip() == name:
            s["status"] = "resolved"
            s["resolved_to"] = args.shop_id
            s["resolved_on"] = date.today().isoformat()
            # 보존 (이력 추적). 원한다면 제거 가능.
            remaining.append(s)
        else:
            remaining.append(s)
    roster["manual_seeds"] = remaining
    save_roster(roster)
    print(f"resolve 완료: {name} → {args.shop_id} (윈도우 만료 {expires.isoformat()})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="manual_seed 추가")
    p_add.add_argument("name")
    p_add.add_argument("--dong", default="", help="동 힌트 (예: 관평동)")
    p_add.add_argument("--shop-type", default="", help="가게 유형 힌트")
    p_add.add_argument("--note", default="", help="제보 메모")
    p_add.add_argument("--added-by", default="user")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="manual_seeds 목록 보기")
    p_list.set_defaults(func=cmd_list)

    p_rm = sub.add_parser("remove", help="manual_seed 제거")
    p_rm.add_argument("name")
    p_rm.set_defaults(func=cmd_remove)

    p_res = sub.add_parser("resolve", help="수동으로 active_shops에 추가")
    p_res.add_argument("name")
    p_res.add_argument("--shop-id", required=True)
    p_res.add_argument("--opened-date", required=True, help="YYYY-MM-DD")
    p_res.add_argument("--dong", default="")
    p_res.add_argument("--address", default="")
    p_res.add_argument("--shop-type", default="")
    p_res.add_argument("--ring", default="")
    p_res.add_argument("--distance-m", type=int, default=None)
    p_res.add_argument("--kid-friendly", action="store_true")
    p_res.add_argument("--source-url", action="append", default=[])
    p_res.set_defaults(func=cmd_resolve)

    return p


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv[1:])
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
