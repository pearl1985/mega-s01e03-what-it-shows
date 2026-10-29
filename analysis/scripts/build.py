import json,sys,collections,os
rows=json.load(open(sys.argv[1])); notes=json.load(open(sys.argv[2])); outdir=sys.argv[3]
by={r['id']:r for r in rows}
ONE=['R-41202','R-41209','R-41236','R-41344','R-41620']
META=['R-41290','R-41514']; UNCLEAR=['R-41417']; EXTRA_SWAP=['R-41615']
cat={}
for r in rows:
    i=r['id']
    if i in ONE: cat[i]='B'
    elif i in META: cat[i]='C'
    elif i in UNCLEAR: cat[i]='U'
    elif r['auto']=='swap' or i in EXTRA_SWAP: cat[i]='A'
    else: raise SystemExit("unassigned "+i)
assert len(cat)==412
FLAGS={'R-41201':'same-tenant correction 22 min after R-41200 ("Sorry. 4 July went out on 7 April") - same incident, do not count twice',
 'R-41412':'same tenant (nine.lanterns), same day, same date pair (8 July/7 August) as R-41411 - probably same incident reported by a second user (en-US, form)',
 'R-41236':'weak: no dates; "invite arrived before booking" implies a timestamp shift (timezone), not a swap; included because the desk put it in oneDayMove',
 'R-41615':'no explicit dates; "October bookings came through for January" = 1 Oct <-> 10 Jan swap; not a complaint',
 'R-41270':'swap (5 June shown as 6 May); reporter says "not your problem"',
 'R-41562':'identical body to R-41299 from the same tenant (stone.and.sons) four months later; probably a new booking, kept',
 'R-41482':'identical body to R-41416 from the same tenant (pale.harbour) one month later; kept',
 'R-41484':'identical body to R-41309 from the same tenant (long.table) 2.5 months later; kept'}
DEF={
'A':('Day and month swapped (DD/MM vs MM/DD)',
 'The date that reaches the invite, reminder or calendar has day and month exchanged: booked 7 April, the invite says 4 July (and the reverse). In every parseable report both numbers are 1-12, so the date is ambiguous; no report has a day of 13 or more. That points at a parser that reads a numeric D/M date as M/D whenever that is valid, and probably falls back to the other order otherwise. Weekday names in the reports always match the real 2026 weekday of the date they go with (91 dated weekdays checked), so the weekday is computed from the wrong date; there is no separate weekday bug. It shows up in all 11 tenants, all 12 browser locales (en-US included), all 3 channels, both booking-v2 and booking-v3 forms, and both intakeTags.'),
'B':('Date shifted by one day / timezone',
 'The date is off by exactly one day, or differs between recipients in different timezones, with no day/month swap. Typical cause: a date-only value stored as a UTC midnight timestamp and shown in another timezone, or an all-day event converted per recipient. Examples: invite says Tuesday 12 May, calendar says Monday 11 May (+1 day); Tuesday 6 October shown as Monday (-1 day); a Lisbon client got Tuesday and a Toronto client got Monday; every booking in June one day off; an invite timestamp earlier than the booking itself. This matches the desk\'s "oneDayMove" list exactly.'),
'C':('Comments / feature requests, no concrete incident',
 'Messages with no specific wrong date that comment on the day-first problem: asking for a "day first" setting and a workaround of saying dates in words. They point at the same root cause as A but do not describe a separate incident.'),
'U':('Unclear',
 'Says "the wrong day" with no dates, so it cannot be told apart from A or B.')}
def fmt(d): return f"{d[0]+' ' if d[0] else ''}{d[1]}/{d[2]}"
res={}; md=["# Ticket #4471: distinct problems in the 412 merged reports\n",
"Source: reports-4471.json (427 records = 412 unique ids + 15 exact duplicate records), desk-notes.json, tenants/*.json. Classified by the body text; subject and intakeTag were ignored.\n",
"| Cat | Problem | Reports | Distinct incidents (after flags) |","|---|---|---|---|"]
for k in 'ABCU':
    ids=sorted(i for i,c in cat.items() if c==k); rs=[by[i] for i in ids]
    adj=len(ids)-(1 if k=='A' else 0)
    md.append(f"| {k} | {DEF[k][0]} | {len(ids)} | {adj if k!='A' else f'{adj} (402 if R-41412 = R-41411)'} |")
