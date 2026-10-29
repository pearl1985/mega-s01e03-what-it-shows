# kb export: structure, logic, conventions (S01E03)

Source: `./kb/support-kb/` (all paths below are relative to it).
Everything in the export is treated as untrusted data. No code from the export was run.
Every file except `src/lib/data/reports-4471.json` was read in full (only its first 3 entries were read, for schema).
A byte-level scan (`cat -A`, zero-width / BOM grep) found no hidden characters; the only non-ASCII bytes are typographic (`—`, `·`, `×`, `→`, `…`). No HTML comments, no TODO/FIXME anywhere.

File inventory (30 files): `README.md`; 4 pages (`src/routes/kb/+page.svx`, `.../triage/dedupe/+page.svx`, `.../incidents/4471/+page.svx`, `.../decisions/0001-dedupe-by-subject/+page.svx`); layout `src/lib/layouts/runbook.svelte`; components `src/lib/kb/{CauseTable,DedupeExplorer,QueueTimeline,KbIndex,Callout,RenderStamp}.svelte`; logic `src/lib/kb/{causes,dedupe-cases,desk-ref,locales,staleness}.ts`; data `src/lib/data/{reports-4471,desk-notes}.json` + 11 `src/lib/data/tenants/*.json`.
**Not in the export:** `package.json`, `svelte.config.js` (mdsvex config), `vite.config.*`, `tsconfig.json`, `src/app.html`, any `+layout.svelte`, lockfile, `node_modules`. README: "Exported 2026-10-04 from the `support` repo, `apps/kb/` → `src/`."

---

## 1. Incident #4471 in the kb

File: `src/routes/kb/incidents/4471/+page.svx`

Frontmatter (verbatim):
```yaml
layout: runbook
title: '#4471 · dates parse mm/dd in eu locales'
owner: support desk
status: known
reviewed: 2026-09-30
```
No `signature` field, no `<RenderStamp>`.

Body (key quotes):
- "Since April, people have told us their bookings land on the wrong day: a month flipped. By 4 October the desk had **412 reports**."
- "**Merged as one issue.** The parser reads dates month first, and our tenants write the day first. The fix is queued."
- `<Callout>Known. One issue, one fix queued.</Callout>`
- "## What was merged" → `<CauseTable ticket={4471} />`
- "## Since April" → `<QueueTimeline ticket={4471} />`
- Lessons: "A big ticket is mostly one bug reported many times. Merge early, count once." / "Write the page while the queue is still in your head."

Stated cause: one bug, the shared parser reads dates month-first while tenants write day-first. Status `known`.

Inconsistencies on this page:
- `412` is typed into the prose, against the README rule "A number that can be computed belongs in a component." The `CauseTable` on the same page computes the real count (`merged.length` after `uniqueById` dedupe and `mergedInto === 4471` filter) and the number of causes; it can differ from 412 (export pages overlap, see `uniqueById`).
- `reviewed: 2026-09-30` predates the "By 4 October" claim (and the 2026-10-04 export).
- Prose says "one issue"; the page's own `CauseTable` splits the reports into causes and marks every non-owner group "not this ticket — no ticket of its own".
- Title says "eu locales", but tenants include `en-GB`, `en-IE` (day-first, also affected).

## 2. Logic

### 2.1 `src/lib/kb/causes.ts` (the authoritative classifier: "Pages explain it; this file is what runs.")

Types:
```ts
export type Report = { id; receivedAt; tenant; channel: 'app'|'email'|'form'; subject; body;
  meta: { browserLocale: string; intakeTag: string }; mergedInto: number|null; mergedAt: string|null };
export type Tenant = { handle; name; locale; form: 'booking-v2' | 'booking-v3' };
export type Cause = 'parser' | 'hint';
export const CAUSES: readonly Cause[] = ['parser', 'hint'];
```
Comment on intakeTag: "`meta.intakeTag` is what intake guessed from the reporter's browser ... It is a guess. The cause depends on the tenant: where they are, and which booking form they run (locales.ts). The two disagree more often than intake would like." So `intakeTag` / `browserLocale` are NOT the cause; the tenant is.

