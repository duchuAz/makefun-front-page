#!/usr/bin/env python3
"""Resolve every story line to a real wire item, so no time on the page is invented.

Each entry in stories.json names a substring of a headline that a feed actually carried on
20 November 2026. This script finds the earliest item carrying it, takes that item's UTC
publication time, and refuses to run if any line matches nothing. Output: resolved.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "day20final.json")


def main() -> int:
    feed = json.load(open(DATA, encoding="utf-8"))
    feed.sort(key=lambda r: r["utc"])
    spec = json.load(open(os.path.join(HERE, "stories.json"), encoding="utf-8"))

    misses = []

    def resolve(entry):
        q = entry["q"]
        hits = [r for r in feed if q.lower() in r["title"].lower()]
        if not hits:
            misses.append(q)
            return None
        first = hits[0]
        out = dict(entry)
        out["hm"] = first["hm"]
        out["utc"] = first["utc"]
        out["feed"] = first["feed"]
        out["link"] = first["link"]
        out["matched"] = first["title"]
        out["n_reports"] = len(hits)
        return out

    leads = [resolve(e) for e in spec["leads"]]
    items = [resolve(e) for e in spec["items"]]
    if misses:
        print("UNRESOLVED (fix the q string):", file=sys.stderr)
        for m in misses:
            print("  ", m, file=sys.stderr)
        return 1

    everything = leads + items
    # Every line must be inside the UTC day, or the page's claim is false.
    outside = [e for e in everything if not e["utc"].startswith("2026-11-20")]
    if outside:
        print("OUTSIDE THE DAY:", [(e["q"], e["utc"]) for e in outside], file=sys.stderr)
        return 1

    items.sort(key=lambda e: e["utc"])   # the grid is a clock; the leads are ranked by weight

    regions = {}
    for e in items:
        regions[e["region"]] = regions.get(e["region"], 0) + 1
    places = {e["place"].split(",")[0] for e in items}

    resolved = {
        "day": spec["day"],
        "day_short": spec["day_short"],
        "leads": leads,
        "items": items,
        "n_items": len(items),
        "n_total": len(items) + len(leads),
        "n_regions": len(regions),
        "n_places": len(places),
        "regions": regions,
        "first_hm": items[0]["hm"],
        "last_hm": items[-1]["hm"],
    }
    json.dump(resolved, open(os.path.join(HERE, "resolved.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    print(f"resolved {len(items)} grid items + {len(leads)} leads = {resolved['n_total']} stories")
    print(f"day span: {resolved['first_hm']} -> {resolved['last_hm']} UTC")
    print(f"regions ({resolved['n_regions']}): {regions}")
    print(f"places: {resolved['n_places']}")
    print()
    for e in leads:
        print(f"  LEAD {e['hm']} {e['place']:<20} {e['head'][:70]}")
    for e in items:
        print(f"  {e['hm']} {e['place']:<20} {e['label'][:64]:<64} [{e['region']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
