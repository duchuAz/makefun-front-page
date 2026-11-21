#!/usr/bin/env python3
"""Write SOURCES.md: one line per story on the page, with the wire copy it came from.

Every headline on entry.png is a substring of a title a feed actually carried on 20 November
2026. This file records the match, the UTC time the feed stamped it, and the link, so any
claim on the page can be traced back to its filing.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..", "repo")


def main():
    r = json.load(open(os.path.join(HERE, "resolved.json"), encoding="utf-8"))
    out = []
    w = out.append

    w("# Sources")
    w("")
    w("Every line on the page is a story a wire service filed on **20 November 2026**. This file")
    w("lists all of them: the place, the UTC time the filing carried, the headline as the wire")
    w("published it, and the link. The times are the ones the feeds stamp, converted to UTC;")
    w("they are what the page prints beside each story.")
    w("")
    w(f"- {r['n_total']} stories: {len(r['leads'])} above the fold and {r['n_items']} in the grid")
    w(f"- filed from {r['first_hm']} to {r['last_hm']} UTC on 20 November 2026")
    w(f"- {r['n_places']} places, {len(set(e['region'] for e in r['items']) - {'SPACE'})} regions")
    w("")
    w("## Above the fold")
    w("")
    for lead in r["leads"]:
        w(f"### {lead['place']} — {lead['hm']} UTC")
        w("")
        w(f"> {lead['head']}")
        w(">")
        w(f"> {lead['deck']}")
        w("")
        w(f"As filed: *{lead['matched']}* — {lead['feed']}")
        w("")
        w(f"<{lead['link']}>")
        w("")
        w(f"Sources named on the page: {lead['src']}.")
        w("")

    w("## The grid")
    w("")
    w("| UTC | Place | Region | As filed | Wire |")
    w("|---|---|---|---|---|")
    for e in r["items"]:
        w(f"| {e['hm']} | {e['place']} | {e['region'].title()} | "
          f"[{e['matched']}]({e['link']}) | {e['feed']} |")
    w("")
    w("## What the page leaves out, and why")
    w("")
    w("The page claims one day, so the boundary was enforced by script rather than by eye: every")
    w("line had to resolve to a wire item stamped inside 20 November 2026 UTC, or the build")
    w("refused to run (`build/resolve.py`). Four stories that would have been easy to include")
    w("failed that test and were moved to the DATE CHECK panel instead:")
    w("")
    w("- **The Shenzhen summit of Trump, Xi and Putin** — held on Thursday 19 November; the")
    w("  trilateral declaration was filed about it on the 20th, but the meeting was the day before.")
    w("- **The World Court's genocide ruling against Myanmar** — handed down on 19 November. The")
    w("  page carries Friday's news instead: the Rohingya reaction to it, filed 09:47 UTC.")
    w("- **The COP31 cover text that dropped the fossil-fuel phase-out** — filed 19 November,")
    w("  19:31 UTC. The page carries Friday's filing, the talks running into overtime.")
    w("- **Anthropic's $81bn IPO** — priced and first traded on 19 November. The page carries")
    w("  Friday's story: the shares falling more than 10% on their second day.")
    w("")
    w("Stories filed after the day are left out for the same reason: Zelensky calling Putin a")
    w('"killer" (Saturday, 07:24 UTC) and the conviction for starting the Palisades fire')
    w("(Saturday, 04:34 UTC).")
    w("")
    w("## How the page was made")
    w("")
    w("- `build/render.py` draws `entry.png` with Pillow; the type is Roboto Slab, Liberation")
    w("  Sans Narrow and Liberation Mono. No photograph, no stock art: the composition is type")
    w("  and rules on newsprint cream.")
    w("- `build/stories.json` holds the selection as written by hand: for each line, a substring")
    w("  of a real headline plus the label the page prints.")
    w("- `build/resolve.py` matches those substrings against 765 items the feeds carried on the")
    w("  day, taken from 46 feeds, and writes `build/resolved.json` — which supplies the time,")
    w("  the place tag and the source for every line, and fails the build on any story that")
    w("  falls outside the day.")
    w("- `main.ts` re-checks the finished PNG the way the gate does (signature, every chunk's")
    w("  CRC, IEND, the IHDR's 1024x1024, the 1 MiB cap) and copies it to `/output/entry.png`.")
    w("")
    w("The feed harvest covered BBC (7 sections), Al Jazeera, Google News (6 topics), The Hindu,")
    w("NDTV, Times of India, Indian Express, Dawn, SCMP, DW, France 24, the Guardian, NPR, CBC,")
    w("ABC Australia, Sky News, Moscow Times, Japan Times, Straits Times, RNZ, allAfrica, Punch,")
    w("Premium Times, Buenos Aires Times, Rio Times, Jerusalem Post, Bangkok Post, Philstar and")
    w("VNExpress.")
    w("")

    path = os.path.join(REPO, "SOURCES.md")
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"wrote {path}: {os.path.getsize(path)} bytes, {len(r['items']) + len(r['leads'])} stories")


if __name__ == "__main__":
    main()
