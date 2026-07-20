"use client";

import { useState, useEffect, useRef } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  Clock, Award, ChevronDown, ChevronRight, CheckCircle,
  Users, Calendar, Loader2, X, Upload, Linkedin, Github
} from "lucide-react";
import { SiteShell } from "../../../components/site/SiteShell";
import { publicApi } from "../../../lib/public-api";

/* ── Types ───────────────────────────────────────────────────────────────── */
interface Submodule { uuid: string; title: string; description?: string; position: number; }
interface Module { uuid: string; title: string; description?: string; position: number; submodules: Submodule[]; }
interface Batch {
  uuid: string; name: string; start_date?: string; end_date?: string;
  application_deadline?: string; max_seats?: number; remaining_seats?: number;
  time_slot?: string; status: string;
}
interface Course {
  uuid: string; title: string; slug: string;
  short_description?: string; description?: string;
  thumbnail_url?: string; duration?: string; level?: string;
  price?: number; certificate_available: boolean;
  skills_covered: string[]; technologies: string[];
  learning_outcomes: string[]; career_opportunities: string[];
  faqs: { question: string; answer: string }[];
  certification?: string; is_published: boolean;
  modules: Module[]; batches: Batch[];
}

/* ── Status badge colours ────────────────────────────────────────────────── */
const BATCH_COLORS: Record<string, { bg: string; color: string; label: string }> = {
  draft:               { bg: "#f1f5f9", color: "#475569", label: "Draft" },
  published:           { bg: "#dbeafe", color: "#1d4ed8", label: "Open" },
  upcoming:            { bg: "#fef3c7", color: "#92400e", label: "Upcoming" },
  active:              { bg: "#d1fae5", color: "#065f46", label: "Active" },
  batch_full:          { bg: "#fee2e2", color: "#991b1b", label: "Full" },
  applications_closed: { bg: "#f3e8ff", color: "#6d28d9", label: "Closed" },
  expired:             { bg: "#f1f5f9", color: "#64748b", label: "Expired" },
  hidden:              { bg: "#f1f5f9", color: "#64748b", label: "Hidden" },
};

/* ── Tiny helpers ────────────────────────────────────────────────────────── */
function Chip({ text, bg = "#dbeafe", color = "#1d4ed8" }: { text: string; bg?: string; color?: string }) {
  return (
    <span style={{
      display: "inline-block", padding: "5px 14px", borderRadius: 999,
      fontSize: 12, fontWeight: 700, background: bg, color
    }}>{text}</span>
  );
}

function SectionHeading({ number, title }: { number?: string; title: string }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 22 }}>
      {number && <span style={{ fontSize: 13, fontWeight: 900, color: "#1d4ed8", minWidth: 28 }}>{number}</span>}
      <h2 style={{ margin: 0, fontSize: 22, fontWeight: 900, color: "#0f172a" }}>{title}</h2>
    </div>
  );
}

