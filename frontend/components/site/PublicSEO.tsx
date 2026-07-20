"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { activeRecords, normalizePublicPage, publicApi, queryPath, type PublicPageResponse, type PublicRecord } from "../../lib/public-api";

function pageKey(pathname: string) {
  if (pathname === "/") return "home";
  const segment = pathname.split("/").filter(Boolean)[0] || "home";
  if (segment === "success") return "success-stories";
  if (segment === "faq") return "faqs";
  return segment;
}

function text(value: unknown) {
  return typeof value === "string" ? value.trim() : "";
}

function ensureMeta(selector: string, create: () => HTMLMetaElement) {
  let element = document.head.querySelector<HTMLMetaElement>(selector);
  if (!element) {
    element = create();
    document.head.appendChild(element);
  }
  return element;
}

function setNamedMeta(name: string, content: string) {
  if (!content) return;
  const element = ensureMeta(`meta[name="${name}"]`, () => {
    const meta = document.createElement("meta");
    meta.setAttribute("name", name);
    return meta;
  });
  element.setAttribute("content", content);
}

function setPropertyMeta(property: string, content: string) {
  if (!content) return;
  const element = ensureMeta(`meta[property="${property}"]`, () => {
    const meta = document.createElement("meta");
    meta.setAttribute("property", property);
    return meta;
  });
  element.setAttribute("content", content);
}

function setCanonical(url: string) {
  if (!url) return;
  let element = document.head.querySelector<HTMLLinkElement>('link[rel="canonical"]');
  if (!element) {
    element = document.createElement("link");
    element.setAttribute("rel", "canonical");
    document.head.appendChild(element);
  }
  element.setAttribute("href", url);
}

function upsertStructuredData(data: unknown) {
  const id = "talenova-structured-data";
  const existing = document.getElementById(id);
  if (existing) existing.remove();
  if (!data) return;
  const script = document.createElement("script");
  script.id = id;
  script.type = "application/ld+json";
  script.textContent = typeof data === "string" ? data : JSON.stringify(data);
  document.head.appendChild(script);
}

export function PublicSEO() {
  const pathname = usePathname();
  const key = pageKey(pathname);
  const origin = typeof window !== "undefined" ? window.location.origin : "";
  const seo = useQuery({
    queryKey: ["public-seo", key],
    queryFn: () => publicApi<PublicRecord[] | PublicPageResponse<PublicRecord>>(queryPath("/seo", { page: 1, page_size: 5, search: key, sort: "page_key", direction: "asc" })),
    select: (data) => activeRecords(normalizePublicPage(data).items).find((item) => item.page_key === key || item.page_key === pathname || text(item.meta_title).toLowerCase().includes(key)),
  });
  const settings = useQuery({
    queryKey: ["public-seo-settings"],
    queryFn: () => publicApi<PublicRecord[] | PublicPageResponse<PublicRecord> | PublicRecord>("/settings/all"),
    select: (data) => normalizePublicPage(data).items[0],
  });

  useEffect(() => {
    const record = seo.data;
    const siteName = text(settings.data?.site_name) || "TALENOVA";
    const defaultTitle = pathname === "/" ? siteName : `${key.replaceAll("-", " ")} | ${siteName}`;
    const title = text(record?.meta_title) || text(record?.site_title) || defaultTitle;
    const description = text(record?.meta_description) || text(settings.data?.tagline);
    const canonical = text(record?.canonical_url) || (origin ? `${origin}${pathname}` : "");
    const robots = text(record?.robots_meta) || "index,follow";
    const openGraph = typeof record?.open_graph === "object" && record.open_graph ? record.open_graph as Record<string, unknown> : {};
    const twitterCards = typeof record?.twitter_cards === "object" && record.twitter_cards ? record.twitter_cards as Record<string, unknown> : {};

    document.title = title;
    setNamedMeta("description", description);
    setNamedMeta("robots", robots);
    setNamedMeta("twitter:card", text(twitterCards.card) || "summary_large_image");
    setNamedMeta("twitter:title", text(twitterCards.title) || title);
    setNamedMeta("twitter:description", text(twitterCards.description) || description);
    setPropertyMeta("og:title", text(openGraph.title) || title);
    setPropertyMeta("og:description", text(openGraph.description) || description);
    setPropertyMeta("og:type", text(openGraph.type) || "website");
    setPropertyMeta("og:url", canonical);
    setCanonical(canonical);
    upsertStructuredData(record?.structured_data);
  }, [key, origin, pathname, seo.data, settings.data]);

  return null;
}
