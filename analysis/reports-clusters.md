# Ticket #4471: distinct problems in the 412 merged reports

Source: reports-4471.json (427 records = 412 unique ids + 15 exact duplicate records), desk-notes.json, tenants/*.json. Classified by the body text; subject and intakeTag were ignored.

| Cat | Problem | Reports | Distinct incidents (after flags) |
|---|---|---|---|
| A | Day and month swapped (DD/MM vs MM/DD) | 404 | 403 (402 if R-41412 = R-41411) |
| B | Date shifted by one day / timezone | 5 | 5 |
| C | Comments / feature requests, no concrete incident | 2 | 2 |
| U | Unclear | 1 | 1 |
| | **Total** | **412** | |

## A. Day and month swapped (DD/MM vs MM/DD) - 404 reports

The date that reaches the invite, reminder or calendar has day and month exchanged: booked 7 April, the invite says 4 July (and the reverse). In every parseable report both numbers are 1-12, so the date is ambiguous; no report has a day of 13 or more. That points at a parser that reads a numeric D/M date as M/D whenever that is valid, and probably falls back to the other order otherwise. Weekday names in the reports always match the real 2026 weekday of the date they go with (91 dated weekdays checked), so the weekday is computed from the wrong date; there is no separate weekday bug. It shows up in all 11 tenants, all 12 browser locales (en-US included), all 3 channels, both booking-v2 and booking-v3 forms, and both intakeTags.

- Tenants: {'harbour.dental': 52, 'kettle.books': 46, 'nine.lanterns': 43, 'morrow.tax': 40, 'long.table': 38, 'ridge.clinic': 35, 'alder.physio': 34, 'pale.harbour': 30, 'stone.and.sons': 30, 'copper.studio': 29, 'lantern.row': 27}
- Browser locales: {'en-GB': 88, 'en-US': 41, 'pl-PL': 36, 'it-IT': 35, 'nl-NL': 34, 'fr-FR': 31, 'da-DK': 26, 'cs-CZ': 25, 'pt-PT': 23, 'en-IE': 23, 'es-ES': 22, 'de-DE': 20}
- Channels: {'app': 199, 'email': 147, 'form': 58}
- intakeTag: {'parser': 363, 'hint': 41}
- Received by month: {'2026-04': 53, '2026-05': 56, '2026-06': 65, '2026-07': 72, '2026-08': 67, '2026-09': 80, '2026-10': 11} (first 2026-04-01T09:12:00+01:00, last 2026-10-04T20:30:00+01:00)
- Examples (verbatim):
  - "Our 7 April reminder went out on 4 July. Is this a joke. It is not April Fools where we are."
  - "Thursday 8 January showed as Saturday 1 August. I moved it myself."
  - "Invite says Friday 7 August. We agreed Wednesday 8 July. Which one do I trust?"
- Flags:
  - R-41201: same-tenant correction 22 min after R-41200 ("Sorry. 4 July went out on 7 April") - same incident, do not count twice
  - R-41270: swap (5 June shown as 6 May); reporter says "not your problem"
  - R-41412: same tenant (nine.lanterns), same day, same date pair (8 July/7 August) as R-41411 - probably same incident reported by a second user (en-US, form)
  - R-41482: identical body to R-41416 from the same tenant (pale.harbour) one month later; kept
  - R-41484: identical body to R-41309 from the same tenant (long.table) 2.5 months later; kept
  - R-41562: identical body to R-41299 from the same tenant (stone.and.sons) four months later; probably a new booking, kept
  - R-41615: no explicit dates; "October bookings came through for January" = 1 Oct <-> 10 Jan swap; not a complaint

| id | received | tenant | locale | tag | channel | intended -> shown | body |
|---|---|---|---|---|---|---|---|
| R-41200 | 2026-04-01T09:12 | harbour.dental | en-GB | parser | app | 7/4 -> 4/7 | Our 7 April reminder went out on 4 July. Is this a joke. It is not April Fools where we are. |
| R-41201 | 2026-04-01T09:34 | harbour.dental | en-GB | parser | app | 7/4 -> 4/7 | Sorry. 4 July went out on 7 April. I have been up since five. |
| R-41203 | 2026-04-03T12:14 | lantern.row | cs-CZ | parser | app | 2/12 -> 12/2 | Booked for 2 December. The invite says 12 February. |
| R-41204 | 2026-04-04T21:55 | kettle.books | nl-NL | parser | email | Monday 12/10 -> Thursday 10/12 | Invite says Thursday 10 December. We agreed Monday 12 October. Which one do I trust? |
| R-41205 | 2026-04-05T12:29 | morrow.tax | en-US | hint | app | 3/10 -> 10/3 | Customer booked 3 October and got an invite for 10 March. Please look at this. |
| R-41206 | 2026-04-05T16:54 | long.table | it-IT | parser | app | 4/3 -> 3/4 | Second time this month: 4 March turned into 3 April. |
| R-41208 | 2026-04-06T14:52 | ridge.clinic | da-DK | parser | email | 2/3 -> 3/2 | Booked for 2 March. The invite says 3 February. |
| R-41210 | 2026-04-07T08:53 | long.table | it-IT | parser | app | 12/4 -> 4/12 | Second time this month: 12 April turned into 4 December. |
| R-41211 | 2026-04-07T09:28 | pale.harbour | pt-PT | parser | app | 5/3 -> 3/5 | The reminder for 5 March arrived for 3 May. |
| R-41212 | 2026-04-07T10:22 | harbour.dental | en-GB | parser | app | 8/12 -> 12/8 | Every booking we make shows the wrong day. 8 December is now 12 August. |
| R-41213 | 2026-04-07T17:14 | kettle.books | nl-NL | parser | email | Monday 1/6 -> Tuesday 6/1 | Monday 1 June showed as Tuesday 6 January. I moved it myself. |
| R-41214 | 2026-04-08T18:22 | copper.studio | es-ES | parser | email | Monday 7/9 -> Thursday 9/7 | Invite says Thursday 9 July. We agreed Monday 7 September. Which one do I trust? |
| R-41215 | 2026-04-08T19:23 | kettle.books | nl-NL | parser | app | 2/3 -> 3/2 | My client came on 3 February instead of 2 March. We sorted it out. |
| R-41216 | 2026-04-11T12:34 | nine.lanterns | pl-PL | parser | app | 12/5 -> 5/12 | We had two people show up on 5 December. They were booked for 12 May. |
| R-41217 | 2026-04-12T15:23 | ridge.clinic | da-DK | parser | email | 9/5 -> 5/9 | The reminder for 9 May arrived for 5 September. |
| R-41218 | 2026-04-12T18:55 | pale.harbour | pt-PT | parser | email | 6/11 -> 11/6 | Customer booked 6 November and got an invite for 11 June. Please look at this. |
| R-41219 | 2026-04-13T13:46 | harbour.dental | en-GB | parser | app | Thursday 12/3 -> Thursday 3/12 | Thursday 12 March showed as Thursday 3 December. I moved it myself. |
| R-41220 | 2026-04-13T18:08 | nine.lanterns | pl-PL | parser | app | 6/5 -> 5/6 | We had two people show up on 5 June. They were booked for 6 May. |
| R-41221 | 2026-04-13T21:27 | long.table | it-IT | parser | email | 2/7 -> 7/2 | Booked for 2 July. The invite says 7 February. |
| R-41222 | 2026-04-14T17:49 | pale.harbour | pt-PT | parser | app | 1/10 -> 10/1 | Customer booked 1 October and got an invite for 10 January. Please look at this. |
| R-41223 | 2026-04-14T19:08 | long.table | it-IT | parser | email | Tuesday 8/12 -> Wednesday 12/8 | Tuesday 8 December showed as Wednesday 12 August. I moved it myself. |
| R-41224 | 2026-04-17T13:50 | morrow.tax | fr-FR | parser | email | 10/9 -> 9/10 | Every booking we make shows the wrong day. 10 September is now 9 October. |
| R-41225 | 2026-04-17T14:02 | alder.physio | de-DE | parser | email | 3/5 -> 5/3 | The reminder for 3 May arrived for 5 March. |
| R-41227 | 2026-04-17T14:23 | harbour.dental | en-GB | parser | app | 6/2 -> 2/6 | We had two people show up on 2 June. They were booked for 6 February. |
| R-41228 | 2026-04-17T17:27 | long.table | it-IT | parser | app | 2/7 -> 7/2 | Customer booked 2 July and got an invite for 7 February. Please look at this. |
| R-41229 | 2026-04-17T20:59 | harbour.dental | en-GB | parser | app | 5/3 -> 3/5 | Every booking we make shows the wrong day. 5 March is now 3 May. |
| R-41230 | 2026-04-17T22:44 | copper.studio | en-GB | parser | form | 6/1 -> 1/6 | My client came on 1 June instead of 6 January. We sorted it out. |
| R-41231 | 2026-04-18T11:22 | long.table | it-IT | parser | app | 8/1 -> 1/8 | Second time this month: 8 January turned into 1 August. |
| R-41232 | 2026-04-19T13:15 | harbour.dental | en-GB | parser | app | 6/1 -> 1/6 | Second time this month: 6 January turned into 1 June. |
| R-41233 | 2026-04-19T21:27 | nine.lanterns | pl-PL | parser | email | 11/10 -> 10/11 | We had two people show up on 10 November. They were booked for 11 October. |
| R-41234 | 2026-04-20T07:46 | pale.harbour | pt-PT | parser | app | 1/3 -> 3/1 | Every booking we make shows the wrong day. 1 March is now 3 January. |
| R-41235 | 2026-04-20T10:50 | ridge.clinic | da-DK | parser | app | 2/5 -> 5/2 | Second time this month: 2 May turned into 5 February. |
| R-41237 | 2026-04-20T21:02 | pale.harbour | pt-PT | parser | app | 12/1 -> 1/12 | The reminder for 12 January arrived for 1 December. |
| R-41238 | 2026-04-20T22:16 | alder.physio | de-DE | parser | app | 8/3 -> 3/8 | Every booking we make shows the wrong day. 8 March is now 3 August. |
| R-41239 | 2026-04-21T10:21 | kettle.books | en-GB | parser | form | 8/11 -> 11/8 | The reminder for 8 November arrived for 11 August. |
| R-41240 | 2026-04-21T12:34 | morrow.tax | fr-FR | parser | form | 7/2 -> 2/7 | Second time this month: 7 February turned into 2 July. |
| R-41241 | 2026-04-21T19:21 | alder.physio | en-US | hint | form | 6/8 -> 8/6 | We had two people show up on 8 June. They were booked for 6 August. |
| R-41242 | 2026-04-22T14:50 | copper.studio | es-ES | parser | app | 5/10 -> 10/5 | The reminder for 5 October arrived for 10 May. |
| R-41243 | 2026-04-22T21:56 | harbour.dental | en-GB | parser | app | 10/5 -> 5/10 | My client came on 5 October instead of 10 May. We sorted it out. |
| R-41244 | 2026-04-23T13:35 | lantern.row | cs-CZ | parser | email | 1/12 -> 12/1 | Second time this month: 1 December turned into 12 January. |
| R-41245 | 2026-04-23T18:38 | ridge.clinic | da-DK | parser | app | 11/10 -> 10/11 | My client came on 10 November instead of 11 October. We sorted it out. |
| R-41246 | 2026-04-24T10:27 | stone.and.sons | en-IE | parser | form | 6/12 -> 12/6 | We had two people show up on 12 June. They were booked for 6 December. |
| R-41247 | 2026-04-24T12:30 | long.table | it-IT | parser | app | 11/3 -> 3/11 | Customer booked 11 March and got an invite for 3 November. Please look at this. |
| R-41248 | 2026-04-24T15:13 | long.table | it-IT | parser | form | Friday 8/5 -> Wednesday 5/8 | Invite says Wednesday 5 August. We agreed Friday 8 May. Which one do I trust? |
| R-41249 | 2026-04-24T19:27 | morrow.tax | fr-FR | parser | email | 11/10 -> 10/11 | My client came on 10 November instead of 11 October. We sorted it out. |
| R-41250 | 2026-04-24T19:35 | stone.and.sons | en-IE | parser | email | 10/12 -> 12/10 | Booked for 10 December. The invite says 12 October. |
| R-41251 | 2026-04-25T20:48 | pale.harbour | pt-PT | parser | form | Wednesday 7/1 -> Wednesday 1/7 | Wednesday 7 January showed as Wednesday 1 July. I moved it myself. |
| R-41252 | 2026-04-26T15:56 | nine.lanterns | pl-PL | parser | email | 3/1 -> 1/3 | The reminder for 3 January arrived for 1 March. |
| R-41253 | 2026-04-27T13:56 | harbour.dental | en-GB | parser | email | 2/4 -> 4/2 | My client came on 4 February instead of 2 April. We sorted it out. |
| R-41254 | 2026-04-28T20:08 | stone.and.sons | en-IE | parser | app | 8/4 -> 4/8 | The reminder for 8 April arrived for 4 August. |
| R-41255 | 2026-04-29T13:22 | kettle.books | nl-NL | parser | email | 6/12 -> 12/6 | Customer booked 6 December and got an invite for 12 June. Please look at this. |
| R-41256 | 2026-04-29T16:38 | long.table | it-IT | parser | form | 7/6 -> 6/7 | My client came on 6 July instead of 7 June. We sorted it out. |
| R-41257 | 2026-04-30T09:53 | harbour.dental | en-GB | parser | email | 12/8 -> 8/12 | Every booking we make shows the wrong day. 12 August is now 8 December. |
| R-41258 | 2026-05-01T11:08 | ridge.clinic | da-DK | parser | email | 12/9 -> 9/12 | We had two people show up on 9 December. They were booked for 12 September. |
| R-41259 | 2026-05-01T12:24 | copper.studio | es-ES | parser | form | 11/4 -> 4/11 | Customer booked 11 April and got an invite for 4 November. Please look at this. |
| R-41260 | 2026-05-01T21:18 | harbour.dental | en-GB | parser | app | 1/11 -> 11/1 | Second time this month: 1 November turned into 11 January. |
| R-41261 | 2026-05-02T10:47 | lantern.row | cs-CZ | parser | email | 2/9 -> 9/2 | Booked for 2 September. The invite says 9 February. |
| R-41262 | 2026-05-02T13:17 | pale.harbour | pt-PT | parser | form | 2/3 -> 3/2 | We had two people show up on 3 February. They were booked for 2 March. |
| R-41263 | 2026-05-02T15:49 | stone.and.sons | en-IE | parser | email | 3/2 -> 2/3 | The reminder for 3 February arrived for 2 March. |
| R-41264 | 2026-05-02T18:18 | alder.physio | de-DE | parser | email | Monday 4/5 -> Sunday 5/4 | Invite says Sunday 5 April. We agreed Monday 4 May. Which one do I trust? |
| R-41265 | 2026-05-03T08:12 | long.table | it-IT | parser | form | 7/8 -> 8/7 | The reminder for 7 August arrived for 8 July. |
| R-41266 | 2026-05-03T11:40 | copper.studio | es-ES | parser | email | 12/11 -> 11/12 | Every booking we make shows the wrong day. 12 November is now 11 December. |
| R-41267 | 2026-05-03T14:36 | kettle.books | nl-NL | parser | app | 12/11 -> 11/12 | The calendar invite for 12 November landed on 11 December. Nobody here touched it. |
| R-41268 | 2026-05-03T16:23 | stone.and.sons | en-IE | parser | email | 5/2 -> 2/5 | The reminder for 5 February arrived for 2 May. |
| R-41269 | 2026-05-04T14:49 | lantern.row | cs-CZ | parser | email | 5/8 -> 8/5 | Second time this month: 5 August turned into 8 May. |
| R-41270 | 2026-05-04T16:03 | morrow.tax | fr-FR | parser | app | 5/6 -> 6/5 | Our 5 June invoice meeting is shown as 6 May. We paid someone on the wrong day because of this. Not your problem. Noting it. |
| R-41271 | 2026-05-04T16:33 | nine.lanterns | en-US | hint | email | 12/1 -> 1/12 | Second time this month: 12 January turned into 1 December. |
| R-41272 | 2026-05-04T21:05 | lantern.row | cs-CZ | parser | app | 1/12 -> 12/1 | We had two people show up on 12 January. They were booked for 1 December. |
| R-41273 | 2026-05-07T10:16 | ridge.clinic | da-DK | parser | app | Saturday 3/1 -> Sunday 1/3 | Saturday 3 January showed as Sunday 1 March. I moved it myself. |
| R-41274 | 2026-05-07T15:27 | nine.lanterns | pl-PL | parser | app | Friday 7/8 -> Wednesday 8/7 | Friday 7 August showed as Wednesday 8 July. I moved it myself. |
| R-41275 | 2026-05-07T18:27 | alder.physio | en-US | hint | form | 7/11 -> 11/7 | My client came on 11 July instead of 7 November. We sorted it out. |
| R-41276 | 2026-05-08T12:58 | morrow.tax | en-GB | parser | app | 11/6 -> 6/11 | Customer booked 11 June and got an invite for 6 November. Please look at this. |
| R-41277 | 2026-05-08T17:43 | ridge.clinic | da-DK | parser | email | 11/1 -> 1/11 | The reminder for 11 January arrived for 1 November. |
| R-41278 | 2026-05-08T18:54 | morrow.tax | fr-FR | parser | app | Friday 9/10 -> Thursday 10/9 | Invite says Thursday 10 September. We agreed Friday 9 October. Which one do I trust? |
| R-41279 | 2026-05-08T19:21 | nine.lanterns | pl-PL | parser | email | 6/11 -> 11/6 | Second time this month: 6 November turned into 11 June. |
| R-41280 | 2026-05-10T16:29 | harbour.dental | en-GB | parser | app | 11/1 -> 1/11 | Every booking we make shows the wrong day. 11 January is now 1 November. |
| R-41281 | 2026-05-11T09:44 | alder.physio | de-DE | parser | email | 7/6 -> 6/7 | Booked for 7 June. The invite says 6 July. |
| R-41282 | 2026-05-12T13:50 | harbour.dental | en-GB | parser | app | 11/4 -> 4/11 | Second time this month: 11 April turned into 4 November. |
| R-41283 | 2026-05-12T16:23 | stone.and.sons | en-US | hint | app | 12/10 -> 10/12 | My client came on 10 December instead of 12 October. We sorted it out. |
| R-41284 | 2026-05-14T11:06 | harbour.dental | en-GB | parser | email | 6/8 -> 8/6 | Every booking we make shows the wrong day. 6 August is now 8 June. |
| R-41285 | 2026-05-14T22:27 | lantern.row | cs-CZ | parser | form | 1/12 -> 12/1 | Booked for 1 December. The invite says 12 January. |
| R-41286 | 2026-05-17T09:27 | long.table | it-IT | parser | app | Friday 11/9 -> Monday 9/11 | Invite says Monday 9 November. We agreed Friday 11 September. Which one do I trust? |
| R-41287 | 2026-05-17T17:10 | nine.lanterns | pl-PL | parser | app | 8/2 -> 2/8 | Second time this month: 8 February turned into 2 August. |
| R-41288 | 2026-05-17T21:53 | kettle.books | nl-NL | parser | app | 7/10 -> 10/7 | Customer booked 7 October and got an invite for 10 July. Please look at this. |
| R-41289 | 2026-05-18T15:42 | harbour.dental | en-GB | parser | app | 7/8 -> 8/7 | Every booking we make shows the wrong day. 7 August is now 8 July. |
| R-41291 | 2026-05-20T09:56 | pale.harbour | pt-PT | parser | email | 12/2 -> 2/12 | The calendar invite for 12 February landed on 2 December. Nobody here touched it. |
| R-41292 | 2026-05-20T14:29 | harbour.dental | en-US | hint | form | Tuesday 10/11 -> Sunday 11/10 | Tuesday 10 November showed as Sunday 11 October. I moved it myself. |
| R-41293 | 2026-05-20T21:10 | pale.harbour | pt-PT | parser | email | 1/9 -> 9/1 | Customer booked 1 September and got an invite for 9 January. Please look at this. |
| R-41294 | 2026-05-21T21:10 | pale.harbour | pt-PT | parser | form | Thursday 5/11 -> Monday 11/5 | Thursday 5 November showed as Monday 11 May. I moved it myself. |
| R-41295 | 2026-05-22T20:49 | nine.lanterns | pl-PL | parser | app | Tuesday 3/2 -> Monday 2/3 | Invite says Monday 2 March. We agreed Tuesday 3 February. Which one do I trust? |
| R-41296 | 2026-05-23T18:39 | copper.studio | es-ES | parser | email | Sunday 7/6 -> Monday 6/7 | Invite says Monday 6 July. We agreed Sunday 7 June. Which one do I trust? |
| R-41297 | 2026-05-23T21:58 | harbour.dental | en-GB | parser | email | 7/6 -> 6/7 | Customer booked 7 June and got an invite for 6 July. Please look at this. |
| R-41298 | 2026-05-24T14:52 | ridge.clinic | en-GB | parser | email | 12/1 -> 1/12 | The reminder for 12 January arrived for 1 December. |
| R-41299 | 2026-05-24T14:39 | stone.and.sons | en-GB | parser | email | 10/9 -> 9/10 | We had two people show up on 9 October. They were booked for 10 September. |
| R-41300 | 2026-05-24T22:57 | long.table | it-IT | parser | email | 12/10 -> 10/12 | Booked for 12 October. The invite says 10 December. |
| R-41301 | 2026-05-26T09:53 | harbour.dental | en-GB | parser | email | 2/7 -> 7/2 | Booked for 2 July. The invite says 7 February. |
| R-41302 | 2026-05-26T18:23 | lantern.row | cs-CZ | parser | email | 5/11 -> 11/5 | The reminder for 5 November arrived for 11 May. |
| R-41303 | 2026-05-27T08:55 | long.table | it-IT | parser | app | 8/11 -> 11/8 | Booked for 8 November. The invite says 11 August. |
| R-41304 | 2026-05-27T09:16 | lantern.row | cs-CZ | parser | form | 8/1 -> 1/8 | The calendar invite for 8 January landed on 1 August. Nobody here touched it. |
| R-41305 | 2026-05-27T13:04 | copper.studio | en-US | hint | form | 9/8 -> 8/9 | Booked for 9 August. The invite says 8 September. |
| R-41306 | 2026-05-27T14:19 | harbour.dental | en-GB | parser | email | Thursday 10/12 -> Monday 12/10 | Thursday 10 December showed as Monday 12 October. I moved it myself. |
| R-41308 | 2026-05-28T09:27 | alder.physio | en-US | hint | form | 5/3 -> 3/5 | We had two people show up on 3 May. They were booked for 5 March. |
| R-41309 | 2026-05-28T17:27 | long.table | it-IT | parser | app | Thursday 8/1 -> Saturday 1/8 | Thursday 8 January showed as Saturday 1 August. I moved it myself. |
| R-41310 | 2026-05-29T21:44 | morrow.tax | fr-FR | parser | app | 12/7 -> 7/12 | The calendar invite for 12 July landed on 7 December. Nobody here touched it. |
| R-41311 | 2026-05-30T10:55 | alder.physio | de-DE | parser | email | 8/5 -> 5/8 | Booked for 8 May. The invite says 5 August. |
| R-41312 | 2026-05-30T20:00 | pale.harbour | en-GB | parser | app | 6/4 -> 4/6 | We had two people show up on 4 June. They were booked for 6 April. |
| R-41313 | 2026-05-31T09:05 | long.table | it-IT | parser | app | 11/5 -> 5/11 | Customer booked 11 May and got an invite for 5 November. Please look at this. |
| R-41314 | 2026-05-31T13:28 | nine.lanterns | pl-PL | parser | app | 8/4 -> 4/8 | Booked for 8 April. The invite says 4 August. |
| R-41315 | 2026-05-31T19:21 | ridge.clinic | da-DK | parser | email | 1/11 -> 11/1 | The calendar invite for 1 November landed on 11 January. Nobody here touched it. |
| R-41316 | 2026-06-01T18:59 | harbour.dental | en-GB | parser | app | Friday 2/10 -> Tuesday 10/2 | Friday 2 October showed as Tuesday 10 February. I moved it myself. |
| R-41317 | 2026-06-01T20:05 | stone.and.sons | en-IE | parser | app | 1/9 -> 9/1 | Second time this month: 1 September turned into 9 January. |
| R-41318 | 2026-06-02T22:28 | lantern.row | cs-CZ | parser | app | 12/11 -> 11/12 | Every booking we make shows the wrong day. 12 November is now 11 December. |
| R-41319 | 2026-06-03T12:43 | harbour.dental | en-GB | parser | email | Saturday 11/4 -> Wednesday 4/11 | Invite says Wednesday 4 November. We agreed Saturday 11 April. Which one do I trust? |
| R-41320 | 2026-06-04T15:35 | harbour.dental | en-GB | parser | app | 11/5 -> 5/11 | We had two people show up on 5 November. They were booked for 11 May. |
| R-41321 | 2026-06-04T16:56 | harbour.dental | en-GB | parser | form | 12/5 -> 5/12 | Customer booked 12 May and got an invite for 5 December. Please look at this. |
| R-41322 | 2026-06-05T09:57 | lantern.row | cs-CZ | parser | app | 12/10 -> 10/12 | My client came on 10 December instead of 12 October. We sorted it out. |
| R-41323 | 2026-06-05T12:35 | morrow.tax | fr-FR | parser | form | 12/8 -> 8/12 | The reminder for 12 August arrived for 8 December. |
| R-41324 | 2026-06-05T16:33 | kettle.books | nl-NL | parser | app | 4/12 -> 12/4 | Customer booked 4 December and got an invite for 12 April. Please look at this. |
| R-41325 | 2026-06-05T22:13 | copper.studio | es-ES | parser | app | 12/6 -> 6/12 | The reminder for 12 June arrived for 6 December. |
| R-41327 | 2026-06-06T08:52 | morrow.tax | fr-FR | parser | email | 1/9 -> 9/1 | My client came on 9 January instead of 1 September. We sorted it out. |
| R-41328 | 2026-06-06T20:06 | morrow.tax | fr-FR | parser | app | 5/2 -> 2/5 | My client came on 2 May instead of 5 February. We sorted it out. |
| R-41329 | 2026-06-07T11:27 | harbour.dental | en-GB | parser | app | 12/11 -> 11/12 | The calendar invite for 12 November landed on 11 December. Nobody here touched it. |
| R-41330 | 2026-06-07T16:11 | alder.physio | de-DE | parser | app | 7/4 -> 4/7 | Customer booked 7 April and got an invite for 4 July. Please look at this. |
| R-41331 | 2026-06-07T17:36 | alder.physio | en-GB | parser | email | 2/4 -> 4/2 | Customer booked 2 April and got an invite for 4 February. Please look at this. |
| R-41332 | 2026-06-07T20:06 | nine.lanterns | pl-PL | parser | app | 9/1 -> 1/9 | We had two people show up on 1 September. They were booked for 9 January. |
| R-41333 | 2026-06-07T22:08 | long.table | it-IT | parser | email | Saturday 12/9 -> Wednesday 9/12 | Saturday 12 September showed as Wednesday 9 December. I moved it myself. |
| R-41334 | 2026-06-08T10:59 | lantern.row | cs-CZ | parser | app | 5/2 -> 2/5 | My client came on 2 May instead of 5 February. We sorted it out. |
| R-41335 | 2026-06-08T20:22 | ridge.clinic | en-GB | parser | email | 9/10 -> 10/9 | The calendar invite for 9 October landed on 10 September. Nobody here touched it. |
| R-41336 | 2026-06-08T20:25 | kettle.books | nl-NL | parser | app | Tuesday 12/5 -> Saturday 5/12 | Tuesday 12 May showed as Saturday 5 December. I moved it myself. |
| R-41337 | 2026-06-08T21:27 | ridge.clinic | da-DK | parser | email | 6/8 -> 8/6 | We had two people show up on 8 June. They were booked for 6 August. |
| R-41338 | 2026-06-09T08:51 | kettle.books | nl-NL | parser | app | Saturday 7/2 -> Thursday 2/7 | Saturday 7 February showed as Thursday 2 July. I moved it myself. |
| R-41339 | 2026-06-09T22:38 | morrow.tax | en-US | hint | form | 5/3 -> 3/5 | The calendar invite for 5 March landed on 3 May. Nobody here touched it. |
| R-41340 | 2026-06-10T18:22 | morrow.tax | fr-FR | parser | app | Tuesday 8/9 -> Sunday 9/8 | Invite says Sunday 9 August. We agreed Tuesday 8 September. Which one do I trust? |
| R-41341 | 2026-06-10T22:43 | nine.lanterns | pl-PL | parser | app | 9/6 -> 6/9 | The calendar invite for 9 June landed on 6 September. Nobody here touched it. |
| R-41342 | 2026-06-11T08:32 | stone.and.sons | en-IE | parser | email | 4/3 -> 3/4 | Every booking we make shows the wrong day. 4 March is now 3 April. |
| R-41343 | 2026-06-11T15:23 | long.table | it-IT | parser | email | 6/5 -> 5/6 | The calendar invite for 6 May landed on 5 June. Nobody here touched it. |
| R-41345 | 2026-06-12T22:52 | ridge.clinic | da-DK | parser | app | 9/2 -> 2/9 | Customer booked 9 February and got an invite for 2 September. Please look at this. |
| R-41346 | 2026-06-13T13:25 | nine.lanterns | pl-PL | parser | app | 11/1 -> 1/11 | Booked for 11 January. The invite says 1 November. |
| R-41347 | 2026-06-13T17:11 | morrow.tax | fr-FR | parser | app | 1/7 -> 7/1 | Second time this month: 1 July turned into 7 January. |
| R-41348 | 2026-06-14T12:50 | morrow.tax | fr-FR | parser | app | 10/7 -> 7/10 | The reminder for 10 July arrived for 7 October. |
| R-41349 | 2026-06-14T14:49 | ridge.clinic | en-GB | parser | form | Thursday 10/9 -> Friday 9/10 | Thursday 10 September showed as Friday 9 October. I moved it myself. |
| R-41350 | 2026-06-15T16:29 | kettle.books | nl-NL | parser | email | 2/6 -> 6/2 | Second time this month: 2 June turned into 6 February. |
| R-41351 | 2026-06-16T08:43 | nine.lanterns | pl-PL | parser | app | 11/2 -> 2/11 | Every booking we make shows the wrong day. 11 February is now 2 November. |
| R-41352 | 2026-06-16T10:44 | ridge.clinic | en-GB | parser | app | 5/3 -> 3/5 | Second time this month: 5 March turned into 3 May. |
| R-41353 | 2026-06-16T10:46 | alder.physio | de-DE | parser | email | 3/8 -> 8/3 | Every booking we make shows the wrong day. 3 August is now 8 March. |
| R-41354 | 2026-06-16T15:49 | long.table | en-US | hint | app | 8/6 -> 6/8 | The calendar invite for 8 June landed on 6 August. Nobody here touched it. |
| R-41355 | 2026-06-16T20:42 | copper.studio | es-ES | parser | app | 6/11 -> 11/6 | Customer booked 6 November and got an invite for 11 June. Please look at this. |
| R-41356 | 2026-06-17T12:32 | harbour.dental | en-GB | parser | app | Wednesday 5/8 -> Friday 8/5 | Wednesday 5 August showed as Friday 8 May. I moved it myself. |
| R-41357 | 2026-06-17T14:48 | kettle.books | nl-NL | parser | app | Wednesday 1/7 -> Wednesday 7/1 | Wednesday 1 July showed as Wednesday 7 January. I moved it myself. |
| R-41358 | 2026-06-17T21:40 | harbour.dental | en-GB | parser | email | 1/7 -> 7/1 | The reminder for 1 July arrived for 7 January. |
| R-41359 | 2026-06-18T08:01 | ridge.clinic | da-DK | parser | email | Thursday 9/4 -> Friday 4/9 | Invite says Friday 4 September. We agreed Thursday 9 April. Which one do I trust? |
| R-41360 | 2026-06-18T11:29 | lantern.row | cs-CZ | parser | email | 10/4 -> 4/10 | We had two people show up on 4 October. They were booked for 10 April. |
| R-41361 | 2026-06-18T21:08 | harbour.dental | en-GB | parser | email | 1/8 -> 8/1 | The calendar invite for 1 August landed on 8 January. Nobody here touched it. |
| R-41362 | 2026-06-19T13:21 | morrow.tax | fr-FR | parser | email | 12/2 -> 2/12 | Customer booked 12 February and got an invite for 2 December. Please look at this. |
| R-41363 | 2026-06-19T14:27 | nine.lanterns | pl-PL | parser | email | 1/12 -> 12/1 | My client came on 12 January instead of 1 December. We sorted it out. |
| R-41364 | 2026-06-20T14:19 | ridge.clinic | da-DK | parser | email | 1/10 -> 10/1 | We had two people show up on 10 January. They were booked for 1 October. |
| R-41365 | 2026-06-20T21:21 | morrow.tax | fr-FR | parser | app | Wednesday 8/4 -> Tuesday 4/8 | Invite says Tuesday 4 August. We agreed Wednesday 8 April. Which one do I trust? |
| R-41366 | 2026-06-21T13:17 | alder.physio | en-US | hint | form | Sunday 11/10 -> Tuesday 10/11 | Sunday 11 October showed as Tuesday 10 November. I moved it myself. |
| R-41367 | 2026-06-22T12:14 | kettle.books | nl-NL | parser | app | Wednesday 11/3 -> Tuesday 3/11 | Wednesday 11 March showed as Tuesday 3 November. I moved it myself. |
| R-41368 | 2026-06-24T09:08 | long.table | it-IT | parser | app | 4/9 -> 9/4 | We had two people show up on 9 April. They were booked for 4 September. |
| R-41369 | 2026-06-25T11:43 | nine.lanterns | en-GB | parser | form | 5/11 -> 11/5 | Booked for 5 November. The invite says 11 May. |
| R-41370 | 2026-06-25T11:59 | pale.harbour | en-US | hint | email | 9/12 -> 12/9 | The calendar invite for 9 December landed on 12 September. Nobody here touched it. |
| R-41371 | 2026-06-25T15:06 | copper.studio | es-ES | parser | app | 7/6 -> 6/7 | The calendar invite for 7 June landed on 6 July. Nobody here touched it. |
| R-41372 | 2026-06-25T20:34 | alder.physio | en-US | hint | form | Sunday 9/8 -> Tuesday 8/9 | Invite says Tuesday 8 September. We agreed Sunday 9 August. Which one do I trust? |
| R-41373 | 2026-06-26T09:18 | kettle.books | nl-NL | parser | app | 7/3 -> 3/7 | Booked for 7 March. The invite says 3 July. |
| R-41374 | 2026-06-26T09:57 | nine.lanterns | pl-PL | parser | app | 9/11 -> 11/9 | The reminder for 9 November arrived for 11 September. |
| R-41375 | 2026-06-27T11:13 | ridge.clinic | da-DK | parser | email | 7/4 -> 4/7 | The calendar invite for 7 April landed on 4 July. Nobody here touched it. |
| R-41376 | 2026-06-27T19:29 | kettle.books | en-GB | parser | app | 12/3 -> 3/12 | The reminder for 12 March arrived for 3 December. |
| R-41377 | 2026-06-28T10:38 | harbour.dental | en-GB | parser | email | 2/3 -> 3/2 | Second time this month: 2 March turned into 3 February. |
| R-41378 | 2026-06-29T08:06 | long.table | it-IT | parser | app | 7/2 -> 2/7 | The reminder for 7 February arrived for 2 July. |
| R-41379 | 2026-06-30T08:21 | harbour.dental | en-GB | parser | app | 10/12 -> 12/10 | We had two people show up on 12 October. They were booked for 10 December. |
| R-41380 | 2026-06-30T10:27 | long.table | it-IT | parser | email | 5/7 -> 7/5 | We had two people show up on 7 May. They were booked for 5 July. |
| R-41381 | 2026-06-30T16:46 | kettle.books | nl-NL | parser | email | 2/10 -> 10/2 | My client came on 10 February instead of 2 October. We sorted it out. |
| R-41382 | 2026-06-30T18:12 | alder.physio | de-DE | parser | app | 6/8 -> 8/6 | Every booking we make shows the wrong day. 6 August is now 8 June. |
| R-41383 | 2026-07-01T13:45 | long.table | en-US | hint | app | Monday 3/8 -> Sunday 8/3 | Monday 3 August showed as Sunday 8 March. I moved it myself. |
| R-41384 | 2026-07-01T15:19 | copper.studio | es-ES | parser | form | 8/1 -> 1/8 | The calendar invite for 8 January landed on 1 August. Nobody here touched it. |
| R-41385 | 2026-07-01T20:36 | harbour.dental | en-GB | parser | app | 5/12 -> 12/5 | Second time this month: 5 December turned into 12 May. |
| R-41386 | 2026-07-01T21:52 | harbour.dental | en-GB | parser | form | 10/8 -> 8/10 | Second time this month: 10 August turned into 8 October. |
| R-41387 | 2026-07-02T08:17 | copper.studio | en-US | hint | form | Friday 10/4 -> Sunday 4/10 | Invite says Sunday 4 October. We agreed Friday 10 April. Which one do I trust? |
| R-41388 | 2026-07-02T21:41 | pale.harbour | pt-PT | parser | email | Wednesday 1/4 -> Sunday 4/1 | Invite says Sunday 4 January. We agreed Wednesday 1 April. Which one do I trust? |
| R-41389 | 2026-07-03T19:42 | ridge.clinic | da-DK | parser | email | Wednesday 4/2 -> Thursday 2/4 | Wednesday 4 February showed as Thursday 2 April. I moved it myself. |
| R-41390 | 2026-07-05T08:08 | harbour.dental | en-US | hint | app | 8/9 -> 9/8 | We had two people show up on 9 August. They were booked for 8 September. |
| R-41391 | 2026-07-05T11:06 | copper.studio | es-ES | parser | email | 12/10 -> 10/12 | The reminder for 12 October arrived for 10 December. |
| R-41392 | 2026-07-05T13:19 | ridge.clinic | en-GB | parser | app | 3/2 -> 2/3 | The reminder for 3 February arrived for 2 March. |
| R-41393 | 2026-07-06T12:22 | kettle.books | nl-NL | parser | email | 1/7 -> 7/1 | The reminder for 1 July arrived for 7 January. |
| R-41394 | 2026-07-06T13:12 | morrow.tax | fr-FR | parser | app | 9/1 -> 1/9 | We had two people show up on 1 September. They were booked for 9 January. |
| R-41395 | 2026-07-07T17:15 | ridge.clinic | da-DK | parser | app | Sunday 5/7 -> Thursday 7/5 | Sunday 5 July showed as Thursday 7 May. I moved it myself. |
| R-41396 | 2026-07-07T19:19 | alder.physio | en-US | hint | form | 4/10 -> 10/4 | My client came on 10 April instead of 4 October. We sorted it out. |
| R-41397 | 2026-07-07T19:05 | stone.and.sons | en-IE | parser | form | 12/4 -> 4/12 | My client came on 4 December instead of 12 April. We sorted it out. |
| R-41398 | 2026-07-07T22:47 | ridge.clinic | da-DK | parser | app | 7/6 -> 6/7 | The calendar invite for 7 June landed on 6 July. Nobody here touched it. |
| R-41399 | 2026-07-08T12:03 | ridge.clinic | da-DK | parser | email | 2/3 -> 3/2 | The reminder for 2 March arrived for 3 February. |
| R-41400 | 2026-07-09T15:16 | copper.studio | es-ES | parser | form | 10/11 -> 11/10 | We had two people show up on 11 October. They were booked for 10 November. |
| R-41401 | 2026-07-09T16:13 | copper.studio | es-ES | parser | app | 6/10 -> 10/6 | We had two people show up on 10 June. They were booked for 6 October. |
| R-41402 | 2026-07-10T13:17 | pale.harbour | pt-PT | parser | app | 4/9 -> 9/4 | The reminder for 4 September arrived for 9 April. |
| R-41403 | 2026-07-10T16:32 | copper.studio | es-ES | parser | app | 7/2 -> 2/7 | The reminder for 7 February arrived for 2 July. |
| R-41404 | 2026-07-10T15:56 | harbour.dental | en-GB | parser | email | 2/1 -> 1/2 | My client came on 1 February instead of 2 January. We sorted it out. |
| R-41405 | 2026-07-11T15:22 | kettle.books | nl-NL | parser | email | 1/10 -> 10/1 | Every booking we make shows the wrong day. 1 October is now 10 January. |
| R-41406 | 2026-07-11T17:06 | pale.harbour | pt-PT | parser | form | 8/7 -> 7/8 | Every booking we make shows the wrong day. 8 July is now 7 August. |
| R-41408 | 2026-07-12T14:40 | kettle.books | en-GB | parser | app | 12/11 -> 11/12 | Every booking we make shows the wrong day. 12 November is now 11 December. |
| R-41409 | 2026-07-12T14:52 | kettle.books | nl-NL | parser | app | 6/4 -> 4/6 | My client came on 4 June instead of 6 April. We sorted it out. |
| R-41410 | 2026-07-12T15:02 | morrow.tax | en-GB | parser | form | Tuesday 10/2 -> Friday 2/10 | Invite says Friday 2 October. We agreed Tuesday 10 February. Which one do I trust? |
| R-41411 | 2026-07-12T17:04 | nine.lanterns | pl-PL | parser | email | Wednesday 8/7 -> Friday 7/8 | Invite says Friday 7 August. We agreed Wednesday 8 July. Which one do I trust? |
| R-41412 | 2026-07-12T22:40 | nine.lanterns | en-US | hint | form | Wednesday 8/7 -> Friday 7/8 | Wednesday 8 July showed as Friday 7 August. I moved it myself. |
| R-41413 | 2026-07-13T16:27 | alder.physio | de-DE | parser | email | 10/5 -> 5/10 | The reminder for 10 May arrived for 5 October. |
| R-41414 | 2026-07-13T20:54 | harbour.dental | en-GB | parser | email | Sunday 7/6 -> Monday 6/7 | Invite says Monday 6 July. We agreed Sunday 7 June. Which one do I trust? |
| R-41415 | 2026-07-14T07:43 | pale.harbour | pt-PT | parser | form | 9/1 -> 1/9 | The calendar invite for 9 January landed on 1 September. Nobody here touched it. |
| R-41416 | 2026-07-14T09:29 | pale.harbour | en-US | hint | form | 1/11 -> 11/1 | The reminder for 1 November arrived for 11 January. |
| R-41418 | 2026-07-14T17:03 | alder.physio | en-US | hint | form | 1/12 -> 12/1 | The reminder for 1 December arrived for 12 January. |
| R-41419 | 2026-07-15T17:57 | alder.physio | de-DE | parser | email | 9/8 -> 8/9 | Booked for 9 August. The invite says 8 September. |
| R-41420 | 2026-07-15T21:14 | copper.studio | es-ES | parser | email | Friday 11/9 -> Monday 9/11 | Invite says Monday 9 November. We agreed Friday 11 September. Which one do I trust? |
| R-41421 | 2026-07-15T22:49 | alder.physio | en-GB | parser | app | 8/7 -> 7/8 | My client came on 7 August instead of 8 July. We sorted it out. |
| R-41422 | 2026-07-16T09:20 | kettle.books | nl-NL | parser | app | Friday 5/6 -> Wednesday 6/5 | Invite says Wednesday 6 May. We agreed Friday 5 June. Which one do I trust? |
| R-41423 | 2026-07-16T12:00 | nine.lanterns | pl-PL | parser | app | 8/10 -> 10/8 | We had two people show up on 10 August. They were booked for 8 October. |
| R-41424 | 2026-07-16T20:03 | alder.physio | en-US | hint | app | 4/8 -> 8/4 | Customer booked 4 August and got an invite for 8 April. Please look at this. |
| R-41425 | 2026-07-16T22:17 | lantern.row | cs-CZ | parser | email | Saturday 1/8 -> Thursday 8/1 | Invite says Thursday 8 January. We agreed Saturday 1 August. Which one do I trust? |
| R-41427 | 2026-07-18T18:09 | lantern.row | cs-CZ | parser | email | 10/7 -> 7/10 | We had two people show up on 7 October. They were booked for 10 July. |
| R-41428 | 2026-07-19T08:01 | copper.studio | es-ES | parser | form | 7/6 -> 6/7 | My client came on 6 July instead of 7 June. We sorted it out. |
| R-41429 | 2026-07-19T15:45 | alder.physio | de-DE | parser | app | 5/12 -> 12/5 | Booked for 5 December. The invite says 12 May. |
| R-41430 | 2026-07-19T22:06 | lantern.row | cs-CZ | parser | app | Tuesday 1/9 -> Friday 9/1 | Tuesday 1 September showed as Friday 9 January. I moved it myself. |
| R-41431 | 2026-07-20T12:27 | harbour.dental | en-GB | parser | app | Sunday 4/10 -> Friday 10/4 | Invite says Friday 10 April. We agreed Sunday 4 October. Which one do I trust? |
| R-41432 | 2026-07-20T15:14 | lantern.row | cs-CZ | parser | app | Monday 12/1 -> Tuesday 1/12 | Monday 12 January showed as Tuesday 1 December. I moved it myself. |
| R-41433 | 2026-07-21T13:32 | harbour.dental | en-GB | parser | app | 12/7 -> 7/12 | Customer booked 12 July and got an invite for 7 December. Please look at this. |
| R-41434 | 2026-07-21T18:41 | nine.lanterns | en-US | hint | email | 1/10 -> 10/1 | The reminder for 1 October arrived for 10 January. |
| R-41435 | 2026-07-21T19:00 | harbour.dental | en-GB | parser | email | 7/10 -> 10/7 | Customer booked 7 October and got an invite for 10 July. Please look at this. |
| R-41436 | 2026-07-21T21:40 | morrow.tax | fr-FR | parser | app | 2/1 -> 1/2 | Customer booked 2 January and got an invite for 1 February. Please look at this. |
| R-41437 | 2026-07-22T07:02 | stone.and.sons | en-IE | parser | app | Wednesday 4/3 -> Friday 3/4 | Wednesday 4 March showed as Friday 3 April. I moved it myself. |
| R-41438 | 2026-07-22T11:54 | kettle.books | nl-NL | parser | email | Wednesday 3/6 -> Friday 6/3 | Wednesday 3 June showed as Friday 6 March. I moved it myself. |
| R-41439 | 2026-07-22T14:51 | alder.physio | en-US | hint | form | 3/1 -> 1/3 | Booked for 3 January. The invite says 1 March. |
| R-41440 | 2026-07-23T16:06 | morrow.tax | fr-FR | parser | email | 1/11 -> 11/1 | Booked for 1 November. The invite says 11 January. |
| R-41441 | 2026-07-23T15:17 | pale.harbour | en-US | hint | form | 6/4 -> 4/6 | The reminder for 6 April arrived for 4 June. |
| R-41442 | 2026-07-24T10:15 | morrow.tax | fr-FR | parser | email | 4/6 -> 6/4 | Every booking we make shows the wrong day. 4 June is now 6 April. |
| R-41443 | 2026-07-24T12:28 | nine.lanterns | pl-PL | parser | app | 10/5 -> 5/10 | Second time this month: 10 May turned into 5 October. |
| R-41444 | 2026-07-25T21:59 | harbour.dental | en-GB | parser | app | 2/5 -> 5/2 | Customer booked 2 May and got an invite for 5 February. Please look at this. |
| R-41445 | 2026-07-26T09:05 | lantern.row | cs-CZ | parser | email | 10/3 -> 3/10 | Second time this month: 10 March turned into 3 October. |
| R-41446 | 2026-07-27T18:22 | copper.studio | es-ES | parser | app | 5/6 -> 6/5 | We had two people show up on 6 May. They were booked for 5 June. |
| R-41447 | 2026-07-27T21:45 | nine.lanterns | pl-PL | parser | app | 2/6 -> 6/2 | My client came on 6 February instead of 2 June. We sorted it out. |
| R-41448 | 2026-07-28T09:48 | nine.lanterns | pl-PL | parser | email | Tuesday 4/8 -> Wednesday 8/4 | Tuesday 4 August showed as Wednesday 8 April. I moved it myself. |
| R-41449 | 2026-07-29T17:47 | alder.physio | de-DE | parser | form | Thursday 8/1 -> Saturday 1/8 | Thursday 8 January showed as Saturday 1 August. I moved it myself. |
| R-41450 | 2026-07-29T20:22 | kettle.books | nl-NL | parser | app | Sunday 5/4 -> Monday 4/5 | Sunday 5 April showed as Monday 4 May. I moved it myself. |
| R-41451 | 2026-07-30T11:32 | ridge.clinic | da-DK | parser | email | 8/6 -> 6/8 | We had two people show up on 6 August. They were booked for 8 June. |
| R-41452 | 2026-07-30T11:48 | kettle.books | nl-NL | parser | email | 10/2 -> 2/10 | We had two people show up on 2 October. They were booked for 10 February. |
| R-41453 | 2026-07-30T15:44 | copper.studio | en-US | hint | form | 10/2 -> 2/10 | Booked for 10 February. The invite says 2 October. |
| R-41454 | 2026-07-31T16:31 | lantern.row | cs-CZ | parser | app | 10/6 -> 6/10 | The calendar invite for 10 June landed on 6 October. Nobody here touched it. |
| R-41455 | 2026-07-31T17:03 | kettle.books | nl-NL | parser | email | 9/5 -> 5/9 | My client came on 5 September instead of 9 May. We sorted it out. |
| R-41456 | 2026-07-31T17:35 | alder.physio | en-US | hint | form | 1/6 -> 6/1 | My client came on 6 January instead of 1 June. We sorted it out. |
| R-41457 | 2026-07-31T19:10 | morrow.tax | fr-FR | parser | app | 6/2 -> 2/6 | Customer booked 6 February and got an invite for 2 June. Please look at this. |
| R-41458 | 2026-08-01T08:35 | morrow.tax | en-GB | parser | app | 2/9 -> 9/2 | Customer booked 2 September and got an invite for 9 February. Please look at this. |
| R-41459 | 2026-08-01T09:27 | harbour.dental | en-GB | parser | app | 9/6 -> 6/9 | Second time this month: 9 June turned into 6 September. |
| R-41460 | 2026-08-01T13:05 | pale.harbour | pt-PT | parser | form | 5/7 -> 7/5 | Second time this month: 5 July turned into 7 May. |
| R-41461 | 2026-08-01T16:27 | long.table | it-IT | parser | email | 3/5 -> 5/3 | We had two people show up on 5 March. They were booked for 3 May. |
| R-41462 | 2026-08-01T16:35 | harbour.dental | en-GB | parser | email | 8/4 -> 4/8 | Every booking we make shows the wrong day. 8 April is now 4 August. |
| R-41463 | 2026-08-02T07:37 | stone.and.sons | en-US | hint | app | 5/10 -> 10/5 | Second time this month: 5 October turned into 10 May. |
| R-41464 | 2026-08-02T14:27 | morrow.tax | fr-FR | parser | app | Sunday 12/4 -> Friday 4/12 | Invite says Friday 4 December. We agreed Sunday 12 April. Which one do I trust? |
| R-41465 | 2026-08-04T07:55 | pale.harbour | pt-PT | parser | app | 10/8 -> 8/10 | The calendar invite for 10 August landed on 8 October. Nobody here touched it. |
| R-41466 | 2026-08-04T22:44 | lantern.row | cs-CZ | parser | app | 11/9 -> 9/11 | We had two people show up on 9 November. They were booked for 11 September. |
| R-41467 | 2026-08-05T14:32 | kettle.books | en-GB | parser | form | Saturday 10/1 -> Thursday 1/10 | Saturday 10 January showed as Thursday 1 October. I moved it myself. |
| R-41468 | 2026-08-05T14:53 | nine.lanterns | pl-PL | parser | app | 6/5 -> 5/6 | Booked for 6 May. The invite says 5 June. |
| R-41469 | 2026-08-05T13:59 | harbour.dental | en-GB | parser | app | 1/8 -> 8/1 | The reminder for 1 August arrived for 8 January. |
| R-41470 | 2026-08-06T11:37 | stone.and.sons | en-US | hint | email | 10/12 -> 12/10 | The calendar invite for 10 December landed on 12 October. Nobody here touched it. |
| R-41471 | 2026-08-06T18:29 | pale.harbour | pt-PT | parser | app | 11/1 -> 1/11 | Second time this month: 11 January turned into 1 November. |
| R-41472 | 2026-08-09T20:37 | alder.physio | en-US | hint | form | Tuesday 9/6 -> Sunday 6/9 | Tuesday 9 June showed as Sunday 6 September. I moved it myself. |
| R-41473 | 2026-08-10T15:27 | nine.lanterns | pl-PL | parser | email | Wednesday 1/7 -> Wednesday 7/1 | Wednesday 1 July showed as Wednesday 7 January. I moved it myself. |
| R-41474 | 2026-08-11T11:28 | nine.lanterns | pl-PL | parser | app | 4/1 -> 1/4 | The calendar invite for 4 January landed on 1 April. Nobody here touched it. |
| R-41475 | 2026-08-11T19:53 | morrow.tax | fr-FR | parser | app | 2/7 -> 7/2 | Booked for 2 July. The invite says 7 February. |
| R-41476 | 2026-08-12T09:16 | nine.lanterns | pl-PL | parser | app | 2/3 -> 3/2 | Booked for 2 March. The invite says 3 February. |
| R-41477 | 2026-08-12T22:58 | kettle.books | nl-NL | parser | email | 10/6 -> 6/10 | Every booking we make shows the wrong day. 10 June is now 6 October. |
| R-41478 | 2026-08-13T09:09 | harbour.dental | en-GB | parser | email | 6/3 -> 3/6 | We had two people show up on 3 June. They were booked for 6 March. |
| R-41479 | 2026-08-14T09:32 | long.table | it-IT | parser | app | Friday 9/10 -> Thursday 10/9 | Invite says Thursday 10 September. We agreed Friday 9 October. Which one do I trust? |
| R-41480 | 2026-08-14T14:24 | long.table | it-IT | parser | app | Monday 8/6 -> Thursday 6/8 | Monday 8 June showed as Thursday 6 August. I moved it myself. |
| R-41481 | 2026-08-14T15:28 | morrow.tax | en-US | hint | email | 1/12 -> 12/1 | We had two people show up on 12 January. They were booked for 1 December. |
| R-41482 | 2026-08-14T14:59 | pale.harbour | pt-PT | parser | email | 1/11 -> 11/1 | The reminder for 1 November arrived for 11 January. |
| R-41483 | 2026-08-14T17:27 | lantern.row | cs-CZ | parser | app | 2/5 -> 5/2 | The reminder for 2 May arrived for 5 February. |
| R-41484 | 2026-08-14T17:28 | long.table | it-IT | parser | app | Thursday 8/1 -> Saturday 1/8 | Thursday 8 January showed as Saturday 1 August. I moved it myself. |
| R-41485 | 2026-08-14T21:55 | alder.physio | de-DE | parser | form | 4/11 -> 11/4 | The reminder for 4 November arrived for 11 April. |
| R-41486 | 2026-08-15T09:19 | kettle.books | nl-NL | parser | app | 5/12 -> 12/5 | Customer booked 5 December and got an invite for 12 May. Please look at this. |
| R-41487 | 2026-08-15T14:00 | nine.lanterns | en-GB | parser | email | 10/9 -> 9/10 | The reminder for 10 September arrived for 9 October. |
| R-41488 | 2026-08-17T16:50 | kettle.books | nl-NL | parser | app | Monday 6/7 -> Sunday 7/6 | Monday 6 July showed as Sunday 7 June. I moved it myself. |
| R-41489 | 2026-08-18T09:32 | kettle.books | en-GB | parser | app | 5/4 -> 4/5 | The reminder for 5 April arrived for 4 May. |
| R-41490 | 2026-08-18T10:36 | ridge.clinic | da-DK | parser | app | 2/6 -> 6/2 | We had two people show up on 6 February. They were booked for 2 June. |
| R-41491 | 2026-08-18T17:53 | ridge.clinic | da-DK | parser | app | 12/10 -> 10/12 | Booked for 12 October. The invite says 10 December. |
| R-41492 | 2026-08-19T12:08 | lantern.row | en-GB | parser | email | 12/11 -> 11/12 | Second time this month: 12 November turned into 11 December. |
| R-41493 | 2026-08-19T11:18 | pale.harbour | en-US | hint | form | 2/7 -> 7/2 | The reminder for 2 July arrived for 7 February. |
| R-41494 | 2026-08-19T16:11 | alder.physio | de-DE | parser | app | 3/11 -> 11/3 | Customer booked 3 November and got an invite for 11 March. Please look at this. |
| R-41495 | 2026-08-19T15:12 | stone.and.sons | en-IE | parser | app | Friday 2/10 -> Tuesday 10/2 | Invite says Tuesday 10 February. We agreed Friday 2 October. Which one do I trust? |
| R-41496 | 2026-08-19T18:17 | nine.lanterns | pl-PL | parser | email | 11/2 -> 2/11 | Booked for 11 February. The invite says 2 November. |
| R-41497 | 2026-08-19T22:37 | morrow.tax | fr-FR | parser | app | 12/11 -> 11/12 | Second time this month: 12 November turned into 11 December. |
| R-41498 | 2026-08-20T14:10 | long.table | it-IT | parser | app | 9/8 -> 8/9 | Second time this month: 9 August turned into 8 September. |
| R-41499 | 2026-08-20T16:53 | lantern.row | en-US | hint | app | 3/6 -> 6/3 | Second time this month: 3 June turned into 6 March. |
| R-41500 | 2026-08-20T22:53 | kettle.books | nl-NL | parser | email | 6/2 -> 2/6 | Second time this month: 6 February turned into 2 June. |
| R-41501 | 2026-08-21T08:13 | morrow.tax | fr-FR | parser | email | Thursday 9/7 -> Monday 7/9 | Invite says Monday 7 September. We agreed Thursday 9 July. Which one do I trust? |
| R-41502 | 2026-08-21T09:49 | kettle.books | nl-NL | parser | email | Thursday 5/3 -> Sunday 3/5 | Thursday 5 March showed as Sunday 3 May. I moved it myself. |
| R-41503 | 2026-08-21T17:09 | copper.studio | en-GB | parser | app | 2/1 -> 1/2 | My client came on 1 February instead of 2 January. We sorted it out. |
| R-41504 | 2026-08-21T19:24 | morrow.tax | en-GB | parser | app | 9/11 -> 11/9 | Customer booked 9 November and got an invite for 11 September. Please look at this. |
| R-41505 | 2026-08-22T12:08 | morrow.tax | en-US | hint | email | 9/6 -> 6/9 | Customer booked 9 June and got an invite for 6 September. Please look at this. |
| R-41506 | 2026-08-22T14:21 | alder.physio | de-DE | parser | app | Wednesday 5/8 -> Friday 8/5 | Invite says Friday 8 May. We agreed Wednesday 5 August. Which one do I trust? |
| R-41508 | 2026-08-22T18:19 | stone.and.sons | en-US | hint | app | 12/7 -> 7/12 | Booked for 12 July. The invite says 7 December. |
| R-41509 | 2026-08-24T15:09 | morrow.tax | fr-FR | parser | app | Sunday 7/6 -> Monday 6/7 | Sunday 7 June showed as Monday 6 July. I moved it myself. |
| R-41510 | 2026-08-24T20:19 | lantern.row | cs-CZ | parser | app | 12/3 -> 3/12 | Customer booked 12 March and got an invite for 3 December. Please look at this. |
| R-41511 | 2026-08-26T14:32 | long.table | it-IT | parser | email | 5/10 -> 10/5 | Every booking we make shows the wrong day. 5 October is now 10 May. |
| R-41512 | 2026-08-26T21:51 | alder.physio | en-US | hint | app | Monday 8/6 -> Thursday 6/8 | Monday 8 June showed as Thursday 6 August. I moved it myself. |
| R-41513 | 2026-08-26T22:28 | kettle.books | en-US | hint | form | 2/9 -> 9/2 | Second time this month: 2 September turned into 9 February. |
| R-41515 | 2026-08-27T20:34 | stone.and.sons | en-IE | parser | email | 6/4 -> 4/6 | Booked for 6 April. The invite says 4 June. |
| R-41516 | 2026-08-28T07:30 | stone.and.sons | en-US | hint | email | 12/7 -> 7/12 | My client came on 7 December instead of 12 July. We sorted it out. |
| R-41517 | 2026-08-29T09:25 | lantern.row | cs-CZ | parser | email | 10/9 -> 9/10 | Customer booked 10 September and got an invite for 9 October. Please look at this. |
| R-41518 | 2026-08-29T18:47 | lantern.row | cs-CZ | parser | app | 11/7 -> 7/11 | My client came on 7 November instead of 11 July. We sorted it out. |
| R-41519 | 2026-08-29T19:02 | nine.lanterns | en-US | hint | form | Wednesday 4/3 -> Friday 3/4 | Invite says Friday 3 April. We agreed Wednesday 4 March. Which one do I trust? |
| R-41520 | 2026-08-29T19:09 | stone.and.sons | en-IE | parser | email | 7/11 -> 11/7 | The calendar invite for 7 November landed on 11 July. Nobody here touched it. |
| R-41521 | 2026-08-30T11:29 | kettle.books | nl-NL | parser | email | 7/5 -> 5/7 | Customer booked 7 May and got an invite for 5 July. Please look at this. |
| R-41522 | 2026-08-30T14:29 | kettle.books | nl-NL | parser | app | 7/12 -> 12/7 | Customer booked 7 December and got an invite for 12 July. Please look at this. |
| R-41523 | 2026-08-31T11:17 | long.table | it-IT | parser | email | 7/11 -> 11/7 | My client came on 11 July instead of 7 November. We sorted it out. |
| R-41524 | 2026-08-31T13:30 | copper.studio | es-ES | parser | app | 11/10 -> 10/11 | The calendar invite for 11 October landed on 10 November. Nobody here touched it. |
| R-41525 | 2026-08-31T19:47 | lantern.row | cs-CZ | parser | email | 12/1 -> 1/12 | Customer booked 12 January and got an invite for 1 December. Please look at this. |
| R-41527 | 2026-08-31T22:57 | long.table | it-IT | parser | app | 10/9 -> 9/10 | We had two people show up on 9 October. They were booked for 10 September. |
| R-41528 | 2026-09-01T08:30 | long.table | it-IT | parser | app | Wednesday 7/1 -> Wednesday 1/7 | Wednesday 7 January showed as Wednesday 1 July. I moved it myself. |
| R-41529 | 2026-09-01T20:06 | ridge.clinic | da-DK | parser | form | 5/11 -> 11/5 | Booked for 5 November. The invite says 11 May. |
| R-41530 | 2026-09-01T20:56 | kettle.books | en-GB | parser | app | 7/3 -> 3/7 | We had two people show up on 3 July. They were booked for 7 March. |
| R-41531 | 2026-09-02T09:34 | morrow.tax | fr-FR | parser | app | 3/8 -> 8/3 | Customer booked 3 August and got an invite for 8 March. Please look at this. |
| R-41532 | 2026-09-02T09:00 | pale.harbour | pt-PT | parser | email | 5/8 -> 8/5 | Booked for 5 August. The invite says 8 May. |
| R-41533 | 2026-09-03T12:19 | nine.lanterns | pl-PL | parser | app | 10/9 -> 9/10 | The calendar invite for 10 September landed on 9 October. Nobody here touched it. |
| R-41534 | 2026-09-03T19:14 | nine.lanterns | pl-PL | parser | email | Saturday 5/12 -> Tuesday 12/5 | Saturday 5 December showed as Tuesday 12 May. I moved it myself. |
| R-41535 | 2026-09-03T20:34 | stone.and.sons | en-IE | parser | app | 5/8 -> 8/5 | Booked for 5 August. The invite says 8 May. |
| R-41536 | 2026-09-04T13:31 | kettle.books | nl-NL | parser | app | 5/12 -> 12/5 | The reminder for 5 December arrived for 12 May. |
| R-41537 | 2026-09-04T14:11 | long.table | it-IT | parser | app | Saturday 10/1 -> Thursday 1/10 | Saturday 10 January showed as Thursday 1 October. I moved it myself. |
| R-41538 | 2026-09-04T16:25 | long.table | it-IT | parser | app | Thursday 2/4 -> Wednesday 4/2 | Invite says Wednesday 4 February. We agreed Thursday 2 April. Which one do I trust? |
| R-41539 | 2026-09-04T16:31 | copper.studio | es-ES | parser | form | 2/3 -> 3/2 | The reminder for 2 March arrived for 3 February. |
| R-41540 | 2026-09-05T13:58 | kettle.books | nl-NL | parser | email | Friday 6/2 -> Tuesday 2/6 | Invite says Tuesday 2 June. We agreed Friday 6 February. Which one do I trust? |
| R-41541 | 2026-09-06T10:14 | kettle.books | en-GB | parser | app | 1/10 -> 10/1 | My client came on 10 January instead of 1 October. We sorted it out. |
| R-41542 | 2026-09-06T14:06 | ridge.clinic | da-DK | parser | form | 11/5 -> 5/11 | The reminder for 11 May arrived for 5 November. |
| R-41543 | 2026-09-06T15:04 | alder.physio | de-DE | parser | app | 1/2 -> 2/1 | Second time this month: 1 February turned into 2 January. |
| R-41544 | 2026-09-06T17:10 | harbour.dental | en-GB | parser | email | Sunday 10/5 -> Monday 5/10 | Sunday 10 May showed as Monday 5 October. I moved it myself. |
| R-41545 | 2026-09-07T08:06 | pale.harbour | pt-PT | parser | app | Wednesday 6/5 -> Friday 5/6 | Wednesday 6 May showed as Friday 5 June. I moved it myself. |
| R-41546 | 2026-09-07T09:00 | stone.and.sons | en-IE | parser | app | 1/12 -> 12/1 | The calendar invite for 1 December landed on 12 January. Nobody here touched it. |
| R-41547 | 2026-09-07T21:27 | long.table | en-GB | parser | app | 8/11 -> 11/8 | Every booking we make shows the wrong day. 8 November is now 11 August. |
| R-41548 | 2026-09-08T08:51 | stone.and.sons | en-IE | parser | app | 12/9 -> 9/12 | My client came on 9 December instead of 12 September. We sorted it out. |
| R-41549 | 2026-09-08T10:00 | harbour.dental | en-GB | parser | app | Friday 3/7 -> Saturday 7/3 | Friday 3 July showed as Saturday 7 March. I moved it myself. |
| R-41550 | 2026-09-08T17:55 | ridge.clinic | en-GB | parser | app | Monday 7/9 -> Thursday 9/7 | Monday 7 September showed as Thursday 9 July. I moved it myself. |
| R-41551 | 2026-09-08T18:03 | kettle.books | nl-NL | parser | email | 9/6 -> 6/9 | Second time this month: 9 June turned into 6 September. |
| R-41552 | 2026-09-09T10:06 | ridge.clinic | da-DK | parser | email | 1/5 -> 5/1 | We had two people show up on 5 January. They were booked for 1 May. |
| R-41553 | 2026-09-09T14:21 | stone.and.sons | en-IE | parser | app | 11/2 -> 2/11 | Booked for 11 February. The invite says 2 November. |
| R-41554 | 2026-09-09T17:50 | morrow.tax | en-GB | parser | app | 8/2 -> 2/8 | Customer booked 8 February and got an invite for 2 August. Please look at this. |
| R-41555 | 2026-09-10T15:00 | ridge.clinic | en-GB | parser | app | 11/1 -> 1/11 | My client came on 1 November instead of 11 January. We sorted it out. |
| R-41556 | 2026-09-10T21:14 | pale.harbour | pt-PT | parser | app | Friday 2/10 -> Tuesday 10/2 | Invite says Tuesday 10 February. We agreed Friday 2 October. Which one do I trust? |
| R-41557 | 2026-09-11T09:38 | morrow.tax | fr-FR | parser | email | 4/10 -> 10/4 | The calendar invite for 4 October landed on 10 April. Nobody here touched it. |
| R-41558 | 2026-09-11T13:08 | kettle.books | en-GB | parser | email | 4/6 -> 6/4 | The reminder for 4 June arrived for 6 April. |
| R-41559 | 2026-09-11T20:20 | stone.and.sons | en-IE | parser | email | Sunday 8/2 -> Sunday 2/8 | Invite says Sunday 2 August. We agreed Sunday 8 February. Which one do I trust? |
| R-41560 | 2026-09-12T18:31 | long.table | it-IT | parser | app | 10/8 -> 8/10 | Second time this month: 10 August turned into 8 October. |
| R-41561 | 2026-09-12T20:47 | alder.physio | de-DE | parser | email | 1/4 -> 4/1 | Customer booked 1 April and got an invite for 4 January. Please look at this. |
| R-41562 | 2026-09-13T09:32 | stone.and.sons | en-IE | parser | app | 10/9 -> 9/10 | We had two people show up on 9 October. They were booked for 10 September. |
| R-41563 | 2026-09-13T12:54 | morrow.tax | fr-FR | parser | email | 1/9 -> 9/1 | Customer booked 1 September and got an invite for 9 January. Please look at this. |
| R-41564 | 2026-09-13T17:15 | nine.lanterns | pl-PL | parser | app | 7/8 -> 8/7 | Booked for 7 August. The invite says 8 July. |
| R-41565 | 2026-09-14T16:40 | harbour.dental | en-GB | parser | app | 9/3 -> 3/9 | Booked for 9 March. The invite says 3 September. |
| R-41566 | 2026-09-14T17:31 | pale.harbour | en-GB | parser | app | 7/6 -> 6/7 | Second time this month: 7 June turned into 6 July. |
| R-41567 | 2026-09-15T15:52 | harbour.dental | en-GB | parser | app | Thursday 11/6 -> Friday 6/11 | Thursday 11 June showed as Friday 6 November. I moved it myself. |
| R-41568 | 2026-09-15T20:35 | alder.physio | de-DE | parser | app | 4/12 -> 12/4 | Booked for 4 December. The invite says 12 April. |
| R-41569 | 2026-09-16T13:14 | morrow.tax | fr-FR | parser | email | 10/2 -> 2/10 | Booked for 10 February. The invite says 2 October. |
| R-41570 | 2026-09-17T12:08 | nine.lanterns | pl-PL | parser | app | 1/6 -> 6/1 | Second time this month: 1 June turned into 6 January. |
| R-41571 | 2026-09-17T13:08 | ridge.clinic | en-GB | parser | email | 4/11 -> 11/4 | The reminder for 4 November arrived for 11 April. |
| R-41572 | 2026-09-17T17:17 | copper.studio | en-US | hint | form | Thursday 7/5 -> Sunday 5/7 | Invite says Sunday 5 July. We agreed Thursday 7 May. Which one do I trust? |
| R-41573 | 2026-09-17T22:45 | morrow.tax | fr-FR | parser | email | 3/2 -> 2/3 | The reminder for 3 February arrived for 2 March. |
| R-41574 | 2026-09-18T12:27 | long.table | it-IT | parser | email | Wednesday 12/8 -> Tuesday 8/12 | Wednesday 12 August showed as Tuesday 8 December. I moved it myself. |
| R-41575 | 2026-09-18T12:46 | nine.lanterns | pl-PL | parser | email | Thursday 2/7 -> Saturday 7/2 | Thursday 2 July showed as Saturday 7 February. I moved it myself. |
| R-41576 | 2026-09-19T22:35 | kettle.books | en-GB | parser | email | 12/1 -> 1/12 | Customer booked 12 January and got an invite for 1 December. Please look at this. |
| R-41577 | 2026-09-20T10:02 | nine.lanterns | en-GB | parser | email | 8/6 -> 6/8 | The calendar invite for 8 June landed on 6 August. Nobody here touched it. |
| R-41578 | 2026-09-20T19:01 | nine.lanterns | pl-PL | parser | email | Friday 9/10 -> Thursday 10/9 | Invite says Thursday 10 September. We agreed Friday 9 October. Which one do I trust? |
| R-41579 | 2026-09-20T18:49 | pale.harbour | pt-PT | parser | email | 1/3 -> 3/1 | The calendar invite for 1 March landed on 3 January. Nobody here touched it. |
| R-41580 | 2026-09-21T08:29 | harbour.dental | en-GB | parser | email | Saturday 5/12 -> Tuesday 12/5 | Saturday 5 December showed as Tuesday 12 May. I moved it myself. |
| R-41581 | 2026-09-22T12:37 | ridge.clinic | da-DK | parser | app | 5/10 -> 10/5 | My client came on 10 May instead of 5 October. We sorted it out. |
| R-41582 | 2026-09-22T17:15 | pale.harbour | pt-PT | parser | form | 7/3 -> 3/7 | The reminder for 7 March arrived for 3 July. |
| R-41583 | 2026-09-22T19:21 | nine.lanterns | pl-PL | parser | app | 5/2 -> 2/5 | My client came on 2 May instead of 5 February. We sorted it out. |
| R-41584 | 2026-09-22T20:01 | copper.studio | en-US | hint | form | 7/11 -> 11/7 | Every booking we make shows the wrong day. 7 November is now 11 July. |
| R-41585 | 2026-09-22T20:01 | copper.studio | es-ES | parser | app | 1/11 -> 11/1 | My client came on 11 January instead of 1 November. We sorted it out. |
| R-41586 | 2026-09-23T10:51 | kettle.books | nl-NL | parser | app | 6/5 -> 5/6 | Booked for 6 May. The invite says 5 June. |
| R-41587 | 2026-09-23T14:33 | harbour.dental | en-GB | parser | form | 12/4 -> 4/12 | My client came on 4 December instead of 12 April. We sorted it out. |
| R-41588 | 2026-09-23T22:11 | copper.studio | es-ES | parser | app | 5/3 -> 3/5 | The calendar invite for 5 March landed on 3 May. Nobody here touched it. |
| R-41589 | 2026-09-24T11:34 | harbour.dental | en-GB | parser | email | 4/8 -> 8/4 | Every booking we make shows the wrong day. 4 August is now 8 April. |
| R-41590 | 2026-09-24T12:40 | stone.and.sons | en-IE | parser | email | 8/5 -> 5/8 | Second time this month: 8 May turned into 5 August. |
| R-41591 | 2026-09-24T19:45 | harbour.dental | en-GB | parser | app | 6/3 -> 3/6 | The reminder for 6 March arrived for 3 June. |
| R-41592 | 2026-09-24T22:01 | nine.lanterns | pl-PL | parser | email | 11/3 -> 3/11 | My client came on 3 November instead of 11 March. We sorted it out. |
| R-41593 | 2026-09-25T08:37 | copper.studio | es-ES | parser | email | Saturday 3/1 -> Sunday 1/3 | Saturday 3 January showed as Sunday 1 March. I moved it myself. |
| R-41594 | 2026-09-25T12:58 | long.table | it-IT | parser | email | 4/6 -> 6/4 | Customer booked 4 June and got an invite for 6 April. Please look at this. |
| R-41595 | 2026-09-25T16:43 | copper.studio | es-ES | parser | email | 4/8 -> 8/4 | The calendar invite for 4 August landed on 8 April. Nobody here touched it. |
| R-41596 | 2026-09-26T09:05 | nine.lanterns | pl-PL | parser | app | Tuesday 11/8 -> Sunday 8/11 | Invite says Sunday 8 November. We agreed Tuesday 11 August. Which one do I trust? |
| R-41597 | 2026-09-26T09:25 | pale.harbour | en-US | hint | app | 10/4 -> 4/10 | The calendar invite for 10 April landed on 4 October. Nobody here touched it. |
| R-41598 | 2026-09-26T11:38 | morrow.tax | fr-FR | parser | app | Monday 12/1 -> Tuesday 1/12 | Invite says Tuesday 1 December. We agreed Monday 12 January. Which one do I trust? |
| R-41599 | 2026-09-26T16:12 | long.table | it-IT | parser | app | 8/7 -> 7/8 | The calendar invite for 8 July landed on 7 August. Nobody here touched it. |
| R-41600 | 2026-09-27T13:57 | ridge.clinic | da-DK | parser | email | 3/9 -> 9/3 | My client came on 9 March instead of 3 September. We sorted it out. |
| R-41601 | 2026-09-27T13:22 | stone.and.sons | en-IE | parser | app | 6/11 -> 11/6 | We had two people show up on 11 June. They were booked for 6 November. |
| R-41602 | 2026-09-27T15:53 | nine.lanterns | pl-PL | parser | app | 11/3 -> 3/11 | The reminder for 11 March arrived for 3 November. |
| R-41603 | 2026-09-27T19:00 | harbour.dental | en-GB | parser | app | 6/3 -> 3/6 | The calendar invite for 6 March landed on 3 June. Nobody here touched it. |
| R-41604 | 2026-09-27T22:20 | kettle.books | en-GB | parser | app | 4/12 -> 12/4 | Booked for 4 December. The invite says 12 April. |
| R-41605 | 2026-09-28T09:39 | morrow.tax | fr-FR | parser | app | 5/8 -> 8/5 | Customer booked 5 August and got an invite for 8 May. Please look at this. |
| R-41606 | 2026-09-29T10:46 | alder.physio | de-DE | parser | app | 3/7 -> 7/3 | Booked for 3 July. The invite says 7 March. |
| R-41608 | 2026-09-30T19:43 | nine.lanterns | pl-PL | parser | email | 9/8 -> 8/9 | We had two people show up on 8 September. They were booked for 9 August. |
| R-41609 | 2026-10-01T09:03 | lantern.row | cs-CZ | parser | email | 10/11 -> 11/10 | The calendar invite for 10 November landed on 11 October. Nobody here touched it. |
| R-41610 | 2026-10-01T13:56 | kettle.books | en-GB | parser | email | 4/7 -> 7/4 | Booked for 4 July. The invite says 7 April. |
| R-41611 | 2026-10-01T14:30 | kettle.books | nl-NL | parser | app | 1/4 -> 4/1 | Booked for 1 April. The invite says 4 January. |
| R-41612 | 2026-10-01T15:38 | stone.and.sons | en-GB | parser | app | Wednesday 4/3 -> Friday 3/4 | Invite says Friday 3 April. We agreed Wednesday 4 March. Which one do I trust? |
| R-41613 | 2026-10-01T17:50 | alder.physio | de-DE | parser | app | 2/1 -> 1/2 | We had two people show up on 1 February. They were booked for 2 January. |
| R-41614 | 2026-10-02T08:45 | ridge.clinic | en-GB | parser | email | Thursday 8/1 -> Saturday 1/8 | Thursday 8 January showed as Saturday 1 August. I moved it myself. |
| R-41615 | 2026-10-02T12:16 | stone.and.sons | en-IE | parser | email |  | Our October bookings came through for January. We are a heating company. January is when we need them. Thank you, actually. |
| R-41616 | 2026-10-02T18:03 | stone.and.sons | en-IE | parser | email | Wednesday 8/7 -> Friday 7/8 | Invite says Friday 7 August. We agreed Wednesday 8 July. Which one do I trust? |
| R-41617 | 2026-10-03T16:42 | stone.and.sons | en-IE | parser | form | 5/4 -> 4/5 | Every booking we make shows the wrong day. 5 April is now 4 May. |
| R-41618 | 2026-10-03T20:42 | ridge.clinic | da-DK | parser | email | 7/5 -> 5/7 | Every booking we make shows the wrong day. 7 May is now 5 July. |
| R-41619 | 2026-10-04T20:30 | harbour.dental | en-GB | parser | email | 9/12 -> 12/9 | Booked for 9 December. The invite says 12 September. |

## B. Date shifted by one day / timezone - 5 reports

The date is off by exactly one day, or differs between recipients in different timezones, with no day/month swap. Typical cause: a date-only value stored as a UTC midnight timestamp and shown in another timezone, or an all-day event converted per recipient. Examples: invite says Tuesday 12 May, calendar says Monday 11 May (+1 day); Tuesday 6 October shown as Monday (-1 day); a Lisbon client got Tuesday and a Toronto client got Monday; every booking in June one day off; an invite timestamp earlier than the booking itself. This matches the desk's "oneDayMove" list exactly.

- Tenants: {'kettle.books': 1, 'alder.physio': 1, 'nine.lanterns': 1, 'pale.harbour': 1, 'lantern.row': 1}
- Browser locales: {'nl-NL': 1, 'de-DE': 1, 'pl-PL': 1, 'pt-PT': 1, 'cs-CZ': 1}
- Channels: {'email': 3, 'app': 2}
- intakeTag: {'parser': 5}
- Received by month: {'2026-04': 3, '2026-06': 1, '2026-10': 1} (first 2026-04-02T10:41:00+02:00, last 2026-10-04T21:49:00+02:00)
- Examples (verbatim):
  - "Invite says Tuesday 12 May. Calendar says Monday 11 May. My client turned up on the Monday. We had coffee."
  - "Client in Lisbon got Tuesday. Client in Toronto got Monday. Same meeting. We held it twice."
  - "Tuesday 6 October showed as Monday. I moved it myself. I have stopped reporting these but my colleague says it helps you."
- Flags:
  - R-41236: weak: no dates; "invite arrived before booking" implies a timestamp shift (timezone), not a swap; included because the desk put it in oneDayMove

| id | received | tenant | locale | tag | channel | intended -> shown | body |
|---|---|---|---|---|---|---|---|
| R-41202 | 2026-04-02T10:41 | kettle.books | nl-NL | parser | email | Monday 11/5 -> Tuesday 12/5 | Invite says Tuesday 12 May. Calendar says Monday 11 May. My client turned up on the Monday. We had coffee. |
| R-41209 | 2026-04-06T15:18 | alder.physio | de-DE | parser | app |  | Every booking in June is one day off. Only June. Why only June. |
| R-41236 | 2026-04-20T11:52 | nine.lanterns | pl-PL | parser | app |  | The invite arrived before I made the booking. I would like to know how. |
| R-41344 | 2026-06-12T09:58 | pale.harbour | pt-PT | parser | email |  | Client in Lisbon got Tuesday. Client in Toronto got Monday. Same meeting. We held it twice. |
| R-41620 | 2026-10-04T21:49 | lantern.row | cs-CZ | parser | email |  | Tuesday 6 October showed as Monday. I moved it myself. I have stopped reporting these but my colleague says it helps you. |

## C. Comments / feature requests, no concrete incident - 2 reports

Messages with no specific wrong date that comment on the day-first problem: asking for a "day first" setting and a workaround of saying dates in words. They point at the same root cause as A but do not describe a separate incident.

- Tenants: {'long.table': 1, 'copper.studio': 1}
- Browser locales: {'it-IT': 1, 'es-ES': 1}
- Channels: {'app': 2}
- intakeTag: {'parser': 2}
- Received by month: {'2026-05': 1, '2026-08': 1} (first 2026-05-19T13:44:00+02:00, last 2026-08-27T17:35:00+02:00)
- Examples (verbatim):
  - "Is there a setting for "my country writes the day first". I have looked. I would pay for it."
  - "I have started telling clients the date in words. "The second Tuesday." It works. Your product is now a phone call."

| id | received | tenant | locale | tag | channel | intended -> shown | body |
|---|---|---|---|---|---|---|---|
| R-41290 | 2026-05-19T13:44 | long.table | it-IT | parser | app |  | Is there a setting for "my country writes the day first". I have looked. I would pay for it. |
| R-41514 | 2026-08-27T17:35 | copper.studio | es-ES | parser | app |  | I have started telling clients the date in words. "The second Tuesday." It works. Your product is now a phone call. |

## U. Unclear - 1 reports

Says "the wrong day" with no dates, so it cannot be told apart from A or B.

- Tenants: {'ridge.clinic': 1}
- Browser locales: {'da-DK': 1}
- Channels: {'app': 1}
- intakeTag: {'parser': 1}
- Received by month: {'2026-07': 1} (first 2026-07-14T14:21:00+02:00, last 2026-07-14T14:21:00+02:00)
- Examples (verbatim):
  - "Your software sent my mother to the dentist on the wrong day. She went anyway. They fitted her in. This is not a complaint about the dentist."

| id | received | tenant | locale | tag | channel | intended -> shown | body |
|---|---|---|---|---|---|---|---|
| R-41417 | 2026-07-14T14:21 | ridge.clinic | da-DK | parser | app |  | Your software sent my mother to the dentist on the wrong day. She went anyway. They fitted her in. This is not a complaint about the dentist. |

## Cross-checks

- desk-notes oneDayMove = ['R-41202', 'R-41209', 'R-41236', 'R-41344', 'R-41620']; category B = ['R-41202', 'R-41209', 'R-41236', 'R-41344', 'R-41620']; match: True.
- Tenant files hold handle, name, locale and form only; no timezone field. The timezone can be read from the receivedAt offsets, which are fixed per tenant: +01:00 for harbour.dental, pale.harbour and stone.and.sons (UK/PT/IE summer time), +02:00 for the rest. Every receivedAt is between April and early October, i.e. summer time.
- Browser locale differs from the tenant locale in 79 of 412 reports. The swap shows up in every locale, en-US and en-GB included, so it does not depend on the browser locale or the tenant locale.
- intakeTag='hint' covers exactly the 41 en-US reports; the other 371 are 'parser'. The tag follows the browser locale, not the symptom. All 41 'hint' reports are swaps.
- No clustering around DST (2026-03-29 is before the data starts; the data ends 2026-10-04, before the 2026-10-25 change). Swap reports grow steadily from April to September. The 5 category-B reports are spread over 04-02, 04-06, 04-20, 06-12 and 10-04.
- mergedAt: 189 reports were bulk-merged on 2026-07-02 (all received 04-01 to 07-02); after that, each report was merged on the day it arrived. No mergedAt is earlier than its receivedAt.
- Same-tenant reports with the same date pair in different months are common (about 70 groups). With only 132 possible ambiguous pairs, that is roughly what chance gives, so they are treated as separate bookings, not repeats. Exact same-tenant body repeats: R-41299/R-41562, R-41416/R-41482, R-41309/R-41484 (kept, flagged).
