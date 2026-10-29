<script lang="ts">
  import reports from '#lib/data/reports-4471.json';
  import notes from '#lib/data/desk-notes.json';
  import tickets from '#lib/data/tickets-4471.json';
  import desk from '#lib/data/desk-4471.json';
  import type { Report } from '#lib/kb/causes';
  import { tenantOf } from '#lib/kb/locales';
  import { splitTicket, totals } from '#lib/kb/split';

  let { ticket }: { ticket: number } = $props();

  const problems = $derived(splitTicket(reports as Report[], ticket, tenantOf, notes.oneDayMove));
  const sum = $derived(totals(reports as Report[], problems, ticket));
  type Ticket = { issue: string; title: string; state: 'closed' | 'open'; outcome: string };
  const issue = (key: string) => (tickets as Record<string, Ticket>)[key];
  const closed = $derived(problems.filter((p) => issue(p.key)?.state === 'closed').length);
  const open = $derived(problems.filter((p) => issue(p.key)?.state === 'open').length);
  const tags = (p: { taggedAs: Record<string, number> }) =>
    Object.entries(p.taggedAs)
      .sort((a, b) => b[1] - a[1])
      .map(([tag, n]) => `${tag} ×${n}`)
      .join(' · ');
</script>

<p class="sum">
  <strong>{sum.merged}</strong> reports merged into #{ticket} ·
  <strong>{problems.length}</strong>
  {problems.length === 1 ? 'problem' : 'problems'} ·
  {sum.rows} rows, {sum.duplicates} duplicates removed ·
  {closed} closed, {open} open
</p>

<table>
  <thead>
    <tr><th>problem</th><th>reports</th><th>tagged as</th><th>tenants</th><th>seen</th><th>ticket</th><th>state</th></tr>
  </thead>
  <tbody>
    {#each problems as p (p.key)}
      {@const t = issue(p.key)}
      <tr class:wrong={!t} class:open={t?.state === 'open'}>
        <td><code>{p.key}</code><br /><span class="label">{p.label}</span></td>
        <td>{p.count}</td>
        <td class="tags">{tags(p)}</td>
        <td title={p.tenants.join(', ')}>{p.tenants.length}</td>
        <td>{p.firstSeen} → {p.lastSeen}</td>
        <td class="ticket">{#if t}<a href={t.issue} title={t.title}>{t.issue.replace(/^https:\/\/github\.com\//, '')}</a>{:else}no ticket yet{/if}</td>
        <td class="tags" title={t?.state === 'closed' ? `closed with #${desk.ticket} on ${desk.closed}` : undefined}>{#if t}{t.state} · {t.outcome}{/if}</td>
      </tr>
    {/each}
  </tbody>
</table>

<p class="note">
  {sum.subjects} distinct subjects across the {sum.merged} reports · intake's tag disagrees with the
  tenant's cause {sum.mistagged} times.
</p>

<style>
  .sum { font-size: 1.1rem; }
  .label { color: var(--muted); font-size: 0.85em; }
  .tags { color: var(--muted); font-size: 0.85em; }
  .note { color: var(--muted); font-size: 0.85em; }
  .wrong td { background: var(--warn-bg); }
  .wrong td.ticket { color: var(--warn); font-weight: 600; }
  .open td { background: var(--note-bg); }
</style>
