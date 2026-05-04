#!/usr/bin/env python3
"""KG JSON → RDF Turtle 변환기.

매일 GHA 파이프라인이 끝난 뒤 실행되어 다음 두 TTL을 생성한다:
  ontology/kg/<date>.ttl       — 해당 날짜 스냅샷 (new/updated/inferred triples)
  ontology/kg/cumulative.ttl   — 누적 스냅샷 (모든 노드 + 모든 트리플)

설계 원칙:
  - 외부 의존성 없음 (rdflib 미사용) — CI 부팅 시간 단축
  - 한국어 라벨/리터럴은 @ko 언어 태그를 부여
  - 추론 트리플(type=inferred)은 prov:wasDerivedFrom 으로 별도 표기
  - confidence/source_id/note 등 메타데이터는 RDF reification 으로 부착

호출:
  python3 scripts/kg_to_ttl.py <YYYY-MM-DD>            # 일별 + cumulative 둘 다 생성
  python3 scripts/kg_to_ttl.py <YYYY-MM-DD> --cumulative-only
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTO_DIR = ROOT / "ontology"
KG_DIR = ONTO_DIR / "kg"

BASE_NS = "https://github.com/tykimos/onto-osint-yuseong-event/ontology"
PREFIXES = {
    "yse": f"{BASE_NS}#",
    "yseo": f"{BASE_NS}/class#",
    "yser": f"{BASE_NS}/relation#",
    "yseent": f"{BASE_NS}/entity/",
    "yseinf": f"{BASE_NS}/inference/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "prov": "http://www.w3.org/ns/prov#",
    "dct": "http://purl.org/dc/terms/",
}

DATATYPE_PROPERTIES = {
    "name", "label", "address", "phone", "website", "fee", "open_hours",
    "regular_holiday", "menu_highlights", "price_range", "instagram",
    "naver_url", "source_url", "category", "venue_type", "shop_type", "dong",
    "org_type", "registration_url", "indoor_outdoor", "weather_dependency",
    "start_date", "end_date", "start_time", "end_time", "registration_deadline",
    "opened_date", "rationale", "transit", "contact",
}
INTEGER_PROPERTIES = {
    "min_age", "max_age", "capacity", "duration_minutes",
    "distance_from_anchor_m", "mention_count",
}
FLOAT_PROPERTIES = {"kid_friendly_score", "radius_km"}
BOOL_PROPERTIES = {
    "is_primary_target", "registration_required", "kid_friendly", "is_new",
    "kids_zone", "stroller_accessible", "nursing_room", "parking",
}

INVALID_LOCAL_RE = re.compile(r"[^A-Za-z0-9_\-]")


def safe_local(name: str) -> str:
    """엔티티 ID를 Turtle 로컬명으로 안전화."""
    if not name:
        return "_blank"
    cleaned = INVALID_LOCAL_RE.sub("_", str(name))
    if not re.match(r"^[A-Za-z_]", cleaned):
        cleaned = "x_" + cleaned
    return cleaned


def escape_literal(value: str) -> str:
    s = str(value).replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return s


def fmt_literal(prop: str, value) -> str:
    """타입 추론하여 Turtle 리터럴로 직렬화."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int,)) and prop in INTEGER_PROPERTIES:
        return f'"{value}"^^xsd:integer'
    if isinstance(value, (float,)) and prop in FLOAT_PROPERTIES:
        return f'"{value}"^^xsd:decimal'
    if isinstance(value, (int, float)):
        return f'"{value}"^^xsd:decimal'
    if prop in BOOL_PROPERTIES and isinstance(value, str):
        if value.lower() in ("true", "false"):
            return value.lower()
    if prop in {"start_date", "end_date", "registration_deadline", "opened_date", "first_seen", "last_seen"}:
        if isinstance(value, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            return f'"{value}"^^xsd:date'
    return f'"{escape_literal(value)}"@ko'


def write_prefixes(out: list[str]) -> None:
    out.append(f"@base <{BASE_NS}/> .")
    for p, uri in PREFIXES.items():
        out.append(f"@prefix {p}: <{uri}> .")
    out.append("")


def emit_class_block(out: list[str], schema: dict) -> None:
    out.append("# === Schema: classes ===")
    for top in schema.get("classes", []):
        for cls in [top, *top.get("subclasses", [])]:
            cid = cls.get("id")
            if not cid:
                continue
            out.append(f"yseo:{safe_local(cid)} a owl:Class ;")
            label = cls.get("label", cid)
            out.append(f"  rdfs:label \"{escape_literal(label)}\"@ko ;")
            desc = cls.get("description")
            if desc:
                out.append(f"  rdfs:comment \"{escape_literal(desc)}\"@ko ;")
            if cls is not top:
                out.append(f"  rdfs:subClassOf yseo:{safe_local(top.get('id'))} ;")
            out[-1] = out[-1].rstrip(" ;") + " ."
    out.append("")


def emit_relation_block(out: list[str], schema: dict) -> None:
    out.append("# === Schema: relations ===")
    for rel in schema.get("relations", []):
        rid = rel.get("id")
        if not rid:
            continue
        out.append(f"yser:{safe_local(rid)} a owl:ObjectProperty ;")
        out.append(f"  rdfs:label \"{escape_literal(rel.get('label', rid))}\"@ko ;")
        if rel.get("domain"):
            out.append(f"  rdfs:domain yseo:{safe_local(rel['domain'])} ;")
        if rel.get("range"):
            out.append(f"  rdfs:range yseo:{safe_local(rel['range'])} ;")
        out[-1] = out[-1].rstrip(" ;") + " ."
    out.append("")


def emit_entity(out: list[str], ent: dict) -> None:
    eid = ent.get("id")
    etype = ent.get("type", "Entity")
    if not eid:
        return
    out.append(f"yseent:{safe_local(eid)} a yseo:{safe_local(etype)} ;")
    name = ent.get("name") or ent.get("label")
    if name:
        out.append(f"  rdfs:label \"{escape_literal(name)}\"@ko ;")
        out.append(f"  yse:name \"{escape_literal(name)}\"@ko ;")
    for ts_field in ("first_seen", "last_seen"):
        if ent.get(ts_field):
            out.append(f"  yse:{ts_field} {fmt_literal(ts_field, ent[ts_field])} ;")
    if ent.get("mention_count") is not None:
        out.append(f"  yse:mention_count {fmt_literal('mention_count', ent['mention_count'])} ;")
    for k, v in (ent.get("properties") or {}).items():
        if v is None or v == "":
            continue
        if k in DATATYPE_PROPERTIES or k in INTEGER_PROPERTIES or k in FLOAT_PROPERTIES or k in BOOL_PROPERTIES:
            out.append(f"  yse:{safe_local(k)} {fmt_literal(k, v)} ;")
        elif isinstance(v, (str, int, float, bool)):
            out.append(f"  yse:{safe_local(k)} {fmt_literal(k, v)} ;")
    out[-1] = out[-1].rstrip(" ;") + " ."


def emit_triple(out: list[str], t: dict, idx: int, source_date: str | None) -> None:
    s = t.get("subject")
    p = t.get("predicate")
    o = t.get("object")
    if not (s and p and o):
        return
    obj_is_literal = isinstance(o, str) and (o.startswith("+") or o.startswith("-"))
    if obj_is_literal:
        obj_str = f'"{escape_literal(o)}"'
    else:
        obj_str = f"yseent:{safe_local(o)}"
    out.append(f"yseent:{safe_local(s)} yser:{safe_local(p)} {obj_str} .")

    stmt_id = f"stmt-{source_date or 'cum'}-{idx:04d}"
    out.append(f"yseinf:{safe_local(stmt_id)} a rdf:Statement ;")
    out.append(f"  rdf:subject yseent:{safe_local(s)} ;")
    out.append(f"  rdf:predicate yser:{safe_local(p)} ;")
    if obj_is_literal:
        out.append(f"  rdf:object \"{escape_literal(o)}\" ;")
    else:
        out.append(f"  rdf:object yseent:{safe_local(o)} ;")
    if t.get("confidence") is not None:
        out.append(f"  yse:confidence \"{t['confidence']}\"^^xsd:decimal ;")
    if t.get("type"):
        out.append(f"  yse:assertionType \"{escape_literal(t['type'])}\" ;")
    if t.get("rule"):
        out.append(f"  prov:wasDerivedFrom \"{escape_literal(t['rule'])}\" ;")
    if t.get("source_id"):
        out.append(f"  dct:source \"{escape_literal(t['source_id'])}\" ;")
    if t.get("date"):
        out.append(f"  dct:date {fmt_literal('start_date', t['date'])} ;")
    if t.get("note"):
        out.append(f"  rdfs:comment \"{escape_literal(t['note'])}\"@ko ;")
    out[-1] = out[-1].rstrip(" ;") + " ."


def _coerce_triple_list(value) -> list:
    """LLM이 카운트(int)/None/list 어느 형태로든 채울 수 있어 list만 통과시킨다."""
    return value if isinstance(value, list) else []


def build_daily_ttl(date_str: str, schema: dict, instances: dict, kg_day: dict) -> str:
    out: list[str] = []
    write_prefixes(out)
    out.append(f"# Onto-OSINT-Yuseong-Event — daily KG snapshot ({date_str})")
    out.append(f"<#snapshot-{date_str}> a prov:Entity ;")
    out.append(f"  dct:date {fmt_literal('start_date', date_str)} ;")
    stats = kg_day.get("stats") or {}
    if isinstance(stats, dict) and stats:
        out.append(f"  yse:new_nodes \"{stats.get('new_nodes', 0)}\"^^xsd:integer ;")
        out.append(f"  yse:new_edges \"{stats.get('new_edges', 0)}\"^^xsd:integer ;")
        out.append(f"  yse:inferred_edges \"{stats.get('inferred_edges', 0)}\"^^xsd:integer ;")
    out[-1] = out[-1].rstrip(" ;") + " ."
    out.append("")

    referenced: set[str] = set()
    triple_groups = [
        ("new_triples", _coerce_triple_list(kg_day.get("new_triples"))),
        ("updated_triples", _coerce_triple_list(kg_day.get("updated_triples"))),
        ("inferred_triples", _coerce_triple_list(kg_day.get("inferred_triples"))),
    ]
    # 대체 스키마: triples 그룹이 비어있고 edges만 채워진 경우
    if not any(g for _, g in triple_groups):
        edges = _coerce_triple_list(kg_day.get("edges"))
        if edges:
            inferred = [e for e in edges if e.get("type") == "inferred"]
            explicit = [e for e in edges if e.get("type") != "inferred"]
            triple_groups = [("new_triples", explicit), ("inferred_triples", inferred)]

    counter = 0
    for group_name, triples in triple_groups:
        if not triples:
            continue
        out.append(f"# --- {group_name} ({len(triples)}) ---")
        for t in triples:
            counter += 1
            emit_triple(out, t, counter, date_str)
            referenced.add(t.get("subject"))
            obj = t.get("object")
            if isinstance(obj, str) and not (obj.startswith("+") or obj.startswith("-")):
                referenced.add(obj)
        out.append("")

    by_id = {e["id"]: e for e in instances.get("entities", []) if e.get("id")}
    daily_nodes = {n["id"]: n for n in (kg_day.get("nodes") or []) if isinstance(n, dict) and n.get("id")}

    if referenced or daily_nodes:
        out.append(f"# --- referenced entities ---")
        for eid in sorted(referenced | daily_nodes.keys()):
            ent = by_id.get(eid)
            if ent:
                emit_entity(out, ent)
            elif eid in daily_nodes:
                n = daily_nodes[eid]
                stub = {"id": eid, "type": n.get("type"), "name": n.get("label") or n.get("name")}
                emit_entity(out, stub)
        out.append("")

    return "\n".join(out) + "\n"


def build_cumulative_ttl(schema: dict, instances: dict, kg_cum: dict) -> str:
    out: list[str] = []
    write_prefixes(out)
    out.append("# Onto-OSINT-Yuseong-Event — cumulative KG")
    last_updated = kg_cum.get("last_updated") or instances.get("last_updated")
    if last_updated:
        out.append(f"<#cumulative> a prov:Entity ;")
        out.append(f"  dct:modified {fmt_literal('start_date', last_updated)} .")
        out.append("")

    emit_class_block(out, schema)
    emit_relation_block(out, schema)

    nodes = kg_cum.get("nodes") or []
    by_id = {e["id"]: e for e in instances.get("entities", []) if e.get("id")}
    out.append(f"# === Entities ({len(by_id)}) ===")
    for ent in instances.get("entities", []):
        emit_entity(out, ent)
    for n in nodes:
        nid = n.get("id")
        if nid and nid not in by_id:
            stub = {"id": nid, "type": n.get("type"), "name": n.get("label")}
            emit_entity(out, stub)
    out.append("")

    triples = kg_cum.get("triples") or []
    out.append(f"# === Triples ({len(triples)}) ===")
    for i, t in enumerate(triples, start=1):
        emit_triple(out, t, i, None)
    out.append("")

    return "\n".join(out) + "\n"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[kg_to_ttl] WARN: {path} JSON decode error: {exc}", file=sys.stderr)
        return {}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: kg_to_ttl.py <YYYY-MM-DD> [--cumulative-only]", file=sys.stderr)
        return 1
    date_str = argv[1]
    cumulative_only = "--cumulative-only" in argv

    schema = load_json(ONTO_DIR / "schema.json")
    instances = load_json(ONTO_DIR / "instances.json")
    kg_cum = load_json(KG_DIR / "cumulative.json")

    KG_DIR.mkdir(parents=True, exist_ok=True)

    if not cumulative_only:
        kg_day = load_json(KG_DIR / f"{date_str}.json")
        if not kg_day:
            print(f"[kg_to_ttl] No daily KG at {KG_DIR / f'{date_str}.json'} — skipping daily TTL.")
        else:
            ttl_day = build_daily_ttl(date_str, schema, instances, kg_day)
            (KG_DIR / f"{date_str}.ttl").write_text(ttl_day, encoding="utf-8")
            print(f"[kg_to_ttl] wrote {KG_DIR / f'{date_str}.ttl'}")

    ttl_cum = build_cumulative_ttl(schema, instances, kg_cum)
    (KG_DIR / "cumulative.ttl").write_text(ttl_cum, encoding="utf-8")
    print(f"[kg_to_ttl] wrote {KG_DIR / 'cumulative.ttl'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
