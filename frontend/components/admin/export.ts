function download(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
  URL.revokeObjectURL(link.href);
}

function keysFor(rows: Record<string, unknown>[]) {
  return Array.from(new Set(rows.flatMap((row) => Object.keys(row)))).filter((key) => key !== "id");
}

export function exportCsv(rows: Record<string, unknown>[], filename: string) {
  if (!rows.length) return;
  const keys = keysFor(rows);
  const csv = [keys.join(","), ...rows.map((row) => keys.map((key) => JSON.stringify(row[key] ?? "")).join(","))].join("\n");
  download(csv, `${filename}.csv`, "text/csv;charset=utf-8");
}

export function exportExcel(rows: Record<string, unknown>[], filename: string) {
  if (!rows.length) return;
  const keys = keysFor(rows);
  const cells = rows.map((row) => `<tr>${keys.map((key) => `<td>${String(row[key] ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;")}</td>`).join("")}</tr>`).join("");
  const header = `<tr>${keys.map((key) => `<th>${key}</th>`).join("")}</tr>`;
  download(`<table>${header}${cells}</table>`, `${filename}.xls`, "application/vnd.ms-excel;charset=utf-8");
}
