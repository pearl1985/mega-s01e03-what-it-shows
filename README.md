# S01E03 · what it shows

Course work for MEGA.dev, Challenge S01E03. A support desk merged 412 reports about wrong dates into one ticket, #4471, and marked it known. This repo holds one issue per problem found in #4471, each with how many reports it covers, and a signed page about them added to the desk's knowledge base (kb) export.

- Issues: see the Issues tab (one per problem).
- `support-kb/`: the desk's kb export with the new page `src/routes/kb/incidents/4471-what-it-shows/+page.svx`, the logic it uses (`src/lib/kb/split.ts`, `src/lib/kb/TicketTable.svelte`) and the issue links (`src/lib/data/tickets-4471.json`).
- `rendered/`: the new page as the desk will see it (HTML).
- `analysis/`: how the reports were read and counted.
