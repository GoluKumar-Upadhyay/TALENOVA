"use client";
import { useState } from "react";
import { uploadFile } from "../../lib/upload";
export default function UploadPreview({ bucket, onUploaded }: { bucket: string; onUploaded: (url: string) => void }) {
  const [preview, setPreview] = useState<string>(); const [busy, setBusy] = useState(false);
  async function choose(file?: File) { if (!file) return; setPreview(URL.createObjectURL(file)); setBusy(true); try { const result = await uploadFile(file, bucket); onUploaded(result.url); } finally { setBusy(false); } }
  return <label className="block cursor-pointer rounded-xl border-2 border-dashed p-5 text-center text-sm text-slate-500"><input type="file" accept="image/*,video/*,.pdf" className="hidden" onChange={e=>choose(e.target.files?.[0])}/>{preview ? <img src={preview} alt="Upload preview" className="mx-auto max-h-36 rounded-lg object-contain"/> : "Drag a file here or click to upload"}<span className="mt-2 block">{busy ? "Uploading…" : "Preview before upload"}</span></label>;
}
