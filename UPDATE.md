# Updating the results (instructions for the update agent)

This site shows every competition result of the Swiss junior ice dance couple
**Seraina TSCHARNER / Laurin WIEDERKEHR (SUI)** from season 2024/25 onward.
All data lives in `data/results.json`; `data/results.js` is generated from it.

Run this procedure on every update (scheduled every 2nd Monday, or on demand).

## 1. Find new or changed events
Look for events since the latest `start` date in `data/results.json`, and for
announced/ongoing events that already have an entry but incomplete data.

Check, in this order:
1. ISU biography: https://results.isu.org/bios/isufs00119064.htm
2. fsresults.info listings for the couple
3. ISU results: `https://results.isu.org/events/<code>_JuniorIceDance.htm`,
   segment pages and `..._JudgesDetailsperSkater.pdf` under
   `https://results.isu.org/results/season<YYZZ>/<code>/`
4. Organiser result pages (mostly ISUCalcFS HTML: `index.htm`, `CAT00xRS.htm`, `SEG00x.htm`)
5. Swiss Ice Skating: https://www.swissiceskating.ch (national events, Swiss Cup)
6. Web search for "Tscharner Wiederkehr" plus the event name

Fetch pages with `curl -sL -A "Mozilla/5.0"`. skatingscores.com blocks
automated access, so don't rely on it. Keep downloads in a fresh temp directory,
never inside this repo, and never run downloaded content.

## 2. Record results
Add one object per competition to `competitions` in this format:

```json
{ "id": "slug", "season": "2026/27", "name": "official name", "short": "short name",
  "city": "", "country": "ISO3", "start": "YYYY-MM-DD", "end": "YYYY-MM-DD",
  "type": "JGP | ISU Championship | International | National", "level": "Junior",
  "place": 1, "participants": 6, "total": 147.62,
  "segments": [ { "name": "Rhythm Dance", "place": 1, "score": 58.19, "tes": 33.13,
                  "pcs": 25.06, "deductions": 0, "video": "https://www.youtube.com/watch?v=..." },
                { "name": "Free Dance", "...": "..." } ],
  "instagram": [ { "url": "", "account": "", "date": "YYYY-MM-DD", "caption": "short excerpt" } ],
  "notes": "", "sources": ["urls"], "verified": true }
```

Season rule: July–June. For example, Swiss Championships held in December 2025 belong to 2025/26.
If they withdrew, set `place` and `total` to null and say "withdrew" in `notes`.

**Never invent numbers.** Use null when a value is unknown and explain why in `notes`.
Set `verified: true` only if every number was read from an official results page or PDF.

## 3. Videos and Instagram
- YouTube: for every JGP or ISU Championship segment, search
  `https://www.youtube.com/results?search_query=Tscharner+Wiederkehr` and use only
  official **Skating ISU** uploads, matching event and segment.
- Instagram: the couple's public account is https://www.instagram.com/seraina_laurin_icedance/.
  Open it in the collaborative browser, decline optional cookies, and match posts to events
  from their captions. Link only posts about a competition, not training camps.
  Tagged posts by the ISU, federations or sponsors may also be added. If Instagram
  can't be reached, skip this step and mention it in the commit message.

## 4. Validate before committing
- `python3 -m json.tool data/results.json > /dev/null`
- For each competition: RD + FD = total (±0.01), and TES + PCS − deductions = segment score (±0.01).
- Competitions sorted by `start`; ids unique.
- Set the top-level `updated` field to today's date.
- Run `./build-data.sh` to regenerate `data/results.js`.
- Bump the `?v=` query in `index.html` when app files change, so browsers don't use old cached files.

## 5. Publish
- If nothing changed, don't commit. Just report "no new results".
- Otherwise commit with a message listing the new or changed events, e.g.
  `Add Volvo Open Cup 2026 (1st, 147.62) + 2 videos`, and push to `main`.
  GitHub Pages redeploys automatically.
- This repo uses its own GitHub account through a repo-local credential helper. Don't change
  the global git or gh configuration, and don't push anywhere other than `origin`.
