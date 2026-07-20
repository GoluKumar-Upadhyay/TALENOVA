"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Mail, Menu, Phone, Search, ShieldCheck, X } from "lucide-react";
import { useState } from "react";
import { activeRecords, normalizePublicPage, publicApi, queryPath, type PublicPageResponse, type PublicRecord } from "../../lib/public-api";
import { PublicSEO } from "./PublicSEO";

const coreLinks = [
  ["Courses", "/courses"],
  ["About", "/about"],
  ["Teachers", "/teachers"],
  ["Success", "/success"],
  ["Gallery", "/gallery"],
  ["Events", "/events"],
  ["Contact", "/contact"],
] as const;

function getText(record: PublicRecord | undefined, field: string, fallback = "") {
  const value = record?.[field];
  return typeof value === "string" && value.trim() ? value : fallback;
}

function safeJson<T>(value: unknown, fallback: T): T {
  if (!value) return fallback;
  if (typeof value === "string") {
    try {
      return JSON.parse(value) as T;
    } catch {
      return fallback;
    }
  }
  return value as T;
}

function useHeaderNavigation() {
  return useQuery({
    queryKey: ["public-navigation", "header"],
    queryFn: () => publicApi<PublicRecord[] | PublicPageResponse<PublicRecord>>(queryPath("/navigation", { page: 1, page_size: 40, location: "header", sort: "display_order", direction: "asc" })),
    select: (data) => activeRecords(normalizePublicPage(data).items)
      .filter((item) => item.location === "header" || item.location == null)
      .map((item) => [getText(item, "label"), getText(item, "href")] as const)
      .filter(([label, href]) => label && href),
  });
}

function useFooterContent() {
  return useQuery({
    queryKey: ["public-footer"],
    queryFn: () => publicApi<PublicRecord[] | PublicPageResponse<PublicRecord> | PublicRecord>("/footer/all"),
    select: (data) => activeRecords(normalizePublicPage(data).items)[0],
  });
}

function useSiteSettings() {
  return useQuery({
    queryKey: ["public-settings"],
    queryFn: () => publicApi<PublicRecord[] | PublicPageResponse<PublicRecord> | PublicRecord>("/settings/all"),
    select: (data) => normalizePublicPage(data).items[0],
  });
}

export function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const navigation = useHeaderNavigation();
  const settings = useSiteSettings();
  const links = navigation.data?.length ? navigation.data : coreLinks;
  const siteName = getText(settings.data, "site_name", "TALENOVA");
  const logo = getText(settings.data, "site_logo_url");
  const tagline = getText(settings.data, "tagline", "Premium learning paths for ambitious teams and career builders.");

  return (
    <header className="site-header">
      <div className="wrap flex min-h-20 items-center justify-between gap-3 py-4 lg:gap-5">
        <Link href="/" className="flex shrink-0 items-center gap-3" onClick={() => setOpen(false)} aria-label={`${siteName} home`}>
          {logo ? <img src={logo} alt="" className="h-9 w-9 rounded-2xl object-contain ring-1 ring-slate-200" /> : <span className="brand-mark">T</span>}
          <span className="flex flex-col leading-none">
            <span className="text-[17px] font-black tracking-tight text-ink md:text-[19px]">{siteName}</span>
            <span className="mt-1 hidden text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-500 md:block">{tagline}</span>
          </span>
        </Link>
        <nav className="hidden min-w-0 flex-1 items-center justify-center gap-1 lg:flex" aria-label="Primary navigation">
          <Link className={pathname === "/" ? "nav-link active" : "nav-link"} href="/">Home</Link>
          {links.map(([label, href]) => (
            <Link key={`${label}-${href}`} className={pathname.startsWith(href) ? "nav-link active" : "nav-link"} href={href}>{label}</Link>
          ))}
        </nav>
        <div className="hidden shrink-0 items-center gap-2 lg:flex">
          <Link href="/search" className="button button-outline px-3" aria-label="Search TALENOVA"><Search size={16} /></Link>
          <Link href="/admin/login" className="button button-outline">Login</Link>
          <Link href="/contact" className="button button-primary">Talk to us <ArrowRight size={16} /></Link>
        </div>
        <button className="rounded-2xl border border-slate-200 bg-white p-2 shadow-sm lg:hidden" onClick={() => setOpen((value) => !value)} aria-label={open ? "Close menu" : "Open menu"} aria-expanded={open}>
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>
      {open && (
        <div className="border-t border-slate-100 bg-white/96 px-6 pb-5 lg:hidden">
          <nav className="wrap flex flex-col gap-2 pt-4" aria-label="Mobile navigation">
            <Link className="mobile-nav-link" href="/" onClick={() => setOpen(false)}>Home</Link>
            {links.map(([label, href]) => <Link key={`${label}-${href}`} className="mobile-nav-link" href={href} onClick={() => setOpen(false)}>{label}</Link>)}
            <Link className="mobile-nav-link" href="/search" onClick={() => setOpen(false)}>Search</Link>
            <Link className="mobile-nav-link" href="/admin/login" onClick={() => setOpen(false)}>Login</Link>
            <Link className="button button-primary mt-3 text-center" href="/contact" onClick={() => setOpen(false)}>Talk to us <ArrowRight size={16} /></Link>
          </nav>
        </div>
      )}
    </header>
  );
}

