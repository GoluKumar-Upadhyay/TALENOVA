"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { CMSForm } from "../../../../../components/admin/CMSForm";
import { ToastStack, createToast, type ToastMessage } from "../../../../../components/admin/Toast";
import { moduleConfig } from "../../../../../components/admin/cms-config";
import { api } from "../../../../../lib/api";
import type { CmsRecord } from "../../../../../types/cms";

export default function EditPage() {
  const { module, id } = useParams<{ module: string; id: string }>();
  const config = moduleConfig(module);
  const router = useRouter();
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const toast = createToast(setToasts);
  const detailPath = config.detailEndpoint?.(id) || `${config.endpoint}/${id}`;
  const detail = useQuery({ queryKey: ["cms-detail", config.module, id], queryFn: () => api<CmsRecord>(detailPath) });
  const update = useMutation({
    mutationFn: (values: Record<string, unknown>) => api(config.updateEndpoint?.(id, values) || `${config.endpoint}/${id}`, { method: "PUT", body: JSON.stringify(values) }),
    onSuccess: () => { toast("success", "Record updated"); router.push(`/admin/${module}`); },
    onError: (error) => toast("error", error instanceof Error ? error.message : "Update failed"),
  });
  return (
    <main className="min-h-screen bg-slate-50 p-6 lg:ml-64 md:p-10">
      <ToastStack items={toasts} onDismiss={(toastId) => setToasts((items) => items.filter((item) => item.id !== toastId))} />
      <Link href={`/admin/${module}`} className="inline-flex items-center gap-2 text-sm font-bold text-brand"><ArrowLeft size={16} />Back to {config.title}</Link>
      <p className="eyebrow mt-8">Edit record</p>
      <h1 className="mt-2 text-3xl font-black">Edit {config.title}</h1>
      <div className="mt-8">
        {detail.isLoading ? <p className="rounded-lg border bg-white p-8 text-slate-500">Loading record...</p> : null}
        {detail.isError ? <p className="rounded-lg border bg-white p-8 text-red-600">Unable to load this record.</p> : null}
        {detail.data ? (
          <CMSForm
            config={config}
            initialValues={detail.data}
            submitLabel="Save changes"
            onSubmit={async (values) => { await update.mutateAsync(values); }}
            onCancel={() => router.push(`/admin/${module}`)}
            onToast={toast}
          />
        ) : null}
      </div>
    </main>
  );
}
