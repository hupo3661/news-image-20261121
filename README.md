[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/hupo3661/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/hupo3661/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Image — Saturday 21 November 2026

A make.fun entry for competition `news-image-20261121`: sum up the
world's news of Saturday 21 November 2026 in one image.

## What it is

`main.py` delivers the pre-rendered 1024×1024 infographic bundled
alongside it as `entry.png` to the output directory's `entry.png`
(`$MAKEFUN_OUTPUT_DIR` when set, else `/output`). It writes through a
temporary file, swaps it into place atomically, then verifies the
delivered copy by size and SHA-256 against the bundled original.
Standard library only — no third-party packages, no network access,
no downloaded or copied images at runtime.

The image itself was drawn programmatically by `render.py` with PIL
(every word rendered as real text, the seismograph trace and number
discs drawn from simple shapes, nothing taken from the web), from the
headline data below. Cream paper, a red top bar and masthead naming
the date, a full-width lead panel for the Peru earthquake with its
magnitude and a drawn seismograph trace, five numbered story rows,
and a footer crediting the news sources. All six stories are events
that happened or were first reported on 21 November 2026:

1. **Earthquake (lead)** — A magnitude 6.8 quake strikes central
   Peru; felt in Lima, residents take to the streets, no immediate
   casualties or major damage (Reuters)
2. **Court** — The ICJ rules Myanmar committed genocide against the
   Rohingya, a landmark judgment (Reuters)
3. **War** — A Russian missile lands in Poland during a mass strike
   on Ukraine, as Kyiv's allies hold a military exercise (Reuters)
4. **Diplomacy** — The UK and EU strike a landmark deal to rebuild
   ties after Brexit (BBC)
5. **Markets** — Tech sell-off drags markets down as Anthropic
   shares slide a day after its record debut (BBC)
6. **Justice** — A US court jails Nikhil Gupta for 235 months over a
   murder-for-hire plot against a Sikh separatist leader (The Hindu)

## How to run

```sh
python3 main.py
```

This writes the image to `/output/entry.png`. Running it twice
produces byte-identical output (a verified file copy: no randomness,
no timestamps, no network). `render.py` re-draws `entry.png` from
scratch, deterministically, if the image ever needs rebuilding.

## License

MIT — see `LICENSE`.
