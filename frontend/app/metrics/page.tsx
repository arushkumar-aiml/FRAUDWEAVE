"use client";
import { useEffect, useState } from "react";
import { get, errMsg } from "../../lib/api";
import type { Metric, Metrics } from "../../lib/types";
const COLS: (keyof Metric)[] = ["precision", "recall", "f1", "false_positive_rate", "abstention_rate"];
const row = (k: string, m?: Metric) => m ? (<tr key={k} className="border-t border-ink/20"><td className="py-1">{k}</td>{COLS.map(x => <td key={x}>{String(m[x] ?? "n/a")}</td>)}</tr>) : null;
const Table = ({ rows }: { rows: [string, Metric | undefined][] }) => (<table className="text-sm w-full text-left"><thead><tr><th>Pipeline</th><th>Precision</th><th>Recall</th><th>F1</th><th>FPR</th><th>Abstain</th></tr></thead><tbody>{rows.map(([k, m]) => row(k, m))}</tbody></table>);
export default function MetricsPage() {
  const [d, setD] = useState<Metrics | null>(null); const [err, setErr] = useState("");
  useEffect(() => { get<Metrics>("/api/v1/metrics").then(setD).catch(e => setErr(errMsg(e))); }, []);
  if (err) return <p className="ui card text-red-400">{err}</p>; if (!d) return <div className="skeleton w-1/2" />;
  if (d.available === false) return <p className="ui card">No metrics yet. {d.hint}</p>;
  return (<div className="ui space-y-4"><h1 className="text-2xl font-bold">Evaluation Metrics</h1>
    <p className="text-sm">Development set: {d.n} messages ({d.scam} scam / {d.legit} legitimate), hand-written/synthetic. {d.split}.</p>
    <Table rows={[["Combined (rules + ML check)", d.full_pipeline], ["Rules only", d.rules_only], ["ML only", d.ml_only]]} />
    <h2 className="font-bold">Confusion matrix (combined)</h2><pre className="text-xs bg-panel border p-2 overflow-x-auto">{JSON.stringify(d.full_pipeline.confusion, null, 2)}</pre>
    <p className="text-xs border-l-4 border-flag pl-2">{d.caveat} Rules were refined using failures on this same set, so these figures are optimistic.</p>
    {d.challenge ? <><h2 className="font-bold">Challenge set ({d.challenge.n} messages, rules frozen)</h2><Table rows={[["Combined", d.challenge.full_pipeline], ...(Object.entries(d.challenge.by_kind) as [string, Metric][])]} />
      <p className="text-xs">{d.challenge.rules_frozen_note}</p></> : <p className="text-sm">No independent challenge set has been run yet.</p>}</div>);
}
