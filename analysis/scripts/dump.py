import json,sys
d=json.load(open(sys.argv[1])); seen=set(); out=[]
for r in d:
    if r['id'] in seen: continue
    seen.add(r['id']); m=r['meta']
    out.append(f"{r['id']}|{r['receivedAt'][:16]}|{r['tenant']}|{m['browserLocale']}|{m['intakeTag']}|{r['channel']}|{r['subject']}|{r['body']}")
open(sys.argv[2],'w').write("\n".join(out)+"\n"); print(len(out))
