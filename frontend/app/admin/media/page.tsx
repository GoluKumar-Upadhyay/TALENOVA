"use client";

import { useEffect, useState } from "react";
import { Search, Trash2, Upload } from "lucide-react";
import { api } from "../../../lib/api";
import { recentUploads, uploadFile } from "../../../lib/upload";
import type { PageResponse } from "../../../types/cms";

type FileItem = { id: string; name: string; folder: string; url: string; type: string; size: number };

function mergeFiles(apiItems: FileItem[], localItems: FileItem[]) {
  const seen = new Set<string>();
  return [...apiItems, ...localItems].filter((item) => {
    const key = item.id || item.url;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export default function MediaManager() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [folder, setFolder] = useState<"images" | "videos" | "documents">("images");
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function load() {
    setError("");
    try {
      const data = await api<PageResponse<FileItem>>(`/storage/files?folder=${folder}&search=${encodeURIComponent(search)}&page_size=100`);
      setFiles(mergeFiles(data.items || [], recentUploads(folder) as FileItem[]));
    } catch (error) {
      setFiles(recentUploads(folder) as FileItem[]);
      setError(error instanceof Error ? error.message : "Storage unavailable");
    }
  }

  useEffect(() => { load(); }, [folder]);

  async function upload(file?: File) {
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      const uploaded = await uploadFile(file, folder);
      setFiles((items) => mergeFiles([uploaded as FileItem], items));
      await load();
    } catch (error) {
      setError(error instanceof Error ? error.message : "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  async function remove(id: string) {
    if (!confirm("Delete this file?")) return;
    await api(`/storage/files/${id}`, { method: "DELETE" });
    await load();
  }

  const accept = folder === "images" ? "image/*" : folder === "videos" ? "video/*" : ".pdf,.doc,.docx,.txt";

  return (
    <main className="min-h-screen bg-slate-50 p-6 lg:ml-64 md:p-10">
      <p className="eyebrow">Media manager</p>
      <h1 className="mt-2 text-3xl font-black">Files and uploads</h1>
      <div className="mt-8 flex flex-wrap gap-3">
        <select value={folder} onChange={(event) => setFolder(event.target.value as "images" | "videos" | "documents")} className="rounded-xl border bg-white p-3">
          <option value="images">Images</option>
          <option value="videos">Videos</option>
          <option value="documents">Documents</option>
        </select>
        <div className="flex rounded-xl border bg-white">
          <Search className="m-3 text-slate-400" size={18} />
          <input value={search} onChange={(event) => setSearch(event.target.value)} onKeyDown={(event) => { if (event.key === "Enter") load(); }} placeholder="Search files" className="p-3 outline-none" />
        </div>
        <button type="button" onClick={load} className="rounded-xl border bg-white px-4 py-3 font-bold">Search</button>
        <label className="flex cursor-pointer items-center gap-2 rounded-xl bg-brand px-4 py-3 font-bold text-white">
          <Upload size={17} />{busy ? "Uploading..." : "Upload"}
          <input type="file" accept={accept} className="hidden" onChange={(event) => upload(event.target.files?.[0])} />
        </label>
      </div>
      {error ? <p className="mt-5 rounded-xl bg-red-50 p-4 text-red-700">{error}</p> : null}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {files.map((file) => (
          <article key={file.id || file.url} className="overflow-hidden rounded-2xl border bg-white">
            {file.type.startsWith("image") ? <img src={file.url} alt={file.name} className="h-40 w-full object-cover" /> : <div className="flex h-40 items-center justify-center bg-slate-100 text-sm text-slate-500">{file.type}</div>}
            <div className="flex items-center justify-between gap-3 p-3">
              <span className="truncate text-sm font-semibold">{file.name}</span>
              <button type="button" onClick={() => remove(file.id)} className="text-red-600" aria-label={`Delete ${file.name}`}><Trash2 size={17} /></button>
            </div>
          </article>
        ))}
        {!files.length && !error ? <p className="col-span-full rounded-2xl border bg-white p-10 text-slate-500">No files found.</p> : null}
      </div>
    </main>
  );
}
