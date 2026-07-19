"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { ImageIcon } from "lucide-react";
import { Controller, useForm } from "react-hook-form";
import type { CmsModuleConfig } from "./cms-config";
import { defaultsFor, normalizeValues, schemaFor } from "./cms-config";
import { FileUploader } from "./FileUploader";
import { MediaPicker } from "./MediaPicker";
import { RichTextEditor } from "./RichTextEditor";

function formValue(value: unknown) {
  if (Array.isArray(value)) return value.join(", ");
  if (value && typeof value === "object") return JSON.stringify(value, null, 2);
  if (typeof value === "boolean") return value;
  return value == null ? "" : String(value);
}

export function CMSForm({
  config,
  initialValues,
  submitLabel,
  onSubmit,
  onCancel,
  onToast,
}: {
  config: CmsModuleConfig;
  initialValues?: Record<string, unknown>;
  submitLabel: string;
  onSubmit: (values: Record<string, unknown>) => Promise<void>;
  onCancel: () => void;
  onToast: (tone: "success" | "error" | "info", message: string) => void;
}) {
  const schema = schemaFor(config);
  const defaults = { ...defaultsFor(config), ...Object.fromEntries(Object.entries(initialValues || {}).map(([key, value]) => [key, formValue(value)])) };
  const form = useForm<Record<string, unknown>>({ resolver: zodResolver(schema), defaultValues: defaults });
  const mediaField = form.watch("__media_field") as string | undefined;
  async function submit(values: Record<string, unknown>) {
    try {
      const normalized = normalizeValues(config, values);
      delete normalized.__media_field;
      await onSubmit(normalized);
    } catch (error) {
      onToast("error", error instanceof Error ? error.message : "Unable to save record");
    }
  }
  return (
    <form onSubmit={form.handleSubmit(submit)} className="grid gap-5 rounded-lg border bg-white p-5 shadow-sm md:grid-cols-2">
      {config.fields.map((field) => (
        <Controller
          key={field.name}
          control={form.control}
          name={field.name}
          render={({ field: control, fieldState }) => {
            const error = fieldState.error?.message;
            const full = field.kind === "textarea" || field.kind === "richtext" || field.kind === "json" || field.kind === "media";
            return (
              <label className={`grid gap-2 text-sm font-bold text-slate-700 ${full ? "md:col-span-2" : ""}`}>
                {field.label}
                {field.kind === "boolean" ? (
                  <input type="checkbox" checked={Boolean(control.value)} onChange={(event) => control.onChange(event.target.checked)} className="h-5 w-5 rounded border" />
                ) : field.kind === "select" ? (
                  <select value={String(control.value ?? "")} onChange={control.onChange} className="rounded-lg border bg-white p-3">
                    {field.options?.map((option) => <option key={option} value={option}>{option}</option>)}
                  </select>
                ) : field.kind === "textarea" ? (
                  <textarea value={String(control.value ?? "")} onChange={control.onChange} className="min-h-28 rounded-lg border p-3" />
                ) : field.kind === "richtext" ? (
                  <RichTextEditor value={String(control.value ?? "")} onChange={control.onChange} />
                ) : field.kind === "json" ? (
                  <textarea value={String(control.value ?? "")} onChange={control.onChange} className="min-h-40 rounded-lg border font-mono text-xs p-3" />
                ) : field.kind === "media" ? (
                  <div className="grid gap-3">
                    <div className="flex gap-2">
                      <input value={String(control.value ?? "")} onChange={control.onChange} className="min-w-0 flex-1 rounded-lg border p-3" />
                      <button type="button" onClick={() => form.setValue("__media_field", field.name)} className="inline-flex items-center gap-2 rounded-lg border px-3 font-bold"><ImageIcon size={16} />Pick</button>
                    </div>
                    {String(control.value || "").startsWith("http") && field.folder === "images" ? <img src={String(control.value)} alt="" className="h-36 w-full rounded-lg object-cover" /> : null}
                    <FileUploader folder={field.folder || "images"} crop={field.crop} onUploaded={(url) => control.onChange(url)} onError={(message) => onToast("error", message)} />
                  </div>
                ) : (
                  <input type={field.kind === "number" ? "number" : "text"} value={String(control.value ?? "")} onChange={control.onChange} className="rounded-lg border p-3" />
                )}
                {error ? <span className="text-xs text-red-600">{error}</span> : null}
              </label>
            );
          }}
        />
      ))}
      <div className="flex justify-end gap-3 md:col-span-2">
        <button type="button" onClick={onCancel} className="rounded-lg border px-4 py-3 text-sm font-bold">Cancel</button>
        <button type="submit" disabled={form.formState.isSubmitting} className="rounded-lg bg-blue-700 px-4 py-3 text-sm font-bold text-white">{form.formState.isSubmitting ? "Saving..." : submitLabel}</button>
      </div>
      {mediaField ? (
        <MediaPicker
          folder={config.fields.find((field) => field.name === mediaField)?.folder || "images"}
          open={Boolean(mediaField)}
          onClose={() => form.setValue("__media_field", "")}
          onSelect={(url) => form.setValue(mediaField, url)}
        />
      ) : null}
    </form>
  );
}
