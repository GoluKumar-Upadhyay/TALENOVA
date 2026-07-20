"use client";

import { ImageIcon, Search, X } from "lucide-react";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api";
import { recentUploads } from "../../lib/upload";
import type { PageResponse } from "../../types/cms";

type MediaItem = { id: string; name: string; folder: string; type: string; url: string };

function mergeMedia(primary: MediaItem[], fallback: MediaItem[], search: string) {
  const seen = new Set<string>();
  const query = search.trim().toLowerCase();
  return [...primary, ...fallback]
    .filter((item) => !query || item.name.toLowerCase().includes(query) || item.url.toLowerCase().includes(query))
    .filter((item) => {
      const key = item.id || item.url;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
}

export function MediaPicker({
  folder,
  open,
  onClose,
  onSelect,
}: {
  folder: "images" | "videos" | "documents";
  open: boolean;
  onClose: () => void;
  onSelect: (url: string) => void;
}) {
  const [search, setSearch] = useState("");
  const [manualUrl, setManualUrl] = useState("");
  const query = useQuery({
    queryKey: ["media-picker", folder, search],
    enabled: open,
    retry: 1,
    queryFn: () => api<PageResponse<MediaItem>>(`/storage/files?folder=${folder}&search=${encodeURIComponent(search)}&page_size=60`),
  });
  if (!open) return null;
  const recent = typeof window === "undefined" ? [] : recentUploads(folder);
  const items = mergeMedia(query.data?.items || [], recent, search);
  const errorText = query.error instanceof Error ? query.error.message : "Unable to load media.";
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/40 p-4">
      <section className="max-h-[85vh] w-full max-w-4xl overflow-hidden rounded-lg border bg-white shadow-xl">
        <header className="flex items-center justify-between border-b p-4">
          <div>
            <h2 className="text-lg font-black">Media picker</h2>
            <p className="text-sm text-slate-500">Choose an existing {folder.slice(0, -1)} asset.</p>
          </div>
          <button type="button" onClick={onClose} className="rounded-lg border p-2"><X size={18} /></button>
        </header>
        <div className="flex items-center gap-2 border-b p-4">
          <Search size={17} className="text-slate-400" />
          <input value={search} onChange={(event) => setSearch(event.target.value)} className="w-full outline-none" placeholder="Search media" />
        </div>
        <div className="grid gap-3 border-b bg-slate-50 p-4 sm:grid-cols-[1fr_auto]">
          <input
            value={manualUrl}
            onChange={(event) => setManualUrl(event.target.value)}
            className="rounded-lg border bg-white px-3 py-2 text-sm outline-none focus:border-blue-400"
            placeholder="Paste an uploaded image URL if the media list is unavailable"
          />
          <button
            type="button"
            disabled={!manualUrl.trim()}
            onClick={() => { onSelect(manualUrl.trim()); onClose(); }}
            className="rounded-lg bg-brand px-4 py-2 text-sm font-bold text-white disabled:opacity-50"
          >
            Use URL
          </button>
        </div>
        <div className="grid max-h-[58vh] gap-3 overflow-y-auto p-4 sm:grid-cols-2 lg:grid-cols-4">
          {query.isLoading && <p className="col-span-full p-8 text-slate-500">Loading media...</p>}
          {query.isError && <p className="col-span-full rounded-lg bg-red-50 p-4 text-sm font-semibold text-red-600">{errorText}</p>}
          {!query.isLoading && !items.length && <p className="col-span-full p-8 text-slate-500">No media found. Upload a file first, or paste the media URL above.</p>}
          {items.map((item) => (
            <button key={item.id} type="button" onClick={() => { onSelect(item.url); onClose(); }} className="overflow-hidden rounded-lg border bg-white text-left hover:border-blue-400">
              {item.type.startsWith("image") ? <img src={item.url} alt={item.name} className="h-32 w-full object-cover" /> : <div className="grid h-32 place-items-center bg-slate-100"><ImageIcon className="text-slate-400" /></div>}
              <span className="block truncate p-3 text-sm font-semibold">{item.name}</span>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}
