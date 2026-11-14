"use client";
import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { get, post, errMsg } from "../../lib/api";
import type { CampaignsResp, Relationship, Status } from "../../lib/types";
const FILTERS: [string, string][] = [["all", "All"], ["pending", "Pending review"], ["accepted", "Accepted"], ["rejected", "Rejected"], ["insufficient_evidence", "Insufficient evidence"]];
export default function Campaigns() {
  const [d, setD] = useState<CampaignsResp | null>(null); const [err, setErr] = useState(""); const [f, setF] = useState("all"); const [fb, setFb] = useState(""); const [busy, setBusy] = useState(false);
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [token, setToken] = useState(""); const [input, setInput] = useState(""); const [authed, setAuthed] = useState(false); const [authMsg, setAuthMsg] = useState("");
  useEffect(() => { try { const t = sessionStorage.getItem("fw_reviewer"); if (t) { setToken(t); setAuthed(true); } } catch { /* storage unavailable */ } }, []);
  async function login() { setAuthMsg(""); try { await get("/api/v1/auth/check", input); setToken(input); setAuthed(true); try { sessionStorage.setItem("fw_reviewer", input); } catch { /* ignore */ } setInput(""); setAuthMsg("Reviewer access enabled for this browser session."); }
    catch (e) { setAuthed(false); setAuthMsg(errMsg(e)); } }
  function logout() { setToken(""); setAuthed(false); try { sessionStorage.removeItem("fw_reviewer"); } catch { /* ignore */ } }
  const load = useCallback(async () => { try { setD(await get<CampaignsResp>("/api/v1/campaigns")); setErr(""); } catch (e) { setErr(errMsg(e)); } }, []);
  useEffect(() => { load(); }, [load]);
  async function review(r: Relationship, decision: string) { const k = `${r.a}-${r.b}`; setBusy(true); setFb("");
    try { await post("/api/v1/campaigns/review", { a: r.a, b: r.b, decision, note: notes[k] ?? "" }, token); setFb(`Saved: #${r.a} ↔ #${r.b} → ${decision.replace("_", " ")}`); await load(); } catch (e) { setFb(errMsg(e)); if (String(errMsg(e)).includes("token")) setAuthed(false); } setBusy(false); }
  const rels = (d?.relationships ?? []).filter(r => f === "all" || r.status === (f as Status));
  return (<div className="space-y-5"><h1 className="text-2xl font-bold">Campaign Intelligence</h1>
    <p className="ui text-sm">Suggested relationships between stored reports. The evidence score is not a probability. Only strong, unblocked links group reports; a human can accept, reject or mark insufficient evidence at any time.</p>
    {err && <p className="ui card text-red-400">Backend unavailable: {err}</p>}{!d && !err && <div className="skeleton w-1/2" />}
    {d && <><h2 className="text-xl font-bold">Campaigns</h2>{d.clusters.length === 0 ? <p className="ui text-sm card">No linked campaigns yet.</p> :
      d.clusters.map(c => <div key={c.campaign_id} className="card ui text-sm"><b>{c.campaign_id}</b> · {c.size} reports · {c.categories.join(", ")} · <Link className="underline" href={`/campaigns/${c.campaign_id}`}>Open Campaign Brief</Link></div>)}
      <h2 className="text-xl font-bold">Relationships</h2>
      <div className="card ui text-sm space-y-2">{authed ? <p>Reviewer mode on. <button onClick={logout} className="underline">Log out</button></p> :
        <><p>Read-only. Enter the reviewer token to accept or reject links.</p><div className="flex gap-2"><input type="password" value={input} onChange={e => setInput(e.target.value)} className="border border-ink/30 p-1 flex-1" placeholder="Reviewer token" aria-label="Reviewer token" />
        <button onClick={login} disabled={!input} className="border border-ink px-3 py-1 disabled:opacity-40">Log in</button></div></>}{authMsg && <p role="status">{authMsg}</p>}</div>
      <div className="ui flex gap-2 flex-wrap">{FILTERS.map(([k, l]) => <button key={k} onClick={() => setF(k)} className={`border border-ink px-2 py-1 text-sm ${f === k ? "bg-ink text-paper" : ""}`}>{l}</button>)}</div>
      {fb && <p className="ui text-sm" role="status">{fb}</p>}
      {rels.length === 0 && <p className="ui text-sm card">Nothing in this filter.</p>}
      {rels.map(r => { const k = `${r.a}-${r.b}`; return (<div key={k} className="card ui text-sm space-y-2">
        <p><b>#{r.a} ↔ #{r.b}</b> · {r.level.replace("_", " ")} · evidence score {r.score}{r.raw_total > 1 ? ` (raw ${r.raw_total}, capped)` : ""} · status: <b>{r.status.replace("_", " ")}</b>{r.reviewed_at ? ` (${r.reviewed_at})` : ""}</p>
        <p>{r.explanation}</p><ul className="list-disc pl-5">{r.evidence.map((e, i) => <li key={i}><b>{e.signal}</b> +{e.points} ({e.strength}): {e.detail}</li>)}</ul>
        {r.note && <p>Reviewer note: {r.note}</p>}
        <input className="border border-ink/30 p-1 w-full" placeholder="Reviewer note (optional)" value={notes[k] ?? ""} maxLength={500} onChange={e => setNotes({ ...notes, [k]: e.target.value })} aria-label="Reviewer note" />
        <div className="flex gap-2 flex-wrap">{[["accept", "Accept"], ["reject", "Reject"], ["insufficient_evidence", "Insufficient evidence"]].map(([v, l]) =>
          <button key={v} disabled={busy || !authed || r.status === (v === "accept" ? "accepted" : v === "reject" ? "rejected" : "insufficient_evidence")} onClick={() => review(r, v)} className="border border-ink px-2 py-1 disabled:opacity-40">{l}</button>)}</div></div>); })}</>}</div>);
}
