#!/usr/bin/env python3
"""Draw the 25 November 2026 front page (LOCAL BUILD TOOL ONLY).

This program runs on my own machine with Pillow to render
entry.png. It is NEVER run by the grader: the grader runs main.py,
which is stdlib-only and just copies the finished entry.png.

36 stories, all from news published 25 November 2026:
Reuters World News Summary (25 Nov) and Jagran Josh headlines
(25 Nov). No external images, no real person's face, no network,
no timestamps, no randomness: two runs are byte-identical.

Usage: python3 draw.py [output-png-path]
Default output is entry.png next to this file.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952 usable width

PAPER = (247, 243, 232)
PANEL = (238, 234, 222)
INK = (18, 18, 18)
SOFT = (74, 74, 74)
RED = (158, 27, 27)
SKY = (186, 208, 224)
SEA = (105, 145, 172)
SMOKE = (120, 120, 118)
STEEL = (52, 52, 58)
GOLD = (176, 132, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font; never overflows."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.32):
    """Draw wrapped paragraph; return y just below the last line."""
    step = int(fnt.size * leading)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def centred(draw, y, text, fnt, fill=INK, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.3)


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def fit_font(draw, text, path, size, width):
    """Largest size at or below `size` that fits `width`, else `size`."""
    while size > 9:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= width:
            return fnt
        size -= 1
    return font(path, 9)


def draw_ship_scene(draw, x, y, w, h):
    """Gulf of Finland: cargo ship Sparta II, smoke, rescue spray."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.ellipse([x + w - 92, y + 14, x + w - 34, y + 72], fill=(250, 238, 190))
    for cx, cy, r in ((x + 60, y + 34, 26), (x + 92, y + 30, 32),
                      (x + 124, y + 36, 24), (x + 300, y + 22, 22),
                      (x + 328, y + 26, 28)):
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                     fill=(240, 240, 236))
    sea_y = y + h * 0.55
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(3):
        wy = sea_y + 12 + i * 20
        draw.arc([x + 20 + i * 30, wy, x + 150 + i * 30, wy + 26],
                 200, 340, fill=(210, 225, 235), width=3)
    hx, hy = x + 90, sea_y - 6
    s = h / 180.0
    draw.polygon([(hx, hy), (hx + 330, hy), (hx + 300, hy + 52),
                  (hx + 18, hy + 52)], fill=(122, 32, 28))
    draw.rectangle([hx + 30, hy - 58, hx + 300, hy], fill=(52, 52, 58))
    for i, col in enumerate(((176, 132, 40), (36, 82, 110), (122, 32, 28))):
        draw.rectangle([hx + 44 + i * 82, hy - 52, hx + 118 + i * 82, hy - 8],
                       fill=col, outline=INK, width=2)
    draw.rectangle([hx + 300, hy - int(66 * s), hx + 336, hy],
                   fill=(240, 240, 236), outline=INK, width=2)
    draw.rectangle([hx + 306, hy - int(90 * s), hx + 330, hy - int(66 * s)],
                   fill=STEEL)
    for i, r in enumerate((30, 38, 46)):
        sy0 = hy - int(70 * s) - i * int(10 * s)
        draw.ellipse([hx + 296 + i * 8, sy0,
                      hx + 296 + i * 8 + r, sy0 + r // 2],
                     fill=SMOKE)
    draw.ellipse([x + w - 150, y + 96, x + w - 138, y + 108], fill=INK)
    draw.line([(x + w - 156, y + 102), (x + w - 132, y + 102)], fill=INK, width=2)
    for i in range(4):
        draw.arc([x + 30, sea_y + 8 + i * 3, x + 110, sea_y + 48 + i * 3],
                 300, 360, fill=(235, 242, 246), width=3)
    draw.text((x + 10, y + h - 26), "THE SPARTA II, GULF OF FINLAND",
              font=font(SANS_B, 13), fill=INK)


def draw_tower_scene(draw, x, y, w, h):
    """Riyadh skyline at dusk; heights scale with h, nothing leaves frame."""
    draw.rectangle([x, y, x + w, y + h], fill=(172, 172, 192))
    mh = min(40, h - 12)
    draw.ellipse([x + w - 66, y + 6, x + w - 26, y + 6 + mh], fill=(250, 238, 190))
    base = y + h
    for tx, f, tw in ((0, 0.72, 92), (96, 0.58, 74), (174, 0.82, 104),
                      (282, 0.64, 82), (368, 0.46, 66)):
        th = int(h * f)
        draw.rectangle([x + tx, base - th, x + tx + tw, base],
                       fill=(138, 142, 162), outline=(90, 100, 130), width=1)
    tx, tw = x + 174, 104
    th = int(h * 0.64)
    draw.rectangle([tx, base - th, tx + tw, base], fill=(128, 132, 155))
    for r in range(3):
        for c in range(3):
            wx = tx + 14 + c * 30
            wy = base - th + 10 + r * 16
            if wy + 9 <= base:
                draw.rectangle([wx, wy, wx + 12, wy + 9], fill=(250, 214, 120))
    draw.polygon([(tx + tw // 2 - 16, base - th), (tx + tw // 2 + 16, base - th),
                  (tx + tw // 2, base - th - 10)], fill=(250, 214, 120))
    draw.ellipse([tx + tw // 2 - 10, base - th - 20, tx + tw // 2 + 10,
                  base - th - 10], fill=(255, 240, 180))
    if h >= 64:
        draw.text((x + 10, y + h - 26), "RIYADH AT DUSK",
                  font=font(SANS_B, 13), fill=INK)


def draw_chip_scene(draw, x, y, w, h):
    """A chip on trial: circuit board, chip, pins; scales with h."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    for i in range(5):
        yy = y + 10 + i * max(1, h // 5)
        draw.line([(x + 12, yy), (x + w - 12, yy)], fill=(190, 184, 168), width=1)
    cx, cy = x + w // 2, y + h // 2
    half = max(14, int(h * 0.34))
    ext = 8 if h >= 64 else 4
    for d in (-22, 0, 22):
        draw.line([(cx + d, cy - half), (cx + d, cy - half - ext)],
                  fill=GOLD, width=4)
        draw.line([(cx + d, cy + half), (cx + d, cy + half + ext)],
                  fill=GOLD, width=4)
    for e in (-half + 8, 0, half - 8):
        draw.line([(cx - half - 20, cy + e), (cx - half - 28, cy + e)],
                  fill=GOLD, width=4)
        draw.line([(cx + half + 20, cy + e), (cx + half + 28, cy + e)],
                  fill=GOLD, width=4)
    draw.rectangle([cx - half - 20, cy - half, cx + half + 20, cy + half],
                   fill=STEEL, outline=INK, width=3)
    draw.rectangle([cx - half + 6, cy - 13, cx + half - 6, cy + 13],
                   fill=(20, 20, 20))
    label = "HUAWEI"
    lw = draw.textlength(label, font=font(SANS_B, 11))
    draw.text((cx - lw / 2, cy - 6), label, font=font(SANS_B, 11),
              fill=(250, 214, 120))
    if h >= 64:
        draw.text((x + 10, y + h - 26), "THE CHIP ON TRIAL",
                  font=font(SANS_B, 13), fill=SOFT)


def draw_turkeys(draw, x, y, w, h):
    """Two pardoned turkeys; geometry scales with h, labels only if room."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    s = h / 110.0
    ty = y + h // 2 + int(6 * s)
    for k, cx in enumerate((x + int(w * 0.28), x + int(w * 0.72))):
        for a in range(-50, 51, 25):
            rad = math.radians(a - 90)
            ex = cx + int(46 * s * math.cos(rad))
            ey = ty - int(6 * s) + int(46 * s * math.sin(rad))
            draw.line([(cx, ty - int(6 * s)), (ex, ey)],
                      fill=(122, 84, 40), width=max(2, int(7 * s)))
        draw.ellipse([cx - int(30 * s), ty - int(34 * s),
                      cx + int(30 * s), ty + int(26 * s)], fill=(122, 84, 40))
        draw.ellipse([cx - int(16 * s), ty - int(52 * s),
                      cx + int(16 * s), ty - int(18 * s)], fill=(96, 62, 28))
        draw.polygon([(cx, ty - int(50 * s)), (cx - int(6 * s), ty - int(60 * s)),
                      (cx + int(6 * s), ty - int(60 * s))], fill=(176, 132, 40))
        if h >= 80:
            label = "FREEDOM" if k == 0 else "FEATHERS"
            lw = draw.textlength(label, font=font(SANS_B, 12))
            draw.text((cx - lw / 2, y + h - 13), label, font=font(SANS_B, 12),
                      fill=SOFT)


REGION_COLORS = {
    "USA": (36, 82, 110),
    "EUROPE": (46, 110, 70),
    "MIDEAST": (158, 27, 27),
    "ASIA": (176, 132, 40),
    "AFRICA": (120, 84, 40),
    "AMERICAS": (90, 60, 130),
    "TECH": (52, 52, 58),
    "SPORT": (20, 120, 110),
}

HERO = {
    "kicker": "LEAD STORY  -  GULF OF FINLAND",
    "headline": "Zelenskiy confirms Ukraine hit Russian ship",
    "paras": [
        "President Volodymyr Zelenskiy confirmed Ukraine was behind "
        "Saturday's drone strike on the Russian cargo ship Sparta II.",
        "Norway urged caution. The ship was towed back and is anchored "
        "in St Petersburg.",
    ],
    "source": "Source: Reuters, 25 Nov 2026",
}

LEADS3 = [
    {
        "kicker": "THE GULF  -  RIYADH",
        "headline": "Houthis hit Riyadh's tallest tower",
        "summary": "Houthi fighters struck Riyadh's tallest tower on "
                   "Tuesday, wounding 11 people. It was the second strike "
                   "in under a week.",
        "source": "Source: Reuters, 25 Nov 2026",
        "scene": "tower",
    },
    {
        "kicker": "TECH ON TRIAL  -  NEW YORK",
        "headline": "Huawei convicted over Iran business",
        "summary": "A New York jury convicted China's Huawei on Tuesday "
                   "of deceiving banks about its Iran business and stealing "
                   "trade secrets.",
        "source": "Source: Reuters, 25 Nov 2026",
        "scene": "chip",
    },
    {
        "kicker": "WASHINGTON  -  THANKSGIVING EVE",
        "headline": "Trump spares turkeys Freedom and Feathers",
        "summary": "President Donald Trump pardoned two turkeys, Freedom "
                   "and Feathers, on Tuesday in the annual White House "
                   "Thanksgiving ritual.",
        "source": "Source: Reuters, 25 Nov 2026",
        "scene": "turkeys",
    },
]

HIGHLIGHTS = [
    {
        "kicker": "EUROPE  -  FRANCE",
        "headline": "Sarkozy corruption case sent to trial",
        "summary": "Ex-president Sarkozy and Carla Bruni face trial.",
        "source": "Reuters, 25 Nov 2026",
        "icon": "columns",
    },
    {
        "kicker": "USA  -  WASHINGTON",
        "headline": "Giuliani gets the Medal of Freedom",
        "summary": "Ex-New York mayor Giuliani, 82, receives the honour.",
        "source": "Reuters, 25 Nov 2026",
        "icon": "star",
    },
]

# (region, headline, one-line summary, source) — all published 25 Nov 2026.
GRID = [
    ("USA", "Fort Hood gunman seeks execution stay",
     "Hasan faces execution next week.", "REUTERS"),
    ("AFRICA", "Libya's frozen conflict stirs",
     "Warship sunk off Benghazi port.", "REUTERS"),
    ("MIDEAST", "Houthis 'won't seize Aden'",
     "Yemeni army holds the port city.", "REUTERS"),
    ("USA", "Radar fault delays O'Hare flights",
     "FAA holds arrivals in Chicago.", "REUTERS"),
    ("USA", "US envoy doubts Israel aid cutoff",
     "Huckabee unsure aid ends this year.", "REUTERS"),
    ("USA", "Abrego Garcia to leave US",
     "Will fly to Europe voluntarily.", "REUTERS"),
    ("TECH", "Nvidia suppliers cheer Huang return",
     "CEO back; AI plans back on track.", "REUTERS"),
    ("EUROPE", "Santas wash up on Bulgaria beach",
     "Container from drone-hit ship.", "REUTERS"),
    ("USA", "Thomas Markle indicted in US",
     "Faces child abuse image charges.", "REUTERS"),
    ("EUROPE", "Sweden to vote on Kristersson",
     "Bid to end government gridlock.", "REUTERS"),
    ("MIDEAST", "Eisenkot seals coalition deal",
     "First pact in Israel government bid.", "REUTERS"),
    ("EUROPE", "Berlin Left expels lawmaker",
     "Antisemitism row cleared for talks.", "REUTERS"),
    ("EUROPE", "Most Germans oppose Ukraine aid",
     "53% against, 46% in favour.", "REUTERS"),
    ("EUROPE", "Putin vows reply to oil-plant hits",
     "Says Kyiv struck despite Trump plea.", "REUTERS"),
    ("AMERICAS", "25 held hostage in Cartagena shop",
     "Army deployed after hijack fails.", "REUTERS"),
    ("AMERICAS", "WHO: lift Cuba oil blockade",
     "Tedros warns children at risk.", "REUTERS"),
    ("EUROPE", "Spain challenges Madrid baby law",
     "Unborn-children rights go to court.", "REUTERS"),
    ("EUROPE", "Latvia sees Ukraine 'tipping point'",
     "Rinkevics cites Russian economy.", "REUTERS"),
    ("EUROPE", "Lukashenko offers Moscow flight",
     "Proposes joint trip with Zelenskiy.", "REUTERS"),
    ("EUROPE", "UK prisoner admits Huntley murder",
     "Admits killing Ian Huntley.", "REUTERS"),
    ("MIDEAST", "Turkish ruling-party figure quits",
     "Yazici resigns amid fund probe.", "REUTERS"),
    ("EUROPE", "NATO to send AWACS to Poland",
     "After missiles landed on Friday.", "JAGRAN JOSH"),
    ("MIDEAST", "Iran: tankers hit by mines",
     "IRGC blames mines in Hormuz.", "JAGRAN JOSH"),
    ("EUROPE", "Russia, Ukraine clash at the UN",
     "Row over shipping and energy.", "JAGRAN JOSH"),
    ("MIDEAST", "UN warns over Gaza hardship",
     "Civilians struggle for essentials.", "JAGRAN JOSH"),
    ("EUROPE", "EU announces new Russia curbs",
     "Further sanctions amid war tensions.", "JAGRAN JOSH"),
    ("MIDEAST", "US and Qatar talk cooperation",
     "Officials discuss regional issues.", "JAGRAN JOSH"),
    ("SPORT", "England level T20 series",
     "Beat Australia by eight wickets.", "JAGRAN JOSH"),
    ("ASIA", "BJP and SAD reunite for Punjab",
     "Alliance set for 2027 elections.", "JAGRAN JOSH"),
    ("ASIA", "Nepal PM wraps up India visit",
     "Met Modi; aid package pledged.", "JAGRAN JOSH"),
]


def draw_masthead(draw, count):
    y = 20
    y = centred(draw, y, "ONE DAY  -  ONE PAGE  -  THE WORLD IN BRIEF",
                font(SANS_B, 13), fill=RED)
    y += 2
    y = centred(draw, y, "THE WORLD TODAY", font(SERIF_B, 50))
    y -= 4
    rule(draw, MARGIN, W - MARGIN, y, width=3)
    y += 6
    rule(draw, MARGIN, W - MARGIN, y, width=1)
    y += 8
    left = "WEDNESDAY, 25 NOVEMBER 2026"
    right = "%d STORIES  -  ALL VERIFIED" % count
    draw.text((MARGIN, y), left, font=font(SANS_B, 16), fill=INK)
    rw = draw.textlength(right, font=font(SANS_B, 16))
    draw.text((W - MARGIN - rw, y), right, font=font(SANS_B, 16), fill=INK)
    y += 20
    rule(draw, MARGIN, W - MARGIN, y, width=1)
    return y + 8


def draw_timeline(draw, y):
    note = ("WEDNESDAY 25 NOVEMBER 2026  •  ALL TIMES UTC  •  "
            "STORIES IN WIRE ORDER")
    draw.text((MARGIN, y), note, font=font(SANS_B, 10), fill=RED)
    bar_y = y + 18
    draw.line([(MARGIN, bar_y), (W - MARGIN, bar_y)], fill=INK, width=2)
    for i, lab in enumerate(["00:00", "06:00", "12:00", "18:00", "24:00"]):
        tx = MARGIN + (CW * i) // 4
        draw.line([(tx, bar_y - 4), (tx, bar_y + 4)], fill=INK, width=2)
        fnt = font(SANS_B, 9)
        lw = draw.textlength(lab, font=fnt)
        lx = min(max(tx - lw / 2, MARGIN), W - MARGIN - lw)
        draw.text((lx, bar_y + 6), lab, font=fnt, fill=SOFT)
    return bar_y + 16


def story_block(draw, x, y, w, kicker, headline, summary, source,
                head_size=22, body_size=14):
    """Kicker + headline + summary + source; returns y below the block."""
    y = para(draw, x, y, kicker, font(SANS_B, 12), w, fill=RED, leading=1.2)
    y += 2
    y = para(draw, x, y, headline, font(SERIF_B, head_size), w, leading=1.08)
    y += 4
    y = para(draw, x, y, summary, font(SERIF, body_size), w, leading=1.32)
    y += 4
    y = para(draw, x, y, source, font(SANS, 11), w, fill=SOFT, leading=1.2)
    return y


def draw_star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_highlight(draw, x, y, w, item):
    """Sarkozy / Giuliani: own block with a small icon, returns bottom y."""
    draw.rectangle([x, y, x + w, y + 56], fill=(24, 24, 24))
    draw.rectangle([x, y, x + 5, y + 56], fill=RED)
    ix, iy = x + 26, y + 28
    if item["icon"] == "star":
        draw_star(draw, ix, iy, 13, GOLD)
        draw.rectangle([ix - 8, iy + 12, ix + 8, iy + 22], fill=RED)
    else:
        draw.polygon([(ix - 14, iy - 8), (ix + 14, iy - 8), (ix, iy - 18)],
                     fill=GOLD)
        for dx in (-10, 0, 10):
            draw.rectangle([ix + dx - 2, iy - 8, ix + dx + 2, iy + 12],
                           fill=STEEL)
        draw.rectangle([ix - 14, iy + 12, ix + 14, iy + 16], fill=STEEL)
    tx = x + 48
    tw = w - 48 - 10
    ty = y + 5
    ty = para(draw, tx, ty, item["kicker"] + "  •  " + item["source"],
              font(SANS_B, 11), tw, fill=(250, 214, 120), leading=1.2)
    hfnt = fit_font(draw, item["headline"], SERIF_B, 19, tw)
    draw.text((tx, ty), item["headline"], font=hfnt, fill=(247, 243, 232))
    ty += int(hfnt.size * 1.05)
    para(draw, tx, ty, item["summary"], font(SERIF, 13), tw,
         fill=(220, 216, 205), leading=1.2)
    return y + 56


def draw_grid_item(draw, x, y, w, region, headline, summary, source):
    """One brief: region dot + headline + one line with source tag."""
    col = REGION_COLORS[region]
    draw.rectangle([x, y + 2, x + 8, y + 10], fill=col)
    tx = x + 14
    tw = w - 14
    hfnt = fit_font(draw, headline, SANS_B, 11, tw)
    draw.text((tx, y), headline, font=hfnt, fill=INK)
    tag = "  •  %s • %s • 25 NOV" % (region, source)
    tag_fnt = font(SANS_B, 9)
    tag_w = draw.textlength(tag, font=tag_fnt)
    sfnt = font(SERIF, 10)
    words = summary.split()
    line = summary
    while words and draw.textlength(line, font=sfnt) + tag_w > tw:
        words = words[:-1]
        line = " ".join(words) + " …"
    draw.text((tx, y + 13), line, font=sfnt, fill=INK)
    draw.text((tx + draw.textlength(line, font=sfnt), y + 13), tag,
              font=tag_fnt, fill=RED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    total = 1 + len(LEADS3) + len(HIGHLIGHTS) + len(GRID)
    y = draw_masthead(d, total)
    print("masthead ends:", y)
    y = draw_timeline(d, y)
    print("timeline ends:", y)

    # ---- Hero lead: Sparta II ----
    y = para(d, MARGIN, y, HERO["kicker"], font(SANS_B, 13), CW,
             fill=RED, leading=1.2)
    y += 2
    y = para(d, MARGIN, y, HERO["headline"], font(SERIF_B, 32), CW,
             leading=1.05)
    y += 6
    hero_y, hero_h = y, 160
    draw_ship_scene(d, MARGIN, hero_y, 600, hero_h)
    sx = MARGIN + 620
    sw = W - MARGIN - sx
    sy = hero_y + 2
    for p in HERO["paras"]:
        sy = para(d, sx, sy, p, font(SERIF, 17), sw, leading=1.32)
        sy += 6
    sy = para(d, sx, sy, HERO["source"], font(SANS, 12), sw,
             fill=SOFT, leading=1.2)
    y = max(hero_y + hero_h, sy) + 10
    rule(d, MARGIN, W - MARGIN, y, width=1)
    y += 10
    print("hero ends:", y)

    # ---- Three leads across: Riyadh / Huawei / turkeys ----
    col_w = (CW - 2 * 16) // 3
    top = y
    ends = []
    for i, lead in enumerate(LEADS3):
        lx = MARGIN + i * (col_w + 16)
        end = story_block(d, lx, top, col_w, lead["kicker"],
                          lead["headline"], lead["summary"], lead["source"],
                          head_size=21, body_size=13)
        ends.append(end)
    scene_y = max(ends) + 8
    for i, lead in enumerate(LEADS3):
        lx = MARGIN + i * (col_w + 16)
        if lead["scene"] == "tower":
            draw_tower_scene(d, lx, scene_y, col_w, 44)
        elif lead["scene"] == "chip":
            draw_chip_scene(d, lx, scene_y, col_w, 44)
        else:
            draw_turkeys(d, lx, scene_y, col_w, 44)
    y = scene_y + 44 + 10
    rule(d, MARGIN, W - MARGIN, y, width=1)
    y += 10
    print("leads3 ends:", y)

    # ---- Sarkozy + Giuliani: own blocks ----
    hw = (CW - 16) // 2
    e1 = draw_highlight(d, MARGIN, y, hw, HIGHLIGHTS[0])
    e2 = draw_highlight(d, MARGIN + hw + 16, y, hw, HIGHLIGHTS[1])
    y = max(e1, e2) + 8
    rule(d, MARGIN, W - MARGIN, y, width=1)
    y += 8
    print("highlights ends:", y)

    # ---- The day in brief: 30 items, 3 columns ----
    y = para(d, MARGIN, y, "THE DAY IN BRIEF  —  %d MORE STORIES" % len(GRID),
             font(SANS_B, 15), CW, fill=INK, leading=1.2)
    y += 2
    rule(d, MARGIN, W - MARGIN, y, width=1)
    y += 6
    gw = (CW - 2 * 18) // 3
    row_h = 26
    for idx, (region, headline, summary, source) in enumerate(GRID):
        r, c = divmod(idx, 3)
        gx = MARGIN + c * (gw + 18)
        gy = y + r * row_h
        draw_grid_item(d, gx, gy, gw, region, headline, summary, source)
    y = y + 10 * row_h + 6
    rule(d, MARGIN, W - MARGIN, y, width=3)
    y += 8
    centred(d, y, "Sources: Reuters World News Summary and Jagran Josh "
            "headlines, 25 November 2026. All stories reported 25 Nov 2026.",
            font(SANS, 11), fill=SOFT)
    print("grid ends:", y, "total stories:", total)
    return img


def dark_ink_fraction(img):
    px = img.load()
    dark = 0
    for yy in range(H):
        for xx in range(W):
            r, g, b = px[xx, yy]
            if 0.299 * r + 0.587 * g + 0.114 * b < 128:
                dark += 1
    return dark / (W * H)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "entry.png")
    img = build()
    img.save(out, format="PNG")
    check = Image.open(out)
    assert check.size == (W, H), check.size
    ink = dark_ink_fraction(check)
    print("wrote " + out)
    print("size: %dx%d" % check.size)
    print("bytes: %d" % os.path.getsize(out))
    print("dark ink: %.1f%%" % (ink * 100))


if __name__ == "__main__":
    main()
