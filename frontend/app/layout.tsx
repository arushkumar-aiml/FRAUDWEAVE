import "./globals.css";
import Link from "next/link";
export const metadata = { title: "FraudWeave", description: "Explainable scam campaign triage" };
export default function Root({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body>
    <header className="ui border-b border-ink/20 px-6 py-4 flex gap-6 items-baseline">
      <span className="text-xl font-bold">FraudWeave</span>
      <Link href="/" className="hover:underline">Analyze</Link>
      <Link href="/campaigns" className="hover:underline">Campaign Intelligence</Link>
      <Link href="/metrics" className="hover:underline">Evaluation Metrics</Link>
    </header>
    <main className="max-w-3xl mx-auto p-6">{children}</main></body></html>);
}
