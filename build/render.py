#!/usr/bin/env python3
"""Draw the front page. Build-time only: the entry itself just copies the PNG.

Input:  DATA, below (every line already resolved to a real wire item and its UTC time)
Output: ../entry.png, the page this repository submits, 1024x1024

Read as a clock: masthead and one dominant lead above the fold, two secondary leads, the
day in numbers, then the remaining 44 stories in four columns running from 00:02 to the
last filing of the night, and a date-check footer naming what was left out and why.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
M = 26
CW = W - 2 * M                      # 972

BG     = (247, 242, 230)
INK    = (23, 19, 15)
ACCENT = (168, 35, 27)
MUTED  = (111, 101, 88)
RULE   = (203, 193, 176)
FAINT  = (150, 141, 124)     # wire names: readable, but never louder than the label

F = {
    "slab":    "/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Bold.otf",
    "slabblk": "/usr/share/fonts/opentype/roboto/slab/RobotoSlab-Black.otf",
    "narrow":  "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
    "narrowb": "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
    "mono":    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
}

font = lambda k, s: ImageFont.truetype(F[k], s)

BOXES = []          # every run of text, for the geometry audit at the end

def tw(d, s, f, tracking=0.0):
    return 0 if not s else d.textlength(s, font=f) + tracking * (len(s) - 1)

def text(d, xy, s, f, fill=INK, tracking=0.0):
    x, y = xy
    if s:
        BOXES.append((x, y, x + tw(d, s, f, tracking), y + f.size, s))
    if tracking:
        for ch in s:
            d.text((x, y), ch, font=f, fill=fill)
            x += d.textlength(ch, font=f) + tracking
    else:
        d.text((x, y), s, font=f, fill=fill)

def tracked_right(d, x_right, y, s, f, fill=INK, tracking=0.0):
    text(d, (x_right - tw(d, s, f, tracking), y), s, f, fill, tracking)

def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(d, trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])

def fit(d, s, key, size, maxw, floor=8):
    while size > floor:
        f = font(key, size)
        if tw(d, s, f) <= maxw:
            return f, size
        size -= 1
    return font(key, floor), floor

def rule(d, y, h=1, col=RULE, x0=M, x1=W - M):
    d.rectangle([x0, y, x1 - 1, y + h - 1], fill=col)

def audit(w, h, slack=1.0):
    """Report runs that leave the page or sit on top of another run."""
    bad = []
    for b in BOXES:
        if b[0] < 0 or b[1] < 0 or b[2] > w or b[3] > h:
            bad.append(f"off-page {b[4]!r} at {b[:4]}")
    ordered = sorted(BOXES, key=lambda b: b[0])
    for i, a in enumerate(ordered):
        for b in ordered[i + 1:]:
            if b[0] >= a[2] - slack:
                break
            if a[1] < b[3] - slack and b[1] < a[3] - slack:
                bad.append(f"overlap {a[4]!r} / {b[4]!r}")
    return bad

# The page, resolved: every line already matched to a wire item and its UTC filing
# time, so this file draws the image without needing the harvest beside it.
DATA = {
    "day": 'FRIDAY 20 NOVEMBER 2026',
    "day_short": '20 NOVEMBER 2026',
    "n_total": 47,
    "n_places": 36,
    "first_hm": '00:02',
    "last_hm": '23:39',
    "leads": [  # UTC, place, wires, headline, deck, region
        ('06:52', 'KYIV, UKRAINE', 'Moscow Times, The Hindu, Reuters',
         "Russian missiles hit Kyiv's bridges, killing eight across Ukraine",
         "One of the war's largest attacks on the capital struck two bridges and railway stations and cut power and water. Poland condemned three airspace violations; the Netherlands summoned Russia's ambassador.", 'EUROPE'),
        ('13:39', 'NEW YORK, USA', "Sky News, Yahoo Finance, Guardian, Barron's",
         "Anthropic's record debut lasts a day as the AI trade melts down",
         "Shares fell more than 10% at Friday's open, a day after the record Nasdaq debut. Nvidia dropped 12%, the fear gauge touched 40, and the Nasdaq erased every gain it made in 2026.", 'AMERICAS'),
        ('14:38', 'ANTALYA, TURKEY', 'France 24, Al Jazeera, The Hindu',
         'COP31 ends in deadlock and overtime over fossil fuels',
         'The draft cover text went out with no reference to a fossil-fuel phase-out, and the talks ran past their Friday deadline as nations quarrelled over the wording.', 'EUROPE'),
    ],
    "items": [  # UTC, place, wire, label, region
        ('00:02', 'LONDON', 'BBC', 'Fridges secured from hackers in a secret operation', 'EUROPE'),
        ('00:50', 'BERLIN', 'BBC', 'Europe says it is ready to talk to Moscow', 'EUROPE'),
        ('02:08', 'CALIFORNIA', 'The Hindu', 'Subpoena for Nvidia over chips and its ex-CEO', 'AMERICAS'),
        ('03:05', 'SYDNEY', 'Straits Times', "Anthropic's data centre opposed by residents", 'OCEANIA'),
        ('03:46', 'RIYADH', 'NBC News', "Houthi strike hits the wealth fund's tower", 'MIDDLE EAST'),
        ('05:30', 'TAIPEI', 'Reuters', 'Taiwan tells Meta of China-linked accounts', 'ASIA-PACIFIC'),
        ('07:13', 'ODISHA', 'Indian Express', 'Cyclone Akvan makes landfall; no casualties', 'SOUTH ASIA'),
        ('07:31', 'BAGHDAD', 'Reuters', 'Troops deploy in an Iran-backed stronghold', 'MIDDLE EAST'),
        ('07:55', 'BEIJING', 'NDTV', "Xi declines to meet Japan's prime minister", 'ASIA-PACIFIC'),
        ('09:17', 'KUNO', 'Indian Express', "A Botswana cheetah's cubs take India to 62", 'SOUTH ASIA'),
        ('09:33', 'ABIDJAN', 'allAfrica', '22 African countries in or near debt distress', 'AFRICA'),
        ('09:47', "COX'S BAZAR", 'The Hindu', "Rohingya welcome the World Court's ruling", 'SOUTH ASIA'),
        ('10:06', 'KHARG ISLAND', 'Euronews', 'A tanker convoy to test the US blockade', 'MIDDLE EAST'),
        ('10:16', 'SEOUL', 'BBC', '111 caught cheating in the Suneung exam', 'ASIA-PACIFIC'),
        ('11:50', 'TALLINN', 'Reuters', 'Moscow cries "Iron Curtain" over the border', 'EUROPE'),
        ('12:01', 'TATARSTAN', 'Kyiv Independent', 'Ukraine strikes the Druzhba pipeline', 'EUROPE'),
        ('12:02', 'WASHINGTON', 'CBS News', 'The US and Israel weigh an assault on Iran', 'AMERICAS'),
        ('12:42', 'TEXAS', 'BBC', 'An execution that took more than an hour', 'AMERICAS'),
        ('13:41', 'KAMPALA', 'allAfrica', 'Gatherings and travel restricted over Ebola', 'AFRICA'),
        ('14:43', 'MADRID', 'BBC', 'Cost-of-living protests across Europe', 'EUROPE'),
        ('15:55', 'JOHANNESBURG', 'BBC', 'Nearly 600 women killed in three months', 'AFRICA'),
        ('16:15', 'TAIPEI', 'Benzinga', "Taiwan's worst week since 1990", 'ASIA-PACIFIC'),
        ('16:40', 'HODEIDA', 'The Hindu', 'Saudi-led strikes hit a Yemen port', 'MIDDLE EAST'),
        ('16:54', 'ROME', 'The Hindu', 'Workers and students strike over wages', 'EUROPE'),
        ('16:55', 'BUENOS AIRES', 'Buenos Aires Times', 'Country risk tops 1,000 as bonds slump', 'AMERICAS'),
        ('17:00', 'NEW YORK', 'SCMP', 'A plan to close Rikers Island by 2032', 'AMERICAS'),
        ('17:03', 'BRUSSELS', 'France 24', 'A "landmark" UK-EU deal after Brexit', 'EUROPE'),
        ('17:15', 'NEW YORK', 'Straits Times', '19 years for a plot to kill a Sikh leader', 'AMERICAS'),
        ('17:33', 'MERCURY', 'IFLScience', 'BepiColombo arrives at Mercury after eight years', 'SPACE'),
        ('17:55', 'LONDON', 'SCMP', 'Researcher: Claude proved the Riemann hypothesis', 'EUROPE'),
        ('18:14', 'COPENHAGEN', 'SCMP', 'A Russian plot to kill a rapper; a diplomat out', 'EUROPE'),
        ('18:21', 'WASHINGTON', 'Straits Times', 'A tax on AI data centres built abroad', 'AMERICAS'),
        ('18:31', 'VOYAGER 1', 'My Modern Met', 'One light-day from Earth', 'SPACE'),
        ('18:43', 'KERCH', 'Al Jazeera', 'Ukraine strikes the Kerch bridge', 'EUROPE'),
        ('19:03', 'WASHINGTON', 'BBC', 'The White House removes its cyber chief', 'AMERICAS'),
        ('19:47', 'POLAND', 'AP', '11 countries drill for a Ukraine mission', 'EUROPE'),
        ('22:14', 'TAIZ', 'BBC', 'A city cut off for weeks by the Houthis', 'MIDDLE EAST'),
        ('22:37', 'PARIS', 'BBC', 'Police sentenced over the Zecler beating', 'EUROPE'),
        ('22:53', 'PORT-AU-PRINCE', 'AP', 'A deal with El Salvador to build prisons', 'AMERICAS'),
        ('22:53', 'NEW YORK', 'BBC', 'GTA 6 takes $3.8bn in a single day', 'AMERICAS'),
        ('23:06', 'ANTALYA', 'Al Jazeera', 'COP31 deadlocks and runs into overtime', 'EUROPE'),
        ('23:09', 'SYDNEY', 'Guardian', 'A coalmine law passes in New South Wales', 'OCEANIA'),
        ('23:15', 'WASHINGTON', 'BBC', 'More UFO footage is declassified', 'AMERICAS'),
        ('23:39', 'THE HAGUE', 'Sydney Morning Herald', "BYD's Land Rover copy is banned in Europe", 'EUROPE'),
    ],
}


def main():
    r = dict(DATA)
    r["leads"] = [dict(zip(("hm", "place", "src", "head", "deck", "region"), t))
                  for t in DATA["leads"]]
    r["items"] = [dict(zip(("hm", "place", "src", "label", "region"), t))
                  for t in DATA["items"]]
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    warn = []

    n_reg = len({e["region"] for e in r["items"]} - {"SPACE"})

    # ── masthead ──────────────────────────────────────────────────────────
    rule(d, 10, h=2)          # a front page is framed top and bottom
    y = 20
    f_kick = font("narrowb", 11)
    text(d, (M, y), "THE WORLD IN ONE DAY", f_kick, ACCENT, tracking=2.4)
    tracked_right(d, W - M, y,
                  f"{r['n_total']} STORIES  ·  {n_reg} REGIONS  ·  {r['n_places']} PLACES",
                  f_kick, MUTED, tracking=1.5)

    y = 37
    f_date, dsize = fit(d, r["day"], "slabblk", 64, CW)
    text(d, (M, y), r["day"], f_date, INK)
    y += dsize + 10

    f_deck = font("narrow", 14.5)
    deck = (f"{r['n_total']} stories, all first filed between {r['first_hm']} and {r['last_hm']} UTC "
            f"on 20 November 2026. Times are UTC; each line names the wire that carried it first.")
    for line in wrap(d, deck, f_deck, CW):
        text(d, (M, y), line, f_deck, MUTED)
        y += 17
    y += 7
    rule(d, y, h=2)
    rule(d, y + 3, h=1)
    y += 9

    # ── above the fold: one dominant lead, two stacked ────────────────────
    text(d, (M, y), "ABOVE THE FOLD", font("narrowb", 10), ACCENT, tracking=2.2)
    tracked_right(d, W - M, y, "THE DAY'S WEIGHT, NOT ITS CLOCK",
                  font("narrow", 9), MUTED, tracking=1.2)
    y += 16

    gut = 22
    colw = (CW - 2 * gut) // 3
    big_w = 2 * colw + gut
    top = y

    def stamp(d, x, yy, lead, size=9.5):
        f_st = font("mono", size)
        s = f"{lead['hm']} UTC"
        text(d, (x, yy), s, f_st, ACCENT)
        text(d, (x + tw(d, s, f_st) + 8, yy), lead["place"], font("narrowb", 9), MUTED, tracking=1.1)

    # dominant lead
    lead = r["leads"][0]
    yy = top
    stamp(d, M, yy, lead, 11)
    yy += 19
    f_h = font("slab", 38)
    for line in wrap(d, lead["head"], f_h, big_w - 6):
        text(d, (M, yy), line, f_h, INK)
        yy += 45
    yy += 5
    f_b = font("narrow", 14)
    for line in wrap(d, lead["deck"], f_b, big_w - 20):
        text(d, (M, yy), line, f_b, INK)
        yy += 17
    yy += 3
    text(d, (M, yy), lead["src"], font("narrow", 10), MUTED)
    left_bottom = yy + 12

    # two secondary leads stacked in the third column
    x3 = M + big_w + gut
    yy = top
    for j, lead in enumerate(r["leads"][1:]):
        stamp(d, x3, yy, lead, 9)
        yy += 15
        f_h = font("slab", 16.5)
        for line in wrap(d, lead["head"], f_h, colw):
            text(d, (x3, yy), line, f_h, INK)
            yy += 20
        yy += 3
        f_b = font("narrow", 11.5)
        for line in wrap(d, lead["deck"], f_b, colw):
            text(d, (x3, yy), line, f_b, INK)
            yy += 13
        yy += 2
        text(d, (x3, yy), lead["src"], font("narrow", 9.5), MUTED)
        yy += 13
        if j == 0:
            d.rectangle([x3, yy + 2, W - M - 1, yy + 2], fill=RULE)
            yy += 9
    right_bottom = yy

    bottom = max(left_bottom, right_bottom)
    d.rectangle([x3 - gut // 2, top, x3 - gut // 2, bottom], fill=RULE)
    y = bottom + 7
    rule(d, y)
    y += 9

    # ── the day in numbers ────────────────────────────────────────────────
    text(d, (M, y), "THE DAY IN NUMBERS", font("narrowb", 10), ACCENT, tracking=2.2)
    y += 15
    stats = [
        ("8", "killed across Ukraine as missiles hit Kyiv's bridges"),
        ("-12%", "Nvidia, on the day the AI trade melted down"),
        ("40", "the fear gauge, as the Nasdaq erased all of 2026"),
        ("$3.8bn", "GTA 6 took in a single day, a record for a launch"),
        ("111", "South Korean students caught cheating in the Suneung"),
        ("600", "women killed in South Africa in three months"),
    ]
    sw = CW // len(stats)
    for i, (big, cap) in enumerate(stats):
        x = M + i * sw
        text(d, (x, y), big, font("slabblk", 28), ACCENT)
        f_cap = font("narrow", 10.5)
        cap_lines = wrap(d, cap, f_cap, sw - 16)
        if len(cap_lines) > 2:
            warn.append(f"stat caption needs {len(cap_lines)} lines: {cap}")
        for k, line in enumerate(cap_lines):
            text(d, (x, y + 31 + k * 11), line, f_cap, INK)
        if i:
            d.rectangle([x - 8, y + 1, x - 8, y + 48], fill=RULE)
    y += 60
    rule(d, y)
    y += 9

    # ── the rest of the day, hour by hour ─────────────────────────────────
    text(d, (M, y), "THE REST OF FRIDAY, HOUR BY HOUR", font("narrowb", 10), ACCENT, tracking=2.2)
    tracked_right(d, W - M, y, "READ DOWN EACH COLUMN, LEFT TO RIGHT",
                  font("narrow", 9), MUTED, tracking=1.2)
    y += 14

    items = r["items"]
    ncol, nrow = 4, 11
    cgut = 15
    cw = (CW - (ncol - 1) * cgut) // ncol
    per = (len(items) + ncol - 1) // ncol
    assert per <= nrow, f"{len(items)} items need {per} rows, only {nrow} available"
    row_h = 35
    f_time, f_place, f_src, f_label = (font("mono", 8.5), font("narrowb", 8.5),
                                      font("narrow", 8), font("narrow", 11.5))

    for c in range(ncol):
        chunk = items[c * per:(c + 1) * per]
        if chunk:
            text(d, (M + c * (cw + cgut), y), f"{chunk[0]['hm']}-{chunk[-1]['hm']}",
                 font("mono", 8), MUTED)
    y += 12
    rule(d, y)
    y += 7

    for idx, it in enumerate(items):
        c, rr = divmod(idx, per)
        x = M + c * (cw + cgut)
        yy = y + rr * row_h
        text(d, (x, yy), it["hm"], f_time, ACCENT)
        text(d, (x + 31, yy), it["place"], f_place, MUTED, tracking=0.8)
        text(d, (x + 31 + tw(d, it["place"], f_place, 0.8) + 7, yy), it["src"], f_src, FAINT)
        if tw(d, it["label"], f_label) > cw:
            warn.append(f"label too wide: {it['label']}")
        text(d, (x, yy + 12), it["label"], f_label, INK)
    y += nrow * row_h
    rule(d, y)
    y += 9

    # ── date check ────────────────────────────────────────────────────────
    text(d, (M, y), "DATE CHECK", font("narrowb", 10), ACCENT, tracking=2.2)
    y += 14
    f_dc = font("narrow", 10)
    for para in [
        "Filed before this day, so left out: the Shenzhen summit of Trump, Xi and Putin (Thursday), the "
        "World Court's genocide ruling against Myanmar (Thursday, 19 November), and the COP31 cover text "
        "that dropped the fossil-fuel phase-out (Thursday, 19:31 UTC).",
        "Filed after, so left out: Zelensky calling Putin a \"killer\" (Saturday, 07:24 UTC), the "
        "Palisades fire conviction (Saturday, 04:34 UTC).",
    ]:
        for line in wrap(d, para, f_dc, CW):
            text(d, (M, y), line, f_dc, MUTED)
            y += 11
        y += 1
    rule(d, y + 3)
    y += 9

    f_foot = font("narrow", 8.5)
    foot = ("Sources: BBC, Reuters, AP, AFP, Al Jazeera, The Hindu, SCMP, France 24, Straits Times, "
            "Guardian, allAfrica, Euronews, CBS, NBC, Barron's, Kyiv Independent, Moscow Times, Indian "
            "Express, NDTV, Benzinga, SMH, Buenos Aires Times — 765 items filed on 20 November 2026, "
            "read from 46 feeds.")
    for line in wrap(d, foot, f_foot, CW):
        text(d, (M, y), line, f_foot, MUTED)
        y += 10
    y += 3
    text(d, (M, y), r["day_short"], font("narrowb", 9), ACCENT, tracking=2.0)
    tracked_right(d, W - M, y, "WORLD EDITION  ·  DRAWN, NOT PHOTOGRAPHED",
                  font("narrowb", 9), MUTED, tracking=1.4)
    rule(d, y + 13, h=2)

    out = os.path.join(HERE, "..", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, optimize=True)
    print(f"wrote entry.png  {os.path.getsize(out)} bytes  bottom={y}  date={dsize}px  runs={len(BOXES)}")
    for b in audit(W, H):
        print("  AUDIT", b)
    for w in warn:
        print("  WARN", w)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
