# THE WORLD TODAY — 25 November 2026

[![Bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/hermansto/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/hermansto/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One day of real world news in a single 1024x1024 front page, drawn
programmatically with Python + Pillow. No external images, no real
person's face. Every story is from the Reuters World News Summary
published 25 November 2026.

## Stories

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

Also today: France orders former president Sarkozy's corruption case
to trial; Trump awards Rudy Giuliani the Medal of Freedom.

## Run

```sh
MAKEFUN_OUTPUT_DIR=/tmp/news25-out python3 main.py
```

Writes only `entry.png` into that directory (default `/output`).
Deterministic: two runs produce byte-identical output.
