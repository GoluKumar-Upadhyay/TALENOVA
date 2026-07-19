"use client";

import Link from "next/link";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowRight,
  Award,
  BookOpen,
  BriefcaseBusiness,
  CalendarDays,
  Camera,
  CheckCircle2,
  GraduationCap,
  ImageIcon,
  Link2,
  MapPin,
  PlayCircle,
  Quote,
  Search,
  Sparkles,
  Star,
  UsersRound,
} from "lucide-react";
import { activeRecords, normalizePublicPage, publicApi, queryPath, type PublicPageResponse, type PublicRecord } from "../../lib/public-api";
import { SectionHeading } from "./SiteShell";

type PublicModuleKey =
  | "courses"
  | "teachers"
  | "founders"
  | "partners"
  | "gallery"
  | "videos"
  | "achievements"
  | "projects"
  | "testimonials"
  | "success-stories"
  | "events"
  | "internships"
  | "faqs";

type ModuleConfig = {
  key: PublicModuleKey;
  endpoint: string;
  eyebrow: string;
  title: string;
  description: string;
  icon: typeof BookOpen;
  titleField: string;
  descriptionField?: string;
  imageField?: string;
  secondaryFields?: string[];
  chipFields?: string[];
  dateField?: string;
  linkField?: string;
  linkLabel?: string;
  filterField?: string;
  emptyLabel: string;
  defaultSort?: string;
};

