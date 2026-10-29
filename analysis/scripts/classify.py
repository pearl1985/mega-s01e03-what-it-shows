import json,sys,re,collections,datetime as dt
data=json.load(open(sys.argv[1])); notes=json.load(open(sys.argv[2])); tdir=sys.argv[3]; outdir=sys.argv[4]
import glob,os
tenants={json.load(open(f))['handle']:json.load(open(f)) for f in glob.glob(os.path.join(tdir,'*.json'))}
M={m:i for i,m in enumerate(['January','February','March','April','May','June','July','August','September','October','November','December'],1)}
WD=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
seen=set(); rows=[]
for r in data:
    if r['id'] in seen: continue
    seen.add(r['id']); rows.append(r)
pat=re.compile(r'(?:(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday) )?(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December)')
# templates: which date is the intended one (booked) and which is shown
TPL=[(r'^Our (.+) reminder went out on (.+?)\.', 'I,S'),
 (r'^Sorry\. (.+) went out on (.+?)\.', 'S,I'),
 (r'^Invite says (.+)\. Calendar says (.+?)\.', 'S,I'),
 (r'^Booked for (.+)\. The invite says (.+?)\.$', 'I,S'),
 (r'^Invite says (.+)\. We agreed (.+?)\. Which', 'S,I'),
 (r'^Customer booked (.+) and got an invite for (.+?)\. Please', 'I,S'),
 (r'^Second time this month: (.+) turned into (.+?)\.$', 'I,S'),
 (r'^Every booking we make shows the wrong day\. (.+) is now (.+?)\.$', 'I,S'),
 (r'^(.+) showed as (.+?)\. I moved it myself\.$', 'I,S'),
 (r'^My client came on (.+) instead of (.+?)\. We sorted', 'S,I'),
 (r'^We had two people show up on (.+)\. They were booked for (.+?)\.$', 'S,I'),
 (r'^The reminder for (.+) arrived for (.+?)\.$', 'I,S'),
 (r'^The calendar invite for (.+) landed on (.+?)\. Nobody', 'I,S'),
 (r'^Our (.+) invoice meeting is shown as (.+?)\.', 'I,S')]
def pd(s):
    m=pat.fullmatch(s.strip())
    if not m: return None
    return (m.group(1),int(m.group(2)),M[m.group(3)])
out=[]
for r in rows:
    b=r['body']; rec={'id':r['id'],'tenant':r['tenant'],'loc':r['meta']['browserLocale'],'tag':r['meta']['intakeTag'],'ch':r['channel'],'recv':r['receivedAt'],'subject':r['subject'],'body':b,'template':None}
    for i,(rx,order) in enumerate(TPL):
        m=re.match(rx,b)
        if m:
            a,c=pd(m.group(1)),pd(m.group(2))
            if a is None or c is None: continue
            I,S=(a,c) if order=='I,S' else (c,a)
            rec.update(template=i,intended=I,shown=S)
            break
    if rec['template'] is not None:
        I,S=rec['intended'],rec['shown']
        rec['swap']= (I[1]==S[2] and I[2]==S[1])
        try:
            di=dt.date(2026,I[2],I[1]); ds=dt.date(2026,S[2],S[1]); rec['delta_days']=(ds-di).days
        except Exception as e: rec['delta_days']=None
        wd=[]
        for x,d in (('I',I),('S',S)):
            if d[0]:
                ok=[y for y in (2025,2026,2027) if WD[dt.date(y,d[2],d[1]).weekday()]==d[0]]
                wd.append(f"{x}:{d[0]} {d[1]}/{d[2]} matches years {ok}")
        rec['weekday_check']=wd
    out.append(rec)
# summary
c=collections.Counter()
for r in out:
    k='unparsed' if r['template'] is None else ('swap' if r['swap'] else 'nonswap')
    r['auto']=k; c[k]+=1
print(c)
for r in out:
    if r['auto']!='swap': print(r['auto'],r['id'],r['tenant'],r['loc'],r['body'])
print("\nweekday anomalies:")
for r in out:
    for w in r.get('weekday_check',[]):
        if '2026' not in w: print(r['id'],w,r['body'])
print("\nweekday coverage:",sum(1 for r in out if r.get('weekday_check')))
print("\nall swap pairs: intended day<=12 always:",all(r['intended'][1]<=12 for r in out if r['auto']=='swap'))
print("intended==shown (day==month) cases:",[r['id'] for r in out if r['template'] is not None and r['intended']==r['shown']])
json.dump(out,open(os.path.join(outdir,'classified-raw.json'),'w'),indent=1,default=str)
