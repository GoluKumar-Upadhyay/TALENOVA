"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Search, Clock, BookOpen, Loader2, Star } from "lucide-react";
import { SiteShell } from "../../components/site/SiteShell";
import { publicApi } from "../../lib/public-api";

interface Course {
  uuid: string; title: string; slug: string;
  short_description?: string; thumbnail_url?: string;
  level?: string; duration?: string; is_published: boolean;
  is_active: boolean; display_order: number; category_id?: number;
}

interface CoursePage { items: Course[]; total: number; page: number; page_size: number; }

const LEVEL_BADGE: Record<string, { bg: string; color: string }> = {
  Beginner:     { bg: "#d1fae5", color: "#065f46" },
  Intermediate: { bg: "#fef3c7", color: "#92400e" },
  Advanced:     { bg: "#fee2e2", color: "#991b1b" },
};

function CourseCard({ course }: { course: Course }) {
  const badge = course.level ? LEVEL_BADGE[course.level] : null;

  return (
    <Link href={`/course/${course.slug}`} className="public-card block h-full no-underline">
      <article className="course-card">
        <div className="course-card__media">
          {course.thumbnail_url ? (
            <img src={course.thumbnail_url} alt={course.title} className="public-card-media" loading="lazy" decoding="async" />
          ) : (
            <div className="course-card__art public-card-media public-card-art" aria-hidden="true">
              <BookOpen size={36} />
            </div>
          )}
          <div className="course-card__overlay" aria-hidden="true" />
          <div className="course-card__badge-row">
            <span className="course-card__badge">Course</span>
            {badge && course.level ? <span className="course-card__level" style={{ background: badge.bg, color: badge.color }}>{course.level}</span> : null}
            <span className="course-card__rating"><Star size={12} className="fill-amber-300 text-amber-300" /> Featured</span>
          </div>
        </div>

        <div className="course-card__body">
          <div className="flex flex-wrap items-center gap-2">
            {course.duration && (
              <span className="mini-pill"><Clock size={12} /> {course.duration}</span>
            )}
            {course.category_id ? <span className="mini-pill">Category {course.category_id}</span> : null}
          </div>
          <h3 className="course-card__title">{course.title}</h3>
          {course.short_description ? <p className="course-card__excerpt line-clamp-2">{course.short_description}</p> : null}
          <div className="course-card__footer">
            <span className="course-card__cta">View details <span aria-hidden="true"></span></span>
            <span className="text-xs font-semibold text-slate-500">Open course page</span>
          </div>
        </div>
      </article>
    </Link>
  );
}

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [level, setLevel] = useState("");

  const fetchCourses = async (q = "", lv = "") => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ page: "1", page_size: "24", sort: "display_order", direction: "asc", published: "true" });
      if (q) params.set("search", q);
      const data = await publicApi<CoursePage>(`/courses?${params}`);
      let items = data.items || [];
      if (lv) items = items.filter(c => c.level === lv);
      setCourses(items);
      setTotal(items.length);
    } catch { setCourses([]); } finally { setLoading(false); }
  };

  useEffect(() => { fetchCourses(); }, []);

  const handleSearch = (e: React.FormEvent) => { e.preventDefault(); fetchCourses(search, level); };

  return (
    <SiteShell>
      {/* Hero */}
      <section style={{
        background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1d4ed8 100%)",
        color: "#fff", padding: "70px 24px 60px", textAlign: "center"
      }}>
        <div style={{ maxWidth: 720, margin: "0 auto" }}>
         
          
          

          {/* Search bar */}
          <form onSubmit={handleSearch} style={{ display: "flex", gap: 10, maxWidth: 600, margin: "0 auto", flexWrap: "wrap" }}>
            <div style={{ position: "relative", flex: 1, minWidth: 200 }}>
              <Search size={15} style={{ position: "absolute", left: 14, top: "50%", transform: "translateY(-50%)", color: "#94a3b8" }} />
              <input value={search} onChange={e => setSearch(e.target.value)}
                placeholder="Search courses..."
                style={{
                  width: "100%", padding: "13px 14px 13px 40px", background: "rgba(255,255,255,.12)",
                  border: "1px solid rgba(255,255,255,.2)", borderRadius: 14, fontSize: 13,
                  color: "#fff", outline: "none", boxSizing: "border-box",
                  backdropFilter: "blur(8px)"
                }} />
            </div>
            <select value={level} onChange={e => { setLevel(e.target.value); fetchCourses(search, e.target.value); }}
              style={{
                padding: "13px 16px", background: "rgba(255,255,255,.12)",
                border: "1px solid rgba(255,255,255,.2)", borderRadius: 14, fontSize: 13,
                color: "#fff", outline: "none", cursor: "pointer"
              }}>
              <option value="" style={{ color: "#000" }}>All Levels</option>
              {["Beginner", "Intermediate", "Advanced"].map(l => <option key={l} value={l} style={{ color: "#000" }}>{l}</option>)}
            </select>
            <button type="submit" style={{
              padding: "13px 22px", background: "#fff", color: "#1d4ed8",
              border: "none", borderRadius: 14, fontWeight: 800, fontSize: 13, cursor: "pointer"
            }}>Search</button>
          </form>
        </div>
      </section>

      {/* Grid */}
      <div className="wrap" style={{ padding: "52px 24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 28 }}>
          <p style={{ margin: 0, fontSize: 12, color: "#64748b" }}>
            {loading ? "Loading..." : `${total} course${total !== 1 ? "s" : ""} found`}
          </p>
          {(search || level) && (
            <button onClick={() => { setSearch(""); setLevel(""); fetchCourses(); }} style={{
              padding: "7px 14px", background: "#f1f5f9", border: "1px solid #e2e8f0",
              borderRadius: 9, fontSize: 12, fontWeight: 700, color: "#475569", cursor: "pointer"
            }}>
              Clear filters ×
            </button>
          )}
        </div>

        {loading ? (
          <div style={{ textAlign: "center", padding: "60px 0", color: "#64748b" }}>
            <Loader2 size={32} style={{ animation: "spin 1s linear infinite" }} />
          </div>
        ) : courses.length === 0 ? (
          <div style={{ textAlign: "center", padding: "70px 0", color: "#94a3b8" }}>
            <BookOpen size={48} style={{ marginBottom: 16, opacity: .4 }} />
            <h3 style={{ margin: "0 0 8px", fontSize: 18, fontWeight: 700, color: "#64748b" }}>No courses found</h3>
            <p style={{ margin: 0, fontSize: 14 }}>Try adjusting your search or check back soon.</p>
          </div>
        ) : (
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
            gap: 22
          }}>
            {courses.map(course => <CourseCard key={course.uuid} course={course} />)}
          </div>
        )}
      </div>
      <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
    </SiteShell>
  );
}