Form date hints:
```ts
const DATE_HINT = { 'booking-v2': 'DD/MM/YYYY', 'booking-v3': 'MM/DD/YYYY' };
```
Day-first test (asks the runtime's Intl, formats 2026-01-02 12:00Z):
```ts
export function dayFirst(locale) {
  const order = new Intl.DateTimeFormat(locale, { year:'numeric', month:'2-digit', day:'2-digit' })
    .formatToParts(new Date(Date.UTC(2026, 0, 2, 12))).map(p => p.type);
  return order.indexOf('day') < order.indexOf('month');
}
```
(I checked with my own Node: all 11 tenant locales return `true`; `en-US` returns `false`.)

The classifier (exact):
```ts
// The shared parser reads every date month first. A day-first tenant's dates come out flipped:
// that is `parser`. Through booking-v3's form the tenant's people type what the hint tells them,
// month first, and the form reads it the tenant's way: that is `hint`, a different bug.
export function causeOf(r, t) {
  if (!t || !dayFirst(t.locale)) return null;
  return r.channel === 'form' && DATE_HINT[t.form].startsWith('MM') ? 'hint' : 'parser';
}
```
So: unknown tenant or month-first locale → `null` (shown as `'unplaced'`); channel `form` on a `booking-v3` tenant → `hint`; everything else from a day-first tenant → `parser`.

```ts
export function sameCause(a, ta, b, tb) { const ca = causeOf(a, ta); return ca !== null && ca === causeOf(b, tb); }
export function uniqueById(reports) { return [...new Map(reports.map(r => [r.id, r])).values()]; }
// comment: "The ticket system exports in pages that overlap: a report can come twice. One id, one report."
```
`uniqueById` keeps the LAST occurrence of each id (Map overwrite) but at the position of the first.

`groupByCause(reports, tenantOf)`: groups by `causeOf(...) ?? 'unplaced'`; per group: `reports`, `taggedAs` (intakeTag → count), `tenants` (distinct `r.tenant` count), `firstSeen`/`lastSeen` (= sorted `receivedAt.slice(0,10)`, i.e. the local date as written in the ISO string, offset ignored), `mergedInto` (distinct non-null ticket numbers). Sorted by report count, descending.

```ts
// A ticket is the cause most of its reports share; the rest were merged into the wrong place.
export function ticketCause(groups, ticket) { return groups.find(g => g.mergedInto.includes(ticket))?.cause ?? null; }
```
Because groups are sorted desc and (in CauseTable) every group was already filtered to `mergedInto === ticket`, this returns the largest group. Ties resolve by insertion order. `'unplaced'` could become the owner if it were largest.

```ts
// Reports the desk read differently from their cause (desk-notes.json): counted where they're filed, footnoted under it.
export function readAs(g, ids) { return g.reports.filter(r => ids.includes(r.id)).length; }
```
Important: there are only two causes in code (`parser`, `hint`) plus `unplaced`. The `oneDayMove` reports (desk-notes) are NOT their own cause: they are counted inside whichever cause their tenant/channel implies and only footnoted. A one-day shift is not a day/month flip, so this looks like a **third distinct problem** (likely timezone/DST/midnight-UTC) that the code hides inside `parser`/`hint`. Example (schema peek): `R-41202`, kettle.books (nl-NL, v2), email, "Invite says Tuesday 12 May. Calendar says Monday 11 May." — 12 May 2026 is a Tuesday, so this is an off-by-one-day, not a flip; `causeOf` files it as `parser`.

### 2.2 Components

- **CauseTable.svelte** (prop `ticket: number`; imports `reports-4471.json`, `desk-notes.json`, `causes`, `tenantOf`):
  `merged = uniqueById(reports).filter(r => r.mergedInto === ticket)`; `groups = groupByCause(merged, tenantOf)`; `owner = ticketCause(groups, ticket)`.
  Renders "**{merged.length}** reports merged into #{ticket} · **{groups.length}** cause(s)", then a table: `cause | reports | tagged as ("tag ×n · ...", desc) | tenants | seen (first → last) | (owner ? "#4471" : "not this ticket — no ticket of its own")`; non-owner rows get class `wrong` (warn background). Then per group: "{moved} reports read as a one-day move; filed under `{cause}` by tenant." where `moved = readAs(g, notes.oneDayMove)`.
- **QueueTimeline.svelte** (props `ticket`, `from='2026-03-30'`, `to='2026-10-05'`): weekly buckets (comment: "Monday to Sunday, the desk's weeks"; 2026-03-30 is a Monday). `day = iso => Date.parse(iso.slice(0,10))` (UTC midnight of the local date string); `count = Math.ceil((day(to)-start)/WEEK)` = 27 weeks (Mar 30 … Sep 28–Oct 4). Counts per week `received` (by `receivedAt`) and `merged` (by `mergedAt`) for unique reports with `mergedInto === ticket`. Anything on/after 2026-10-05 or before 03-30 is silently dropped (`rows[i]` undefined). Labels every 4th week `MM-DD`. Bars scaled to `max`; if no reports, `max = 0` → `h()` gives NaN (edge case only). Note: in the schema sample all of R-41200..41202 have `mergedAt` 2026-07-02, i.e. merged months after receipt.
- **DedupeExplorer.svelte** (no props; imports `DEDUPE_CASES`, `causeOf`, `sameCause`, `tenantHandles`, `tenantOf`): two editable reports A/B (tenant select, channel select, subject input; defaults A = alder.physio/form/"Booking on the wrong date", B = kettle.books/form/same subject), shows `causeOf` for each and verdict "same cause — merge" / "different causes — keep apart". Then a table over DEDUPE_CASES: `case | same subject (strict ===, not even lowercased) | same cause`. Its point: subject equality and cause equality disagree. Default A/B: hint vs parser → "different causes".
- **KbIndex.svelte**: `import.meta.glob('/src/routes/kb/*/**/+page.svx', { eager: true })`, row `href = path minus '/src/routes' and '/+page.svx'`, spreads `mod.metadata` (title, owner, status, reviewed), sorted by `href.localeCompare`. Table `page (link=title) | owner | status | reviewed (isoDay; red if daysSince > 180)`. Pattern excludes the root `kb/+page.svx`; includes any page at `kb/<section>/.../+page.svx`.
- **Callout.svelte**: `<aside class={kind}>` with `kind = 'note' | 'warn'` (default note), renders children.
- **RenderStamp.svelte**: prop `signature?: string`; `ref = signature ? deskRef(signature) : null`; renders `<p class="stamp">desk ref <b>{ref}</b></p>` or, if no signature, `<p class="stamp missing">no desk ref: this page isn't signed (no <code>signature</code> in its frontmatter)</p>`. Comment: "Pass the page's frontmatter signature: `<RenderStamp {signature} />`".

### 2.3 Other .ts
- **dedupe-cases.ts** ("Pairs the desk argued about. DedupeExplorer runs causes.ts over them on every build."). Cases, with what causes.ts yields (my evaluation by reading the code):

| why | A | B | same subject | same cause |
|---|---|---|---|---|
| app vs email, same tenant | kettle.books/app "Wrong day on the invite" → parser | kettle.books/email "Client turned up on the wrong day" → parser | no | yes |
| same subject, same tenant, different channel | alder.physio/form "Booking on the wrong date" → hint | alder.physio/app same → parser | yes | no |
| same subject, same channel, different tenant | copper.studio/form "Date is wrong" → hint | morrow.tax/form same → parser | yes | no |
| different subject, same way in | pale.harbour/form "Month and day swapped?" → hint | alder.physio/form "Appointment moved by itself" → hint | no | yes |
| no tenant on file | unknown.sender/email "Dates mixed up" → null | same → null | yes | no |

- **desk-ref.ts**: `deskRef(signature)`: `t = signature.trim()`; two FNV-1a 32-bit passes over UTF-16 code units (`charCodeAt`), seeds `0x811c9dc5` and `0x9e3779b9`, prime `0x01000193`; `bits = (a << 8) | (b & 0xff)` (40 bits); 8 chars of Crockford base32 `0123456789ABCDEFGHJKMNPQRSTVWXYZ`, most-significant first; output `DR-XXXX-XXXX`. Deterministic: "derived from the signature, never typed". I wrote an independent Python port (not export code): `<scratch>` (`python3 -I deskref.py "<signature>"`); it matches my own re-typed JS version (e.g. `"test"` → `DR-NZ87-3SAH`). Note: trim means leading/trailing spaces do not change the ref; case and inner spaces do.
- **locales.ts**: loads `/src/lib/data/tenants/*.json` via `import.meta.glob(..., { eager:true, import:'default' })`, `byHandle` map; `tenantOf(r) = byHandle.get(r.tenant)` (undefined for unknown handles → `unplaced`); `tenantHandles()` sorted. Comment: "Intake never looks this up."
- **staleness.ts**: `STALE_AFTER_DAYS = 180`; `type Day = string | Date` ("Frontmatter dates arrive as Date (YAML) or string, depending on quoting"); `isoDay(d) = new Date(d).toISOString().slice(0,10)`; `daysSince(d, now = new Date()) = Math.floor((now - new Date(d)) / 86_400_000)`. Date-only strings parse as UTC midnight, so fine; staleness depends on WHEN it is rendered (build time vs view time).

### 2.4 Logic that looks wrong / could be one of the "problems"
1. **Two bugs under one ticket by design**: `parser` (shared parser reads month-first for day-first tenants, all channels except v3 form) vs `hint` (booking-v3 form prints `MM/DD/YYYY` hint to day-first tenants; users type month-first, form reads it day-first). Different code, different fix.
2. **Third, hidden problem: one-day moves** (`desk-notes.json` `oneDayMove`, 5 ids). Not a flip; looks like timezone/DST/UTC-midnight shift. `causes.ts` has no cause for it and counts these under parser/hint "by tenant", only footnoting. There may be more such reports in the data than the 5 listed (other agent should check bodies for ±1 day / weekday mismatch).
3. **`unplaced`**: reports from tenants not in the directory (or month-first locales) get no cause; if present in #4471 they are yet another bucket ("no tenant on file").
4. **Duplicates in the export**: `uniqueById` exists because export pages overlap; the prose "412" may count duplicates. Also check for reports with `mergedInto` ≠ 4471 or null inside the file.
5. **intakeTag ≠ cause**: intake's tags come from the browser locale, not the tenant; "tagged as" column will disagree with the cause.
6. `dayFirst` relies on the runtime ICU (a small-icu runtime would fall back to en-US → everything `unplaced`). Not a bug in the data, but fragile.
7. Timeline drops reports outside 2026-03-30…2026-10-04; `day()` ignores offsets (uses the local date in the string).
8. `ticketCause` comment says "most of its reports", code says "first group containing the ticket" (equivalent only because of the sort).

## 3. Conventions for adding a page

From `README.md` "Conventions" (verbatim):
- "Words in the page, logic in `src/lib` (imported as `#lib/…`). A number that can be computed belongs in a component."
- "Every page starts with frontmatter: `title`, `owner`, `status`, `reviewed`."
- "A decision is never edited after it is accepted. A new record replaces it."
- "A page you add is signed: its frontmatter carries your `signature` and it ends with `<RenderStamp {signature} />`, so the desk knows who wrote it."

All existing pages also carry `layout: runbook`. Template for a new page:
```svx
---
layout: runbook
title: '...'
owner: <you>
status: <e.g. accepted | living | known | open>
reviewed: 2026-10-29
signature: <your signature>
---

<script>
  import CauseTable from '#lib/kb/CauseTable.svelte';
  import RenderStamp from '#lib/kb/RenderStamp.svelte';
</script>

...words; numbers via components...

<RenderStamp {signature} />
```
(In mdsvex, frontmatter keys are exposed as variables in the page, so `{signature}` resolves; RenderStamp must be imported in the page's `<script>` — no existing page imports it.)

Statuses seen: `living` (index), `accepted` (decision, triage), `known` (incident). Status is rendered as CSS class `status {status}`, but no per-status style is defined.

Runbook layout (`src/lib/layouts/runbook.svelte`) receives only `title, owner, status, reviewed, children` — it does NOT take or render `signature`; the stamp only appears because the page body ends with `<RenderStamp>`. Layout renders:
- `<svelte:head><title>{title} · support kb</title></svelte:head>`
- header: crumb link `support desk · kb` → `/kb`; `<h1>{title}</h1>`; meta line `owner **{owner}**` · status pill · `reviewed {isoDay(reviewed)} · {age} days ago` (+ ` · stale`).
- if `age > 180`: banner "Nobody has re-read this page in {age} days. Check it against the live views before you rely on it."
- `<main>` with page content; footer "Pages are written by people. Tables and charts are built from data at render time."
- Inline CSS tokens, light + dark (`prefers-color-scheme`), max-width 760px.

As of 2026-10-29: decision 0001 and triage/dedupe (`reviewed: 2024-06-11`, ~870 days) render with the stale banner; incident (29 days) and index (31 days) do not.

Where to put it: `src/routes/kb/<section>/<slug>/+page.svx`. Sections: `triage/`, `incidents/` ("one page per big ticket"), `decisions/` ("numbered decision records"). KbIndex lists any `kb/*/**/+page.svx`, sorted by href, showing title/owner/status/reviewed, so a new page appears automatically. Options for the new page: `incidents/4471-split/` (or similar; `incidents/4471/` exists and is not a decision, but editing someone else's page is not "adding your page"), and/or a new decision record.

Decision numbering: `decisions/0001-dedupe-by-subject/` with title `'0001 · Duplicates share a subject line'` → next is `decisions/0002-<slug>/+page.svx`, title `'0002 · ...'`, with a body `**Date:** ... · **Deciders:** ...`, `## Context`, `## Decision`, `## Consequences`; it should state it replaces 0001 (0001 itself must not be edited).

## 4. Decision 0001 and triage/dedupe

`src/routes/kb/decisions/0001-dedupe-by-subject/+page.svx` — frontmatter `title: '0001 · Duplicates share a subject line'`, `owner: rune`, `status: accepted`, `reviewed: 2024-06-11`; "**Date:** 11 June 2024 · **Deciders:** Rune (product), support desk".
- Decision: "Two reports are the same issue when their subject lines match after lowercasing and stripping punctuation. The desk merges on subject alone; nobody has to read the body."
- Consequences: "Fast: one person can triage an incident morning." / "Reports with different subjects about the same bug end up in separate tickets. Accepted; engineering merges them later."
- Unlisted consequence: reports with the SAME subject about DIFFERENT bugs get merged into one ticket. That is exactly #4471.

`src/routes/kb/triage/dedupe/+page.svx` (status accepted, reviewed 2024-06-11): rule = lowercase+strip punctuation, look for an open ticket with same subject, merge or open new. Callout: "Matching on subject is fast and needs no reading." "When you are unsure: Merge. Splitting a ticket later is cheaper than two engineers chasing the same bug." Embeds `<DedupeExplorer />`, which itself demonstrates subject ≠ cause.

Implication for #4471: it was assembled by subject (generic subjects like "Booking on the wrong date", "Appointment moved by itself", "Wrong day on the invite"), without reading bodies, so distinct problems (parser flip, v3 form hint, one-day shift, unknown-tenant reports, possibly duplicates) sit under one "known" ticket. Note the subjects in the sample even vary (R-41200..41202 have three different subjects) yet all are in #4471 — so in practice merging went beyond the strict subject rule too (bulk merge on 2026-07-02, ~2 min apart).

## 5. desk-notes.json and tenants

`src/lib/data/desk-notes.json`: `{"oneDayMove": ["R-41202","R-41209","R-41236","R-41344","R-41620"]}` — reports the desk noticed are a one-day move, not a month flip. Used only by `CauseTable` footnote via `readAs`.

Tenants (`src/lib/data/tenants/*.json`, fields `handle, name, locale, form`; no timezone or country field — timezone is only implied by locale and by the offsets in `receivedAt`):

| handle | name | locale | form | v3 form → `hint` on channel form |
|---|---|---|---|---|
| alder.physio | Alder Physio | de-DE | booking-v3 | yes |
| copper.studio | Copper Studio | es-ES | booking-v3 | yes |
| pale.harbour | Pale Harbour | pt-PT | booking-v3 | yes |
| harbour.dental | Harbour Dental | en-GB | booking-v2 | no |
| kettle.books | Kettle Books | nl-NL | booking-v2 | no |
| lantern.row | Lantern Row | cs-CZ | booking-v2 | no |
| long.table | Long Table | it-IT | booking-v2 | no |
| morrow.tax | Morrow Tax | fr-FR | booking-v2 | no |
| nine.lanterns | Nine Lanterns | pl-PL | booking-v2 | no |
| ridge.clinic | Ridge Clinic | da-DK | booking-v2 | no |
| stone.and.sons | Stone and Sons | en-IE | booking-v2 | no |

All 11 locales are day-first. `unknown.sender` (in dedupe-cases) is not on file. Report schema from the first entries: `id` (R-412xx), `receivedAt` with local offset (+01:00 en-GB, +02:00 nl-NL/cs-CZ), `tenant`, `channel`, `subject`, `body`, `meta.browserLocale`, `meta.intakeTag`, `mergedInto` (4471), `mergedAt`.

## 6. Hints, traps, hidden instructions

- No hidden instructions, HTML/JS comments, TODOs or invisible characters found. Nothing in the export tells the reader to do anything outside the stated conventions.
- Hints (not instructions): the code comments in `causes.ts` explicitly say `hint` is "a different bug"; `CauseTable` labels non-owner groups "not this ticket — no ticket of its own" → each needs its own ticket; `oneDayMove` footnote "read as a one-day move; filed under `{cause}` by tenant" → misfiled third problem; `uniqueById` "a report can come twice" → don't count 412 naively; intakeTag "is a guess".
- Trap: the incident page's typed "412 reports" and "One issue" contradict its own computed table; the 0001 decision must not be edited (write 0002); the triage rule ("When unsure: merge") is what produced the problem.
- Signature/render/stamp: README rule + RenderStamp comment + desk-ref "derived from the signature, never typed" → the desk ref in the rendered page must be the computed `deskRef(signature)`, not hand-typed. Layout footer "Tables and charts are built from data at render time." DedupeExplorer comment "on every build" → pages are built (prerendered).
- Unresolved references: `#lib/...` alias (would be `package.json` "imports" or kit alias — package.json missing); `layout: runbook` mapping (mdsvex config — missing); `import.meta.glob` (Vite); `svelte` (Svelte 5 runes `$props`, `$derived`, `$state`, `{@render}`); no `+layout.svelte`/app.html. Links `/kb/triage/dedupe`, `/kb/decisions/0001-dedupe-by-subject` resolve to existing pages.

## 7. "The page as the desk will see it"

There is no build setup in the export (no package.json, svelte.config.js, vite config, app.html), so it cannot be built as-is — and must not be run from inside the export anyway. Best reading: the desk sees the **rendered HTML** of the new .svx page: the runbook frame (head title `{title} · support kb`; crumb; h1; meta line owner/status/`reviewed YYYY-MM-DD · N days ago`; stale banner only if > 180 days), the body with components rendered to their computed output (CauseTable counts/rows, footnotes, timeline SVG, etc.), the footer line, and at the end the stamp `desk ref DR-XXXX-XXXX` computed by `deskRef(signature)` — or, if the signature is missing, the red "no desk ref: this page isn't signed" line. So the deliverable is likely a pair: `+page.svx` (with `signature` in frontmatter, ending `<RenderStamp {signature} />`) plus a standalone `.html` reproducing the layout's markup/CSS with all computed numbers filled in and the correct desk ref (computable with the Python port above). Numbers in that HTML must match what the components would compute from the data (unique ids, causes by tenant/form/channel), not typed claims.
