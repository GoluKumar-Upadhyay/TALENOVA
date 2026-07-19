"use client";

import { Bold, Italic, List, ListOrdered } from "lucide-react";
import { useEffect, useRef } from "react";

export function RichTextEditor({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (ref.current && ref.current.innerHTML !== value) ref.current.innerHTML = value || "";
  }, [value]);
  function command(name: string) {
    document.execCommand(name);
    onChange(ref.current?.innerHTML || "");
  }
  return (
    <div className="overflow-hidden rounded-lg border bg-white">
      <div className="flex gap-1 border-b bg-slate-50 p-2">
        <button type="button" title="Bold" onClick={() => command("bold")} className="rounded-md p-2 hover:bg-white"><Bold size={16} /></button>
        <button type="button" title="Italic" onClick={() => command("italic")} className="rounded-md p-2 hover:bg-white"><Italic size={16} /></button>
        <button type="button" title="Bullet list" onClick={() => command("insertUnorderedList")} className="rounded-md p-2 hover:bg-white"><List size={16} /></button>
        <button type="button" title="Numbered list" onClick={() => command("insertOrderedList")} className="rounded-md p-2 hover:bg-white"><ListOrdered size={16} /></button>
      </div>
      <div
        ref={ref}
        contentEditable
        onInput={() => onChange(ref.current?.innerHTML || "")}
        className="min-h-40 p-3 text-sm leading-6 outline-none"
      />
    </div>
  );
}
