"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useMemo, useState } from "react";
import { DataTable } from "../../../components/admin/DataTable";
import { ToastStack, createToast, type ToastMessage } from "../../../components/admin/Toast";
import { moduleConfig } from "../../../components/admin/cms-config";
import { api } from "../../../lib/api";
import type { CmsRecord, PageResponse } from "../../../types/cms";

function collection(data: CmsRecord[] | PageResponse<CmsRecord> | CmsRecord | undefined): { items: CmsRecord[]; total: number } {
  if (!data) return { items: [] as CmsRecord[], total: 0 };
  if (Array.isArray(data)) return { items: data, total: data.length };
  if ("items" in data && Array.isArray(data.items)) return { items: data.items as CmsRecord[], total: typeof data.total === "number" ? data.total : data.items.length };
  return { items: [data], total: 1 };
}

export default function ModulePage() {
  const { module } = useParams<{ module: string }>();
  const config = moduleConfig(module);
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(24);
  const [sort, setSort] = useState(config.defaultSort);
  const [direction, setDirection] = useState<"asc" | "desc">("asc");
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const toast = createToast(setToasts);
  const queryKey = ["cms-list", config.module];
  const path = useMemo(() => {
    const params = new URLSearchParams({ page: String(page), page_size: String(pageSize), sort, direction });
    if (search) params.set("search", search);
    for (const [key, value] of Object.entries(filters)) if (value) params.set(key, value);
    return `${config.listEndpoint || config.endpoint}?${params.toString()}`;
  }, [config.endpoint, config.listEndpoint, direction, filters, page, pageSize, search, sort]);
  const list = useQuery({ queryKey: [...queryKey, path], queryFn: () => api<CmsRecord[] | PageResponse<CmsRecord> | CmsRecord>(path) });
  const parsed = collection(list.data);
  const remove = useMutation({
    mutationFn: (id: string) => api(config.deleteEndpoint?.(id) || `${config.endpoint}/${id}`, { method: "DELETE" }),
    onSuccess: () => { toast("success", "Record deleted"); queryClient.invalidateQueries({ queryKey }); },
    onError: (error) => toast("error", error instanceof Error ? error.message : "Delete failed"),
  });
  const toggle = useMutation({
    mutationFn: ({ row, checked }: { row: CmsRecord; checked: boolean }) => {
      const id = String(row.uuid);
      const field = config.statusField || "is_active";
      const value = typeof row[field] === "boolean" ? checked : checked ? config.statusLabels?.[1] || "read" : config.statusLabels?.[0] || "new";
      return api(config.updateEndpoint?.(id, row) || `${config.endpoint}/${id}`, { method: "PUT", body: JSON.stringify({ ...row, [field]: value }) });
    },
    onSuccess: () => { toast("success", "Status updated"); queryClient.invalidateQueries({ queryKey }); },
    onError: (error) => toast("error", error instanceof Error ? error.message : "Status update failed"),
  });
  function changeSort(field: string) {
    if (field === sort) setDirection((value) => value === "asc" ? "desc" : "asc");
    else { setSort(field); setDirection("asc"); }
  }
  return (
    <main className="min-h-screen bg-slate-50 p-6 lg:ml-64 md:p-10">
      <ToastStack items={toasts} onDismiss={(id) => setToasts((items) => items.filter((item) => item.id !== id))} />
      <p className="eyebrow">CMS management</p>
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="mt-2 text-3xl font-black">{config.title}</h1>
          <p className="mt-2 text-sm text-slate-500">Manage live {config.title.toLowerCase()} records.</p>
        </div>
        <Link href={`/admin/${module}/new`} className="inline-flex items-center gap-2 rounded-lg bg-brand px-4 py-3 font-bold text-white"><Plus size={18} />Add record</Link>
      </div>
      <DataTable
        config={config}
        rows={parsed.items}
        total={parsed.total}
        page={page}
        pageSize={pageSize}
        search={search}
        sort={sort}
        direction={direction}
        filters={filters}
        loading={list.isLoading}
        error={list.isError}
        onSearch={(value) => { setSearch(value); setPage(1); }}
        onSort={changeSort}
        onPage={setPage}
        onPageSize={(size) => { setPageSize(size); setPage(1); }}
        onFilter={(field, value) => { setFilters((current) => ({ ...current, [field]: value })); setPage(1); }}
        onDelete={(id) => remove.mutate(id)}
        onBulkDelete={(ids) => Promise.all(ids.map((id) => remove.mutateAsync(id))).then(() => { toast("success", "Selected records deleted"); }).catch((error) => toast("error", error instanceof Error ? error.message : "Bulk delete failed"))}
        onStatusToggle={(row, checked) => toggle.mutate({ row, checked })}
      />
    </main>
  );
}
