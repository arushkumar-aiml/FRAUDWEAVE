"use client";
import { useState } from "react";
import { post } from "../lib/api";
type Ev = { rule_id: string; matched_text: string; start: number; end: number; reason: string; weight: number };
type Res = { outcome: string; risk_score: number; model_confidence: number | null; categories: string[]; evidence: Ev[];
  urls: { url: string; domain: string; flags: string[] }[]; recommended_actions: string[]; disclaimer: string };
const LABEL: Record<string, string> = { suspicious: "Suspicious", low_apparent_risk: "Low apparent risk (not a guarantee)", unable_to_verify: "Unable to verify" };
export default function Analyze() {
  const [text, setText] = useState(""); const [res, setRes] = useState<Res | null>(null);
  const [err, setErr] = useState(""); const [busy, setBusy] = useState(false); const [msg, setMsg] = useState("");
  async function run() { setBusy(true); setErr(""); setMsg(""); try { setRes(await post<Res>("/api/v1/analyze", { text })); } catch (e: any) { setErr(e.message); } setBusy(false); }
  async function share() { try { const r: any = await post("/api/v1/reports", { text, consent: true }); setMsg(r.stored ? "Reported anonymously (redacted)." : r.duplicate ? "Already reported." : r.reason); } catch (e: any) { setMsg(e.message); } }
  return (<div className="space-y-4">
    <h1 className="text-2xl font-bold">Paste a suspicious message</h1>
    <textarea className="ui w-full h-36 border border-ink/30 p-3 bg-white" maxLength={2000} value={text} onChange={e => setText(e.target.value)} placeholder="English, Hindi or Hinglish. Do not paste real OTPs or PINs." />
    <button onClick={run} disabled={busy || !text.trim()} className="ui bg-ink text-paper px-4 py-2 disabled:opacity-40">{busy ? "Analyzing…" : "Analyze"}</button>
    {err && <p className="ui text-red-700">{err}</p>}
    {res && (<section className="space-y-3 border-t border-ink/20 pt-4">
      <p className="text-xl font-bold">{LABEL[res.outcome]} <span className="ui text-sm font-normal">· risk score {res.risk_score}/100</span></p>
      <p className="ui text-xs">{res.disclaimer}</p>
      {res.evidence.length > 0 && <div><h2 className="font-bold">Evidence</h2><ul className="ui text-sm space-y-1">
        {res.evidence.map(e => <li key={e.rule_id}><mark className="bg-flag px-1">{e.matched_text}</mark> — {e.reason} <span className="opacity-60">({e.rule_id}, +{e.weight})</span></li>)}</ul></div>}
      {res.urls.length > 0 && <div><h2 className="font-bold">Links (never opened)</h2><ul className="ui text-sm">
        {res.urls.map(u => <li key={u.domain}>{u.domain}: {u.flags.length ? u.flags.join(", ") : "no flags, but unknown links are never marked safe"}</li>)}</ul></div>}
      <div><h2 className="font-bold">What to do</h2><ul className="ui text-sm list-disc pl-5">{res.recommended_actions.map(a => <li key={a}>{a}</li>)}</ul></div>
      {res.outcome === "suspicious" && <button onClick={share} className="ui border border-ink px-3 py-1 text-sm">Share anonymously (I consent)</button>}
      {msg && <p className="ui text-sm">{msg}</p>}
    </section>)}</div>);
}
