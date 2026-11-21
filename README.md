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

Nothing is asserted that a wire did not file. `build/stories.json` is the selection as written by
hand: for each line, a substring of a real headline and the label the page prints.
`build/resolve.py` matches those substrings against the 765 items 46 feeds carried on the day and
writes `build/resolved.json`, which supplies each line's UTC time, place tag and source — and stops
the build if any story falls outside 20 November 2026 UTC. That check caught four stories that
looked like Friday's and were not, including the Shenzhen summit and the COP31 cover text.

`build/render.py` draws the page from that file. `SOURCES.md` lists all 47 stories with the
headline as the wire published it and a link to it.

| | |
|---|---|
| `main.ts` | the entry: check the PNG the way the gate does, copy it to `/output/entry.png` |
| `entry.png` | the page: 1024x1024, 212,191 bytes |
| `SOURCES.md` | every story on the page, its UTC filing time, the wire and the link |
| `build/` | the harvest's selection, the resolver and the renderer |

## Licence

MIT. The page is drawn from headlines and facts the named wires published; the composition, the
selection and the code are this repository's own.
