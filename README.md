# S01E03 · what it shows

Course work for MEGA.dev, Challenge S01E03. A support desk merged 412 reports about wrong dates into one ticket, #4471, and marked it known. This repo holds one issue per problem found in #4471, each with how many reports it covers, and a signed page about them added to the desk's knowledge base (kb) export.

## Issues

| problem | reports | issue |
|---|---|---|
| `parser`: shared parser reads day-first dates month first | 374 | https://github.com/pearl1985/mega-s01e03-what-it-shows/issues/1 |
| `hint`: booking-v3 hints MM/DD/YYYY, reads the day first | 33 | https://github.com/pearl1985/mega-s01e03-what-it-shows/issues/2 |
| `oneDayMove`: date shifts by one day (timezone / day boundary) | 5 | https://github.com/pearl1985/mega-s01e03-what-it-shows/issues/3 |

412 unique reports (427 rows, 15 duplicates removed).

## Page

- Source: `support-kb/src/routes/kb/incidents/4471-what-it-shows/+page.svx`, with the logic it uses
  (`support-kb/src/lib/kb/split.ts`, `support-kb/src/lib/kb/TicketTable.svelte`) and the issue links
  (`support-kb/src/lib/data/tickets-4471.json`).
- Rendered: `rendered/kb/incidents/4471-what-it-shows/index.html` (text version: `rendered/4471-what-it-shows.txt`).
  `rendered/` is the full static build of the kb, built 2026-10-29.
- Signature: `Slawek Michrowski` · desk ref `DR-2ZEV-HMQY`.

## Rebuild

```sh
cd support-kb && npm install && npm run build
```

Output goes to `support-kb/build/`. The "reviewed … days ago" line is computed at build time.
`support-kb/` is the kb export plus the new page and the SvelteKit scaffolding needed to build it
(`package.json`, `svelte.config.js`, `vite.config.ts`, `tsconfig.json`, `src/app.html`, `src/routes/+layout.js`).

## analysis/

How the reports were read and counted: `reports-clusters.md` / `.json` (reports grouped by cause),
`kb-structure.md` (how the kb export is built), `page-build-notes.md` (how the page was written and checked),
`scripts/` (the Python and Node scripts used for the counts and the check of `split.ts`).
