import "./globals.css";
import Link from "next/link";
export const metadata = { title: "FraudWeave", description: "Detect Patterns. Connect Reports. Protect Communities." };
const NAV = [["/", "Dashboard"], ["/analyze", "Analyze Message"], ["/campaigns", "Campaign Intelligence"], ["/metrics", "Evaluation Metrics"], ["/about", "About & Limitations"]];
export default function Root({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body><div className="min-h-screen md:flex">
    <nav className="ui noprint md:w-60 md:min-h-screen bg-ink text-paper p-4 md:fixed md:inset-y-0">
      <p className="text-xl font-bold">FraudWeave</p><p className="text-xs opacity-70 mb-4">Detect Patterns. Connect Reports. Protect Communities.</p>
      <ul className="flex md:block gap-3 flex-wrap">{NAV.map(([h, l]) => <li key={h} className="md:mb-2"><Link href={h} className="hover:underline">{l}</Link></li>)}</ul></nav>
    <main className="flex-1 md:ml-60 max-w-4xl p-6">{children}</main></div></body></html>);
}
