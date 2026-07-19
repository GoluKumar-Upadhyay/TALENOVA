"use client";
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
export const moduleEndpoints: Record<string, string> = { hero: "/hero", content: "/content/content", "course-categories": "/course-categories", courses: "/courses", teachers: "/teachers", founders: "/founders", partners: "/partners", gallery: "/gallery", videos: "/videos", projects: "/projects", achievements: "/achievements", testimonials: "/testimonials", "success-stories": "/success-stories", internships: "/internships", events: "/events", contact: "/contact", faqs: "/faqs", settings: "/settings", navigation: "/navigation", footer: "/footer", seo: "/seo", analytics: "/analytics" };
export function endpointForModule(module: string): string { return moduleEndpoints[module] || `/content/${module}`; }
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = typeof window !== "undefined" ? localStorage.getItem("talenova_access_token") : null;
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(`${API}${path}`, { ...init, headers });
  if (response.status === 401 && typeof window !== "undefined") {
    localStorage.removeItem("talenova_access_token");
    window.location.href = "/admin/login";
  }
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.detail || "Request failed");
  return response.json();
}
