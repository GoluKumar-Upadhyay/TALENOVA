"use client";

export function StatusToggle({ checked, onChange, labels = ["Inactive", "Active"], disabled }: { checked: boolean; onChange: (checked: boolean) => void; labels?: [string, string]; disabled?: boolean }) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={`inline-flex min-w-28 items-center justify-between gap-2 rounded-full border px-2 py-1 text-xs font-bold ${checked ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-slate-200 bg-slate-100 text-slate-600"}`}
    >
      <span className={`h-5 w-5 rounded-full ${checked ? "bg-emerald-500" : "bg-slate-400"}`} />
      {checked ? labels[1] : labels[0]}
    </button>
  );
}
