"use client";

import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Pencil } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { moduleConfig } from "../../../../components/admin/cms-config";
import { api } from "../../../../lib/api";
import type { CmsRecord } from "../../../../types/cms";

function valueText(value: unknown) {
  if (value == null || value === "") return "—";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (typeof value === "object") return JSON.stringify(value, null, 2);
  return String(value);
}

export default function ViewPage() {
  const { module, id } = useParams<{ module: string; id: string }>();
  const config = moduleConfig(module);
  const detailPath = config.detailEndpoint?.(id) || `${config.endpoint}/${id}`;
  const result = useQuery({ queryKey: ["cms-detail", config.module, id], queryFn: () => api<CmsRecord>(detailPath) });
  return (
    <main className="min-h-screen bg-slate-50 p-6 lg:ml-64 md:p-10">
      <Link href={`/admin/${module}`} className="inline-flex items-center gap-2 text-sm font-bold text-brand"><ArrowLeft size={16} />Back to {config.title}</Link>
      <div className="mt-8 flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="eyebrow">View details</p>
          <h1 className="mt-2 text-3xl font-black">{config.title}</h1>
        </div>
        <Link href={`/admin/${module}/${id}/edit`} className="inline-flex items-center gap-2 rounded-lg bg-brand px-4 py-3 font-bold text-white"><Pencil size={17} />Edit</Link>
      </div>
      <section className="mt-8 rounded-lg border bg-white p-6 shadow-sm">
        {result.isLoading ? <p className="text-slate-500">Loading record...</p> : null}
        {result.isError ? <p className="text-red-600">Unable to load this record.</p> : null}
        {result.data ? (
          <dl className="grid gap-5 md:grid-cols-2">
            {config.fields.map((field) => (
              <div key={field.name} className={field.kind === "richtext" || field.kind === "json" ? "md:col-span-2" : ""}>
                <dt className="text-xs font-black uppercase tracking-wide text-slate-500">{field.label}</dt>
                {field.kind === "media" && String(result.data?.[field.name] || "").startsWith("http") ? (
                  <dd className="mt-2"><img src={String(result.data[field.name])} alt="" className="max-h-56 rounded-lg object-contain" /></dd>
                ) : field.kind === "richtext" ? (
                  <dd className="prose mt-2 max-w-none text-sm leading-6" dangerouslySetInnerHTML={{ __html: String(result.data[field.name] || "—") }} />
                ) : (
                  <dd className="mt-2 whitespace-pre-wrap rounded-lg bg-slate-50 p-3 text-sm text-slate-700">{valueText(result.data[field.name])}</dd>
                )}
              </div>
            ))}
          </dl>
        ) : null}
      </section>
    </main>
  );
}
