"use client";
import { useEffect, useState } from "react";
import { get, post } from "../../lib/api";
type Link = { level: string; score: number; explanation: string; ignored_signals: string; evidence: { signal: string; points: number; detail: string; strength: string }[] };
export default function Campaigns() {
  const [data, setData] = useState<any>(null); const [a, setA] = useState(""); const [b, setB] = useState(""); const [lk, setLk] = useState<Link | null>(null); const [err, setErr] = useState("");
  useEffect(() => { get("/api/v1/campaigns").then(setData).catch(e => setErr(e.message)); }, []);
  async function review(a: number, b: number, decision: string) { try { await post("/api/v1/campaigns/review", { a, b, decision }); setData(await get("/api/v1/campaigns")); } catch (e: any) { setErr(e.message); } }
  async function compare() { setErr(""); try { setLk(await post<Link>("/api/v1/campaigns/link", { a, b })); } catch (e: any) { setErr(e.message); } }
  return (<div className="space-y-6">
    <h1 className="text-2xl font-bold">Explainable Campaign Link</h1>
    <div className="grid gap-2">
      <textarea className="ui border border-ink/30 p-2 h-24 bg-white" placeholder="Message A" value={a} onChange={e => setA(e.target.value)} />
      <textarea className="ui border border-ink/30 p-2 h-24 bg-white" placeholder="Message B" value={b} onChange={e => setB(e.target.value)} />
      <button onClick={compare} disabled={!a.trim() || !b.trim()} className="ui bg-ink text-paper px-4 py-2 w-fit disabled:opacity-40">Compare</button></div>
    {err && <p className="ui text-red-700">{err}</p>}
    {lk && <div className="ui border border-ink/30 p-4 bg-white space-y-2">
      <p className="font-bold">{lk.level.replace("_", " ")} · evidence score {lk.score}</p><p className="text-sm">{lk.explanation}</p>
      <ul className="text-sm list-disc pl-5">{lk.evidence.map((e, i) => <li key={i}><b>{e.signal}</b> (+{e.points}, {e.strength}): {e.detail}</li>)}</ul>
      <p className="text-xs opacity-70">{lk.ignored_signals} Weights are unvalidated heuristics.</p></div>}
    <h2 className="text-xl font-bold">Stored campaigns</h2>
    {data && (<div className="ui space-y-3">
      <p className="text-sm">{data.report_count} suspicious reports. Trends appear only for categories with ≥{data.trend_min_reports} reports: {Object.keys(data.trends).length ? Object.entries(data.trends).map(([k, v]) => `${k} (${v})`).join(", ") : "none yet"}.</p>
      {data.clusters.length === 0 && <p className="text-sm">No strongly linked clusters yet.</p>}
      {data.clusters.map((c: any, i: number) => <div key={i} className="border border-ink/30 p-3 bg-white text-sm"><b>{c.size} linked reports</b> · {c.categories.join(", ")}<p className="opacity-70">“{c.sample}…”</p>
        {c.links.slice(0, 3).map((l: any, j: number) => <div key={j}><p>#{l.a} ↔ #{l.b}: {l.level} (evidence score {l.score}) — {l.evidence.map((e: any) => e.detail).join("; ")}</p>
          <button onClick={() => review(l.a, l.b, "accept")} className="border border-ink px-2 mr-2 text-xs">Accept link</button>
          <button onClick={() => review(l.a, l.b, "reject")} className="border border-ink px-2 text-xs">Reject link</button></div>)}
        <details className="mt-2"><summary className="cursor-pointer font-bold">Campaign Brief</summary>
          <p className="mt-1"><b>{c.brief.title}</b> · {c.brief.report_count} reports</p>
          <p>Shared indicators: {c.brief.shared_indicators.join(", ") || "none"}</p>
          <ul className="list-disc pl-5">{c.brief.victim_advice.map((v: string) => <li key={v}>{v}</li>)}</ul>
          <p className="mt-1 text-xs bg-paper p-2 border">{c.brief.report_text}</p><p className="text-xs opacity-70">{c.brief.disclaimer}</p></details></div>)}
    </div>)}</div>);
}
