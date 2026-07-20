"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Plus, BookOpen, Clock, Users, Edit2, Trash2, Eye,
  Upload, X, Loader2, Search, Tag
} from "lucide-react";
import { api } from "../../../lib/api";

interface Course {
  uuid: string;
  title: string;
  slug: string;
  short_description?: string;
  thumbnail_url?: string;
  level?: string;
  duration?: string;
  is_published: boolean;
  is_active: boolean;
  display_order: number;
  category_id?: number;
}

interface CoursePage {
  items: Course[];
  total: number;
  page: number;
  page_size: number;
}

const LEVEL_COLORS: Record<string, string> = {
  Beginner: "bg-emerald-100 text-emerald-700",
  Intermediate: "bg-amber-100 text-amber-700",
  Advanced: "bg-red-100 text-red-700",
};

export default function AdminCoursesPage() {
  const router = useRouter();
  const [courses, setCourses] = useState<Course[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState("");
  const [title, setTitle] = useState("");
  const [thumbnailUrl, setThumbnailUrl] = useState("");
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const fetchCourses = async (q = "") => {
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: "1", page_size: "50", sort: "display_order", direction: "asc",
      });
      if (q) params.set("search", q);
      const data = await api<CoursePage>(`/courses?${params}`);
      setCourses(data.items);
      setTotal(data.total);
    } catch {
      setCourses([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchCourses(); }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCourses(search);
  };

  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      const form = new FormData();
      form.append("file", file);
      form.append("folder", "images");
      const token = localStorage.getItem("talenova_access_token");
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/storage/upload`,
        { method: "POST", headers: { Authorization: `Bearer ${token}` }, body: form }
      );
      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      setThumbnailUrl(data.url);
    } catch {
      alert("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) { setCreateError("Course name is required."); return; }
    setCreating(true);
    setCreateError("");
    try {
      const course = await api<Course>("/courses", {
        method: "POST",
        body: JSON.stringify({ title: title.trim(), thumbnail_url: thumbnailUrl || undefined }),
      });
      setShowCreate(false);
      setTitle("");
      setThumbnailUrl("");
      router.push(`/admin/courses/${course.uuid}`);
    } catch (err: unknown) {
      setCreateError(err instanceof Error ? err.message : "Failed to create course.");
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (uuid: string, name: string) => {
    if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
    try {
      await api(`/courses/${uuid}`, { method: "DELETE" });
      setCourses(prev => prev.filter(c => c.uuid !== uuid));
    } catch {
      alert("Failed to delete course.");
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#f8fafc", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ background: "#fff", borderBottom: "1px solid #e2e8f0", padding: "20px 32px" }}>
        <div style={{ maxWidth: 1200, margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <Link href="/admin" style={{ color: "#64748b", fontSize: 13, textDecoration: "none" }}>← Admin</Link>
              <span style={{ color: "#cbd5e1" }}>/</span>
              <span style={{ color: "#1e293b", fontSize: 13, fontWeight: 700 }}>Courses</span>
            </div>
            <h1 style={{ margin: "4px 0 0", fontSize: 26, fontWeight: 800, color: "#0f172a" }}>
              Course Management
            </h1>
            <p style={{ margin: "4px 0 0", color: "#64748b", fontSize: 13 }}>
              {total} course{total !== 1 ? "s" : ""} · Click a card to manage curriculum, batches & applications
            </p>
          </div>
          <button
            onClick={() => { setShowCreate(true); setCreateError(""); setTitle(""); setThumbnailUrl(""); }}
            style={{
              display: "flex", alignItems: "center", gap: 8,
              background: "#1d4ed8", color: "#fff", border: "none",
              padding: "11px 20px", borderRadius: 12, fontWeight: 700, fontSize: 14,
              cursor: "pointer", boxShadow: "0 4px 14px rgba(29,78,216,.25)"
            }}
          >
            <Plus size={17} /> New Course
          </button>
        </div>
      </div>

      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "28px 32px" }}>
        {/* Search */}
        <form onSubmit={handleSearch} style={{ display: "flex", gap: 10, marginBottom: 28 }}>
          <div style={{ position: "relative", flex: 1 }}>
            <Search size={15} style={{ position: "absolute", left: 13, top: "50%", transform: "translateY(-50%)", color: "#94a3b8" }} />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search courses..."
              style={{
                width: "100%", padding: "11px 14px 11px 38px", border: "1px solid #e2e8f0",
                borderRadius: 12, fontSize: 14, outline: "none", background: "#fff",
                boxSizing: "border-box"
              }}
            />
          </div>
          <button type="submit" style={{
            padding: "11px 20px", background: "#1d4ed8", color: "#fff",
            border: "none", borderRadius: 12, fontWeight: 700, fontSize: 13, cursor: "pointer"
          }}>Search</button>
          {search && <button type="button" onClick={() => { setSearch(""); fetchCourses(); }} style={{
            padding: "11px 16px", background: "#f1f5f9", color: "#475569",
            border: "1px solid #e2e8f0", borderRadius: 12, fontWeight: 600, fontSize: 13, cursor: "pointer"
          }}>Clear</button>}
        </form>

        {/* Grid */}
        {loading ? (
          <div style={{ textAlign: "center", padding: "80px 0", color: "#64748b" }}>
            <Loader2 size={32} style={{ animation: "spin 1s linear infinite", marginBottom: 12 }} />
            <p>Loading courses...</p>
          </div>
        ) : courses.length === 0 ? (
          <div style={{
            textAlign: "center", padding: "80px 0",
            background: "#fff", borderRadius: 20, border: "2px dashed #e2e8f0"
          }}>
            <BookOpen size={48} style={{ color: "#cbd5e1", marginBottom: 16 }} />
            <h3 style={{ color: "#64748b", margin: "0 0 8px", fontSize: 18, fontWeight: 700 }}>No courses yet</h3>
            <p style={{ color: "#94a3b8", margin: "0 0 24px", fontSize: 14 }}>
              Create your first course to get started
            </p>
            <button
              onClick={() => setShowCreate(true)}
              style={{
                display: "inline-flex", alignItems: "center", gap: 8,
                background: "#1d4ed8", color: "#fff", border: "none",
                padding: "12px 24px", borderRadius: 12, fontWeight: 700, fontSize: 14, cursor: "pointer"
              }}
            >
              <Plus size={16} /> Create First Course
            </button>
          </div>
        ) : (
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
            gap: 20
          }}>
            {courses.map(course => (
              <div
                key={course.uuid}
                style={{
                  background: "#fff", borderRadius: 18, overflow: "hidden",
                  border: "1px solid #e2e8f0",
                  boxShadow: "0 4px 16px rgba(0,0,0,.04)",
                  transition: "transform .2s, box-shadow .2s",
                  display: "flex", flexDirection: "column"
                }}
              >
                {/* Thumbnail */}
                <div style={{
                  height: 180, background: course.thumbnail_url
                    ? `url(${course.thumbnail_url}) center/cover`
                    : "linear-gradient(135deg, #dbeafe 0%, #1d4ed8 100%)",
                  position: "relative"
                }}>
                  <div style={{
                    position: "absolute", top: 12, right: 12, display: "flex", gap: 6
                  }}>
                    <span style={{
                      padding: "4px 10px", borderRadius: 999, fontSize: 11, fontWeight: 700,
                      background: course.is_published ? "rgba(16,185,129,.9)" : "rgba(100,116,139,.85)",
                      color: "#fff", backdropFilter: "blur(4px)"
                    }}>
                      {course.is_published ? "Published" : "Draft"}
                    </span>
                  </div>
                  {course.level && (
                    <div style={{ position: "absolute", bottom: 12, left: 12 }}>
                      <span style={{
                        padding: "4px 10px", borderRadius: 999, fontSize: 11, fontWeight: 700,
                        background: "rgba(255,255,255,.9)", color: "#1d4ed8"
                      }}>
                        {course.level}
                      </span>
                    </div>
                  )}
                </div>

                {/* Content */}
                <div style={{ padding: "18px 20px 14px", flex: 1 }}>
                  <h3 style={{ margin: "0 0 6px", fontSize: 16, fontWeight: 800, color: "#0f172a", lineHeight: 1.3 }}>
                    {course.title}
                  </h3>
                  {course.short_description && (
                    <p style={{
                      margin: "0 0 12px", color: "#64748b", fontSize: 13, lineHeight: 1.6,
                      display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical",
                      overflow: "hidden"
                    }}>
                      {course.short_description}
                    </p>
                  )}
                  <div style={{ display: "flex", gap: 12, alignItems: "center", color: "#94a3b8", fontSize: 12 }}>
                    {course.duration && (
                      <span style={{ display: "flex", alignItems: "center", gap: 4 }}>
                        <Clock size={12} /> {course.duration}
                      </span>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div style={{
                  padding: "12px 20px 16px",
                  borderTop: "1px solid #f1f5f9",
                  display: "flex", gap: 8
                }}>
                  <button
                    onClick={() => router.push(`/admin/courses/${course.uuid}`)}
                    style={{
                      flex: 1, padding: "10px", background: "#1d4ed8", color: "#fff",
                      border: "none", borderRadius: 10, fontWeight: 700, fontSize: 13,
                      cursor: "pointer", display: "flex", alignItems: "center",
                      justifyContent: "center", gap: 6
                    }}
                  >
                    <Edit2 size={14} /> Manage
                  </button>
                  <a
                    href={`/course/${course.slug}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{
                      padding: "10px 14px", background: "#f1f5f9", color: "#475569",
                      border: "1px solid #e2e8f0", borderRadius: 10, fontWeight: 600,
                      fontSize: 13, cursor: "pointer", display: "flex",
                      alignItems: "center", gap: 6, textDecoration: "none"
                    }}
                  >
                    <Eye size={14} />
                  </a>
                  <button
                    onClick={() => handleDelete(course.uuid, course.title)}
                    style={{
                      padding: "10px 14px", background: "#fff", color: "#ef4444",
                      border: "1px solid #fecaca", borderRadius: 10, fontWeight: 600,
                      fontSize: 13, cursor: "pointer", display: "flex",
                      alignItems: "center", gap: 6
                    }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Create Modal */}
      {showCreate && (
        <div style={{
          position: "fixed", inset: 0, background: "rgba(0,0,0,.5)",
          display: "flex", alignItems: "center", justifyContent: "center",
          zIndex: 1000, padding: 20
        }}>
          <div style={{
            background: "#fff", borderRadius: 24, width: "100%", maxWidth: 480,
            boxShadow: "0 25px 60px rgba(0,0,0,.2)"
          }}>
            <div style={{
              padding: "24px 28px 0",
              display: "flex", alignItems: "center", justifyContent: "space-between"
            }}>
              <div>
                <h2 style={{ margin: 0, fontSize: 20, fontWeight: 800, color: "#0f172a" }}>
                  Create New Course
                </h2>
                <p style={{ margin: "4px 0 0", color: "#64748b", fontSize: 13 }}>
                  Only name and thumbnail needed. Add all details later.
                </p>
              </div>
              <button onClick={() => setShowCreate(false)} style={{
                background: "#f1f5f9", border: "none", borderRadius: 10,
                padding: 8, cursor: "pointer", color: "#475569"
              }}>
                <X size={18} />
              </button>
            </div>

            <form onSubmit={handleCreate} style={{ padding: "24px 28px" }}>
              <div style={{ marginBottom: 20 }}>
                <label style={{ display: "block", fontWeight: 700, fontSize: 13, color: "#374151", marginBottom: 8 }}>
                  Course Name <span style={{ color: "#ef4444" }}>*</span>
                </label>
                <input
                  value={title}
                  onChange={e => setTitle(e.target.value)}
                  placeholder="e.g. Machine Learning Fundamentals"
                  autoFocus
                  style={{
                    width: "100%", padding: "12px 14px", border: "1px solid #d1d5db",
                    borderRadius: 12, fontSize: 14, outline: "none", boxSizing: "border-box"
                  }}
                />
              </div>

              <div style={{ marginBottom: 24 }}>
                <label style={{ display: "block", fontWeight: 700, fontSize: 13, color: "#374151", marginBottom: 8 }}>
                  Course Thumbnail
                </label>
                {thumbnailUrl ? (
                  <div style={{ position: "relative" }}>
                    <img src={thumbnailUrl} alt="" style={{
                      width: "100%", height: 160, objectFit: "cover",
                      borderRadius: 12, border: "1px solid #e2e8f0"
                    }} />
                    <button type="button" onClick={() => setThumbnailUrl("")} style={{
                      position: "absolute", top: 8, right: 8, background: "rgba(0,0,0,.6)",
                      border: "none", borderRadius: 8, padding: "4px 8px",
                      color: "#fff", cursor: "pointer", fontSize: 11, fontWeight: 700
                    }}>
                      Remove
                    </button>
                  </div>
                ) : (
                  <div
                    onClick={() => fileRef.current?.click()}
                    style={{
                      border: "2px dashed #d1d5db", borderRadius: 12, padding: "32px 20px",
                      textAlign: "center", cursor: "pointer", color: "#94a3b8",
                      transition: "border-color .2s",
                    }}
                  >
                    {uploading ? (
                      <><Loader2 size={24} style={{ animation: "spin 1s linear infinite", marginBottom: 8 }} /><p style={{ margin: 0, fontSize: 13 }}>Uploading...</p></>
                    ) : (
                      <><Upload size={24} style={{ marginBottom: 8 }} /><p style={{ margin: "0 0 4px", fontSize: 13, fontWeight: 600 }}>Click to upload thumbnail</p><p style={{ margin: 0, fontSize: 11 }}>JPG, PNG, WEBP · max 5MB</p></>
                    )}
                  </div>
                )}
                <input
                  ref={fileRef} type="file" accept="image/*" style={{ display: "none" }}
                  onChange={e => e.target.files?.[0] && handleUpload(e.target.files[0])}
                />
                <input
                  value={thumbnailUrl}
                  onChange={e => setThumbnailUrl(e.target.value)}
                  placeholder="…or paste image URL"
                  style={{
                    width: "100%", marginTop: 8, padding: "10px 14px",
                    border: "1px solid #e2e8f0", borderRadius: 10, fontSize: 13,
                    outline: "none", color: "#374151", boxSizing: "border-box"
                  }}
                />
              </div>

              {createError && (
                <p style={{ color: "#ef4444", fontSize: 13, margin: "0 0 16px", fontWeight: 600 }}>
                  {createError}
                </p>
              )}

              <div style={{ display: "flex", gap: 10 }}>
                <button type="button" onClick={() => setShowCreate(false)} style={{
                  flex: 1, padding: "12px", background: "#f8fafc",
                  border: "1px solid #e2e8f0", borderRadius: 12,
                  fontWeight: 700, fontSize: 14, cursor: "pointer", color: "#475569"
                }}>
                  Cancel
                </button>
                <button type="submit" disabled={creating} style={{
                  flex: 2, padding: "12px", background: creating ? "#93c5fd" : "#1d4ed8",
                  color: "#fff", border: "none", borderRadius: 12,
                  fontWeight: 700, fontSize: 14, cursor: creating ? "not-allowed" : "pointer",
                  display: "flex", alignItems: "center", justifyContent: "center", gap: 8
                }}>
                  {creating ? <><Loader2 size={16} style={{ animation: "spin 1s linear infinite" }} /> Creating...</> : "Create Course →"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <style>{`@keyframes spin { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }`}</style>
    </div>
  );
}
