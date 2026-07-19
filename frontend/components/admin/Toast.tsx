"use client";

import { CheckCircle2, Info, XCircle } from "lucide-react";
import type { ToastTone } from "../../types/cms";

export type ToastMessage = { id: number; tone: ToastTone; message: string };

export function ToastStack({ items, onDismiss }: { items: ToastMessage[]; onDismiss: (id: number) => void }) {
  return (
    <div className="fixed right-4 top-4 z-50 grid w-full max-w-sm gap-3">
      {items.map((toast) => {
        const Icon = toast.tone === "success" ? CheckCircle2 : toast.tone === "error" ? XCircle : Info;
        const tone = toast.tone === "success" ? "border-emerald-200 bg-emerald-50 text-emerald-800" : toast.tone === "error" ? "border-red-200 bg-red-50 text-red-800" : "border-blue-200 bg-blue-50 text-blue-800";
        return (
          <button key={toast.id} type="button" onClick={() => onDismiss(toast.id)} className={`flex items-start gap-3 rounded-lg border p-4 text-left text-sm font-semibold shadow-sm ${tone}`}>
            <Icon size={18} className="mt-0.5 shrink-0" />
            <span>{toast.message}</span>
          </button>
        );
      })}
    </div>
  );
}

export function createToast(setItems: React.Dispatch<React.SetStateAction<ToastMessage[]>>) {
  return (tone: ToastTone, message: string) => {
    const id = Date.now() + Math.floor(Math.random() * 1000);
    setItems((items) => [...items, { id, tone, message }]);
    window.setTimeout(() => setItems((items) => items.filter((item) => item.id !== id)), 3500);
  };
}
