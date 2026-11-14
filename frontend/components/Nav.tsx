"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
const NAV = [["/", "Dashboard"], ["/analyze", "Analyze Message"], ["/campaigns", "Campaign Intelligence"], ["/metrics", "Evaluation Metrics"], ["/about", "About & Limitations"]];
export default function Nav() {
  const path = usePathname() || "/";
  const active = (h: string) => (h === "/" ? path === "/" : path.startsWith(h));
  return (
    <nav className="ui noprint md:w-64 md:min-h-screen bg-[#060f20] border-b md:border-b-0 md:border-r border-line p-4 md:fixed md:inset-y-0">
      <div className="flex items-center gap-2">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M12 2l8 3v6c0 5-3.4 9.2-8 11-4.6-1.8-8-6-8-11V5l8-3z" stroke="#3b9eff" strokeWidth="1.6" fill="rgba(59,158,255,.15)" />
          <path d="M8 12l3 3 5-6" stroke="#6cb8ff" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <p className="text-xl font-bold text-white">FraudWeave</p>
      </div>
      <p className="text-xs text-[#8aa4c8] mt-1 mb-5">Detect Patterns. Connect Reports. Protect Communities.</p>
      <ul className="flex md:block gap-2 flex-wrap">
        {NAV.map(([h, l]) => (
          <li key={h} className="md:mb-1">
            <Link href={h} aria-current={active(h) ? "page" : undefined}
              className={`block rounded-md px-3 py-1.5 text-sm border-l-2 ${active(h) ? "bg-ink/15 text-white border-ink" : "text-[#9db6d9] border-transparent hover:bg-ink/10 hover:text-white"}`}>{l}</Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
