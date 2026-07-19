"use client";

import { ImageIcon, Search, X } from "lucide-react";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../../lib/api";
import type { PageResponse } from "../../types/cms";

type MediaItem = { id: string; name: string; folder: string; type: string; url: string };

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
  const query = useQuery({
    queryKey: ["media-picker", folder, search],
    enabled: open,
    queryFn: () => api<PageResponse<MediaItem>>(`/storage/files?folder=${folder}&search=${encodeURIComponent(search)}&page_size=60`),
  });
  if (!open) return null;
  const items = query.data?.items || [];
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
        <div className="grid max-h-[58vh] gap-3 overflow-y-auto p-4 sm:grid-cols-2 lg:grid-cols-4">
          {query.isLoading && <p className="col-span-full p-8 text-slate-500">Loading media...</p>}
          {query.isError && <p className="col-span-full p-8 text-red-600">Unable to load media.</p>}
          {!query.isLoading && !items.length && <p className="col-span-full p-8 text-slate-500">No media found.</p>}
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
