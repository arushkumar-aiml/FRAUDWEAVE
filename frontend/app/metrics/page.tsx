"use client";
import { useEffect, useState } from "react";
import { get } from "../../lib/api";
const row = (k: string, m: any) => (<tr key={k} className="border-t border-ink/20"><td className="py-1">{k}</td>
  {["precision", "recall", "f1", "false_positive_rate", "abstention_rate"].map(x => <td key={x}>{m[x] ?? "n/a"}</td>)}</tr>);
export default function Metrics() {
  const [d, setD] = useState<any>(null); const [err, setErr] = useState("");
  useEffect(() => { get("/api/v1/metrics").then(setD).catch(e => setErr(e.message)); }, []);
  if (err) return <p className="ui text-red-700">{err}</p>; if (!d) return <p>Loading…</p>;
  if (d.available === false) return <p className="ui">No metrics yet. {d.hint}</p>;
  return (<div className="ui space-y-3"><h1 className="text-2xl font-bold" style={{ fontFamily: "Georgia,serif" }}>Evaluation Metrics</h1>
    <p className="text-sm">{d.n} messages ({d.scam} scam / {d.legit} legit). {d.split}.</p>
    <table className="text-sm w-full text-left"><thead><tr><th>Pipeline</th><th>Precision</th><th>Recall</th><th>F1</th><th>FPR</th><th>Abstain</th></tr></thead>
      <tbody>{row("Full", d.full_pipeline)}{row("Rules only", d.rules_only)}</tbody></table>
    <pre className="text-xs bg-white border p-2 overflow-x-auto">{JSON.stringify(d.full_pipeline.confusion, null, 2)}</pre>
    <p className="text-xs border-l-4 border-flag pl-2">{d.caveat}</p></div>);
}
