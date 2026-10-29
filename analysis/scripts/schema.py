import json,sys,collections,re
d=json.load(open(sys.argv[1]))
print("type",type(d).__name__,"n",len(d))
keys=collections.Counter(); metakeys=collections.Counter()
for r in d:
    keys[tuple(sorted(r.keys()))]+=1
    m=r.get('meta')
    if isinstance(m,dict): metakeys[tuple(sorted(m.keys()))]+=1
    else: metakeys[repr(m)]+=1
print("keysets",keys); print("metakeys",metakeys)
for k in ['channel','tenant','mergedInto']:
    print(k,collections.Counter(repr(r.get(k)) for r in d))
for k in ['browserLocale','intakeTag']:
    print(k,collections.Counter(repr((r.get('meta') or {}).get(k)) for r in d))
for k in ['receivedAt','mergedAt']:
    v=[r.get(k) for r in d]; s=[x for x in v if isinstance(x,str)]
    print(k,"min",min(s),"max",max(s),"nonstr",sum(1 for x in v if not isinstance(x,str)))
    print(k,"offsets",collections.Counter(re.sub(r'^.*?T[\d:.]+','',x) for x in s))
    print(k,"formats",collections.Counter(re.sub(r'\d','9',x) for x in s))
ids=collections.Counter(r.get('id') for r in d); print("dup ids",[i for i,c in ids.items() if c>1])
print("id format",collections.Counter(re.sub(r'\d','9',str(r.get('id'))) for r in d))
b=collections.defaultdict(list)
for r in d: b[r.get('body')].append(r['id'])
print("dup bodies",[(v,k[:80]) for k,v in b.items() if len(v)>1])
sb=collections.Counter(r.get('subject') for r in d); print("subjects",len(sb)); 
for s,c in sb.most_common(): print(c,repr(s))
print("mergedAt per day",collections.Counter((r.get('mergedAt') or '')[:10] for r in d))
print("received per day",sorted(collections.Counter((r.get('receivedAt') or '')[:10] for r in d).items()))
