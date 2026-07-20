"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  ArrowLeft, Save, Eye, Plus, Trash2, GripVertical, ChevronDown, ChevronRight,
  Loader2, Check, X, Download, Search, Filter, AlertCircle, Upload
} from "lucide-react";
import { api } from "../../../../lib/api";

/* ── Types ───────────────────────────────────────────────────────────────── */

interface Submodule { uuid: string; title: string; description?: string; position: number; }
interface Module { uuid: string; title: string; description?: string; position: number; submodules: Submodule[]; }
interface Batch {
  uuid: string; name: string; start_date?: string; end_date?: string;
  application_deadline?: string; max_seats?: number; remaining_seats?: number;
  time_slot?: string; status: string; course_id: number;
}
interface Application {
  uuid: string; full_name: string; email: string; phone?: string;
  college?: string; degree?: string; current_year?: string;
  linkedin_url?: string; github_url?: string; motivation?: string;
  resume_url?: string; status: string; created_at: string;
}
interface Course {
  uuid: string; title: string; slug: string;
  short_description?: string; description?: string;
  thumbnail_url?: string; duration?: string; level?: string;
  price?: number; certificate_available: boolean;
  skills_covered: string[]; technologies: string[];
  learning_outcomes: string[]; career_opportunities: string[];
  faqs: { question: string; answer: string }[];
  prerequisites: string[]; certification?: string;
  is_published: boolean; is_active: boolean; is_coming_soon: boolean;
  category_id?: number; mentor_id?: number; display_order: number;
}

type Tab = "overview" | "curriculum" | "batches" | "applications" | "seo" | "settings";

const TABS: { id: Tab; label: string }[] = [
  { id: "overview", label: "Overview" },
  { id: "curriculum", label: "Curriculum" },
  { id: "batches", label: "Batches" },
  { id: "applications", label: "Applications" },
  { id: "seo", label: "SEO" },
  { id: "settings", label: "Settings" },
];

const BATCH_STATUSES = ["draft","published","upcoming","active","batch_full","applications_closed","expired","hidden"];
const TIME_SLOTS = ["morning","afternoon","evening","weekend","online","offline","hybrid"];
const LEVELS = ["Beginner","Intermediate","Advanced"];
const APP_STATUS_COLORS: Record<string, { bg: string; color: string }> = {
  pending:  { bg: "#fef3c7", color: "#92400e" },
  approved: { bg: "#d1fae5", color: "#065f46" },
  rejected: { bg: "#fee2e2", color: "#991b1b" },
};

/* ── Helpers ─────────────────────────────────────────────────────────────── */

function Pill({ text, color, bg }: { text: string; color: string; bg: string }) {
  return (
    <span style={{
      padding: "3px 10px", borderRadius: 999, fontSize: 11, fontWeight: 700,
      background: bg, color, textTransform: "capitalize"
    }}>{text.replace("_", " ")}</span>
  );
}

function TagInput({ label, values, onChange }: {
  label: string; values: string[]; onChange: (v: string[]) => void;
}) {
  const [input, setInput] = useState("");
  const add = () => {
    const v = input.trim();
    if (v && !values.includes(v)) { onChange([...values, v]); setInput(""); }
  };
  return (
    <div>
      <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 6 }}>{label}</label>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 8 }}>
        {values.map(v => (
          <span key={v} style={{
            display: "inline-flex", alignItems: "center", gap: 5,
            padding: "4px 10px", background: "#dbeafe", color: "#1d4ed8",
            borderRadius: 999, fontSize: 12, fontWeight: 600
          }}>
            {v}
            <button type="button" onClick={() => onChange(values.filter(x => x !== v))}
              style={{ background: "none", border: "none", cursor: "pointer", padding: 0, color: "#3b82f6", fontSize: 14, lineHeight: 1 }}>×</button>
          </span>
        ))}
      </div>
      <div style={{ display: "flex", gap: 6 }}>
        <input value={input} onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && (e.preventDefault(), add())}
          placeholder={`Add ${label.toLowerCase()}...`}
          style={{
            flex: 1, padding: "8px 12px", border: "1px solid #d1d5db",
            borderRadius: 9, fontSize: 13, outline: "none"
          }} />
        <button type="button" onClick={add} style={{
          padding: "8px 14px", background: "#eff6ff", border: "1px solid #bfdbfe",
          borderRadius: 9, fontSize: 12, fontWeight: 700, color: "#1d4ed8", cursor: "pointer"
        }}>Add</button>
      </div>
    </div>
  );
}

function FieldRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "180px 1fr", gap: 16, alignItems: "start", padding: "14px 0", borderBottom: "1px solid #f1f5f9" }}>
      <label style={{ fontWeight: 700, fontSize: 13, color: "#374151", paddingTop: 10 }}>{label}</label>
      <div>{children}</div>
    </div>
  );
}

function Input({ value, onChange, placeholder, type = "text", ...rest }: {
  value: string | number; onChange: (v: string) => void; placeholder?: string; type?: string; [k: string]: unknown;
}) {
  return (
    <input value={value} onChange={e => onChange(e.target.value)} type={type} placeholder={placeholder}
      style={{
        width: "100%", padding: "10px 13px", border: "1px solid #d1d5db",
        borderRadius: 10, fontSize: 13, outline: "none", boxSizing: "border-box" as const,
        ...((rest.style as object) || {})
      }} {...rest} />
  );
}

function Textarea({ value, onChange, placeholder, rows = 4 }: {
  value: string; onChange: (v: string) => void; placeholder?: string; rows?: number;
}) {
  return (
    <textarea value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} rows={rows}
      style={{
        width: "100%", padding: "10px 13px", border: "1px solid #d1d5db",
        borderRadius: 10, fontSize: 13, outline: "none", resize: "vertical", boxSizing: "border-box" as const
      }} />
  );
}

function Select({ value, onChange, options }: {
  value: string; onChange: (v: string) => void; options: string[];
}) {
  return (
    <select value={value} onChange={e => onChange(e.target.value)}
      style={{
        width: "100%", padding: "10px 13px", border: "1px solid #d1d5db",
        borderRadius: 10, fontSize: 13, outline: "none", background: "#fff"
      }}>
      <option value="">— None —</option>
      {options.map(o => <option key={o} value={o}>{o.replace("_", " ")}</option>)}
    </select>
  );
}

/* ── Overview Tab ────────────────────────────────────────────────────────── */