export const publicModuleConfigs: Record<PublicModuleKey, ModuleConfig> = {
  courses: {
    key: "courses",
    endpoint: "/courses",
    eyebrow: "Courses",
    title: "Build skills with visible proof.",
    description: "Explore TALENOVA courses shaped around career-ready capability, projects, tools, and a clear path to action.",
    icon: BookOpen,
    titleField: "title",
    descriptionField: "short_description",
    imageField: "thumbnail_url",
    secondaryFields: ["duration", "certification"],
    chipFields: ["tools", "projects", "prerequisites"],
    linkField: "registration_url",
    linkLabel: "Register interest",
    filterField: "is_coming_soon",
    emptyLabel: "No courses are published right now.",
    defaultSort: "display_order",
  },
  teachers: {
    key: "teachers",
    endpoint: "/teachers",
    eyebrow: "Teachers",
    title: "Learn with mentors who make context clear.",
    description: "Meet the faculty and practitioners supporting learners with domain clarity, reviews, and career-focused guidance.",
    icon: GraduationCap,
    titleField: "name",
    descriptionField: "biography",
    imageField: "image_url",
    secondaryFields: ["designation", "qualification", "experience"],
    chipFields: ["skills"],
    linkField: "linkedin_url",
    linkLabel: "LinkedIn",
    emptyLabel: "No teachers are published right now.",
    defaultSort: "display_order",
  },
  founders: {
    key: "founders",
    endpoint: "/founders",
    eyebrow: "Founders",
    title: "The people shaping TALENOVA.",
    description: "Read about the founding team, their work, research interests, experience, and the thinking behind the platform.",
    icon: Star,
    titleField: "name",
    descriptionField: "bio",
    imageField: "photo_url",
    secondaryFields: ["founder_type"],
    chipFields: ["achievements", "research"],
    linkField: "resume_url",
    linkLabel: "View profile",
    filterField: "founder_type",
    emptyLabel: "No founder profiles are published right now.",
    defaultSort: "display_order",
  },
  partners: {
    key: "partners",
    endpoint: "/partners",
    eyebrow: "Partners",
    title: "Built with institutions, communities, and industry.",
    description: "TALENOVA partners with colleges, companies, technology teams, and communities to make learning more useful.",
    icon: Link2,
    titleField: "name",
    descriptionField: "description",
    imageField: "logo_url",
    secondaryFields: ["partner_type"],
    linkField: "website_url",
    linkLabel: "Visit partner",
    filterField: "partner_type",
    emptyLabel: "No partners are published right now.",
    defaultSort: "display_order",
  },
  gallery: {
    key: "gallery",
    endpoint: "/gallery",
    eyebrow: "Gallery",
    title: "Moments from the TALENOVA learning space.",
    description: "A visual journal of workshops, reviews, demo days, collaborations, and community energy.",
    icon: Camera,
    titleField: "alt_text",
    descriptionField: "caption",
    imageField: "image_url",
    secondaryFields: ["category_id"],
    filterField: "category_id",
    emptyLabel: "No gallery images are published right now.",
    defaultSort: "display_order",
  },
  videos: {
    key: "videos",
    endpoint: "/videos",
    eyebrow: "Videos",
    title: "Watch ideas become clearer.",
    description: "Browse talks, explainers, demos, and learning moments from TALENOVA.",
    icon: PlayCircle,
    titleField: "title",
    descriptionField: "description",
    imageField: "thumbnail_url",
    secondaryFields: ["category", "duration_seconds"],
    linkField: "youtube_url",
    linkLabel: "Watch video",
    filterField: "category",
    emptyLabel: "No videos are published right now.",
    defaultSort: "display_order",
  },
  achievements: {
    key: "achievements",
    endpoint: "/achievements",
    eyebrow: "Achievements",
    title: "Milestones that show momentum.",
    description: "Achievements from learners, teams, and the wider TALENOVA community.",
    icon: Award,
    titleField: "title",
    descriptionField: "description",
    imageField: "image_url",
    secondaryFields: ["achievement_type"],
    filterField: "achievement_type",
    emptyLabel: "No achievements are published right now.",
    defaultSort: "display_order",
  },
  projects: {
    key: "projects",
    endpoint: "/projects",
    eyebrow: "Projects",
    title: "Portfolio work with decisions behind it.",
    description: "Explore projects that show technologies, trade-offs, demos, repositories, and practical problem solving.",
    icon: BriefcaseBusiness,
    titleField: "title",
    descriptionField: "description",
    imageField: "image_url",
    secondaryFields: ["status"],
    chipFields: ["technologies", "tags"],
    linkField: "demo_url",
    linkLabel: "Open demo",
    filterField: "status",
    emptyLabel: "No projects are published right now.",
    defaultSort: "display_order",
  },
  testimonials: {
    key: "testimonials",
    endpoint: "/testimonials",
    eyebrow: "Testimonials",
    title: "Learners in their own words.",
    description: "Read honest reflections from students and professionals who worked through TALENOVA programmes.",
    icon: Quote,
    titleField: "student_name",
    descriptionField: "review",
    imageField: "photo_url",
    secondaryFields: ["college", "designation", "course_completed", "placement_company", "package"],
    filterField: "rating",
    emptyLabel: "No testimonials are published right now.",
    defaultSort: "display_order",
  },
  "success-stories": {
    key: "success-stories",
    endpoint: "/success-stories",
    eyebrow: "Success Stories",
    title: "Proof, progress, and the journey between.",
    description: "Follow learner journeys from their starting point to internships, placements, projects, and confidence.",
    icon: Sparkles,
    titleField: "name",
    descriptionField: "story",
    imageField: "image_url",
    secondaryFields: ["course", "batch", "internship", "placement", "job_role", "college"],
    chipFields: ["achievement_tags"],
    linkField: "linkedin_url",
    linkLabel: "LinkedIn",
    filterField: "course",
    emptyLabel: "No success stories are published right now.",
    defaultSort: "display_order",
  },
  events: {
    key: "events",
    endpoint: "/events",
    eyebrow: "Events",
    title: "Workshops, sessions, and live learning moments.",
    description: "Find upcoming and past TALENOVA events, from webinars to campus workshops and demo days.",
    icon: CalendarDays,
    titleField: "title",
    descriptionField: "description",
    imageField: "banner_url",
    secondaryFields: ["event_type", "mode", "location"],
    dateField: "event_date",
    linkField: "registration_url",
    linkLabel: "Register",
    filterField: "mode",
    emptyLabel: "No events are published right now.",
    defaultSort: "display_order",
  },
  internships: {
    key: "internships",
    endpoint: "/internships",
    eyebrow: "Internships",
    title: "Real work, guided practice, clearer confidence.",
    description: "Explore internship opportunities connected to companies, skills, eligibility, timelines, and outcomes.",
    icon: BriefcaseBusiness,
    titleField: "title",
    descriptionField: "description",
    imageField: "company_logo_url",
    secondaryFields: ["company", "internship_type", "duration", "stipend", "location", "last_date"],
    chipFields: ["skills"],
    linkField: "application_url",
    linkLabel: "Apply",
    filterField: "internship_type",
    emptyLabel: "No internships are published right now.",
    defaultSort: "display_order",
  },
  faqs: {
    key: "faqs",
    endpoint: "/faqs",
    eyebrow: "FAQ",
    title: "Answers before the first conversation.",
    description: "Clear answers about courses, internships, admissions, placements, payments, and the TALENOVA learning model.",
    icon: Search,
    titleField: "question",
    descriptionField: "answer",
    secondaryFields: ["page", "category"],
    filterField: "category",
    emptyLabel: "No FAQs are published right now.",
    defaultSort: "display_order",
  },
};

