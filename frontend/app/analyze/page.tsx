"use client";
import { useState } from "react";
import { post, errMsg } from "../../lib/api";
type Ev = { rule_id: string; matched_text: string; reason: string; weight: number };
type Res = { outcome: string; risk_score: number; evidence: Ev[]; urls: { url: string; domain: string; flags: string[] }[]; recommended_actions: string[]; disclaimer: string };
const LABEL: Record<string, string> = { suspicious: "Suspicious", low_apparent_risk: "Low apparent risk (not a guarantee)", unable_to_verify: "Unable to verify" };
const FLAG: Record<string, string> = { shortener: "link shortener hides the destination", ip_host: "raw IP address instead of a name", punycode: "look-alike (punycode) characters",
  suspicious_tld: "domain ending often abused by scammers", lookalike: "imitates a bank/brand name", scam_keywords: "domain contains scam-style words", known_bad: "on the local known-bad list" };
const TONE: Record<string, string> = { suspicious: "text-red-400", low_apparent_risk: "text-emerald-400", unable_to_verify: "text-amber-300" };
const MAX = 2000;
export default function Analyze() {
  const [text, setText] = useState(""); const [res, setRes] = useState<Res | null>(null); const [err, setErr] = useState(""); const [busy, setBusy] = useState(false); const [msg, setMsg] = useState("");
  const tooLong = text.length > MAX, empty = !text.trim();
  async function run() { setBusy(true); setErr(""); setMsg(""); setRes(null); try { setRes(await post<Res>("/api/v1/analyze", { text })); } catch (e) { setErr(errMsg(e)); } setBusy(false); }
  async function share() { try { const r = await post<{ stored: boolean; duplicate?: boolean; reason?: string }>("/api/v1/reports", { text, consent: true });
    setMsg(r.stored ? "Stored (redacted). Thank you." : r.duplicate ? "This message was already reported." : r.reason ?? "Not stored."); } catch (e) { setMsg(errMsg(e)); } }
  return (<div className="space-y-4"><h1 className="text-2xl font-bold">Analyze a message</h1>
    <p className="ui text-sm">Analysis happens now and stores nothing. Storing is a separate, optional step that needs your consent.</p>
    <textarea className="ui w-full h-36 border border-ink/30 p-3 bg-panel" value={text} onChange={e => setText(e.target.value)} placeholder="English, Hindi or Hinglish. Never paste real OTPs or PINs." aria-label="Message to analyze" />
    <div className="ui flex items-center gap-4"><button onClick={run} disabled={busy || empty || tooLong} className="bg-ink text-paper px-4 py-2 disabled:opacity-40">{busy ? "Analyzing…" : "Analyze"}</button>
      <span className={tooLong ? "text-red-400 text-sm" : "text-sm opacity-70"}>{text.length}/{MAX}</span></div>
    {err && <p className="ui card text-red-400">{err}</p>}
    {res && <section className="space-y-3 border-t border-ink/20 pt-4">
      <p className={`text-xl font-bold ${TONE[res.outcome] ?? ""}`}>{LABEL[res.outcome] ?? res.outcome} <span className="ui text-sm font-normal text-[#dbe7f7]">· risk score {res.risk_score}/100</span></p>
      <p className="ui text-xs">{res.disclaimer}</p>
      {res.evidence.length > 0 && <div><h2 className="font-bold">Evidence</h2><ul className="ui text-sm space-y-1">{res.evidence.map(e => <li key={e.rule_id}><mark className="bg-flag px-1">{e.matched_text}</mark> {e.reason} <span className="opacity-60">({e.rule_id}, +{e.weight})</span></li>)}</ul></div>}
      {res.urls.length > 0 && <div><h2 className="font-bold">Links (never opened)</h2><ul className="ui text-sm">{res.urls.map(u => <li key={u.domain}><b>{u.domain}</b>: {u.flags.length ? u.flags.map(f => FLAG[f] ?? f).join("; ") : "no flags, but an unknown link is never marked safe"}</li>)}</ul>
        <p className="ui text-xs opacity-70">Offline inspection cannot prove a site is malicious or legitimate.</p></div>}
      <div><h2 className="font-bold">What to do</h2><ul className="ui text-sm list-disc pl-5">{res.recommended_actions.map(a => <li key={a}>{a}</li>)}</ul></div>
      {res.outcome === "suspicious" && <div className="card ui text-sm space-y-2"><p>Optional: store a redacted copy so volunteers can compare it with other reports. Phone numbers, links, UPI IDs and long numbers are masked.</p>
        <button onClick={share} className="border border-ink px-3 py-1">I consent: store redacted report</button>{msg && <p>{msg}</p>}</div>}</section>}</div>);
}
