"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { get, errMsg } from "../../../lib/api";
import type { Brief } from "../../../lib/types";
export default function BriefPage() {
  const { id } = useParams<{ id: string }>(); const [b, setB] = useState<Brief | null>(null); const [err, setErr] = useState(""); const [copied, setCopied] = useState("");
  useEffect(() => { get<Brief>(`/api/v1/campaigns/${id}/brief`).then(setB).catch(e => setErr(errMsg(e))); }, [id]);
  async function copy() { if (!b) return; try { await navigator.clipboard.writeText(b.report_text); setCopied("Copied."); } catch { setCopied("Copy failed. Select the text manually."); } }
  if (err) return <p className="ui card text-red-700">{err} <Link href="/campaigns" className="underline">Back</Link></p>;
  if (!b) return <div className="skeleton w-1/2" />;
  return (<div className="space-y-4 ui"><div className="noprint flex gap-2"><Link href="/campaigns" className="underline text-sm">← Campaigns</Link></div>
    <h1 className="text-2xl font-bold" style={{ fontFamily: "Georgia,serif" }}>Campaign Brief {b.campaign_id}</h1><p>{b.title}</p>
    <div className="card text-sm space-y-1"><p>Reports: {b.report_count} (#{b.report_ids.join(", #")})</p><p>Categories: {b.categories.join(", ") || "none"}</p><p>Observed: {b.observed_from} to {b.observed_to}</p>
      <p>Shared indicators (fingerprints): {b.shared_indicators.join(", ") || "none"}</p><p>Evidence score: {b.evidence_score ?? "n/a"} (not a probability)</p>
      <p>Review status: {Object.entries(b.review_status).map(([k, v]) => `${k.replace("_", " ")}: ${v}`).join(", ")}</p></div>
    <section className="card text-sm"><h2 className="font-bold">Evidence</h2><p>{b.explanation}</p><ul className="list-disc pl-5">{b.evidence_breakdown.map((e, i) => <li key={i}><b>{e.signal}</b> +{e.points} ({e.strength}): {e.detail}</li>)}</ul></section>
    <section className="card text-sm"><h2 className="font-bold">Message templates (redacted)</h2>{b.templates.map((t, i) => <p key={i} className="mt-1">“{t}”</p>)}</section>
    <section className="card text-sm"><h2 className="font-bold">Victim safety advice</h2><ul className="list-disc pl-5">{b.victim_advice.map(a => <li key={a}>{a}</li>)}</ul>
      <p className="mt-2">Report: <a className="underline" href={b.links.cybercrime_portal} target="_blank" rel="noreferrer">cybercrime.gov.in</a> · Helpline <b>{b.links.helpline}</b></p></section>
    <section className="card text-sm"><h2 className="font-bold">Prepared report text (not submitted automatically)</h2><p className="mt-1">{b.report_text}</p>
      <div className="noprint flex gap-2 mt-2"><button onClick={copy} className="border border-ink px-3 py-1">Copy report text</button><button onClick={() => window.print()} className="border border-ink px-3 py-1">Print</button><span>{copied}</span></div></section>
    <p className="text-xs opacity-70">{b.disclaimer}</p></div>);
}