export function plainText(value: unknown) {
  if (value == null) return "";
  if (Array.isArray(value)) return value.map(plainText).filter(Boolean).join(", ");
  if (typeof value === "object") {
    return Object.values(value as Record<string, unknown>).map(plainText).filter(Boolean).join(", ");
  }
  return String(value).replace(/<[^>]*>/g, "").trim();
}

export function htmlValue(value: unknown) {
  return plainText(value) ? String(value) : "";
}

export function imageUrl(item: PublicRecord, field?: string) {
  const value = field ? item[field] : undefined;
  return typeof value === "string" && value.startsWith("http") ? value : "";
}

export function itemTitle(item: PublicRecord, config: ModuleConfig) {
  return plainText(item[config.titleField]) || "Untitled record";
}

export function usePublicList(module: PublicModuleKey, options: { page?: number; pageSize?: number; search?: string; filter?: string; featured?: boolean } = {}) {
  const config = publicModuleConfigs[module];
  const page = options.page || 1;
  const pageSize = options.pageSize || 12;
  const path = queryPath(config.endpoint, {
    page,
    page_size: pageSize,
    sort: config.defaultSort || "display_order",
    direction: "asc",
    search: options.search,
    [config.filterField || ""]: options.filter,
    is_featured: options.featured || undefined,
  });
  return useQuery({
    queryKey: ["public", module, path],
    queryFn: () => publicApi<PublicRecord[] | PublicPageResponse<PublicRecord> | PublicRecord>(path),
    select: (data) => {
      const pageData = normalizePublicPage(data);
      return { ...pageData, items: activeRecords(pageData.items) };
    },
  });
}

export function EmptyState({ label }: { label: string }) {
  return (
    <div className="empty-state">
      <CheckCircle2 size={28} />
      <p>{label}</p>
    </div>
  );
}

export function LoadingGrid() {
  return (
    <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3" aria-label="Loading content">
      {Array.from({ length: 6 }).map((_, index) => <div key={index} className="skeleton-card" />)}
    </div>
  );
}

export function PublicCard({ item, config, compact = false }: { item: PublicRecord; config: ModuleConfig; compact?: boolean }) {
  const title = itemTitle(item, config);
  const description = config.descriptionField ? htmlValue(item[config.descriptionField]) : "";
  const image = imageUrl(item, config.imageField);
  const Icon = config.icon;
  const chips = (config.chipFields || [])
    .flatMap((field) => {
      const value = item[field];
      if (Array.isArray(value)) return value.map(plainText);
      return plainText(value).split(",").map((part) => part.trim());
    })
    .filter(Boolean)
    .slice(0, compact ? 3 : 6);
  const secondary = (config.secondaryFields || []).map((field) => plainText(item[field])).filter(Boolean);
  const date = config.dateField ? plainText(item[config.dateField]) : "";
  const href = config.linkField ? plainText(item[config.linkField]) : "";

  return (
    <article className="public-card reveal">
      {image ? (
        <img src={image} alt={title} className="public-card-media" loading="lazy" />
      ) : (
        <div className="public-card-media public-card-art" aria-hidden="true">
          <Icon size={34} />
        </div>
      )}
      <div className="p-5">
        <div className="flex flex-wrap items-center gap-2">
          {date ? <span className="mini-pill"><CalendarDays size={13} />{date}</span> : null}
          {secondary.slice(0, compact ? 1 : 3).map((value) => <span key={value} className="mini-pill">{value}</span>)}
        </div>
        <h3 className="mt-4 text-xl font-black text-ink">{title}</h3>
        {description ? <div className="mt-3 line-clamp-4 text-sm leading-6 text-slate-600" dangerouslySetInnerHTML={{ __html: description }} /> : null}
        {chips.length ? <div className="mt-5 flex flex-wrap gap-2">{chips.map((chip) => <span key={chip} className="soft-chip">{chip}</span>)}</div> : null}
        {href ? (
          <a href={href} target="_blank" rel="noreferrer" className="mt-6 inline-flex items-center gap-2 text-sm font-black text-brand">
            {config.linkLabel || "Open"}
            <ArrowRight size={15} />
          </a>
        ) : null}
      </div>
    </article>
  );
}

