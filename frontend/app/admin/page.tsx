"use client";

import { useEffect, useState } from "react";
import {
  Activity,
  Award,
  BookOpen,
  BriefcaseBusiness,
  FileText,
  Footprints,
  GalleryHorizontal,
  Globe,
  GraduationCap,
  Image,
  LayoutDashboard,
  Link2,
  LogOut,
  Menu,
  MessageSquare,
  Navigation,
  Newspaper,
  PanelTop,
  Quote,
  Search,
  Settings,
  Star,
  Trophy,
  Users,
  Video,
} from "lucide-react";
import { api } from "../../lib/api";
import { adminModules } from "./modules";

type Summary = Record<string, number>;

const moduleIcons = {
  hero: PanelTop,
  content: FileText,
  "course-categories": GraduationCap,
  courses: BookOpen,
  teachers: Users,
  founders: Star,
  partners: Link2,
  gallery: GalleryHorizontal,
  videos: Video,
  projects: BriefcaseBusiness,
  achievements: Trophy,
  testimonials: Quote,
  "success-stories": Award,
  internships: BriefcaseBusiness,
  events: Activity,
  contact: MessageSquare,
  faqs: Search,
  settings: Settings,
  navigation: Navigation,
  footer: Footprints,
  seo: Globe,
  analytics: Activity,
} as const;

const summaryCards = [
  ["Courses", "total_courses", BookOpen],
  ["Teachers", "total_teachers", Users],
  ["Contacts", "total_contacts", MessageSquare],
  ["Events", "total_events", Activity],
  ["Internships", "total_internships", BriefcaseBusiness],
  ["Testimonials", "total_testimonials", Quote],
  ["Gallery images", "total_gallery_images", Image],
  ["Videos", "total_videos", Video],
] as const;

export default function AdminDashboard() {
  const [summary, setSummary] = useState<Summary>({});
  const [error, setError] = useState("");

  useEffect(() => {
    api<{ summary: Summary }>("/analytics/dashboard")
      .then((data) => setSummary(data.summary))
      .catch((error) => setError(error instanceof Error ? error.message : "Unable to load dashboard analytics"));
  }, []);

  function logout() {
    localStorage.removeItem("talenova_access_token");
    window.location.href = "/admin/login";
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <aside className="fixed hidden h-screen w-64 overflow-y-auto border-r bg-white p-5 lg:block">
        <a href="/admin" className="text-xl font-black text-brand">
          TALENOVA<span className="text-ink">.</span>
        </a>
        <nav className="mt-10 space-y-1 pb-20">
          <a href="/admin" className="flex items-center gap-3 rounded-xl bg-blue-50 p-3 text-sm font-bold text-brand">
            <LayoutDashboard size={18} />
            Overview
          </a>
          {adminModules.map(([path, label]) => {
            const Icon = moduleIcons[path] || FileText;
            return (
              <a key={path} href={`/admin/${path}`} className="flex items-center gap-3 rounded-xl p-3 text-sm font-semibold text-slate-600 hover:bg-slate-50">
                <Icon size={18} />
                {label}
              </a>
            );
          })}
        </nav>
        <button onClick={logout} className="fixed bottom-8 flex items-center gap-3 rounded-xl bg-white p-3 text-sm font-bold text-slate-500">
          <LogOut size={18} />
          Sign out
        </button>
      </aside>
      <main className="lg:ml-64">
        <header className="flex h-20 items-center justify-between border-b bg-white px-6">
          <div>
            <p className="text-sm text-slate-500">Administration</p>
            <h1 className="text-xl font-black">Dashboard overview</h1>
          </div>
          <button className="rounded-xl border p-2 lg:hidden" aria-label="Open admin menu">
            <Menu />
          </button>
        </header>
        <div className="p-6 md:p-10">
          <p className="eyebrow">Live data</p>
          <h2 className="mt-2 text-3xl font-black">Platform at a glance</h2>
          {error ? <p className="mt-4 rounded-xl bg-red-50 p-4 text-sm text-red-700">{error}</p> : null}
          <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {summaryCards.map(([label, key, Icon]) => (
              <div className="rounded-2xl border bg-white p-5 shadow-sm" key={key}>
                <div className="flex items-center justify-between">
                  <p className="text-sm font-semibold text-slate-500">{label}</p>
                  <Icon size={19} className="text-brand" />
                </div>
                <p className="mt-4 text-3xl font-black">{summary[key] ?? "—"}</p>
              </div>
            ))}
          </div>
          <section className="mt-8 rounded-2xl border bg-white p-6">
            <div className="flex items-center gap-3">
              <Activity className="text-brand" />
              <h2 className="text-lg font-black">CMS modules</h2>
            </div>
            <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
              {adminModules.map(([path, label]) => {
                const Icon = moduleIcons[path] || FileText;
                return (
                  <a key={path} href={`/admin/${path}`} className="flex items-center justify-between rounded-xl border p-4 text-sm font-bold text-slate-700 transition hover:border-brand hover:text-brand">
                    <span className="flex items-center gap-3">
                      <Icon size={18} />
                      {label}
                    </span>
                    <span>Manage</span>
                  </a>
                );
              })}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
