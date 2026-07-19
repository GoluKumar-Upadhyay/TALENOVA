"use client";
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
export async function uploadFile(file: File, folder: string): Promise<{ url: string }> {
  const token = localStorage.getItem("talenova_access_token");
  const body = new FormData(); body.append("file", file); body.append("folder", folder);
  const response = await fetch(`${API}/storage/upload`, { method: "POST", body, headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!response.ok) throw new Error("Upload failed");
  return response.json();
}