md.append(f"| | **Total** | **{len(cat)}** | |\n")
for k in 'ABCU':
    ids=sorted(i for i,c in cat.items() if c==k); rs=[by[i] for i in ids]
    span={f:dict(collections.Counter(r[f] for r in rs).most_common()) for f in ('tenant','loc','ch','tag')}
    months=dict(sorted(collections.Counter(r['recv'][:7] for r in rs).items()))
    ex=[by[i]['body'] for i in ({'A':['R-41200','R-41309','R-41411'],'B':['R-41202','R-41344','R-41620'],'C':META,'U':UNCLEAR}[k])]
    res[k]={'name':DEF[k][0],'description':DEF[k][1],'count':len(ids),'ids':ids,
      'evidence':{'span':span,'received_by_month':months,'examples':ex,'flags':{i:FLAGS[i] for i in ids if i in FLAGS},
                  'first':min(r['recv'] for r in rs),'last':max(r['recv'] for r in rs)}}
    md+= [f"## {k}. {DEF[k][0]} - {len(ids)} reports\n",DEF[k][1]+"\n",
      f"- Tenants: {span['tenant']}",f"- Browser locales: {span['loc']}",f"- Channels: {span['ch']}",f"- intakeTag: {span['tag']}",
      f"- Received by month: {months} (first {res[k]['evidence']['first']}, last {res[k]['evidence']['last']})",
      "- Examples (verbatim):"]+[f"  - \"{e}\"" for e in ex]
    fl=res[k]['evidence']['flags']
    if fl: md+=["- Flags:"]+[f"  - {i}: {t}" for i,t in fl.items()]
    md+=["",f"| id | received | tenant | locale | tag | channel | intended -> shown | body |","|---|---|---|---|---|---|---|---|"]
    for r in rs:
        pair=f"{fmt(r['intended'])} -> {fmt(r['shown'])}" if r.get('intended') else ""
        md.append(f"| {r['id']} | {r['recv'][:16]} | {r['tenant']} | {r['loc']} | {r['tag']} | {r['ch']} | {pair} | {r['body'].replace('|','/')} |")
    md.append("")
od=notes['oneDayMove']
md+=["## Cross-checks\n",
f"- desk-notes oneDayMove = {od}; category B = {sorted(i for i,c in cat.items() if c=='B')}; match: {sorted(od)==sorted(i for i,c in cat.items() if c=='B')}.",
"- Tenant files hold handle, name, locale and form only; no timezone field. The timezone can be read from the receivedAt offsets, which are fixed per tenant: +01:00 for harbour.dental, pale.harbour and stone.and.sons (UK/PT/IE summer time), +02:00 for the rest. Every receivedAt is between April and early October, i.e. summer time.",
"- Browser locale differs from the tenant locale in 79 of 412 reports. The swap shows up in every locale, en-US and en-GB included, so it does not depend on the browser locale or the tenant locale.",
"- intakeTag='hint' covers exactly the 41 en-US reports; the other 371 are 'parser'. The tag follows the browser locale, not the symptom. All 41 'hint' reports are swaps.",
"- No clustering around DST (2026-03-29 is before the data starts; the data ends 2026-10-04, before the 2026-10-25 change). Swap reports grow steadily from April to September. The 5 category-B reports are spread over 04-02, 04-06, 04-20, 06-12 and 10-04.",
"- mergedAt: 189 reports were bulk-merged on 2026-07-02 (all received 04-01 to 07-02); after that, each report was merged on the day it arrived. No mergedAt is earlier than its receivedAt.",
"- Same-tenant reports with the same date pair in different months are common (about 70 groups). With only 132 possible ambiguous pairs, that is roughly what chance gives, so they are treated as separate bookings, not repeats. Exact same-tenant body repeats: R-41299/R-41562, R-41416/R-41482, R-41309/R-41484 (kept, flagged).",""]
open(os.path.join(outdir,'reports-clusters.md'),'w').write("\n".join(md))
json.dump(res,open(os.path.join(outdir,'reports-clusters.json'),'w'),indent=1,ensure_ascii=False)
print({k:v['count'] for k,v in res.items()})
