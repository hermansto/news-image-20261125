#!/usr/bin/env python3
"""THE WORLD TODAY - front page for 25 November 2026.

One day of real world news in a single 1024x1024 PNG, drawn with
Python stdlib + Pillow only. No external images, no real person's
face, no timestamps, no randomness: two runs are byte-identical.

Stories (all from the Reuters World News Summary published
25 November 2026):
  1. Zelenskiy confirms Ukraine hit the Russian ship Sparta II
     in the Gulf of Finland; Norway urges caution.
  2. Houthis hit Riyadh's tallest tower; 11 wounded.
  3. Huawei convicted in New York over its Iran business.
  4. Trump pardons turkeys Freedom and Feathers.
Also today: Sarkozy corruption case sent to trial; Giuliani
receives the Medal of Freedom.

Writes ONLY to os.environ.get("MAKEFUN_OUTPUT_DIR", "/output").
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36
CW = W - 2 * MARGIN  # 952 usable width

PAPER = (247, 243, 232)
INK = (18, 18, 18)
SOFT = (74, 74, 74)
RED = (158, 27, 27)
SKY = (186, 208, 224)
SEA = (105, 145, 172)
SEA_DARK = (70, 105, 135)
SMOKE = (120, 120, 118)
STEEL = (52, 52, 58)
GOLD = (176, 132, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
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


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.35):
    """Draw wrapped paragraph; return y just below the last line."""
    size = fnt.size
    step = int(size * leading)
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


def draw_masthead(draw):
    y = 26
    y = centred(draw, y, "ONE DAY  -  ONE PAGE  -  THE WORLD IN BRIEF",
                font(SANS_B, 15), fill=RED)
    y += 2
    y = centred(draw, y, "THE WORLD TODAY", font(SERIF_B, 80))
    y -= 6
    rule(draw, MARGIN, W - MARGIN, y, width=3)
    y += 7
    rule(draw, MARGIN, W - MARGIN, y, width=1)
    y += 10
    left = "WEDNESDAY, 25 NOVEMBER 2026"
    right = "FOUR STORIES  -  ALL VERIFIED"
    draw.text((MARGIN, y), left, font=font(SANS_B, 17), fill=INK)
    rw = draw.textlength(right, font=font(SANS_B, 17))
    draw.text((W - MARGIN - rw, y), right, font=font(SANS_B, 17), fill=INK)
    y += 30
    rule(draw, MARGIN, W - MARGIN, y, width=1)
    return y + 12


def draw_ship_scene(draw, x, y, w, h):
    """Gulf of Finland: cargo ship Sparta II, smoke, rescue spray."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun + clouds
    draw.ellipse([x + w - 92, y + 14, x + w - 34, y + 72], fill=(250, 238, 190))
    for cx, cy, r in ((x + 60, y + 34, 26), (x + 92, y + 30, 32),
                      (x + 124, y + 36, 24), (x + 300, y + 22, 22),
                      (x + 328, y + 26, 28)):
        draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                     fill=(240, 240, 236))
    # sea
    sea_y = y + h * 0.55
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(3):
        wy = sea_y + 12 + i * 20
        draw.arc([x + 20 + i * 30, wy, x + 150 + i * 30, wy + 26],
                 200, 340, fill=(210, 225, 235), width=3)
    # cargo ship: hull, containers, bridge, funnel, smoke
    hx, hy = x + 90, sea_y - 6
    draw.polygon([(hx, hy), (hx + 330, hy), (hx + 300, hy + 52),
                  (hx + 18, hy + 52)], fill=(122, 32, 28))
    draw.rectangle([hx + 30, hy - 58, hx + 300, hy], fill=(52, 52, 58))
    for i, col in enumerate(((176, 132, 40), (36, 82, 110), (122, 32, 28))):
        draw.rectangle([hx + 44 + i * 82, hy - 52, hx + 118 + i * 82, hy - 8],
                       fill=col, outline=INK, width=2)
    draw.rectangle([hx + 300, hy - 74, hx + 336, hy], fill=(240, 240, 236),
                   outline=INK, width=2)
    draw.rectangle([hx + 306, hy - 96, hx + 330, hy - 74], fill=STEEL)
    for i, r in enumerate((30, 38, 46)):
        draw.ellipse([hx + 296 + i * 8, hy - 92 - i * 14,
                      hx + 296 + i * 8 + r, hy - 92 - i * 14 + r // 2],
                     fill=SMOKE)
    # drone + rescue spray
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
    draw.ellipse([x + w - 66, y + 8, x + w - 26, y + 48], fill=(250, 238, 190))
    base = y + h
    for tx, f, tw in ((0, 0.72, 92), (96, 0.58, 74), (174, 0.82, 104),
                      (282, 0.64, 82), (368, 0.46, 66)):
        th = int(h * f)
        draw.rectangle([x + tx, base - th, x + tx + tw, base],
                       fill=(138, 142, 162), outline=(90, 100, 130), width=1)
    # tallest tower, centre, with lit windows and a strike flash
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
    draw.text((x + 10, y + h - 26), "RIYADH AT DUSK", font=font(SANS_B, 13),
              fill=INK)


def draw_chip_scene(draw, x, y, w, h):
    """A chip on trial: circuit board, chip, pins; scales with h."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    for i in range(5):
        yy = y + 10 + i * max(1, h // 5)
        draw.line([(x + 12, yy), (x + w - 12, yy)], fill=(190, 184, 168), width=1)
    cx, cy = x + w // 2, y + h // 2
    half = max(20, int(h * 0.34))
    for d in (-22, 0, 22):
        draw.line([(cx + d, cy - half), (cx + d, cy - half - 8)],
                  fill=GOLD, width=4)
        draw.line([(cx + d, cy + half), (cx + d, cy + half + 8)],
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
    draw.text((x + 10, y + h - 26), "THE CHIP ON TRIAL", font=font(SANS_B, 13),
              fill=SOFT)


def draw_turkeys(draw, x, y, w, h):
    """Two pardoned turkeys: fan tails, round bodies, no faces of people."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    for k, tx in enumerate((x + 5, x + w - 87)):
        ty = y + h // 2 + 6
        for a in range(-50, 51, 25):
            import math
            rad = math.radians(a - 90)
            ex = tx + 52 + int(46 * math.cos(rad))
            ey = ty - 6 + int(46 * math.sin(rad))
            draw.line([(tx + 52, ty - 6), (ex, ey)], fill=(122, 84, 40), width=7)
        draw.ellipse([tx + 22, ty - 34, tx + 82, ty + 26], fill=(122, 84, 40))
        draw.ellipse([tx + 36, ty - 52, tx + 68, ty - 18], fill=(96, 62, 28))
        draw.polygon([(tx + 52, ty - 50), (tx + 46, ty - 60),
                      (tx + 58, ty - 60)], fill=(176, 132, 40))
        label = "FREEDOM" if k == 0 else "FEATHERS"
        draw.text((tx + 8, y + h - 13), label, font=font(SANS_B, 12), fill=SOFT)


def story_block(draw, x, y, w, kicker, headline, summary, source,
                head_size=34, body_size=19):
    """Kicker + headline + summary + source; returns y below the block."""
    y = para(draw, x, y, kicker, font(SANS_B, 14), w, fill=RED, leading=1.2)
    y += 2
    y = para(draw, x, y, headline, font(SERIF_B, head_size), w,
             leading=1.08)
    y += 4
    y = para(draw, x, y, summary, font(SERIF, body_size), w, leading=1.32)
    y += 4
    y = para(draw, x, y, source, font(SANS, 13), w, fill=SOFT, leading=1.2)
    return y


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = draw_masthead(d)

    # ---- Lead story: Ukraine / Sparta II ----
    y = para(d, MARGIN, y, "LEAD STORY  -  GULF OF FINLAND",
             font(SANS_B, 14), CW, fill=RED, leading=1.2)
    y += 2
    y = para(d, MARGIN, y, "Zelenskiy confirms Ukraine hit Russian ship",
             font(SERIF_B, 42), CW, leading=1.05)
    y += 6
    hero_y, hero_h = y, 180
    draw_ship_scene(d, MARGIN, hero_y, 600, hero_h)
    sx = MARGIN + 620
    sw = W - MARGIN - sx
    sy = hero_y + 2
    sy = para(d, sx, sy,
              "President Volodymyr Zelenskiy confirmed Ukraine was behind "
              "Saturday's drone strike on the Russian cargo ship Sparta II.",
              font(SERIF, 18), sw, leading=1.32)
    sy += 8
    sy = para(d, sx, sy,
              "Norway urged caution. The ship was towed back and is "
              "anchored in St Petersburg.",
              font(SERIF, 18), sw, leading=1.32)
    sy += 8
    sy = para(d, sx, sy, "Source: Reuters, 25 Nov 2026", font(SANS, 13),
             sw, fill=SOFT, leading=1.2)
    y = max(hero_y + hero_h, sy) + 12
    rule(d, MARGIN, W - MARGIN, y, width=1)
    y += 14

    # ---- Row two: Riyadh + Huawei (text first, scenes below it) ----
    col_w = (CW - 24) // 2
    x2 = MARGIN + col_w + 24
    top = y
    end1 = story_block(d, MARGIN, top, col_w,
                       "THE GULF  -  RIYADH",
                       "Houthis hit Riyadh's tallest tower",
                       "Yemen's Houthi fighters struck the tallest tower "
                       "in Riyadh on Tuesday, wounding at least 11 people, "
                       "Saudi Civil Defense said. It was the second strike "
                       "on the tower in less than a week.",
                       "Source: Reuters, 25 Nov 2026",
                       head_size=28, body_size=17)
    end2 = story_block(d, x2, top, col_w,
                       "TECH ON TRIAL  -  NEW YORK",
                       "Huawei convicted over Iran business",
                       "A New York jury convicted China's Huawei on Tuesday "
                       "of deceiving banks about its business in Iran and "
                       "stealing trade secrets. The case began in 2018.",
                       "Source: Reuters, 25 Nov 2026",
                       head_size=28, body_size=17)
    scene_y = max(end1, end2) + 8
    draw_tower_scene(d, MARGIN, scene_y, col_w, 80)
    draw_chip_scene(d, x2, scene_y, col_w, 80)
    y = scene_y + 80 + 12
    rule(d, MARGIN, W - MARGIN, y, width=1)
    y += 12

    # ---- Row three: turkeys + also today ----
    draw_turkeys(d, MARGIN, y, 200, 110)
    text_end = story_block(d, MARGIN + 220, y, CW - 220,
                           "WASHINGTON  -  THANKSGIVING EVE",
                           "Trump spares turkeys Freedom and Feathers",
                           "President Donald Trump pardoned two turkeys, "
                           "Freedom and Feathers, on Tuesday in the annual "
                           "White House Thanksgiving ritual.",
                           "Source: Reuters, 25 Nov 2026",
                           head_size=26, body_size=18)
    y = max(y + 110, text_end) + 8
    rule(d, MARGIN, W - MARGIN, y, width=1)
    y += 8
    d.rectangle([MARGIN, y, W - MARGIN, y + 44], fill=(24, 24, 24))
    also = ("ALSO TODAY:  France orders former president Sarkozy's "
            "corruption case to trial  -  Trump awards Rudy Giuliani the "
            "Medal of Freedom.")
    for i, line in enumerate(wrap(d, also, font(SANS_B, 15), CW - 24)):
        d.text((MARGIN + 12, y + 5 + i * 19), line, font=font(SANS_B, 15),
               fill=(247, 243, 232))
    y += 52
    rule(d, MARGIN, W - MARGIN, y, width=3)
    y += 8
    centred(d, y, "Sources: Reuters World News Summary, 25 November 2026. "
            "All stories reported on 25 November 2026.",
            font(SANS, 13), fill=SOFT)
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
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    check = Image.open(path)
    assert check.size == (W, H), check.size
    ink = dark_ink_fraction(check)
    print(f"wrote {path}")
    print(f"size: {check.size[0]}x{check.size[1]}")
    print(f"bytes: {os.path.getsize(path)}")
    print(f"dark ink: {ink * 100:.1f}%")


if __name__ == "__main__":
    main()