/* ── Apply Form Modal ────────────────────────────────────────────────────── */
function ApplyModal({ course, onClose }: { course: Course; onClose: () => void }) {
  const [form, setForm] = useState({
    full_name: "", email: "", phone: "", college: "", degree: "",
    current_year: "", linkedin_url: "", github_url: "", motivation: "",
    resume_url: "", batch_id: "",
  });
  const [uploading, setUploading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState("");
  const [agree, setAgree] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const set = (k: string, v: string) => setForm(p => ({ ...p, [k]: v }));

  const uploadResume = async (file: File) => {
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      fd.append("folder", "documents");
      const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      const res = await fetch(`${API}/storage/upload`, { method: "POST", body: fd });
      if (!res.ok) throw new Error("Upload failed");
      const d = await res.json();
      set("resume_url", d.url);
    } catch { alert("Resume upload failed."); } finally { setUploading(false); }
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!agree) { setError("Please accept the terms."); return; }
    if (!form.full_name || !form.email) { setError("Name and email are required."); return; }
    setSubmitting(true); setError("");
    try {
      const payload = { ...form, batch_id: form.batch_id ? parseInt(form.batch_id) : undefined };
      const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      const res = await fetch(`${API}/courses/${course.uuid}/applications`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const d = await res.json();
        throw new Error(d.detail || "Submission failed");
      }
      setDone(true);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Submission failed");
    } finally { setSubmitting(false); }
  };

  const activeBatches = course.batches.filter(b => ["published", "upcoming", "active"].includes(b.status));

  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,.6)",
      display: "flex", alignItems: "center", justifyContent: "center",
      zIndex: 1000, padding: 16, backdropFilter: "blur(4px)"
    }}>
      <div style={{
        background: "#fff", borderRadius: 24, width: "100%", maxWidth: 560,
        maxHeight: "92vh", overflow: "auto",
        boxShadow: "0 32px 80px rgba(0,0,0,.25)"
      }}>
        <div style={{
          position: "sticky", top: 0, background: "#fff", borderBottom: "1px solid #f1f5f9",
          padding: "20px 28px", display: "flex", justifyContent: "space-between", alignItems: "center",
          zIndex: 1, borderRadius: "24px 24px 0 0"
        }}>
          <div>
            <h2 style={{ margin: 0, fontSize: 18, fontWeight: 800, color: "#0f172a" }}>Apply Now</h2>
            <p style={{ margin: "3px 0 0", fontSize: 13, color: "#64748b" }}>{course.title}</p>
          </div>
          <button onClick={onClose} style={{ background: "#f1f5f9", border: "none", borderRadius: 10, padding: 8, cursor: "pointer" }}>
            <X size={18} />
          </button>
        </div>

        {done ? (
          <div style={{ padding: "60px 28px", textAlign: "center" }}>
            <div style={{
              width: 64, height: 64, background: "#d1fae5", borderRadius: "50%",
              display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 20px"
            }}>
              <CheckCircle size={32} style={{ color: "#059669" }} />
            </div>
            <h3 style={{ margin: "0 0 10px", fontSize: 20, fontWeight: 800, color: "#0f172a" }}>Application Submitted!</h3>
            <p style={{ margin: "0 0 24px", color: "#64748b", fontSize: 14, lineHeight: 1.7 }}>
              Thank you for applying to <strong>{course.title}</strong>. We'll review your application and get back to you shortly.
            </p>
            <button onClick={onClose} style={{
              padding: "12px 28px", background: "#1d4ed8", color: "#fff",
              border: "none", borderRadius: 12, fontWeight: 700, fontSize: 14, cursor: "pointer"
            }}>Close</button>
          </div>
        ) : (
          <form onSubmit={submit} style={{ padding: "24px 28px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
              {[
                ["full_name", "Full Name *", "text", "Your full name"],
                ["email", "Email *", "email", "your@email.com"],
                ["phone", "Phone Number", "tel", "+91 9999999999"],
                ["college", "College / University", "text", "Your institution"],
                ["degree", "Degree / Program", "text", "B.Tech, MBA..."],
                ["current_year", "Current Year", "text", "1st, 2nd, Final, Graduate"],
              ].map(([k, lbl, t, ph]) => (
                <div key={k} style={k === "full_name" || k === "email" ? {} : {}}>
                  <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>{lbl}</label>
                  <input type={t} value={form[k as keyof typeof form]} onChange={e => set(k, e.target.value)}
                    placeholder={ph} required={k === "full_name" || k === "email"}
                    style={{ width: "100%", padding: "10px 12px", border: "1px solid #d1d5db", borderRadius: 10, fontSize: 13, outline: "none", boxSizing: "border-box" }} />
                </div>
              ))}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginTop: 14 }}>
              <div>
                <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>LinkedIn Profile</label>
                <div style={{ position: "relative" }}>
                  <Linkedin size={13} style={{ position: "absolute", left: 11, top: "50%", transform: "translateY(-50%)", color: "#94a3b8" }} />
                  <input value={form.linkedin_url} onChange={e => set("linkedin_url", e.target.value)}
                    placeholder="linkedin.com/in/..." style={{ width: "100%", padding: "10px 12px 10px 30px", border: "1px solid #d1d5db", borderRadius: 10, fontSize: 13, outline: "none", boxSizing: "border-box" }} />
                </div>
              </div>
              <div>
                <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>GitHub Profile</label>
                <div style={{ position: "relative" }}>
                  <Github size={13} style={{ position: "absolute", left: 11, top: "50%", transform: "translateY(-50%)", color: "#94a3b8" }} />
                  <input value={form.github_url} onChange={e => set("github_url", e.target.value)}
                    placeholder="github.com/username" style={{ width: "100%", padding: "10px 12px 10px 30px", border: "1px solid #d1d5db", borderRadius: 10, fontSize: 13, outline: "none", boxSizing: "border-box" }} />
                </div>
              </div>
            </div>

            {activeBatches.length > 0 && (
              <div style={{ marginTop: 14 }}>
                <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>Preferred Batch</label>
                <select value={form.batch_id} onChange={e => set("batch_id", e.target.value)}
                  style={{ width: "100%", padding: "10px 12px", border: "1px solid #d1d5db", borderRadius: 10, fontSize: 13, outline: "none", background: "#fff" }}>
                  <option value="">— No preference —</option>
                  {activeBatches.map(b => (
                    <option key={b.uuid} value={b.uuid}>
                      {b.name}{b.start_date ? ` · ${b.start_date}` : ""}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div style={{ marginTop: 14 }}>
              <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>Why do you want to join this course?</label>
              <textarea value={form.motivation} onChange={e => set("motivation", e.target.value)}
                placeholder="Share your motivation, goals, and what you hope to achieve..." rows={4}
                style={{ width: "100%", padding: "10px 12px", border: "1px solid #d1d5db", borderRadius: 10, fontSize: 13, outline: "none", resize: "vertical", boxSizing: "border-box" }} />
            </div>

            {/* Resume upload */}
            <div style={{ marginTop: 14 }}>
              <label style={{ display: "block", fontWeight: 700, fontSize: 12, color: "#374151", marginBottom: 5 }}>Resume (PDF)</label>
              {form.resume_url ? (
                <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 14px", background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 10 }}>
                  <CheckCircle size={14} style={{ color: "#16a34a" }} />
                  <span style={{ fontSize: 12, color: "#15803d", fontWeight: 600 }}>Resume uploaded</span>
                  <button type="button" onClick={() => set("resume_url", "")} style={{ marginLeft: "auto", background: "none", border: "none", cursor: "pointer", color: "#64748b", fontSize: 12 }}>Remove</button>
                </div>
              ) : (
                <div onClick={() => fileRef.current?.click()} style={{
                  border: "2px dashed #d1d5db", borderRadius: 10, padding: "16px",
                  textAlign: "center", cursor: "pointer", color: "#94a3b8"
                }}>
                  {uploading ? <Loader2 size={18} style={{ animation: "spin 1s linear infinite" }} /> : <Upload size={18} style={{ marginBottom: 4 }} />}
                  <p style={{ margin: "4px 0 0", fontSize: 12 }}>{uploading ? "Uploading..." : "Click to upload resume"}</p>
                </div>
              )}
              <input ref={fileRef} type="file" accept=".pdf,.doc,.docx" style={{ display: "none" }}
                onChange={e => e.target.files?.[0] && uploadResume(e.target.files[0])} />
            </div>

            {/* Terms */}
            <label style={{ display: "flex", alignItems: "flex-start", gap: 10, marginTop: 18, cursor: "pointer" }}>
              <input type="checkbox" checked={agree} onChange={e => setAgree(e.target.checked)}
                style={{ marginTop: 2, accentColor: "#1d4ed8" }} />
              <span style={{ fontSize: 12, color: "#64748b", lineHeight: 1.6 }}>
                I agree to the <Link href="/terms" style={{ color: "#1d4ed8", fontWeight: 700 }}>Terms & Conditions</Link> and <Link href="/privacy" style={{ color: "#1d4ed8", fontWeight: 700 }}>Privacy Policy</Link>. I understand my application will be reviewed by the admin team.
              </span>
            </label>

            {error && <p style={{ color: "#ef4444", fontSize: 13, margin: "12px 0 0", fontWeight: 600 }}>{error}</p>}

            <button type="submit" disabled={submitting} style={{
              width: "100%", marginTop: 20, padding: "14px",
              background: submitting ? "#93c5fd" : "linear-gradient(135deg, #1d4ed8, #3b82f6)",
              color: "#fff", border: "none", borderRadius: 14, fontWeight: 800,
              fontSize: 15, cursor: submitting ? "not-allowed" : "pointer",
              display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
              boxShadow: "0 8px 24px rgba(29,78,216,.3)"
            }}>
              {submitting ? <><Loader2 size={16} style={{ animation: "spin 1s linear infinite" }} /> Submitting...</> : "Submit Application →"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

/* ── Main Detail Page ────────────────────────────────────────────────────── */
export default function CourseDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);
  const [openModules, setOpenModules] = useState<Set<string>>(new Set());
  const [openFaqs, setOpenFaqs] = useState<Set<number>>(new Set());
  const [showApply, setShowApply] = useState(false);

  useEffect(() => {
    publicApi<Course>(`/courses/slug/${slug}`)
      .then(data => { setCourse(data); setOpenModules(new Set([data.modules?.[0]?.uuid || ""])); })
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false));
  }, [slug]);

  const toggleMod = (uuid: string) => setOpenModules(prev => {
    const s = new Set(prev);
    s.has(uuid) ? s.delete(uuid) : s.add(uuid);
    return s;
  });

  const toggleFaq = (i: number) => setOpenFaqs(prev => {
    const s = new Set(prev);
    s.has(i) ? s.delete(i) : s.add(i);
    return s;
  });

  if (loading) return (
    <SiteShell>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: "120px 0", color: "#64748b" }}>
        <Loader2 size={32} style={{ animation: "spin 1s linear infinite" }} />
        <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
      </div>
    </SiteShell>
  );

  if (notFound || !course) return (
    <SiteShell>
      <div style={{ textAlign: "center", padding: "100px 24px", color: "#64748b" }}>
        <h1 style={{ fontSize: 32, fontWeight: 900, color: "#0f172a", marginBottom: 12 }}>Course Not Found</h1>
        <p style={{ marginBottom: 28 }}>This course doesn't exist or is no longer available.</p>
        <Link href="/courses" style={{ padding: "12px 24px", background: "#1d4ed8", color: "#fff", borderRadius: 12, fontWeight: 700, fontSize: 14, textDecoration: "none" }}>
          Browse All Courses
        </Link>
      </div>
    </SiteShell>
  );

  const activeBatches = course.batches.filter(b => ["published", "upcoming", "active"].includes(b.status));
  const totalTopics = course.modules.reduce((s, m) => s + m.submodules.length, 0);

  return (
    <SiteShell>
      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section style={{
        background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%)",
        color: "#fff", padding: "52px 24px 48px"
      }}>
        <div className="wrap" style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 40, alignItems: "center" }}>
          <div>
            <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
              {course.level && <Chip text={course.level} bg="#1e3a5f" color="#93c5fd" />}
              {course.certificate_available && <Chip text="Certificate" bg="#14532d" color="#86efac" />}
            </div>
            <h1 style={{ margin: "0 0 16px", fontSize: "clamp(1.8rem,4vw,2.8rem)", fontWeight: 900, lineHeight: 1.1 }}>{course.title}</h1>
            {course.short_description && (
              <p style={{ margin: "0 0 24px", fontSize: 16, color: "#bfdbfe", lineHeight: 1.7, maxWidth: 600 }}>{course.short_description}</p>
            )}
            <div style={{ display: "flex", gap: 20, flexWrap: "wrap", fontSize: 13, color: "#93c5fd" }}>
              {course.duration && <span style={{ display: "flex", alignItems: "center", gap: 6 }}><Clock size={14} /> {course.duration}</span>}
              {course.modules.length > 0 && <span style={{ display: "flex", alignItems: "center", gap: 6 }}><Users size={14} /> {course.modules.length} Modules · {totalTopics} Topics</span>}
            </div>
          </div>
          {course.thumbnail_url && (
            <img src={course.thumbnail_url} alt={course.title} style={{
              width: 280, height: 190, objectFit: "cover", borderRadius: 16,
              boxShadow: "0 24px 60px rgba(0,0,0,.4)", flexShrink: 0
            }} />
          )}
        </div>
      </section>

      {/* ── Body ──────────────────────────────────────────────────────── */}
      <div className="wrap" style={{ padding: "48px 24px", display: "grid", gridTemplateColumns: "1fr 320px", gap: 40, alignItems: "start" }}>
        {/* Left column */}
        <div>
          {/* About */}
          {course.description && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="About This Course" />
              <div style={{ fontSize: 15, color: "#374151", lineHeight: 1.8 }} dangerouslySetInnerHTML={{ __html: course.description.replace(/\n/g, "<br/>") }} />
            </section>
          )}

          {/* Learning Outcomes */}
          {course.learning_outcomes?.length > 0 && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="What You'll Learn" />
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: 12 }}>
                {course.learning_outcomes.map((o, i) => (
                  <div key={i} style={{ display: "flex", gap: 10, alignItems: "flex-start", padding: "12px 14px", background: "#f0fdf4", border: "1px solid #bbf7d0", borderRadius: 12 }}>
                    <CheckCircle size={15} style={{ color: "#16a34a", flexShrink: 0, marginTop: 2 }} />
                    <span style={{ fontSize: 13, color: "#15803d", lineHeight: 1.5 }}>{o}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Skills */}
          {course.skills_covered?.length > 0 && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="Skills You'll Build" />
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {course.skills_covered.map((s, i) => (
                  <Chip key={i} text={s} bg="#dbeafe" color="#1e40af" />
                ))}
              </div>
            </section>
          )}

          {/* Technologies */}
          {course.technologies?.length > 0 && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="Technologies & Tools" />
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {course.technologies.map((t, i) => (
                  <span key={i} style={{
                    padding: "8px 16px", background: "#fff", border: "1px solid #e2e8f0",
                    borderRadius: 10, fontSize: 13, fontWeight: 700, color: "#374151"
                  }}>{t}</span>
                ))}
              </div>
            </section>
          )}

          {/* Curriculum */}
          {course.modules?.length > 0 && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="Course Curriculum" />
              <p style={{ margin: "0 0 20px", fontSize: 13, color: "#64748b" }}>
                {course.modules.length} modules · {totalTopics} topics
              </p>
              <div style={{ border: "1px solid #e2e8f0", borderRadius: 16, overflow: "hidden" }}>
                {course.modules.map((mod, modIdx) => (
                  <div key={mod.uuid} style={{ borderTop: modIdx > 0 ? "1px solid #f1f5f9" : undefined }}>
                    <button onClick={() => toggleMod(mod.uuid)} style={{
                      width: "100%", display: "flex", alignItems: "center", gap: 14,
                      padding: "18px 22px", background: openModules.has(mod.uuid) ? "#f8fafc" : "#fff",
                      border: "none", cursor: "pointer", textAlign: "left"
                    }}>
                      <div style={{
                        width: 28, height: 28, borderRadius: "50%", background: "#dbeafe",
                        color: "#1d4ed8", fontSize: 12, fontWeight: 800, display: "flex",
                        alignItems: "center", justifyContent: "center", flexShrink: 0
                      }}>{modIdx + 1}</div>
                      <span style={{ flex: 1, fontWeight: 700, fontSize: 15, color: "#0f172a" }}>{mod.title}</span>
                      <span style={{ fontSize: 12, color: "#94a3b8", marginRight: 8 }}>{mod.submodules.length} topics</span>
                      {openModules.has(mod.uuid) ? <ChevronDown size={16} style={{ color: "#94a3b8" }} /> : <ChevronRight size={16} style={{ color: "#94a3b8" }} />}
                    </button>
                    {openModules.has(mod.uuid) && mod.submodules.length > 0 && (
                      <div style={{ background: "#f8fafc", borderTop: "1px solid #f1f5f9", padding: "8px 22px 14px 66px" }}>
                        {mod.submodules.map((sub, si) => (
                          <div key={sub.uuid} style={{
                            display: "flex", alignItems: "center", gap: 10,
                            padding: "8px 0", borderTop: si > 0 ? "1px solid #f1f5f9" : undefined
                          }}>
                            <span style={{ fontSize: 11, color: "#94a3b8", minWidth: 18 }}>{si + 1}.</span>
                            <span style={{ fontSize: 13, color: "#374151" }}>{sub.title}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Certificate */}
          {course.certificate_available && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="Certificate" />
              <div style={{
                display: "flex", gap: 16, alignItems: "center", padding: "20px 24px",
                background: "linear-gradient(120deg, #fef3c7, #fef9ec)", border: "1px solid #fde68a",
                borderRadius: 16
              }}>
                <Award size={36} style={{ color: "#d97706", flexShrink: 0 }} />
                <div>
                  <p style={{ margin: "0 0 4px", fontWeight: 800, fontSize: 15, color: "#92400e" }}>Certificate of Completion</p>
                  <p style={{ margin: 0, fontSize: 13, color: "#78350f", lineHeight: 1.6 }}>
                    {course.certification || "Earn a recognized certificate upon successfully completing this program."}
                  </p>
                </div>
              </div>
            </section>
          )}

          {/* Career */}
          {course.career_opportunities?.length > 0 && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="Career Opportunities" />
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {course.career_opportunities.map((c, i) => (
                  <Chip key={i} text={c} bg="#f0fdf4" color="#166534" />
                ))}
              </div>
            </section>
          )}

          {/* FAQs */}
          {course.faqs?.length > 0 && (
            <section style={{ marginBottom: 48 }}>
              <SectionHeading title="Frequently Asked Questions" />
              <div style={{ border: "1px solid #e2e8f0", borderRadius: 16, overflow: "hidden" }}>
                {course.faqs.map((faq, i) => (
                  <div key={i} style={{ borderTop: i > 0 ? "1px solid #f1f5f9" : undefined }}>
                    <button onClick={() => toggleFaq(i)} style={{
                      width: "100%", display: "flex", alignItems: "center", justifyContent: "space-between",
                      padding: "18px 22px", background: openFaqs.has(i) ? "#f8fafc" : "#fff",
                      border: "none", cursor: "pointer", textAlign: "left"
                    }}>
                      <span style={{ fontWeight: 700, fontSize: 14, color: "#0f172a", paddingRight: 16 }}>{faq.question}</span>
                      {openFaqs.has(i) ? <ChevronDown size={16} style={{ color: "#94a3b8", flexShrink: 0 }} /> : <ChevronRight size={16} style={{ color: "#94a3b8", flexShrink: 0 }} />}
                    </button>
                    {openFaqs.has(i) && (
                      <div style={{ padding: "0 22px 18px", fontSize: 14, color: "#475569", lineHeight: 1.7, background: "#f8fafc", borderTop: "1px solid #f1f5f9" }}>
                        {faq.answer}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>

        {/* ── Right sticky sidebar ─────────────────────────────────── */}
        <div style={{ position: "sticky", top: 100 }}>
          <div style={{
            background: "#fff", border: "1px solid #e2e8f0", borderRadius: 20,
            overflow: "hidden", boxShadow: "0 8px 30px rgba(0,0,0,.08)"
          }}>
            {/* CTA */}
            <div style={{ padding: "24px 24px 20px" }}>
              {course.price != null && course.price > 0 ? (
                <div style={{ marginBottom: 16 }}>
                  <span style={{ fontSize: 28, fontWeight: 900, color: "#0f172a" }}>₹{course.price.toLocaleString()}</span>
                </div>
              ) : (
                <div style={{ display: "inline-flex", padding: "4px 12px", background: "#d1fae5", borderRadius: 999, marginBottom: 16 }}>
                  <span style={{ fontSize: 12, fontWeight: 800, color: "#065f46" }}>Free Enrollment</span>
                </div>
              )}
              <button onClick={() => setShowApply(true)} style={{
                width: "100%", padding: "15px", background: "linear-gradient(135deg, #1d4ed8, #3b82f6)",
                color: "#fff", border: "none", borderRadius: 14, fontWeight: 800, fontSize: 16,
                cursor: "pointer", boxShadow: "0 8px 24px rgba(29,78,216,.3)",
                transition: "transform .15s, box-shadow .15s"
              }}
                onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.transform = "translateY(-2px)"; (e.currentTarget as HTMLButtonElement).style.boxShadow = "0 12px 32px rgba(29,78,216,.4)"; }}
                onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.transform = "none"; (e.currentTarget as HTMLButtonElement).style.boxShadow = "0 8px 24px rgba(29,78,216,.3)"; }}
              >
                Apply Now →
              </button>
              <p style={{ margin: "10px 0 0", textAlign: "center", fontSize: 11, color: "#94a3b8" }}>No payment required to apply</p>
            </div>

            {/* Quick stats */}
            <div style={{ borderTop: "1px solid #f1f5f9", padding: "16px 24px" }}>
              {[
                course.duration && ["Duration", course.duration],
                course.level && ["Level", course.level],
                course.modules.length > 0 && ["Modules", `${course.modules.length} modules, ${totalTopics} topics`],
                course.certificate_available && ["Certificate", "Included"],
              ].filter(Boolean).map((row, i) => row && (
                <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", fontSize: 13, borderTop: i > 0 ? "1px solid #f8fafc" : undefined }}>
                  <span style={{ color: "#64748b" }}>{row[0]}</span>
                  <span style={{ fontWeight: 700, color: "#0f172a" }}>{row[1]}</span>
                </div>
              ))}
            </div>

            {/* Batches */}
            {activeBatches.length > 0 && (
              <div style={{ borderTop: "1px solid #f1f5f9", padding: "16px 24px" }}>
                <p style={{ margin: "0 0 12px", fontWeight: 800, fontSize: 13, color: "#0f172a" }}>
                  <Calendar size={13} style={{ marginRight: 6, verticalAlign: "middle" }} />
                  Upcoming Batches
                </p>
                {activeBatches.map(batch => {
                  const bc = BATCH_COLORS[batch.status] || BATCH_COLORS.draft;
                  return (
                    <div key={batch.uuid} style={{ marginBottom: 10, padding: "12px 14px", background: "#f8fafc", border: "1px solid #f1f5f9", borderRadius: 12 }}>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                        <span style={{ fontWeight: 700, fontSize: 13, color: "#0f172a" }}>{batch.name}</span>
                        <span style={{ padding: "2px 8px", borderRadius: 999, fontSize: 10, fontWeight: 800, background: bc.bg, color: bc.color }}>{bc.label}</span>
                      </div>
                      <div style={{ fontSize: 12, color: "#64748b", display: "grid", gap: 3 }}>
                        {batch.start_date && <span>📅 Starts {batch.start_date}</span>}
                        {batch.application_deadline && <span>⏰ Apply by {batch.application_deadline}</span>}
                        {batch.remaining_seats != null && <span>💺 {batch.remaining_seats} seats left</span>}
                        {batch.time_slot && <span>🕐 {batch.time_slot}</span>}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <Link href="/courses" style={{ display: "block", marginTop: 12, textAlign: "center", fontSize: 12, color: "#64748b", fontWeight: 600, textDecoration: "none" }}>
            ← Back to all courses
          </Link>
        </div>
      </div>

      {showApply && course && <ApplyModal course={course} onClose={() => setShowApply(false)} />}
      <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </SiteShell>
  );
}
