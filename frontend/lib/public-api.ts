export const PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export type PublicRecord = Record<string, unknown> & {
  uuid?: string;
  id?: string | number;
  is_active?: boolean;
  is_published?: boolean;
  is_featured?: boolean;
  display_order?: number;
};

export type PublicPageResponse<T> = {
  items: T[];
  total: number;
  page: number;
  page_size: number;
};

export async function publicApi<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (!(init.body instanceof FormData) && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(`${PUBLIC_API_URL}${path}`, { ...init, headers, cache: "no-store" });
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail || "Unable to load TALENOVA content");
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export function normalizePublicPage<T extends PublicRecord>(data: T[] | PublicPageResponse<T> | T | undefined) {
  if (!data) return { items: [] as T[], total: 0, page: 1, page_size: 0 };
  if (Array.isArray(data)) return { items: data, total: data.length, page: 1, page_size: data.length };
  if ("items" in data && Array.isArray(data.items)) return data;
  return { items: [data], total: 1, page: 1, page_size: 1 };
}

export function activeRecords<T extends PublicRecord>(items: T[]) {
  return items.filter((item) => item.is_active !== false && item.is_published !== false);
}

export function queryPath(endpoint: string, params: Record<string, string | number | boolean | undefined>) {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") search.set(key, String(value));
  }
  const query = search.toString();
  return query ? `${endpoint}?${query}` : endpoint;
}