export function FeaturedSection({ module, limit = 3, title, description }: { module: PublicModuleKey; limit?: number; title?: string; description?: string }) {
  const config = publicModuleConfigs[module];
  const result = usePublicList(module, { pageSize: limit, featured: true });
  const items = result.data?.items || [];
  return (
    <section className="wrap py-20">
      <SectionHeading eyebrow={config.eyebrow} title={title || config.title} description={description || config.description} action={<Link href={module === "success-stories" ? "/success" : `/${module === "faqs" ? "faq" : module}`} className="button button-outline">View all <ArrowRight size={16} /></Link>} />
      <div className="mt-10">
        {result.isLoading ? <LoadingGrid /> : null}
        {result.isError ? <EmptyState label={`Unable to load ${config.eyebrow.toLowerCase()} right now.`} /> : null}
        {!result.isLoading && !result.isError && !items.length ? <EmptyState label={config.emptyLabel} /> : null}
        {items.length ? <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">{items.map((item) => <PublicCard key={String(item.uuid || item.id || itemTitle(item, config))} item={item} config={config} compact />)}</div> : null}
      </div>
    </section>
  );
}

export function PublicModulePage({ module }: { module: PublicModuleKey }) {
  const config = publicModuleConfigs[module];
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("");
  const [page, setPage] = useState(1);
  const result = usePublicList(module, { page, pageSize: 12, search, filter });
  const items = result.data?.items || [];
  const total = result.data?.total || items.length;
  const filterValues = Array.from(new Set(items.map((item) => config.filterField ? plainText(item[config.filterField]) : "").filter(Boolean))).slice(0, 10);

  return (
    <main>
      <section className="page-hero">
        <div className="wrap py-20 md:py-28">
          <p className="eyebrow">{config.eyebrow}</p>
          <h1 className="page-title mt-4">{config.title}</h1>
          <p className="page-lede mt-5">{config.description}</p>
        </div>
      </section>
      <section className="wrap py-20">
        <div className="public-toolbar">
          <label className="search-box">
            <Search size={18} />
            <span className="sr-only">Search {config.eyebrow}</span>
            <input value={search} onChange={(event) => { setSearch(event.target.value); setPage(1); }} placeholder={`Search ${config.eyebrow.toLowerCase()}`} />
          </label>
          {config.filterField ? (
            <select value={filter} onChange={(event) => { setFilter(event.target.value); setPage(1); }} className="filter-select" aria-label={`Filter ${config.eyebrow}`}>
              <option value="">All {config.eyebrow}</option>
              {filterValues.map((value) => <option key={value} value={value}>{value}</option>)}
            </select>
          ) : null}
        </div>
        <div className="mt-10">
          {result.isLoading ? <LoadingGrid /> : null}
          {result.isError ? <EmptyState label={`Unable to load ${config.eyebrow.toLowerCase()} right now.`} /> : null}
          {!result.isLoading && !result.isError && !items.length ? <EmptyState label={config.emptyLabel} /> : null}
          {items.length ? <div className={module === "gallery" ? "grid gap-5 sm:grid-cols-2 lg:grid-cols-3" : "grid gap-5 md:grid-cols-2 lg:grid-cols-3"}>{items.map((item) => <PublicCard key={String(item.uuid || item.id || itemTitle(item, config))} item={item} config={config} />)}</div> : null}
        </div>
        {total > 12 ? (
          <div className="mt-10 flex items-center justify-center gap-3">
            <button className="button button-outline" disabled={page <= 1} onClick={() => setPage((value) => Math.max(1, value - 1))}>Previous</button>
            <span className="text-sm font-bold text-slate-500">Page {page}</span>
            <button className="button button-outline" disabled={items.length < 12} onClick={() => setPage((value) => value + 1)}>Next</button>
          </div>
        ) : null}
      </section>
    </main>
  );
}

export function TrustStrip() {
  return (
    <div className="wrap">
      <div className="stat-strip">
        {[
          ["Industry-aligned", "Projects and reviews tied to practical outcomes"],
          ["Mentor-led", "Guidance from educators and practitioners"],
          ["Portfolio-first", "Every learner builds visible evidence"],
          ["Partnership-ready", "Designed for colleges and teams"],
        ].map(([title, text]) => (
          <div className="stat-item" key={title}>
            <strong>{title}</strong>
            <span>{text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
