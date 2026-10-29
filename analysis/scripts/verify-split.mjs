// Runs the kb's own TypeScript (causes.ts, desk-ref.ts, split.ts) from work-kb with Node 22 type stripping.
// usage: node ./scripts/verify-split.mjs ./work-kb
import { registerHooks } from 'node:module';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

// This Node build has no built-in type stripping (ERR_NO_TYPESCRIPT), so .ts files are
// transpiled with the typescript package (TS_DEPS: a dir whose node_modules has typescript).
const tsDeps = process.env.TS_DEPS ?? '<scratch>
const ts = createRequire(join(tsDeps, 'package.json'))('typescript');

const root = process.argv[2] ?? './work-kb';
const lib = join(root, 'src/lib');

// '#lib/kb/causes' has no extension (Vite resolves it); Node ESM does not, so add .ts here.
registerHooks({
  resolve(spec, ctx, next) {
    if (spec.startsWith('#lib/')) {
      const p = join(lib, spec.slice(5));
      const file = existsSync(p) ? p : p + '.ts';
      return { url: pathToFileURL(file).href, shortCircuit: true };
    }
    return next(spec, ctx);
  },
  load(url, ctx, next) {
    if (url.endsWith('.ts')) {
      const src = readFileSync(fileURLToPath(url), 'utf8');
      const out = ts.transpileModule(src, { compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022, verbatimModuleSyntax: false } });
      return { format: 'module', source: out.outputText, shortCircuit: true };
    }
    return next(url, ctx);
  },
});

const json = (p) => JSON.parse(readFileSync(join(lib, p), 'utf8'));
const reports = json('data/reports-4471.json');
const notes = json('data/desk-notes.json');
const tickets = json('data/tickets-4471.json');

// locales.ts uses Vite's import.meta.glob, which Node lacks: build the same directory here.
const tenants = readdirSync(join(lib, 'data/tenants')).map((f) => json('data/tenants/' + f));
const byHandle = new Map(tenants.map((t) => [t.handle, t]));
const tenantOf = (r) => byHandle.get(r.tenant);

const causes = await import('#lib/kb/causes');
const { splitTicket, totals } = await import('#lib/kb/split');
const { deskRef } = await import('#lib/kb/desk-ref');

const ps = splitTicket(reports, 4471, tenantOf, notes.oneDayMove);
for (const p of ps)
  console.log(p.key.padEnd(10), p.count, '| tenants', p.tenants.length, p.tenants.join(','), '| channels', JSON.stringify(p.channels),
    '| tagged', JSON.stringify(p.taggedAs), '| mistagged', p.mistagged, '|', p.firstSeen, '→', p.lastSeen,
    '| issue', tickets[p.key]?.issue ?? '(none)');
console.log('oneDayMove ids', ps.find((p) => p.key === 'oneDayMove')?.ids.join(','));
console.log('totals', JSON.stringify(totals(reports, ps, 4471)));
// cross-check against CauseTable's own grouping
const g = causes.groupByCause(causes.uniqueById(reports).filter((r) => r.mergedInto === 4471), tenantOf);
console.log('CauseTable groups', g.map((x) => `${x.cause}=${x.reports.length}`).join(' '));
for (const s of ['SIGNATURE_PLACEHOLDER', 'test']) console.log('deskRef', JSON.stringify(s), deskRef(s));