export function SiteFooter() {
  const footer = useFooterContent();
  const settings = useSiteSettings();
  const record = footer.data;
  const siteName = getText(settings.data, "site_name", "TALENOVA");
  const logo = getText(record, "logo_url") || getText(settings.data, "site_logo_url");
  const description = getText(record, "description", getText(settings.data, "tagline", "A career transformation platform where ambitious learners learn deeply, build visibly, and move into industry with confidence."));
  const copyright = getText(record, "copyright_text", `Copyright ${new Date().getFullYear()} ${siteName}. All rights reserved.`);
  const quickLinks = safeJson<{ label: string; href: string }[]>(record?.quick_links, [
    { label: "Courses", href: "/courses" },
    { label: "About", href: "/about" },
    { label: "Success stories", href: "/success" },
    { label: "Gallery", href: "/gallery" },
  ]);
  const legalLinks = safeJson<{ label: string; href: string }[]>(record?.legal_links, [
    { label: "Privacy", href: "/privacy" },
    { label: "Terms", href: "/terms" },
    { label: "Cookies", href: "/cookies" },
  ]);
  const contactDetails = safeJson<Record<string, string>>(record?.contact_details, {});

  return (
    <footer className="relative mt-24 overflow-hidden bg-[#05070f] text-white">
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-brand to-transparent" aria-hidden="true" />
      <div className="pointer-events-none absolute -left-32 -top-32 h-72 w-72 rounded-full bg-brand/20 blur-[100px]" aria-hidden="true" />
      <div className="pointer-events-none absolute -right-24 bottom-0 h-64 w-64 rounded-full bg-indigo-500/10 blur-[100px]" aria-hidden="true" />

      <div className="wrap relative py-16 md:py-20">
        <div className="grid gap-10 md:grid-cols-[1.5fr_1fr_1fr_1.2fr] md:gap-8">
          <div>
            <div className="flex items-center gap-3">
              {logo ? <img src={logo} alt="" className="h-11 w-11 rounded-2xl object-contain ring-1 ring-white/10" /> : <span className="brand-mark">T</span>}
              <span className="text-xl font-black tracking-tight text-white">{siteName}</span>
            </div>
            <div className="mt-5 max-w-sm text-sm leading-7 text-slate-400" dangerouslySetInnerHTML={{ __html: description }} />
            <div className="mt-7 flex flex-wrap gap-3">
              <Link href="/courses" className="inline-flex items-center gap-2 rounded-full bg-brand px-5 py-2.5 text-sm font-bold text-white shadow-[0_8px_24px_rgba(59,130,246,0.35)] transition hover:brightness-110">
                Explore courses <ArrowRight size={16} />
              </Link>
              <Link href="/contact" className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-5 py-2.5 text-sm font-bold text-white transition hover:bg-white/10">
                Contact us
              </Link>
            </div>
          </div>

          <div>
            <p className="text-xs font-black uppercase tracking-[0.2em] text-white/40">Explore</p>
            <div className="mt-5 grid gap-3.5 text-sm text-slate-400">
              {quickLinks.map((link) => (
                <Link key={`${link.label}-${link.href}`} href={link.href} className="w-fit border-b border-transparent transition hover:border-brand/60 hover:text-white">
                  {link.label}
                </Link>
              ))}
            </div>
          </div>

          <div>
            <p className="text-xs font-black uppercase tracking-[0.2em] text-white/40">Policies</p>
            <div className="mt-5 grid gap-3.5 text-sm text-slate-400">
              {legalLinks.map((link) => (
                <Link key={`${link.label}-${link.href}`} href={link.href} className="w-fit border-b border-transparent transition hover:border-brand/60 hover:text-white">
                  {link.label}
                </Link>
              ))}
              <Link href="/admin/login" className="w-fit border-b border-transparent text-slate-500 transition hover:border-brand/60 hover:text-white">
                Content management
              </Link>
            </div>
          </div>

          <div>
            <p className="text-xs font-black uppercase tracking-[0.2em] text-white/40">Keep in touch</p>
            <p className="mt-5 text-sm leading-7 text-slate-400">
              {contactDetails.email ? "" : "Have a learning goal, a team challenge, or a partnership idea?"}
            </p>
            <div className="mt-4 flex flex-col gap-3">
              {contactDetails.email ? (
                <a href={`mailto:${contactDetails.email}`} className="flex items-center gap-2.5 text-sm font-semibold text-slate-300 transition hover:text-white">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white/10 text-brand"><Mail size={14} /></span>
                  {contactDetails.email}
                </a>
              ) : null}
              {contactDetails.phone ? (
                <a href={`tel:${contactDetails.phone}`} className="flex items-center gap-2.5 text-sm font-semibold text-slate-300 transition hover:text-white">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white/10 text-brand"><Phone size={14} /></span>
                  {contactDetails.phone}
                </a>
              ) : null}
            </div>
            <Link href="/contact" className="mt-5 inline-flex items-center gap-2 rounded-full border border-brand/30 bg-brand/10 px-4 py-2 text-sm font-bold text-white transition hover:bg-brand/20">
              Talk to {siteName}
              <ShieldCheck size={15} />
            </Link>
          </div>
        </div>
      </div>

      <div className="relative border-t border-white/10">
        <div className="wrap flex flex-col gap-2 py-6 text-xs font-medium text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <span>{copyright}</span>
          <span className="text-slate-600">Learn with intent. Build with proof.</span>
        </div>
      </div>
    </footer>
  );
}