function OverviewTab({ course, onSaved }: { course: Course; onSaved: (c: Course) => void }) {
  const [form, setForm] = useState({ ...course });
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const set = (k: string, v: unknown) => setForm(prev => ({ ...prev, [k]: v }));

  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      const form2 = new FormData();
      form2.append("file", file);
      form2.append("folder", "images");
      const token = localStorage.getItem("talenova_access_token");
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/storage/upload`,
        { method: "POST", headers: { Authorization: `Bearer ${token}` }, body: form2 }
      );
      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      set("thumbnail_url", data.url);
    } catch { alert("Upload failed."); } finally { setUploading(false); }
  };

  const save = async () => {
    setSaving(true);
    try {
      const updated = await api<Course>(`/courses/${course.uuid}`, {
        method: "PUT", body: JSON.stringify(form),
      });
      onSaved(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : "Save failed");
    } finally { setSaving(false); }
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <h2 style={{ margin: 0, fontSize: 18, fontWeight: 800, color: "#0f172a" }}>Course Overview</h2>
        <button onClick={save} disabled={saving} style={{
          display: "flex", alignItems: "center", gap: 7,
          padding: "10px 20px", background: saved ? "#10b981" : "#1d4ed8",
          color: "#fff", border: "none", borderRadius: 11,
          fontWeight: 700, fontSize: 13, cursor: saving ? "not-allowed" : "pointer",
          transition: "background .3s"
        }}>
          {saving ? <Loader2 size={15} style={{ animation: "spin 1s linear infinite" }} /> : saved ? <Check size={15} /> : <Save size={15} />}
          {saving ? "Saving..." : saved ? "Saved!" : "Save Changes"}
        </button>
      </div>

      {/* Thumbnail */}
      <div style={{ marginBottom: 24 }}>
        <label style={{ display: "block", fontWeight: 700, fontSize: 13, color: "#374151", marginBottom: 8 }}>Course Thumbnail</label>
        <div style={{ display: "flex", gap: 14, alignItems: "flex-start" }}>
          <div style={{
            width: 220, height: 130, borderRadius: 12, overflow: "hidden",
            background: form.thumbnail_url ? `url(${form.thumbnail_url}) center/cover` : "linear-gradient(135deg,#dbeafe,#1d4ed8)",
            border: "1px solid #e2e8f0", flexShrink: 0
          }} />
          <div style={{ flex: 1 }}>
            <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
              <button type="button" onClick={() => fileRef.current?.click()} style={{
                display: "flex", alignItems: "center", gap: 6,
                padding: "8px 14px", background: "#f8fafc", border: "1px solid #e2e8f0",
                borderRadius: 9, fontSize: 12, fontWeight: 700, cursor: "pointer", color: "#374151"
              }}>
                {uploading ? <Loader2 size={13} style={{ animation: "spin 1s linear infinite" }} /> : <Upload size={13} />}
                Upload Image
              </button>
            </div>
            <input
              value={form.thumbnail_url || ""}
              onChange={e => set("thumbnail_url", e.target.value)}
              placeholder="Or paste image URL..."
              style={{ width: "100%", padding: "9px 12px", border: "1px solid #d1d5db", borderRadius: 9, fontSize: 13, outline: "none", boxSizing: "border-box" }}
            />
            <input ref={fileRef} type="file" accept="image/*" style={{ display: "none" }}
              onChange={e => e.target.files?.[0] && handleUpload(e.target.files[0])} />
          </div>
        </div>
      </div>

      <FieldRow label="Course Title">
        <Input value={form.title || ""} onChange={v => set("title", v)} placeholder="Course title" />
      </FieldRow>
      <FieldRow label="Short Description">
        <Textarea value={form.short_description || ""} onChange={v => set("short_description", v)} placeholder="Brief summary (shown on cards)" rows={2} />
      </FieldRow>
      <FieldRow label="Full Description">
        <Textarea value={form.description || ""} onChange={v => set("description", v)} placeholder="Detailed course description..." rows={6} />
      </FieldRow>
      <FieldRow label="Level">
        <Select value={form.level || ""} onChange={v => set("level", v)} options={LEVELS} />
      </FieldRow>
      <FieldRow label="Duration">
        <Input value={form.duration || ""} onChange={v => set("duration", v)} placeholder="e.g. 3 months, 12 weeks" />
      </FieldRow>
      <FieldRow label="Price (₹)">
        <Input value={form.price?.toString() || ""} onChange={v => set("price", v ? parseFloat(v) : null)} type="number" placeholder="0 for free" />
      </FieldRow>
      <FieldRow label="Certificate">
        <label style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer" }}>
          <input type="checkbox" checked={form.certificate_available} onChange={e => set("certificate_available", e.target.checked)}
            style={{ width: 18, height: 18, accentColor: "#1d4ed8" }} />
          <span style={{ fontSize: 13, color: "#374151" }}>Certificate available on completion</span>
        </label>
      </FieldRow>
      <FieldRow label="Certification Info">
        <Textarea value={form.certification || ""} onChange={v => set("certification", v)} placeholder="Certificate details..." rows={2} />
      </FieldRow>

      <div style={{ marginTop: 24, display: "grid", gap: 20 }}>
        <TagInput label="Learning Outcomes" values={form.learning_outcomes || []} onChange={v => set("learning_outcomes", v)} />
        <TagInput label="Skills Covered" values={form.skills_covered || []} onChange={v => set("skills_covered", v)} />
        <TagInput label="Technologies Used" values={form.technologies || []} onChange={v => set("technologies", v)} />
        <TagInput label="Career Opportunities" values={form.career_opportunities || []} onChange={v => set("career_opportunities", v)} />
        <TagInput label="Prerequisites" values={form.prerequisites || []} onChange={v => set("prerequisites", v)} />
      </div>

      {/* FAQs */}
      <div style={{ marginTop: 24 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <label style={{ fontWeight: 700, fontSize: 13, color: "#374151" }}>FAQs</label>
          <button type="button" onClick={() => set("faqs", [...(form.faqs || []), { question: "", answer: "" }])}
            style={{ display: "flex", alignItems: "center", gap: 5, padding: "6px 12px", background: "#eff6ff", border: "1px solid #bfdbfe", borderRadius: 8, fontSize: 12, fontWeight: 700, color: "#1d4ed8", cursor: "pointer" }}>
            <Plus size={12} /> Add FAQ
          </button>
        </div>
        {(form.faqs || []).map((faq, i) => (
          <div key={i} style={{ marginBottom: 12, padding: 14, background: "#f8fafc", borderRadius: 12, border: "1px solid #e2e8f0" }}>
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <button type="button" onClick={() => set("faqs", form.faqs.filter((_, j) => j !== i))}
                style={{ background: "none", border: "none", cursor: "pointer", color: "#ef4444", fontSize: 12 }}>Remove</button>
            </div>
            <input value={faq.question} onChange={e => set("faqs", form.faqs.map((f, j) => j === i ? { ...f, question: e.target.value } : f))}
              placeholder="Question" style={{ width: "100%", padding: "8px 12px", border: "1px solid #d1d5db", borderRadius: 8, fontSize: 13, marginBottom: 8, outline: "none", boxSizing: "border-box" }} />
            <textarea value={faq.answer} onChange={e => set("faqs", form.faqs.map((f, j) => j === i ? { ...f, answer: e.target.value } : f))}
              placeholder="Answer" rows={2}
              style={{ width: "100%", padding: "8px 12px", border: "1px solid #d1d5db", borderRadius: 8, fontSize: 13, outline: "none", resize: "vertical", boxSizing: "border-box" }} />
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── Curriculum Tab ──────────────────────────────────────────────────────── */

function CurriculumTab({ courseUuid }: { courseUuid: string }) {
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedModules, setExpandedModules] = useState<Set<string>>(new Set());
  const [addingModule, setAddingModule] = useState(false);
  const [newModTitle, setNewModTitle] = useState("");
  const [editingMod, setEditingMod] = useState<string | null>(null);
  const [editModTitle, setEditModTitle] = useState("");
  const [addingSubIn, setAddingSubIn] = useState<string | null>(null);
  const [newSubTitle, setNewSubTitle] = useState("");
  const [editingSub, setEditingSub] = useState<string | null>(null);
  const [editSubTitle, setEditSubTitle] = useState("");
  const [saving, setSaving] = useState(false);
  const dragMod = useRef<number | null>(null);
  const dragSub = useRef<{ modIdx: number; subIdx: number } | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try { setModules(await api<Module[]>(`/courses/${courseUuid}/modules`)); }
    catch { setModules([]); } finally { setLoading(false); }
  }, [courseUuid]);

  useEffect(() => { load(); }, [load]);

  const toggleMod = (uuid: string) => setExpandedModules(prev => {
    const s = new Set(prev);
    s.has(uuid) ? s.delete(uuid) : s.add(uuid);
    return s;
  });

  const addModule = async () => {
    if (!newModTitle.trim()) return;
    setSaving(true);
    try {
      await api(`/courses/${courseUuid}/modules`, { method: "POST", body: JSON.stringify({ title: newModTitle.trim(), position: modules.length }) });
      setNewModTitle(""); setAddingModule(false); await load();
    } finally { setSaving(false); }
  };

  const updateModule = async (uuid: string) => {
    setSaving(true);
    try {
      await api(`/courses/${courseUuid}/modules/${uuid}`, { method: "PUT", body: JSON.stringify({ title: editModTitle }) });
      setEditingMod(null); await load();
    } finally { setSaving(false); }
  };

  const deleteModule = async (uuid: string) => {
    if (!confirm("Delete this module and all its submodules?")) return;
    await api(`/courses/${courseUuid}/modules/${uuid}`, { method: "DELETE" });
    await load();
  };

  const addSubmodule = async (modUuid: string) => {
    if (!newSubTitle.trim()) return;
    const mod = modules.find(m => m.uuid === modUuid);
    setSaving(true);
    try {
      await api(`/courses/${courseUuid}/modules/${modUuid}/submodules`, {
        method: "POST", body: JSON.stringify({ title: newSubTitle.trim(), position: mod?.submodules.length || 0 })
      });
      setNewSubTitle(""); setAddingSubIn(null); await load();
    } finally { setSaving(false); }
  };

  const updateSubmodule = async (modUuid: string, subUuid: string) => {
    setSaving(true);
    try {
      await api(`/courses/${courseUuid}/modules/${modUuid}/submodules/${subUuid}`, {
        method: "PUT", body: JSON.stringify({ title: editSubTitle })
      });
      setEditingSub(null); await load();
    } finally { setSaving(false); }
  };

  const deleteSubmodule = async (modUuid: string, subUuid: string) => {
    if (!confirm("Delete this submodule?")) return;
    await api(`/courses/${courseUuid}/modules/${modUuid}/submodules/${subUuid}`, { method: "DELETE" });
    await load();
  };

  const handleModDragStart = (idx: number) => { dragMod.current = idx; };
  const handleModDragOver = (e: React.DragEvent, idx: number) => {
    e.preventDefault();
    if (dragMod.current === null || dragMod.current === idx) return;
    const reordered = [...modules];
    const [moved] = reordered.splice(dragMod.current, 1);
    reordered.splice(idx, 0, moved);
    dragMod.current = idx;
    setModules(reordered);
  };
  const handleModDragEnd = async () => {
    if (dragMod.current === null) return;
    dragMod.current = null;
    await api(`/courses/${courseUuid}/modules/reorder`, {
      method: "PUT", body: JSON.stringify({ ordered_uuids: modules.map(m => m.uuid) })
    });
  };

  const handleSubDragStart = (modIdx: number, subIdx: number) => { dragSub.current = { modIdx, subIdx }; };
  const handleSubDragOver = (e: React.DragEvent, modIdx: number, subIdx: number) => {
    e.preventDefault();
    if (!dragSub.current || dragSub.current.modIdx !== modIdx || dragSub.current.subIdx === subIdx) return;
    const mods = [...modules];
    const subs = [...mods[modIdx].submodules];
    const [moved] = subs.splice(dragSub.current.subIdx, 1);
    subs.splice(subIdx, 0, moved);
    mods[modIdx] = { ...mods[modIdx], submodules: subs };
    dragSub.current.subIdx = subIdx;
    setModules(mods);
  };
  const handleSubDragEnd = async (modIdx: number, modUuid: string) => {
    if (!dragSub.current) return;
    dragSub.current = null;
    await api(`/courses/${courseUuid}/modules/${modUuid}/submodules/reorder`, {
      method: "PUT", body: JSON.stringify({ ordered_uuids: modules[modIdx].submodules.map(s => s.uuid) })
    });
  };

  if (loading) return <div style={{ textAlign: "center", padding: 60, color: "#64748b" }}><Loader2 size={28} style={{ animation: "spin 1s linear infinite" }} /></div>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 18, fontWeight: 800, color: "#0f172a" }}>Curriculum</h2>
          <p style={{ margin: "4px 0 0", color: "#64748b", fontSize: 13 }}>
            {modules.length} module{modules.length !== 1 ? "s" : ""} · Drag to reorder
          </p>
        </div>
        <button onClick={() => { setAddingModule(true); setNewModTitle(""); }} style={{
          display: "flex", alignItems: "center", gap: 7,
          padding: "10px 18px", background: "#1d4ed8", color: "#fff",
          border: "none", borderRadius: 11, fontWeight: 700, fontSize: 13, cursor: "pointer"
        }}>
          <Plus size={15} /> Add Module
        </button>
      </div>

      {/* Add module inline */}
      {addingModule && (
        <div style={{
          padding: 16, background: "#eff6ff", border: "2px solid #bfdbfe",
          borderRadius: 14, marginBottom: 16, display: "flex", gap: 10, alignItems: "center"
        }}>
          <input autoFocus value={newModTitle} onChange={e => setNewModTitle(e.target.value)}
            onKeyDown={e => e.key === "Enter" && addModule()}
            placeholder="Module title..."
            style={{ flex: 1, padding: "10px 13px", border: "1px solid #93c5fd", borderRadius: 9, fontSize: 14, outline: "none" }} />
          <button onClick={addModule} disabled={saving} style={{
            padding: "10px 18px", background: "#1d4ed8", color: "#fff", border: "none",
            borderRadius: 9, fontWeight: 700, fontSize: 13, cursor: "pointer"
          }}>{saving ? "..." : "Add"}</button>
          <button onClick={() => setAddingModule(false)} style={{
            padding: "10px 14px", background: "#fff", border: "1px solid #e2e8f0",
            borderRadius: 9, cursor: "pointer", color: "#64748b"
          }}><X size={14} /></button>
        </div>
      )}

      {modules.length === 0 && !addingModule && (
        <div style={{
          textAlign: "center", padding: 60, background: "#f8fafc",
          borderRadius: 16, border: "2px dashed #e2e8f0", color: "#94a3b8"
        }}>
          <BookOpen size={36} style={{ marginBottom: 12 }} />
          <p style={{ margin: 0, fontWeight: 600 }}>No modules yet. Click "Add Module" to start building the curriculum.</p>
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {modules.map((mod, modIdx) => (
          <div
            key={mod.uuid}
            draggable
            onDragStart={() => handleModDragStart(modIdx)}
            onDragOver={e => handleModDragOver(e, modIdx)}
            onDragEnd={handleModDragEnd}
            style={{
              background: "#fff", border: "1px solid #e2e8f0", borderRadius: 16,
              overflow: "hidden", boxShadow: "0 2px 8px rgba(0,0,0,.04)"
            }}
          >
            {/* Module header */}
            <div style={{
              display: "flex", alignItems: "center", gap: 10, padding: "14px 18px",
              background: "#f8fafc", cursor: "pointer", userSelect: "none"
            }}>
              <GripVertical size={16} style={{ color: "#cbd5e1", cursor: "grab" }} />
              <button onClick={() => toggleMod(mod.uuid)} style={{
                background: "none", border: "none", cursor: "pointer", color: "#64748b", padding: 0
              }}>
                {expandedModules.has(mod.uuid) ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
              </button>
              <span style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", minWidth: 60 }}>
                Module {modIdx + 1}
              </span>
              {editingMod === mod.uuid ? (
                <>
                  <input autoFocus value={editModTitle} onChange={e => setEditModTitle(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && updateModule(mod.uuid)}
                    style={{ flex: 1, padding: "6px 10px", border: "1px solid #93c5fd", borderRadius: 8, fontSize: 14, outline: "none" }}
                    onClick={e => e.stopPropagation()} />
                  <button onClick={e => { e.stopPropagation(); updateModule(mod.uuid); }} style={{
                    padding: "6px 12px", background: "#1d4ed8", color: "#fff",
                    border: "none", borderRadius: 8, fontWeight: 700, fontSize: 12, cursor: "pointer"
                  }}>Save</button>
                  <button onClick={e => { e.stopPropagation(); setEditingMod(null); }} style={{
                    padding: "6px 10px", background: "#f1f5f9", border: "none", borderRadius: 8, cursor: "pointer"
                  }}><X size={12} /></button>
                </>
              ) : (
                <>
                  <span onClick={() => toggleMod(mod.uuid)} style={{ flex: 1, fontSize: 15, fontWeight: 700, color: "#0f172a" }}>{mod.title}</span>
                  <span style={{ fontSize: 11, color: "#94a3b8" }}>{mod.submodules.length} topic{mod.submodules.length !== 1 ? "s" : ""}</span>
                  <button onClick={e => { e.stopPropagation(); setEditingMod(mod.uuid); setEditModTitle(mod.title); }} style={{
                    padding: "5px 10px", background: "#eff6ff", border: "none", borderRadius: 7, cursor: "pointer", color: "#1d4ed8", fontSize: 11, fontWeight: 700
                  }}>Edit</button>
                  <button onClick={e => { e.stopPropagation(); deleteModule(mod.uuid); }} style={{
                    padding: "5px 10px", background: "#fee2e2", border: "none", borderRadius: 7, cursor: "pointer", color: "#ef4444", fontSize: 11, fontWeight: 700
                  }}>Delete</button>
                </>
              )}
            </div>

            {/* Submodules */}
            {expandedModules.has(mod.uuid) && (
              <div style={{ padding: "8px 18px 14px" }}>
                {mod.submodules.map((sub, subIdx) => (
                  <div
                    key={sub.uuid}
                    draggable
                    onDragStart={() => handleSubDragStart(modIdx, subIdx)}
                    onDragOver={e => handleSubDragOver(e, modIdx, subIdx)}
                    onDragEnd={() => handleSubDragEnd(modIdx, mod.uuid)}
                    style={{
                      display: "flex", alignItems: "center", gap: 8, padding: "9px 12px",
                      background: "#f8fafc", borderRadius: 9, marginBottom: 6,
                      border: "1px solid #f1f5f9"
                    }}
                  >
                    <GripVertical size={13} style={{ color: "#cbd5e1", cursor: "grab" }} />
                    <span style={{ fontSize: 11, color: "#94a3b8", minWidth: 20 }}>{subIdx + 1}.</span>
                    {editingSub === sub.uuid ? (
                      <>
                        <input autoFocus value={editSubTitle} onChange={e => setEditSubTitle(e.target.value)}
                          onKeyDown={e => e.key === "Enter" && updateSubmodule(mod.uuid, sub.uuid)}
                          style={{ flex: 1, padding: "5px 9px", border: "1px solid #93c5fd", borderRadius: 7, fontSize: 13, outline: "none" }} />
                        <button onClick={() => updateSubmodule(mod.uuid, sub.uuid)} style={{ padding: "5px 10px", background: "#1d4ed8", color: "#fff", border: "none", borderRadius: 7, fontWeight: 700, fontSize: 11, cursor: "pointer" }}>Save</button>
                        <button onClick={() => setEditingSub(null)} style={{ padding: "5px 8px", background: "#f1f5f9", border: "none", borderRadius: 7, cursor: "pointer" }}><X size={11} /></button>
                      </>
                    ) : (
                      <>
                        <span style={{ flex: 1, fontSize: 13, color: "#334155" }}>{sub.title}</span>
                        <button onClick={() => { setEditingSub(sub.uuid); setEditSubTitle(sub.title); }} style={{ padding: "4px 9px", background: "#eff6ff", border: "none", borderRadius: 6, cursor: "pointer", color: "#1d4ed8", fontSize: 11, fontWeight: 700 }}>Edit</button>
                        <button onClick={() => deleteSubmodule(mod.uuid, sub.uuid)} style={{ padding: "4px 9px", background: "#fee2e2", border: "none", borderRadius: 6, cursor: "pointer", color: "#ef4444", fontSize: 11, fontWeight: 700 }}>Del</button>
                      </>
                    )}
                  </div>
                ))}

                {/* Add submodule */}
                {addingSubIn === mod.uuid ? (
                  <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
                    <input autoFocus value={newSubTitle} onChange={e => setNewSubTitle(e.target.value)}
                      onKeyDown={e => e.key === "Enter" && addSubmodule(mod.uuid)}
                      placeholder="Submodule title..."
                      style={{ flex: 1, padding: "8px 12px", border: "1px solid #93c5fd", borderRadius: 9, fontSize: 13, outline: "none" }} />
                    <button onClick={() => addSubmodule(mod.uuid)} style={{ padding: "8px 14px", background: "#1d4ed8", color: "#fff", border: "none", borderRadius: 9, fontWeight: 700, fontSize: 12, cursor: "pointer" }}>Add</button>
                    <button onClick={() => { setAddingSubIn(null); setNewSubTitle(""); }} style={{ padding: "8px 12px", background: "#f1f5f9", border: "none", borderRadius: 9, cursor: "pointer" }}><X size={13} /></button>
                  </div>
                ) : (
                  <button onClick={() => { setAddingSubIn(mod.uuid); setNewSubTitle(""); if (!expandedModules.has(mod.uuid)) toggleMod(mod.uuid); }} style={{
                    display: "flex", alignItems: "center", gap: 6,
                    marginTop: 6, padding: "7px 12px", background: "#f0fdf4",
                    border: "1px dashed #86efac", borderRadius: 9, color: "#16a34a",
                    fontWeight: 700, fontSize: 12, cursor: "pointer"
                  }}>
                    <Plus size={12} /> Add Submodule
                  </button>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// Temp: fix missing BookOpen import in CurriculumTab
function BookOpen({ size, style }: { size: number; style?: React.CSSProperties }) {
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={style}><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>;
}

/* ── Batches Tab ─────────────────────────────────────────────────────────── */

function BatchesTab({ courseUuid }: { courseUuid: string }) {
  const [batches, setBatches] = useState<Batch[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editUuid, setEditUuid] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const emptyForm = { name: "", start_date: "", end_date: "", application_deadline: "", max_seats: "", remaining_seats: "", time_slot: "", status: "draft" };
  const [form, setForm] = useState<Record<string, string>>(emptyForm);

  const load = useCallback(async () => {
    setLoading(true);
    try { setBatches(await api<Batch[]>(`/courses/${courseUuid}/batches`)); }
    catch { setBatches([]); } finally { setLoading(false); }
  }, [courseUuid]);

  useEffect(() => { load(); }, [load]);

  const openNew = () => { setForm(emptyForm); setEditUuid(null); setShowForm(true); };
  const openEdit = (b: Batch) => {
    setForm({
      name: b.name, start_date: b.start_date || "", end_date: b.end_date || "",
      application_deadline: b.application_deadline || "",
      max_seats: b.max_seats?.toString() || "", remaining_seats: b.remaining_seats?.toString() || "",
      time_slot: b.time_slot || "", status: b.status
    });
    setEditUuid(b.uuid); setShowForm(true);
  };

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        ...form,
        max_seats: form.max_seats ? parseInt(form.max_seats) : null,
        remaining_seats: form.remaining_seats ? parseInt(form.remaining_seats) : null,
      };
      if (editUuid) {
        await api(`/courses/${courseUuid}/batches/${editUuid}`, { method: "PUT", body: JSON.stringify(payload) });
      } else {
        await api(`/courses/${courseUuid}/batches`, { method: "POST", body: JSON.stringify(payload) });
      }
      setShowForm(false); await load();
    } catch (e: unknown) { alert(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };

  const deleteBatch = async (uuid: string) => {
    if (!confirm("Delete this batch?")) return;
    await api(`/courses/${courseUuid}/batches/${uuid}`, { method: "DELETE" });
    await load();
  };

  const STATUS_COLORS: Record<string, string> = {
    draft: "#f1f5f9", published: "#dbeafe", upcoming: "#fef3c7",
    active: "#d1fae5", batch_full: "#fee2e2", applications_closed: "#f3e8ff",
    expired: "#f1f5f9", hidden: "#f1f5f9"
  };
  const STATUS_TEXT: Record<string, string> = {
    draft: "#475569", published: "#1d4ed8", upcoming: "#92400e",
    active: "#065f46", batch_full: "#991b1b", applications_closed: "#6d28d9",
    expired: "#475569", hidden: "#475569"
  };

  if (loading) return <div style={{ textAlign: "center", padding: 60 }}><Loader2 size={28} style={{ animation: "spin 1s linear infinite", color: "#64748b" }} /></div>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <h2 style={{ margin: 0, fontSize: 18, fontWeight: 800, color: "#0f172a" }}>Batches</h2>
        <button onClick={openNew} style={{
          display: "flex", alignItems: "center", gap: 7,
          padding: "10px 18px", background: "#1d4ed8", color: "#fff",
          border: "none", borderRadius: 11, fontWeight: 700, fontSize: 13, cursor: "pointer"
        }}><Plus size={15} /> Add Batch</button>
      </div>

      {batches.length === 0 && !showForm && (
        <div style={{ textAlign: "center", padding: 60, background: "#f8fafc", borderRadius: 16, border: "2px dashed #e2e8f0" }}>
          <p style={{ color: "#94a3b8", fontWeight: 600 }}>No batches yet. Create a batch to accept applications.</p>
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {batches.map(b => (
          <div key={b.uuid} style={{
            background: "#fff", border: "1px solid #e2e8f0", borderRadius: 14,
            padding: "18px 20px", display: "flex", gap: 16, alignItems: "flex-start"
          }}>
            <div style={{ flex: 1 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6 }}>
                <span style={{ fontWeight: 800, fontSize: 15, color: "#0f172a" }}>{b.name}</span>
                <span style={{
                  padding: "3px 10px", borderRadius: 999, fontSize: 11, fontWeight: 700,
                  background: STATUS_COLORS[b.status] || "#f1f5f9",
                  color: STATUS_TEXT[b.status] || "#475569"
                }}>{b.status.replace("_", " ")}</span>
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 16, fontSize: 12, color: "#64748b" }}>
                {b.start_date && <span>📅 Starts: <strong>{b.start_date}</strong></span>}
                {b.end_date && <span>🏁 Ends: <strong>{b.end_date}</strong></span>}
                {b.application_deadline && <span>⏰ Deadline: <strong>{b.application_deadline}</strong></span>}
                {b.time_slot && <span>🕐 Slot: <strong>{b.time_slot}</strong></span>}
                {b.max_seats != null && <span>💺 Seats: <strong>{b.remaining_seats ?? b.max_seats}/{b.max_seats}</strong></span>}
              </div>
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={() => openEdit(b)} style={{ padding: "8px 14px", background: "#eff6ff", border: "none", borderRadius: 9, cursor: "pointer", color: "#1d4ed8", fontWeight: 700, fontSize: 12 }}>Edit</button>
              <button onClick={() => deleteBatch(b.uuid)} style={{ padding: "8px 14px", background: "#fee2e2", border: "none", borderRadius: 9, cursor: "pointer", color: "#ef4444", fontWeight: 700, fontSize: 12 }}>Delete</button>
            </div>
          </div>
        ))}
      </div>

      {/* Batch form modal */}
      {showForm && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000, padding: 20 }}>
          <div style={{ background: "#fff", borderRadius: 20, width: "100%", maxWidth: 560, maxHeight: "90vh", overflow: "auto", padding: 28 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 20 }}>
              <h3 style={{ margin: 0, fontSize: 17, fontWeight: 800 }}>{editUuid ? "Edit Batch" : "New Batch"}</h3>
              <button onClick={() => setShowForm(false)} style={{ background: "none", border: "none", cursor: "pointer" }}><X size={18} /></button>
            </div>
            <div style={{ display: "grid", gap: 14 }}>
              {[["name", "Batch Name", "text"], ["start_date", "Start Date", "date"], ["end_date", "End Date", "date"], ["application_deadline", "Application Deadline", "date"], ["max_seats", "Max Seats", "number"], ["remaining_seats", "Remaining Seats", "number"]].map(([k, lbl, t]) => (
                <div key={k}>
                  <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>{lbl}</label>
                  <input type={t} value={form[k] || ""} onChange={e => setForm(p => ({ ...p, [k]: e.target.value }))}
                    style={{ width: "100%", padding: "9px 12px", border: "1px solid #d1d5db", borderRadius: 9, fontSize: 13, outline: "none", boxSizing: "border-box" }} />
                </div>
              ))}
              <div>
                <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>Time Slot</label>
                <select value={form.time_slot} onChange={e => setForm(p => ({ ...p, time_slot: e.target.value }))}
                  style={{ width: "100%", padding: "9px 12px", border: "1px solid #d1d5db", borderRadius: 9, fontSize: 13, outline: "none", background: "#fff" }}>
                  <option value="">— None —</option>
                  {TIME_SLOTS.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>Status</label>
                <select value={form.status} onChange={e => setForm(p => ({ ...p, status: e.target.value }))}
                  style={{ width: "100%", padding: "9px 12px", border: "1px solid #d1d5db", borderRadius: 9, fontSize: 13, outline: "none", background: "#fff" }}>
                  {BATCH_STATUSES.map(s => <option key={s} value={s}>{s.replace("_", " ")}</option>)}
                </select>
              </div>
            </div>
            <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
              <button onClick={() => setShowForm(false)} style={{ flex: 1, padding: 12, background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 11, fontWeight: 700, cursor: "pointer" }}>Cancel</button>
              <button onClick={save} disabled={saving} style={{ flex: 2, padding: 12, background: "#1d4ed8", color: "#fff", border: "none", borderRadius: 11, fontWeight: 700, cursor: "pointer" }}>
                {saving ? "Saving..." : editUuid ? "Update Batch" : "Create Batch"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ── Applications Tab ────────────────────────────────────────────────────── */

function ApplicationsTab({ courseUuid }: { courseUuid: string }) {
  const [apps, setApps] = useState<Application[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [selected, setSelected] = useState<Application | null>(null);
  const [updating, setUpdating] = useState(false);

  const load = useCallback(async (q = "", s = "") => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page: "1", page_size: "100" });
      if (q) params.set("search", q);
      if (s) params.set("status", s);
      const data = await api<{ items: Application[]; total: number }>(`/courses/${courseUuid}/applications?${params}`);
      setApps(data.items); setTotal(data.total);
    } catch { setApps([]); } finally { setLoading(false); }
  }, [courseUuid]);

  useEffect(() => { load(); }, [load]);

  const updateStatus = async (uuid: string, status: string) => {
    setUpdating(true);
    try {
      await api(`/courses/${courseUuid}/applications/${uuid}`, { method: "PUT", body: JSON.stringify({ status }) });
      setApps(prev => prev.map(a => a.uuid === uuid ? { ...a, status } : a));
      if (selected?.uuid === uuid) setSelected(prev => prev ? { ...prev, status } : null);
    } finally { setUpdating(false); }
  };

  const exportCSV = () => {
    const headers = ["Name", "Email", "Phone", "College", "Degree", "Year", "Status", "Applied At"];
    const rows = apps.map(a => [a.full_name, a.email, a.phone || "", a.college || "", a.degree || "", a.current_year || "", a.status, new Date(a.created_at).toLocaleDateString()]);
    const csv = [headers, ...rows].map(r => r.map(c => `"${c}"`).join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = `applications-${courseUuid}.csv`; a.click();
    URL.revokeObjectURL(url);
  };

  if (loading) return <div style={{ textAlign: "center", padding: 60 }}><Loader2 size={28} style={{ animation: "spin 1s linear infinite", color: "#64748b" }} /></div>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <div>
          <h2 style={{ margin: 0, fontSize: 18, fontWeight: 800, color: "#0f172a" }}>Applications</h2>
          <p style={{ margin: "4px 0 0", color: "#64748b", fontSize: 13 }}>{total} application{total !== 1 ? "s" : ""}</p>
        </div>
        {apps.length > 0 && (
          <button onClick={exportCSV} style={{ display: "flex", alignItems: "center", gap: 6, padding: "9px 16px", background: "#f1f5f9", border: "1px solid #e2e8f0", borderRadius: 10, fontWeight: 700, fontSize: 12, cursor: "pointer" }}>
            <Download size={14} /> Export CSV
          </button>
        )}
      </div>

      {/* Filters */}
      <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
        <div style={{ position: "relative", flex: 1 }}>
          <Search size={14} style={{ position: "absolute", left: 11, top: "50%", transform: "translateY(-50%)", color: "#94a3b8" }} />
          <input value={search} onChange={e => setSearch(e.target.value)} onKeyDown={e => e.key === "Enter" && load(search, statusFilter)}
            placeholder="Search by name or email..." style={{ width: "100%", padding: "9px 12px 9px 32px", border: "1px solid #e2e8f0", borderRadius: 10, fontSize: 13, outline: "none", boxSizing: "border-box" }} />
        </div>
        <select value={statusFilter} onChange={e => { setStatusFilter(e.target.value); load(search, e.target.value); }}
          style={{ padding: "9px 12px", border: "1px solid #e2e8f0", borderRadius: 10, fontSize: 13, outline: "none", background: "#fff" }}>
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
        <button onClick={() => load(search, statusFilter)} style={{ padding: "9px 16px", background: "#1d4ed8", color: "#fff", border: "none", borderRadius: 10, fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Search</button>
      </div>

      {apps.length === 0 ? (
        <div style={{ textAlign: "center", padding: 60, background: "#f8fafc", borderRadius: 16, border: "2px dashed #e2e8f0" }}>
          <p style={{ color: "#94a3b8", fontWeight: 600, margin: 0 }}>No applications yet.</p>
        </div>
      ) : (
        <div style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 16, overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#f8fafc" }}>
                {["Name", "Email", "College", "Status", "Applied", "Actions"].map(h => (
                  <th key={h} style={{ padding: "12px 16px", textAlign: "left", fontSize: 11, fontWeight: 800, color: "#64748b", textTransform: "uppercase", letterSpacing: ".04em" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {apps.map((app, i) => {
                const sc = APP_STATUS_COLORS[app.status] || { bg: "#f1f5f9", color: "#475569" };
                return (
                  <tr key={app.uuid} style={{ borderTop: "1px solid #f1f5f9", background: i % 2 ? "#fafafa" : "#fff" }}>
                    <td style={{ padding: "12px 16px" }}>
                      <button onClick={() => setSelected(app)} style={{ background: "none", border: "none", cursor: "pointer", fontWeight: 700, fontSize: 13, color: "#1d4ed8", textAlign: "left" }}>
                        {app.full_name}
                      </button>
                    </td>
                    <td style={{ padding: "12px 16px", fontSize: 13, color: "#475569" }}>{app.email}</td>
                    <td style={{ padding: "12px 16px", fontSize: 13, color: "#475569" }}>{app.college || "—"}</td>
                    <td style={{ padding: "12px 16px" }}>
                      <Pill text={app.status} bg={sc.bg} color={sc.color} />
                    </td>
                    <td style={{ padding: "12px 16px", fontSize: 12, color: "#94a3b8" }}>{new Date(app.created_at).toLocaleDateString()}</td>
                    <td style={{ padding: "12px 16px" }}>
                      <div style={{ display: "flex", gap: 6 }}>
                        {app.status !== "approved" && <button onClick={() => updateStatus(app.uuid, "approved")} disabled={updating} style={{ padding: "5px 10px", background: "#d1fae5", border: "none", borderRadius: 7, color: "#065f46", fontWeight: 700, fontSize: 11, cursor: "pointer" }}>Approve</button>}
                        {app.status !== "rejected" && <button onClick={() => updateStatus(app.uuid, "rejected")} disabled={updating} style={{ padding: "5px 10px", background: "#fee2e2", border: "none", borderRadius: 7, color: "#991b1b", fontWeight: 700, fontSize: 11, cursor: "pointer" }}>Reject</button>}
                        {app.status !== "pending" && <button onClick={() => updateStatus(app.uuid, "pending")} disabled={updating} style={{ padding: "5px 10px", background: "#fef3c7", border: "none", borderRadius: 7, color: "#92400e", fontWeight: 700, fontSize: 11, cursor: "pointer" }}>Pending</button>}
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Detail modal */}
      {selected && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000, padding: 20 }}>
          <div style={{ background: "#fff", borderRadius: 20, width: "100%", maxWidth: 520, maxHeight: "90vh", overflow: "auto", padding: 28 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 20 }}>
              <h3 style={{ margin: 0, fontSize: 17, fontWeight: 800 }}>{selected.full_name}</h3>
              <button onClick={() => setSelected(null)} style={{ background: "none", border: "none", cursor: "pointer" }}><X size={18} /></button>
            </div>
            {Object.entries({
              Email: selected.email, Phone: selected.phone || "—", College: selected.college || "—",
              Degree: selected.degree || "—", "Current Year": selected.current_year || "—",
              LinkedIn: selected.linkedin_url || "—", GitHub: selected.github_url || "—",
            }).map(([k, v]) => (
              <div key={k} style={{ display: "flex", gap: 12, marginBottom: 10, fontSize: 13 }}>
                <span style={{ minWidth: 100, fontWeight: 700, color: "#374151" }}>{k}</span>
                <span style={{ color: "#64748b" }}>{v}</span>
              </div>
            ))}
            {selected.motivation && (
              <div style={{ marginTop: 12, padding: 14, background: "#f8fafc", borderRadius: 12 }}>
                <p style={{ margin: "0 0 6px", fontWeight: 700, fontSize: 12, color: "#374151" }}>Why this course?</p>
                <p style={{ margin: 0, fontSize: 13, color: "#475569", lineHeight: 1.6 }}>{selected.motivation}</p>
              </div>
            )}
            {selected.resume_url && (
              <a href={selected.resume_url} target="_blank" rel="noopener noreferrer" style={{ display: "flex", alignItems: "center", gap: 6, marginTop: 14, padding: "9px 14px", background: "#eff6ff", border: "1px solid #bfdbfe", borderRadius: 10, color: "#1d4ed8", fontWeight: 700, fontSize: 13, textDecoration: "none" }}>
                <Download size={14} /> Download Resume
              </a>
            )}
            <div style={{ display: "flex", gap: 8, marginTop: 20 }}>
              {["pending", "approved", "rejected"].map(s => (
                <button key={s} onClick={() => updateStatus(selected.uuid, s)} disabled={updating || selected.status === s}
                  style={{
                    flex: 1, padding: "10px", border: "none", borderRadius: 10, fontWeight: 700, fontSize: 12, cursor: "pointer",
                    background: selected.status === s ? (APP_STATUS_COLORS[s]?.bg || "#f1f5f9") : "#f8fafc",
                    color: selected.status === s ? (APP_STATUS_COLORS[s]?.color || "#475569") : "#64748b",
                    opacity: updating ? .6 : 1
                  }}>
                  {s.charAt(0).toUpperCase() + s.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ── SEO Tab ─────────────────────────────────────────────────────────────── */

function SeoTab({ course, onSaved }: { course: Course; onSaved: (c: Course) => void }) {
  const [slug, setSlug] = useState(course.slug || "");
  const [saving, setSaving] = useState(false);

  const save = async () => {
    setSaving(true);
    try {
      const updated = await api<Course>(`/courses/${course.uuid}`, { method: "PUT", body: JSON.stringify({ slug }) });
      onSaved(updated); alert("Slug updated!");
    } catch (e: unknown) { alert(e instanceof Error ? e.message : "Save failed"); }
    finally { setSaving(false); }
  };

  return (
    <div>
      <h2 style={{ margin: "0 0 20px", fontSize: 18, fontWeight: 800, color: "#0f172a" }}>SEO & Slug</h2>
      <FieldRow label="URL Slug">
        <div>
          <Input value={slug} onChange={setSlug} placeholder="course-slug" />
          <p style={{ margin: "6px 0 0", fontSize: 11, color: "#94a3b8" }}>
            Public URL: /course/<strong>{slug || "[slug]"}</strong>
          </p>
        </div>
      </FieldRow>
      <div style={{ marginTop: 20 }}>
        <button onClick={save} disabled={saving} style={{
          padding: "11px 22px", background: "#1d4ed8", color: "#fff", border: "none",
          borderRadius: 11, fontWeight: 700, fontSize: 13, cursor: "pointer"
        }}>{saving ? "Saving..." : "Update Slug"}</button>
      </div>
    </div>
  );
}

/* ── Settings Tab ────────────────────────────────────────────────────────── */

function SettingsTab({ course, onSaved }: { course: Course; onSaved: (c: Course) => void }) {
  const router = useRouter();
  const [published, setPublished] = useState(course.is_published);
  const [active, setActive] = useState(course.is_active);
  const [comingSoon, setComingSoon] = useState(course.is_coming_soon);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const save = async () => {
    setSaving(true);
    try {
      const updated = await api<Course>(`/courses/${course.uuid}`, {
        method: "PUT", body: JSON.stringify({ is_published: published, is_active: active, is_coming_soon: comingSoon })
      });
      onSaved(updated);
    } finally { setSaving(false); }
  };

  const deleteCourse = async () => {
    if (!confirm(`Permanently delete "${course.title}"? This cannot be undone.`)) return;
    setDeleting(true);
    try {
      await api(`/courses/${course.uuid}`, { method: "DELETE" });
      router.push("/admin/courses");
    } finally { setDeleting(false); }
  };

  return (
    <div>
      <h2 style={{ margin: "0 0 20px", fontSize: 18, fontWeight: 800, color: "#0f172a" }}>Course Settings</h2>
      <div style={{ background: "#fff", border: "1px solid #e2e8f0", borderRadius: 16, padding: 24, marginBottom: 20 }}>
        {[["Published", "Make this course visible on the public website", published, setPublished],
          ["Active", "Allow applications and enrollment", active, setActive],
          ["Coming Soon", "Show as coming soon instead of open", comingSoon, setComingSoon]
        ].map(([lbl, desc, val, setVal]) => (
          <div key={lbl as string} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 0", borderBottom: "1px solid #f1f5f9" }}>
            <div>
              <p style={{ margin: 0, fontWeight: 700, fontSize: 14, color: "#0f172a" }}>{lbl as string}</p>
              <p style={{ margin: "3px 0 0", fontSize: 12, color: "#64748b" }}>{desc as string}</p>
            </div>
            <label style={{ position: "relative", display: "inline-block", width: 44, height: 24, cursor: "pointer" }}>
              <input type="checkbox" checked={val as boolean} onChange={e => (setVal as (v: boolean) => void)(e.target.checked)} style={{ display: "none" }} />
              <div style={{
                position: "absolute", inset: 0, borderRadius: 999, transition: ".2s",
                background: (val as boolean) ? "#1d4ed8" : "#d1d5db"
              }} />
              <div style={{
                position: "absolute", top: 2, left: (val as boolean) ? 22 : 2, width: 20, height: 20,
                background: "#fff", borderRadius: "50%", transition: ".2s",
                boxShadow: "0 1px 3px rgba(0,0,0,.2)"
              }} />
            </label>
          </div>
        ))}
        <div style={{ marginTop: 20 }}>
          <button onClick={save} disabled={saving} style={{ padding: "11px 22px", background: "#1d4ed8", color: "#fff", border: "none", borderRadius: 11, fontWeight: 700, fontSize: 13, cursor: "pointer" }}>
            {saving ? "Saving..." : "Save Settings"}
          </button>
        </div>
      </div>

      {/* Danger zone */}
      <div style={{ background: "#fff", border: "1px solid #fecaca", borderRadius: 16, padding: 24 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
          <AlertCircle size={16} style={{ color: "#ef4444" }} />
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 800, color: "#ef4444" }}>Danger Zone</h3>
        </div>
        <p style={{ margin: "0 0 16px", fontSize: 13, color: "#64748b" }}>
          Deleting this course will permanently remove all modules, submodules, batches, and applications.
        </p>
        <button onClick={deleteCourse} disabled={deleting} style={{
          padding: "10px 20px", background: "#ef4444", color: "#fff", border: "none",
          borderRadius: 10, fontWeight: 700, fontSize: 13, cursor: "pointer"
        }}>
          {deleting ? "Deleting..." : "Delete Course Permanently"}
        </button>
      </div>
    </div>
  );
}

/* ── Main Page ───────────────────────────────────────────────────────────── */

export default function CourseManagementPage() {
  const { uuid } = useParams<{ uuid: string }>();
  const router = useRouter();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<Tab>("overview");

  useEffect(() => {
    api<Course>(`/courses/${uuid}`)
      .then(setCourse)
      .catch(() => router.push("/admin/courses"))
      .finally(() => setLoading(false));
  }, [uuid, router]);

  if (loading) return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", minHeight: "100vh", fontFamily: "system-ui, sans-serif" }}>
      <Loader2 size={32} style={{ animation: "spin 1s linear infinite", color: "#1d4ed8" }} />
      <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </div>
  );

  if (!course) return null;

  return (
    <div style={{ minHeight: "100vh", background: "#f8fafc", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ background: "#fff", borderBottom: "1px solid #e2e8f0", padding: "0 32px" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "16px 0 0" }}>
            <Link href="/admin/courses" style={{ display: "flex", alignItems: "center", gap: 5, color: "#64748b", fontSize: 12, textDecoration: "none", fontWeight: 700 }}>
              <ArrowLeft size={14} /> Courses
            </Link>
            <span style={{ color: "#cbd5e1" }}>/</span>
            <span style={{ fontSize: 12, color: "#1e293b", fontWeight: 700 }}>{course.title}</span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0 0" }}>
            <div>
              <h1 style={{ margin: 0, fontSize: 22, fontWeight: 800, color: "#0f172a" }}>{course.title}</h1>
              <div style={{ display: "flex", gap: 8, marginTop: 6 }}>
                <span style={{
                  padding: "3px 10px", borderRadius: 999, fontSize: 11, fontWeight: 700,
                  background: course.is_published ? "#d1fae5" : "#f1f5f9",
                  color: course.is_published ? "#065f46" : "#475569"
                }}>{course.is_published ? "Published" : "Draft"}</span>
                {course.slug && <span style={{ fontSize: 11, color: "#94a3b8" }}>/course/{course.slug}</span>}
              </div>
            </div>
            <a href={`/course/${course.slug}`} target="_blank" rel="noopener noreferrer" style={{
              display: "flex", alignItems: "center", gap: 6,
              padding: "9px 16px", background: "#f8fafc", border: "1px solid #e2e8f0",
              borderRadius: 10, color: "#475569", fontWeight: 700, fontSize: 12, textDecoration: "none"
            }}>
              <Eye size={13} /> Preview
            </a>
          </div>

          {/* Tabs */}
          <div style={{ display: "flex", gap: 2, marginTop: 16 }}>
            {TABS.map(tab => (
              <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
                padding: "10px 18px", background: "none", border: "none", cursor: "pointer",
                fontSize: 13, fontWeight: 700,
                color: activeTab === tab.id ? "#1d4ed8" : "#64748b",
                borderBottom: activeTab === tab.id ? "2px solid #1d4ed8" : "2px solid transparent",
                transition: "color .15s"
              }}>{tab.label}</button>
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "28px 32px" }}>
        {activeTab === "overview" && <OverviewTab course={course} onSaved={setCourse} />}
        {activeTab === "curriculum" && <CurriculumTab courseUuid={course.uuid} />}
        {activeTab === "batches" && <BatchesTab courseUuid={course.uuid} />}
        {activeTab === "applications" && <ApplicationsTab courseUuid={course.uuid} />}
        {activeTab === "seo" && <SeoTab course={course} onSaved={setCourse} />}
        {activeTab === "settings" && <SettingsTab course={course} onSaved={setCourse} />}
      </div>

      <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </div>
  );
}
