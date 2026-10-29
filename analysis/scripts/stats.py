import json,sys,collections,datetime as dt,glob,os
rows=json.load(open(sys.argv[1])); tdir=sys.argv[2]
tenants={}
for f in glob.glob(os.path.join(tdir,'*.json')):
    t=json.load(open(f)); tenants[t['handle']]=t
P=lambda *a: print(*a)
off=collections.Counter((r['recv'][:7],r['recv'][-6:]) for r in rows); P("recv month x offset",sorted(off.items()))
P("offset by tenant",sorted(collections.Counter((r['tenant'],r['recv'][-6:]) for r in rows).items()))
raw=json.load(open(sys.argv[3])); bad=[]
for r in raw:
    a=dt.datetime.fromisoformat(r['receivedAt']); b=dt.datetime.fromisoformat(r['mergedAt'])
    if b<a: bad.append((r['id'],r['receivedAt'],r['mergedAt']))
P("mergedAt<receivedAt",bad)
P("merged 07-02 received range",min(r['receivedAt'] for r in raw if r['mergedAt'][:10]=='2026-07-02'),max(r['receivedAt'] for r in raw if r['mergedAt'][:10]=='2026-07-02'))
P("recv order non-monotonic by id:",[ (raw[i]['id'],raw[i]['receivedAt']) for i in range(1,len(raw)) if raw[i]['receivedAt'][:16]<raw[i-1]['receivedAt'][:16] and raw[i]['id']!=raw[i-1]['id']][:40])
P("tag x locale",collections.Counter((r['tag'],r['loc']) for r in rows))
P("tenant locale vs browser locale")
for t in sorted(tenants):
    c=collections.Counter(r['loc'] for r in rows if r['tenant']==t)
    P(" ",t,tenants[t]['locale'],tenants[t]['form'],dict(c))
for k in ('auto',):
    for key in ('tenant','loc','tag','ch'):
        P(key,sorted(collections.Counter((r[key],r['auto']) for r in rows).items()))
P("form x auto",collections.Counter((tenants[r['tenant']]['form'],r['auto']) for r in rows))
P("template usage",collections.Counter(r['template'] for r in rows))
P("subject x auto",collections.Counter((r['subject'],r['auto']) for r in rows if r['auto']!='swap'))
# browser locale matches tenant locale?
P("browser==tenant locale",collections.Counter(r['loc']==tenants[r['tenant']]['locale'] for r in rows))
# month of intended date
P("intended month",sorted(collections.Counter(r['intended'][2] for r in rows if r.get('intended')).items()))
P("intended day",sorted(collections.Counter(r['intended'][1] for r in rows if r.get('intended')).items()))
P("received month x auto",sorted(collections.Counter((r['recv'][:7],r['auto']) for r in rows).items()))
# same-tenant repeats: same unordered pair
g=collections.defaultdict(list)
for r in rows:
    if r.get('intended'):
        key=(r['tenant'],frozenset([(r['intended'][1],r['intended'][2]),(r['shown'][1],r['shown'][2])]))
        g[key].append((r['id'],r['recv'][:16],r['body']))
P("\nsame tenant same date pair:")
for k,v in g.items():
    if len(v)>1: P(k[0],v)
# same tenant same day
P("\nsame tenant same calendar day:")
g2=collections.defaultdict(list)
for r in rows: g2[(r['tenant'],r['recv'][:10])].append((r['id'],r['recv'][11:16],r['body'][:70]))
for k,v in sorted(g2.items()):
    if len(v)>1: P(k,v)
P("\nfollow-up words:",[(r['id'],r['body']) for r in rows if any(w in r['body'].lower() for w in ('sorry','ignore','actually','meant','correction','previous'))])