export function SiteShell({ children }: { children: React.ReactNode }) {
  return <><PublicSEO /><SiteHeader /><Breadcrumbs />{children}<SiteFooter /></>;
}

export function Breadcrumbs() {
  const pathname = usePathname();
  if (pathname === "/") return null;
  const segments = pathname.split("/").filter(Boolean);
  return (
    <nav className="breadcrumb-wrap" aria-label="Breadcrumb">
      <ol className="wrap flex flex-wrap items-center gap-2 py-3 text-xs font-bold text-slate-500">
        <li><Link href="/" className="rounded-full bg-white px-3 py-1.5 text-slate-700 shadow-sm transition hover:text-brand focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand">Home</Link></li>
        {segments.map((segment, index) => {
          const href = `/${segments.slice(0, index + 1).join("/")}`;
          const label = segment.replaceAll("-", " ");
          const current = index === segments.length - 1;
          return (
            <li key={href} className="flex items-center gap-2">
              <span aria-hidden="true">/</span>
              {current ? <span aria-current="page" className="capitalize text-slate-700">{label}</span> : <Link href={href} className="rounded-full px-2 py-1 capitalize transition hover:bg-white hover:text-brand focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand">{label}</Link>}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

export function SectionHeading({ eyebrow, title, description, action }: { eyebrow: string; title: string; description?: string; action?: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
      <div className="max-w-3xl">
        <div className="brand-metadata"><span className="h-2 w-2 rounded-full bg-emerald-500" aria-hidden="true" />{eyebrow}</div>
        <h2 className="section-title mt-4">{title}</h2>
        {description && <p className="section-copy mt-3">{description}</p>}
      </div>
      {action}
    </div>
  );
}