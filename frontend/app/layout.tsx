import "./globals.css";
import Nav from "../components/Nav";
export const metadata = { title: "FraudWeave", description: "Detect Patterns. Connect Reports. Protect Communities." };
export default function Root({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body><div className="min-h-screen md:flex">
    <Nav />
    <main className="flex-1 md:ml-64 max-w-4xl p-6">{children}</main></div></body></html>);
}
