"use client";

import { UploadCloud } from "lucide-react";
import { useState } from "react";
import { uploadFile } from "../../lib/upload";
import { ImageCropper } from "./ImageCropper";

export function FileUploader({
  folder,
  crop,
  onUploaded,
  onError,
}: {
  folder: "images" | "videos" | "documents";
  crop?: boolean;
  onUploaded: (url: string) => void;
  onError: (message: string) => void;
}) {
  const [busy, setBusy] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const accept = folder === "images" ? "image/*" : folder === "videos" ? "video/*" : ".pdf,.doc,.docx,.txt";
  async function upload(next: File) {
    setBusy(true);
    try {
      const result = await uploadFile(next, folder);
      onUploaded(result.url);
      setFile(null);
    } catch (error) {
      onError(error instanceof Error ? error.message : "Upload failed");
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="grid gap-3">
      <label className="flex cursor-pointer items-center justify-center gap-2 rounded-lg border border-dashed bg-slate-50 p-4 text-sm font-bold text-slate-600 hover:bg-white">
        <UploadCloud size={18} />{busy ? "Uploading..." : `Upload ${folder.slice(0, -1)}`}
        <input type="file" accept={accept} className="hidden" onChange={(event) => {
          const selected = event.target.files?.[0];
          if (!selected) return;
          if (crop && selected.type.startsWith("image/")) setFile(selected);
          else upload(selected);
        }} />
      </label>
      {file && <ImageCropper file={file} onCropped={upload} />}
    </div>
  );
}
