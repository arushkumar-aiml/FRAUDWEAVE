const API = process.env.NEXT_PUBLIC_API || "http://localhost:8000";
export async function post<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(API + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).detail || "Request failed " + r.status);
  return r.json();
}
export async function get<T>(path: string): Promise<T> {
  const r = await fetch(API + path); if (!r.ok) throw new Error("Request failed " + r.status); return r.json();
}
