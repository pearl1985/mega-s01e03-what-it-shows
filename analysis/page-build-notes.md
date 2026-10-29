# Page build notes: #4471 "what it shows" (S01E03)

Sources: kb export (pristine, untouched) `./kb/support-kb/`;
work copy `./work-kb/` (`diff -rq` shows only the 5 additions below).

## Files created (all in work-kb unless noted)
- `package.json` — `{"type":"module","imports":{"#lib/*":"./src/lib/*"}}`
- `src/lib/data/tickets-4471.json` — keys parser / hint / oneDayMove, fields `issue` (placeholder
  `https://github.com/OWNER/REPO/issues/1..3`), `title`.
- `src/lib/kb/split.ts` — `mergedInto(reports, ticket)`, `splitTicket(reports, ticket, tenantOf, oneDayMove)`
  → `Problem[]` {key, label, count, tenants[], channels{}, firstSeen, lastSeen, taggedAs{}, mistagged, ids[]},
  `totals(reports, problems, ticket)` → {rows, unique, duplicates, merged, subjects, mistagged}; `LABELS`.
  `tenantOf` is a parameter (same as `groupByCause`) so split.ts does not import locales.ts
  (which needs Vite's `import.meta.glob`) and can run in plain Node.
- `src/lib/kb/TicketTable.svelte` — props `{ ticket }`, `$props`/`$derived`, same table/CSS classes as
  CauseTable (`.sum`, `.tags`, `.note`, `.wrong`). Columns: problem (key + label) | reports | tagged as |
  tenants (count, handles in title) | seen | ticket (link from tickets-4471.json; a problem without an
  entry gets the `.wrong` row and "no ticket yet"). Sum line: "412 reports merged into #4471 · 3 problems ·
  427 rows, 15 duplicates removed". Note line: "12 distinct subjects across the 412 reports · intake's tag
  disagrees with the tenant's cause 38 times."
- `src/routes/kb/incidents/4471-what-it-shows/+page.svx` — the page.
- (outside work-kb) `./scripts/verify-split.mjs`.

## Computed (Node run of the kb's own causes.ts / split.ts / desk-ref.ts)
| problem | reports | tenants | channels | tagged as | mistagged | seen |
|---|---|---|---|---|---|---|
| parser | 374 | 11 | app 202, email 147, form 25 | parser 351, hint 23 | 23 | 2026-04-01 → 2026-10-04 |
| hint | 33 | 3 (alder.physio, copper.studio, pale.harbour) | form 33 | hint 18, parser 15 | 15 | 2026-04-17 → 2026-09-22 |
| oneDayMove | 5 | 5 (alder.physio, kettle.books, lantern.row, nine.lanterns, pale.harbour) | email 3, app 2 | parser 5 | 0 | 2026-04-02 → 2026-10-04 |

Totals: rows 427, unique 412, duplicates 15, merged 412, subjects 12, mistagged 38.
Cross-check: CauseTable's own grouping gives parser=379, hint=33 (379 − 5 = 374).
oneDayMove ids: R-41202, R-41209, R-41236, R-41344, R-41620 (all filed under `parser` by causes.ts).

"mistagged" = intakeTag ≠ causeOf(report, tenant) (causes.ts rule), which gives the decided 38.
If one-day moves tagged `parser` were counted as wrong too (intake has no tag for them), it would be 43.

Desk refs (deskRef from desk-ref.ts, confirmed by the independent Python port in scratchpad):
- `SIGNATURE_PLACEHOLDER` → `DR-Z3HV-58YZ` (will change when the real signature is put in)
- `test` → `DR-NZ87-3SAH` (confirmed)

## How the verification ran
- Node v22.22.1 here is built WITHOUT TypeScript support: `.ts` → `ERR_NO_TYPESCRIPT`
  (`--experimental-strip-types` does not help; amaro is missing from this distro build).
- Workaround: typescript 6.0.3 installed **offline from the local npm cache** (no network,
  `--ignore-scripts`) into the scratchpad `.../scratchpad/tsdeps`; the script registers
  `module.registerHooks` (resolve: `#lib/...` → `src/lib/...` + `.ts` when extensionless; load:
  `ts.transpileModule`, types removed, no type check).
- locales.ts uses `import.meta.glob` (Vite-only), not JSON imports, so it cannot run in Node at all.
  Not modified; the script builds the same `tenantOf` from `src/lib/data/tenants/*.json`.
- Extensionless imports (`#lib/kb/causes`) also do not resolve in plain Node ESM even with the
  package.json map; Vite resolves them. Hence the resolve hook.
- Run: `node ./scripts/verify-split.mjs ./work-kb`
  (env `TS_DEPS` = dir whose node_modules has typescript).

## Conventions / choices to review
- Route `incidents/4471-what-it-shows/` kept: README says incidents/ is "one page per big ticket";
  a sibling of `incidents/4471/` sorts next to it in KbIndex. Alternative would be a decision 0002
  (replaces 0001); not created (one page only). The page says replacing 0001 is its own record.
- `status: proposed` is a new status value (existing: living, accepted, known); the layout renders it as
  a class with no special style, so it is harmless.
- `owner: harness` as instructed.
- Prose has no counts; the title's "three" was given by you. The callout avoids a number. Ids that are
  names (0001, #4471, MM/DD/YYYY) remain. Subject quoted in prose, "Wrong day on the invite", was checked:
  it occurs in all three problems (parser 44, hint 5, oneDayMove 1).
- The existing 4471 page and decision 0001 are untouched; the new page links to both.
- `reviewed: 2026-10-29` unquoted → YAML Date; staleness.ts handles both.

## What a SvelteKit + mdsvex build needs (for "as the desk will see it")
npm devDependencies: `svelte@^5` (runes, `{@render}`, Snippet), `@sveltejs/kit@^2`, `@sveltejs/vite-plugin-svelte`,
`vite`, `mdsvex`, `@sveltejs/adapter-static` (prerender to HTML), `typescript` (lang="ts" in components).
Files to add (not in export): `svelte.config.js`, `vite.config.ts`, `src/app.html`, optional `tsconfig.json`,
`src/routes/+layout.js` with `export const prerender = true`.

svelte.config.js sketch:
```js
import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { mdsvex } from 'mdsvex';
import { fileURLToPath } from 'node:url';
export default {
  extensions: ['.svelte', '.svx'],
  preprocess: [vitePreprocess(), mdsvex({ extensions: ['.svx'],
    layout: { runbook: fileURLToPath(new URL('./src/lib/layouts/runbook.svelte', import.meta.url)) } })],
  kit: { adapter: adapter(), alias: { '#lib': 'src/lib', '#lib/*': 'src/lib/*' } },
};
```
Notes: mdsvex passes frontmatter as props to the layout and exposes it as variables in the page,
so `{signature}` resolves. Check mdsvex 0.12 vs Svelte 5: layouts with `$props()` + `children`
snippet need a Svelte-5-compatible mdsvex (0.12.x). The `#lib` alias can come from kit `alias` or from
package.json `imports` (Vite honours subpath imports; with the map `./src/lib/*` extensionless .ts imports
are resolved by Vite). `import.meta.glob('/src/...')` is root-relative: run Vite from work-kb. Staleness
is computed at build time (`new Date()`), so build on 2026-10-29 for "0 days ago".
