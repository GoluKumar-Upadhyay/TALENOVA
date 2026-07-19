"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Menu, X } from "lucide-react";
import { useState } from "react";
import { activeRecords, normalizePublicPage, publicApi, queryPath, type PublicPageResponse, type PublicRecord } from "../../lib/public-api";

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

  return (
    <header className="site-header">
      <div className="wrap flex h-20 items-center justify-between">
        <Link href="/" className="flex items-center gap-3" onClick={() => setOpen(false)} aria-label={`${siteName} home`}>
          {logo ? <img src={logo} alt="" className="h-10 w-10 rounded-xl object-contain" /> : <span className="brand-mark">T</span>}
          <span className="text-xl font-black tracking-tight text-ink">{siteName}</span>
        </Link>
        <nav className="hidden items-center gap-6 md:flex" aria-label="Primary navigation">
          <Link className={pathname === "/" ? "nav-link active" : "nav-link"} href="/">Home</Link>
          {links.map(([label, href]) => (
            <Link key={`${label}-${href}`} className={pathname.startsWith(href) ? "nav-link active" : "nav-link"} href={href}>{label}</Link>
          ))}
        </nav>
        <div className="hidden items-center gap-3 md:flex">
          <Link href="/search" className="button button-outline">Search</Link>
          <Link href="/contact" className="button button-primary">Start a conversation</Link>
        </div>
        <button className="rounded-xl border border-slate-200 p-2 md:hidden" onClick={() => setOpen((value) => !value)} aria-label={open ? "Close menu" : "Open menu"} aria-expanded={open}>
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>
      {open && (
        <div className="border-t border-slate-100 bg-white px-6 pb-5 md:hidden">
          <nav className="wrap flex flex-col gap-1 pt-3" aria-label="Mobile navigation">
            <Link className="mobile-nav-link" href="/" onClick={() => setOpen(false)}>Home</Link>
            {links.map(([label, href]) => <Link key={`${label}-${href}`} className="mobile-nav-link" href={href} onClick={() => setOpen(false)}>{label}</Link>)}
            <Link className="button button-primary mt-3 text-center" href="/contact" onClick={() => setOpen(false)}>Start a conversation</Link>
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
  const copyright = getText(record, "copyright_text", `© ${new Date().getFullYear()} ${siteName}. All rights reserved.`);
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
    <footer className="mt-24 border-t border-slate-200 bg-slate-50">
      <div className="wrap grid gap-10 py-14 md:grid-cols-[1.5fr_1fr_1fr_1.2fr]">
        <div>
          <div className="flex items-center gap-3">
            {logo ? <img src={logo} alt="" className="h-10 w-10 rounded-xl object-contain" /> : <span className="brand-mark">T</span>}
            <span className="text-xl font-black text-ink">{siteName}</span>
          </div>
          <div className="mt-5 max-w-sm text-sm leading-7 text-slate-600" dangerouslySetInnerHTML={{ __html: description }} />
        </div>
        <div>
          <p className="footer-heading">Explore</p>
          <div className="mt-4 grid gap-3 text-sm">
            {quickLinks.map((link) => <Link key={`${link.label}-${link.href}`} href={link.href}>{link.label}</Link>)}
          </div>
        </div>
        <div>
          <p className="footer-heading">Policies</p>
          <div className="mt-4 grid gap-3 text-sm">
            {legalLinks.map((link) => <Link key={`${link.label}-${link.href}`} href={link.href}>{link.label}</Link>)}
            <Link href="/admin/login">Content management</Link>
          </div>
        </div>
        <div>
          <p className="footer-heading">Keep in touch</p>
          <p className="mt-4 text-sm leading-7 text-slate-600">{contactDetails.email || "Have a learning goal, a team challenge, or a partnership idea?"}</p>
          {contactDetails.phone ? <p className="mt-2 text-sm font-bold text-slate-600">{contactDetails.phone}</p> : null}
          <Link href="/contact" className="mt-4 inline-flex text-sm font-bold text-brand">Talk to {siteName} <span aria-hidden="true" className="ml-2">→</span></Link>
        </div>
      </div>
      <div className="wrap flex flex-col gap-2 border-t border-slate-200 py-5 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
        <span>{copyright}</span>
        <span>Learn with intent. Build with proof.</span>
      </div>
    </footer>
  );
}

export function SiteShell({ children }: { children: React.ReactNode }) {
  return <><SiteHeader />{children}<SiteFooter /></>;
}

export function SectionHeading({ eyebrow, title, description, action }: { eyebrow: string; title: string; description?: string; action?: React.ReactNode }) {
  return <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between"><div className="max-w-2xl"><p className="eyebrow">{eyebrow}</p><h2 className="section-title mt-3">{title}</h2>{description && <p className="section-copy mt-4">{description}</p>}</div>{action}</div>;
}
