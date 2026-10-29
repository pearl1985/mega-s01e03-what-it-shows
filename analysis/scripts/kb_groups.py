import json, sys, glob, os, collections
reports_path, tenants_dir, notes_path = sys.argv[1:4]
reports = json.load(open(reports_path))
tenants = {}
for f in glob.glob(os.path.join(tenants_dir, '*.json')):
    t = json.load(open(f)); tenants[t['handle']] = t
notes = json.load(open(notes_path))
one_day = set(notes.get('oneDayMove', []))
print('total items', len(reports))
ids = [r['id'] for r in reports]
dups = [i for i, c in collections.Counter(ids).items() if c > 1]
print('distinct ids', len(set(ids)), 'duplicated ids', len(dups), dups[:20])
# check duplicates identical?
byid = collections.defaultdict(list)
for r in reports: byid[r['id']].append(r)
nonident = [i for i in dups if any(json.dumps(x, sort_keys=True) != json.dumps(byid[i][0], sort_keys=True) for x in byid[i])]
print('duplicated ids with differing content', nonident)
uniq = list({r['id']: r for r in reports}.values())
print('unique reports', len(uniq))
print('mergedInto values', collections.Counter(str(r.get('mergedInto')) for r in uniq))
print('channels', collections.Counter(r['channel'] for r in uniq))
print('intakeTags', collections.Counter(r['meta']['intakeTag'] for r in uniq))
print('tenants in reports not on file', sorted({r['tenant'] for r in uniq} - set(tenants)))
print('receivedAt range', min(r['receivedAt'] for r in uniq), max(r['receivedAt'] for r in uniq))
def cause(r):
    t = tenants.get(r['tenant'])
    if not t: return 'unplaced'
    return 'hint' if (r['channel'] == 'form' and t['form'] == 'booking-v3') else 'parser'
groups = collections.defaultdict(list)
for r in uniq: groups[cause(r)].append(r)
for c, rs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
    print(f'\n== {c}: {len(rs)} reports; tenants {len({r["tenant"] for r in rs})}; merged {sorted({r.get("mergedInto") for r in rs}, key=str)}')
    print('  tags', dict(collections.Counter(r['meta']['intakeTag'] for r in rs)))
    print('  channels', dict(collections.Counter(r['channel'] for r in rs)))
    print('  first/last', min(r['receivedAt'][:10] for r in rs), max(r['receivedAt'][:10] for r in rs))
    print('  oneDayMove in group', sorted(r['id'] for r in rs if r['id'] in one_day))
print('\noneDayMove ids present:', sorted(i for i in one_day if i in byid), 'missing:', sorted(one_day - set(byid)))
for i in sorted(one_day):
    if i in byid:
        r = byid[i][0]; print(f'  {i} {r["tenant"]} {r["channel"]} {r["receivedAt"]} | {r["subject"]} | {r["body"][:160]}')
# duplicates: how many extra copies
print('\nextra copies total', len(reports) - len(uniq))
