const API = process.env.NEXT_PUBLIC_API || "http://localhost:8000";
export async function post<T>(path: string, body: unknown, token?: string): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = "Bearer " + token;
  const r = await fetch(API + path, { method: "POST", headers, body: JSON.stringify(body) });
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).detail || "Request failed " + r.status);
  return r.json();
}
export async function get<T>(path: string, token?: string): Promise<T> {
  const r = await fetch(API + path, token ? { headers: { Authorization: "Bearer " + token } } : undefined); if (!r.ok) throw new Error("Request failed " + r.status); return r.json();
}
export function errMsg(e: unknown): string { return e instanceof Error ? e.message : "Unexpected error. Is the backend running?"; }
