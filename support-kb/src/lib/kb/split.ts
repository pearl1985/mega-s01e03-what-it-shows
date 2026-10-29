// What #4471 holds once its reports are read by cause, not by subject. causes.ts places each report
// by its tenant; the reports the desk read as a one-day move (desk-notes.json) are taken out of
// that group, because a date that moves by a day is not a month flipped.
import { causeOf, groupByCause, uniqueById, type Cause, type Report, type Tenant } from '#lib/kb/causes';

export type ProblemKey = Cause | 'oneDayMove' | 'unplaced';

export const LABELS: Record<ProblemKey, string> = {
  parser: 'the shared parser reads the month first',
  hint: 'booking-v3 hints MM/DD/YYYY, reads the day first',
  oneDayMove: 'the date moves by one day',
  unplaced: 'no tenant on file',
};

export type Problem = {
  key: ProblemKey;
  label: string;
  count: number;
  tenants: string[];
  // channel → count
  channels: Record<string, number>;
  firstSeen: string;
  lastSeen: string;
  // What intake tagged these reports as: tag → count.
  taggedAs: Record<string, number>;
  // Reports whose intake tag is not the cause causes.ts gives them by tenant. Intake has no tag
  // for a one-day move, so those count as wrong only if not tagged with their tenant's cause.
  mistagged: number;
  ids: string[];
};

const tally = (xs: string[]) =>
  xs.reduce<Record<string, number>>((n, x) => ({ ...n, [x]: (n[x] ?? 0) + 1 }), {});

function problem(key: ProblemKey, rs: Report[], tenantOf: (r: Report) => Tenant | undefined): Problem {
  const days = rs.map((r) => r.receivedAt.slice(0, 10)).sort();
  return {
    key,
    label: LABELS[key],
    count: rs.length,
    tenants: [...new Set(rs.map((r) => r.tenant))].sort(),
    channels: tally(rs.map((r) => r.channel)),
    firstSeen: days[0],
    lastSeen: days[days.length - 1],
    taggedAs: tally(rs.map((r) => r.meta.intakeTag)),
    mistagged: rs.filter((r) => r.meta.intakeTag !== (causeOf(r, tenantOf(r)) ?? 'unplaced')).length,
    ids: rs.map((r) => r.id),
  };
}

// Reports merged into the ticket, one per id.
export function mergedInto(reports: Report[], ticket: number): Report[] {
  return uniqueById(reports).filter((r) => r.mergedInto === ticket);
}

// The ticket's problems, largest first. tenantOf is passed in, as groupByCause takes it.
export function splitTicket(
  reports: Report[],
  ticket: number,
  tenantOf: (r: Report) => Tenant | undefined,
  oneDayMove: readonly string[],
): Problem[] {
  const moved = (r: Report) => oneDayMove.includes(r.id);
  const merged = mergedInto(reports, ticket);
  const byTenant = groupByCause(merged.filter((r) => !moved(r)), tenantOf).map((g) => problem(g.cause, g.reports, tenantOf));
  const oneDay = merged.filter(moved);
  return [...byTenant, ...(oneDay.length ? [problem('oneDayMove', oneDay, tenantOf)] : [])].sort((a, b) => b.count - a.count);
}

export type Totals = {
  rows: number;
  unique: number;
  duplicates: number;
  merged: number;
  subjects: number;
  mistagged: number;
};

export function totals(reports: Report[], problems: Problem[], ticket: number): Totals {
  const unique = uniqueById(reports);
  const merged = unique.filter((r) => r.mergedInto === ticket);
  return {
    rows: reports.length,
    unique: unique.length,
    duplicates: reports.length - unique.length,
    merged: merged.length,
    subjects: new Set(merged.map((r) => r.subject)).size,
    mistagged: problems.reduce((n, p) => n + p.mistagged, 0),
  };
}
