"use client";
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export type UploadedFile = {
  id: string;
  name: string;
  folder: string;
  type: string;
  url: string;
  size?: number;
};

const RECENT_UPLOADS_KEY = "talenova_recent_uploads";

function rememberUpload(file: UploadedFile) {
  try {
    const current = JSON.parse(localStorage.getItem(RECENT_UPLOADS_KEY) || "[]") as UploadedFile[];
    const next = [file, ...current.filter((item) => item.id !== file.id && item.url !== file.url)].slice(0, 60);
    localStorage.setItem(RECENT_UPLOADS_KEY, JSON.stringify(next));
  } catch {
    localStorage.setItem(RECENT_UPLOADS_KEY, JSON.stringify([file]));
  }
}

export function recentUploads(folder?: string): UploadedFile[] {
  try {
    const items = JSON.parse(localStorage.getItem(RECENT_UPLOADS_KEY) || "[]") as UploadedFile[];
    return folder ? items.filter((item) => item.folder === folder || item.folder.startsWith(`${folder}/`)) : items;
  } catch {
    return [];
  }
}

export async function uploadFile(file: File, folder: string): Promise<UploadedFile> {
  const token = localStorage.getItem("talenova_access_token");
  const body = new FormData(); body.append("file", file); body.append("folder", folder);
  const response = await fetch(`${API}/storage/upload`, { method: "POST", body, headers: token ? { Authorization: `Bearer ${token}` } : {} });
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    throw new Error(detail?.detail || "Upload failed");
  }
  const uploaded = await response.json() as UploadedFile;
  rememberUpload(uploaded);
  return uploaded;
}
