"use client";

import { Crop, RotateCcw } from "lucide-react";
import { useRef, useState } from "react";

export function ImageCropper({ file, onCropped }: { file: File; onCropped: (file: File) => void }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [zoom, setZoom] = useState(1);
  const [preview] = useState(() => URL.createObjectURL(file));
  async function crop() {
    const image = new Image();
    image.src = preview;
    await image.decode();
    const canvas = canvasRef.current;
    if (!canvas) return;
    const size = Math.min(image.width, image.height);
    canvas.width = 800;
    canvas.height = 800;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const scaled = size / zoom;
    const sx = (image.width - scaled) / 2;
    const sy = (image.height - scaled) / 2;
    ctx.clearRect(0, 0, 800, 800);
    ctx.drawImage(image, sx, sy, scaled, scaled, 0, 0, 800, 800);
    canvas.toBlob((blob) => {
      if (!blob) return;
      onCropped(new File([blob], file.name.replace(/\.[^.]+$/, ".webp"), { type: "image/webp" }));
    }, "image/webp", 0.92);
  }
  return (
    <div className="rounded-lg border bg-slate-50 p-3">
      <div className="grid gap-3 md:grid-cols-[180px_1fr]">
        <img src={preview} alt="Crop preview" className="aspect-square w-full rounded-lg object-cover" />
        <div className="grid content-between gap-3">
          <label className="text-sm font-bold text-slate-700">Crop zoom
            <input type="range" min="1" max="2" step="0.05" value={zoom} onChange={(event) => setZoom(Number(event.target.value))} className="mt-3 w-full" />
          </label>
          <div className="flex gap-2">
            <button type="button" onClick={crop} className="inline-flex items-center gap-2 rounded-lg bg-slate-950 px-3 py-2 text-sm font-bold text-white"><Crop size={16} />Apply crop</button>
            <button type="button" onClick={() => setZoom(1)} className="inline-flex items-center gap-2 rounded-lg border bg-white px-3 py-2 text-sm font-bold"><RotateCcw size={16} />Reset</button>
          </div>
        </div>
      </div>
      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}
