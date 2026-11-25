# THE WORLD TODAY — 25 November 2026

[![Bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/hermansto/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/hermansto/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One day of real world news in a single 1024x1024 front page: 36 stories,
all published 25 November 2026. No external images, no real person's
face. Every story carries its source and date on the page.

## Stories

Lead stories:

1. **Zelenskiy confirms Ukraine hit Russian ship** — Ukraine behind
   Saturday's drone strike on the cargo ship Sparta II in the Gulf of
   Finland; Norway urges caution. (Reuters, 25 Nov 2026)
2. **Houthis hit Riyadh's tallest tower** — 11 wounded, Saudi Civil
   Defense said; second strike on the tower in less than a week.
   (Reuters, 25 Nov 2026)
3. **Huawei convicted over Iran business** — New York jury convicts
   China's Huawei of deceiving banks about its Iran business and
   stealing trade secrets. (Reuters, 25 Nov 2026)
4. **Trump spares turkeys Freedom and Feathers** — annual White House
   Thanksgiving pardon. (Reuters, 25 Nov 2026)

Also in their own blocks: France orders former president Sarkozy's
corruption case to trial, and Trump awards Rudy Giuliani the Medal of
Freedom. (Reuters, 25 Nov 2026)

Plus 30 more stories in "The Day in Brief", each tagged with its
region, source and date — from the Reuters World News Summary and the
Jagran Josh headlines, both published 25 November 2026.

## How it is built

- `draw.py` renders `entry.png` with Pillow on the builder's own
  machine. It is a local build tool and is never run by the grader.
- `main.py` is the program the grader runs: standard library only,
  it copies the finished `entry.png` into the output directory and
  verifies the copy (PNG magic, 1024x1024, byte-identical, sha256).

## Run

```sh
python3 draw.py            # re-render entry.png (local, needs Pillow)
MAKEFUN_OUTPUT_DIR=/tmp/news25-out python3 main.py   # ship it
```

`main.py` writes only `entry.png` into that directory (default
`/output`). Deterministic: two runs produce byte-identical output.
