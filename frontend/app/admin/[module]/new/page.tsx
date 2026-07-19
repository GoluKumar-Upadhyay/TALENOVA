"use client";

import { useMutation } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { CMSForm } from "../../../../components/admin/CMSForm";
import { ToastStack, createToast, type ToastMessage } from "../../../../components/admin/Toast";
import { moduleConfig } from "../../../../components/admin/cms-config";
import { api } from "../../../../lib/api";

export default function CreatePage() {
  const { module } = useParams<{ module: string }>();
  const config = moduleConfig(module);
  const router = useRouter();
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const toast = createToast(setToasts);
  const create = useMutation({
    mutationFn: (values: Record<string, unknown>) => api(config.createEndpoint?.(values) || config.endpoint, { method: config.createMethod || "POST", body: JSON.stringify(values) }),
    onSuccess: () => { toast("success", "Record created"); router.push(`/admin/${module}`); },
    onError: (error) => toast("error", error instanceof Error ? error.message : "Create failed"),
  });
  return (
    <main className="min-h-screen bg-slate-50 p-6 lg:ml-64 md:p-10">
      <ToastStack items={toasts} onDismiss={(id) => setToasts((items) => items.filter((item) => item.id !== id))} />
      <Link href={`/admin/${module}`} className="inline-flex items-center gap-2 text-sm font-bold text-brand"><ArrowLeft size={16} />Back to {config.title}</Link>
      <p className="eyebrow mt-8">Create record</p>
      <h1 className="mt-2 text-3xl font-black">New {config.title}</h1>
      <div className="mt-8">
        <CMSForm
          config={config}
          submitLabel="Create record"
          onSubmit={async (values) => { await create.mutateAsync(values); }}
          onCancel={() => router.push(`/admin/${module}`)}
          onToast={toast}
        />
      </div>
    </main>
  );
}
