"use client";

import {
  type ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { ChevronDown, ChevronUp, Eye, Pencil, Search, SlidersHorizontal, Trash2 } from "lucide-react";
import Link from "next/link";
import { useMemo, useState } from "react";
import type { CmsModuleConfig } from "./cms-config";
import type { CmsRecord } from "../../types/cms";
import { ConfirmDialog } from "./ConfirmDialog";
import { ExportActions } from "./ExportActions";
import { StatusToggle } from "./StatusToggle";

function labelFor(key: string) {
  return key.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function display(value: unknown) {
  if (value == null || value === "") return "—";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

export function DataTable({
  config,
  rows,
  total,
  page,
  pageSize,
  search,
  sort,
  direction,
  filters,
  loading,
  error,
  onSearch,
  onSort,
  onPage,
  onPageSize,
  onFilter,
  onDelete,
  onBulkDelete,
  onStatusToggle,
}: {
  config: CmsModuleConfig;
  rows: CmsRecord[];
  total: number;
  page: number;
  pageSize: number;
  search: string;
  sort: string;
  direction: "asc" | "desc";
  filters: Record<string, string>;
  loading: boolean;
  error: boolean;
  onSearch: (value: string) => void;
  onSort: (field: string) => void;
  onPage: (page: number) => void;
  onPageSize: (size: number) => void;
  onFilter: (field: string, value: string) => void;
  onDelete: (id: string) => void;
  onBulkDelete: (ids: string[]) => void;
  onStatusToggle: (row: CmsRecord, checked: boolean) => void;
}) {
  const [selection, setSelection] = useState<Record<string, boolean>>({});
  const [confirm, setConfirm] = useState<{ mode: "one" | "bulk"; id?: string } | null>(null);
  const filterFields = config.fields.filter((field) => field.filter);
  const selectedIds = Object.entries(selection).filter(([, selected]) => selected).map(([id]) => id);
  const pageCount = Math.max(1, Math.ceil(total / pageSize));

  const columns = useMemo<ColumnDef<CmsRecord>[]>(() => {
    const base: ColumnDef<CmsRecord>[] = [
      {
        id: "select",
        header: () => (
          <input
            type="checkbox"
            checked={rows.length > 0 && rows.every((row) => row.uuid && selection[row.uuid])}
            onChange={(event) => {
              const checked = event.target.checked;
              setSelection(Object.fromEntries(rows.map((row) => [String(row.uuid), checked])));
            }}
            aria-label="Select all rows"
          />
        ),
        cell: ({ row }) => (
          <input
            type="checkbox"
            checked={Boolean(row.original.uuid && selection[row.original.uuid])}
            onChange={(event) => {
              const id = String(row.original.uuid || "");
              setSelection((current) => ({ ...current, [id]: event.target.checked }));
            }}
            aria-label="Select row"
          />
        ),
      },
      ...config.tableColumns.map((key): ColumnDef<CmsRecord> => ({
        accessorKey: key,
        header: () => (
          <button type="button" onClick={() => onSort(key)} className="inline-flex items-center gap-1 font-black">
            {labelFor(key)}
            {sort === key ? direction === "asc" ? <ChevronUp size={14} /> : <ChevronDown size={14} /> : null}
          </button>
        ),
        cell: ({ getValue, row }) => {
          if (key === config.statusField && typeof getValue() === "boolean") {
            return <StatusToggle checked={Boolean(getValue())} labels={config.statusLabels} onChange={(checked) => onStatusToggle(row.original, checked)} />;
          }
          return <span className="line-clamp-2">{display(getValue())}</span>;
        },
      })),
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => {
          const id = String(row.original.uuid || "");
          return (
            <div className="flex items-center gap-2">
              <Link title="View" href={`/admin/${config.module}/${id}`} className="rounded-md border p-2 hover:bg-slate-50"><Eye size={15} /></Link>
              <Link title="Edit" href={`/admin/${config.module}/${id}/edit`} className="rounded-md border p-2 hover:bg-slate-50"><Pencil size={15} /></Link>
              <button title="Delete" type="button" onClick={() => setConfirm({ mode: "one", id })} className="rounded-md border p-2 text-red-600 hover:bg-red-50"><Trash2 size={15} /></button>
            </div>
          );
        },
      },
    ];
    return base;
  }, [config, direction, onSort, onStatusToggle, rows, selection, sort]);

  const table = useReactTable({ data: rows, columns, getCoreRowModel: getCoreRowModel(), getRowId: (row) => String(row.uuid) });

  return (
    <section className="mt-8 rounded-lg border bg-white shadow-sm">
      <div className="grid gap-4 border-b p-4 xl:grid-cols-[1fr_auto_auto]">
        <div className="flex items-center gap-2 rounded-lg border bg-white px-3">
          <Search size={17} className="text-slate-400" />
          <input value={search} onChange={(event) => onSearch(event.target.value)} placeholder={`Search ${config.title.toLowerCase()}`} className="h-11 w-full outline-none" />
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <SlidersHorizontal size={17} className="text-slate-400" />
          {filterFields.map((field) => (
            <select key={field.name} value={filters[field.name] || ""} onChange={(event) => onFilter(field.name, event.target.value)} className="h-11 rounded-lg border bg-white px-3 text-sm font-semibold">
              <option value="">{field.label}</option>
              {field.kind === "boolean" ? (
                <>
                  <option value="true">Yes</option>
                  <option value="false">No</option>
                </>
              ) : field.options?.map((option) => <option key={option} value={option}>{option}</option>)}
            </select>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          <ExportActions rows={rows} filename={config.module} />
          <button type="button" disabled={!selectedIds.length} onClick={() => setConfirm({ mode: "bulk" })} className="inline-flex items-center gap-2 rounded-lg border bg-white px-3 py-2 text-sm font-bold text-red-600 disabled:opacity-40"><Trash2 size={16} />Bulk delete</button>
        </div>
      </div>

      {loading ? <p className="p-8 text-slate-500">Loading records...</p> : null}
      {error ? <p className="p-8 text-red-600">Unable to load records.</p> : null}
      {!loading && !error && !rows.length ? <p className="p-8 text-slate-500">No records match the current view.</p> : null}

      {!loading && !error && rows.length ? (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[880px] text-left text-sm">
            <thead className="border-b bg-slate-50 text-xs uppercase text-slate-500">
              {table.getHeaderGroups().map((group) => (
                <tr key={group.id}>{group.headers.map((header) => <th key={header.id} className="p-4">{flexRender(header.column.columnDef.header, header.getContext())}</th>)}</tr>
              ))}
            </thead>
            <tbody>
              {table.getRowModel().rows.map((row) => (
                <tr key={row.id} className="border-b last:border-0 hover:bg-slate-50">
                  {row.getVisibleCells().map((cell) => <td key={cell.id} className="max-w-xs p-4 align-top">{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}

      <div className="flex flex-wrap items-center justify-between gap-3 border-t p-4 text-sm">
        <span className="font-semibold text-slate-600">{total} records</span>
        <div className="flex items-center gap-2">
          <select value={pageSize} onChange={(event) => onPageSize(Number(event.target.value))} className="rounded-lg border bg-white p-2 font-semibold">
            {[10, 24, 50, 100].map((size) => <option key={size} value={size}>{size} / page</option>)}
          </select>
          <button type="button" disabled={page <= 1} onClick={() => onPage(page - 1)} className="rounded-lg border px-3 py-2 font-bold disabled:opacity-40">Previous</button>
          <span className="px-2 font-bold">Page {page} of {pageCount}</span>
          <button type="button" disabled={page >= pageCount} onClick={() => onPage(page + 1)} className="rounded-lg border px-3 py-2 font-bold disabled:opacity-40">Next</button>
        </div>
      </div>

      <ConfirmDialog
        open={Boolean(confirm)}
        title={confirm?.mode === "bulk" ? "Delete selected records?" : "Delete this record?"}
        message={confirm?.mode === "bulk" ? "Selected records will be removed from this module." : "This record will be removed from this module."}
        confirmLabel="Delete"
        onCancel={() => setConfirm(null)}
        onConfirm={() => {
          if (confirm?.mode === "bulk") onBulkDelete(selectedIds);
          if (confirm?.mode === "one" && confirm.id) onDelete(confirm.id);
          setSelection({});
          setConfirm(null);
        }}
      />
    </section>
  );
}
