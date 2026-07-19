"use client";

import { Download, FileSpreadsheet } from "lucide-react";
import { exportCsv, exportExcel } from "./export";

export function ExportActions({ rows, filename }: { rows: Record<string, unknown>[]; filename: string }) {
  return (
    <div className="flex flex-wrap gap-2">
      <button type="button" onClick={() => exportCsv(rows, filename)} disabled={!rows.length} className="inline-flex items-center gap-2 rounded-lg border bg-white px-3 py-2 text-sm font-bold disabled:opacity-50"><Download size={16} />CSV</button>
      <button type="button" onClick={() => exportExcel(rows, filename)} disabled={!rows.length} className="inline-flex items-center gap-2 rounded-lg border bg-white px-3 py-2 text-sm font-bold disabled:opacity-50"><FileSpreadsheet size={16} />Excel</button>
    </div>
  );
}
