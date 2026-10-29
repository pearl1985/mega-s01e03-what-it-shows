import json,sys,collections
d=json.load(open(sys.argv[1]))
g=collections.defaultdict(list)
for i,r in enumerate(d): g[r['id']].append((i,r))
for k,v in g.items():
    if len(v)>1:
        a,b=v[0][1],v[1][1]
        diff={f:(a[f],b[f]) for f in a if a[f]!=b[f]}
        print(k,"idx",[x[0] for x in v],"identical" if not diff else diff)
