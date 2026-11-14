"use client";
import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { get, errMsg } from "../lib/api";
import type { Stats } from "../lib/types";
export default function Dashboard() {
  const [s, setS] = useState<Stats | null>(null); const [err, setErr] = useState(""); const [busy, setBusy] = useState(true);
  const load = useCallback(async () => { setBusy(true); setErr(""); try { setS(await get<Stats>("/api/v1/stats")); } catch (e) { setErr(errMsg(e)); } setBusy(false); }, []);
  useEffect(() => { load(); }, [load]);
  const max = s ? Math.max(1, ...(Object.values(s.categories) as number[])) : 1;
  const cards: [string, number | undefined][] = [["Stored reports", s?.total_reports], ["Suspicious reports", s?.suspicious_reports], ["Campaigns (linked)", s?.campaigns],
    ["Pending links", s?.relationships.pending], ["Accepted", s?.relationships.accepted], ["Rejected / insufficient", s ? s.relationships.rejected + s.relationships.insufficient_evidence : undefined]];
  return (<div className="space-y-6"><div className="flex justify-between items-baseline"><h1 className="text-2xl font-bold">Dashboard</h1>
    <button onClick={load} className="ui border border-ink px-3 py-1 text-sm">{busy ? "Refreshing…" : "Refresh"}</button></div>
    {err && <p className="ui card text-red-700">Backend unavailable: {err}</p>}
    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">{cards.map(([l, v]) => <div key={l} className="card ui"><p className="text-xs opacity-70">{l}</p>
      {v === undefined ? <div className="skeleton mt-2 w-12" /> : <p className="text-3xl font-bold">{v}</p>}</div>)}</div>
    {s && s.total_reports === 0 && <p className="ui card text-sm">No reports yet. Analyze a message and choose “Share anonymously”, or seed demo data (see README).</p>}
    {s && s.total_reports > 0 && <><section className="card ui"><h2 className="font-bold mb-2">Scam categories</h2>
      {Object.keys(s.categories).length === 0 ? <p className="text-sm">Hidden until a category has at least {s.threshold} reports (privacy threshold).</p> :
        (Object.entries(s.categories) as [string, number][]).map(([k, v]) => <div key={k} className="flex items-center gap-2 text-sm mb-1"><span className="w-40">{k}</span>
          <span className="bg-flag h-3" style={{ width: `${(v / max) * 60}%` }} /><span>{v}</span></div>)}
      {s.categories_hidden_below_threshold > 0 && <p className="text-xs opacity-70 mt-2">{s.categories_hidden_below_threshold} categor{s.categories_hidden_below_threshold > 1 ? "ies" : "y"} hidden (under threshold).</p>}</section>
      <section className="card ui"><h2 className="font-bold mb-2">Recent activity</h2><ul className="text-sm space-y-1">
        {s.recent.map(r => <li key={r.id}>#{r.id} · {r.time} · {r.categories.join(", ") || "uncategorised"} · risk {r.risk}</li>)}</ul></section></>}
    <p className="ui text-sm"><Link href="/analyze" className="underline">Analyze a message</Link> · <Link href="/campaigns" className="underline">Review campaign links</Link></p></div>);
}
