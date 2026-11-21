# makefun-front-page

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/duchuAz/makefun-front-page/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/duchuAz/makefun-front-page/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**Friday 20 November 2026, as a front page.** One image, 1024 by 1024: a dated masthead, three
leads, the day in six numbers, and 44 more stories in four columns running from 00:02 to 23:39 UTC.
No photograph, no stock art, no news feed at run time — every mark on it is type and rule drawn by
`build/render.py` on newsprint cream.

The page is built to be read as a clock. Each line carries the UTC time the story was first filed
and the wire that carried it, so the grid reads down each column from the first filing of the day to
the last. Above the fold sits the day's weight rather than its clock: the missile attack on Kyiv's
bridges, the AI trade melting down a day after Anthropic's record debut, and COP31 running past its
deadline over the words "fossil fuel". A date-check panel at the foot names what was deliberately
left out and why — the Shenzhen summit and the World Court's genocide ruling were Thursday's news,
and Zelensky calling Putin a "killer" was Saturday's.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` needs Node 22 and nothing else. It reads `entry.png` from the repository and re-checks it
against the gate's own rules before copying it to `/output/entry.png`: the PNG signature, every
chunk's CRC, an IEND that ends the file, the IHDR's 1024 by 1024, and the 1 MiB cap. A file that
would be listed with a Valid of 0 is refused with the reason, rather than submitted.

## How the page was made

Nothing is asserted that a wire did not file. The day was harvested at build time: 46 feeds — BBC,
Al Jazeera, Google News, The Hindu, NDTV, Dawn, SCMP, DW, France 24, the Guardian, NPR, CBC, ABC,
Sky, Moscow Times, Japan Times, Straits Times, RNZ, allAfrica, Punch, Premium Times, the Buenos
Aires Times, the Rio Times, the Jerusalem Post, Bangkok Post, Philstar, VnExpress and more — carried
765 items on 20 November 2026. Each story on the page was then matched back to the item that filed
it first, and the build stopped on any story whose filing time fell outside that UTC day. That check
caught four that looked like Friday's and were not: the Shenzhen summit and the COP31 cover text
were Thursday's, and Zelensky calling Putin a "killer" was Saturday's.

`build/render.py` carries the result of that work as `DATA` — every line with the UTC time it was
first filed, the place tag, the wire and the label the page prints — and draws the image from it.
Running it in a clone rewrites `entry.png` byte for byte; the harvest dump and the resolver that
produced `DATA` are build inputs and are not committed, so the repository needs no network and no
feed to reproduce the page. `SOURCES.md` lists all 47 stories with the headline as the wire
published it, its UTC time and a link to it.

| | |
|---|---|
| `main.ts` | the entry: check the PNG the way the gate does, copy it to `/output/entry.png` |
| `entry.png` | the page: 1024x1024, 212,191 bytes |
| `SOURCES.md` | every story on the page, its UTC filing time, the wire and the link |
| `build/render.py` | the page's data and the renderer that draws `entry.png` from it |

## Licence

MIT. The page is drawn from headlines and facts the named wires published; the composition, the
selection and the code are this repository's own.
