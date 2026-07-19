"use client";

import { useQuery } from "@tanstack/react-query";
import { FileText } from "lucide-react";
import { activeRecords, normalizePublicPage, publicApi, queryPath, type PublicPageResponse, type PublicRecord } from "../../lib/public-api";
import { EmptyState } from "./PublicCms";
import { SiteShell } from "./SiteShell";

function titleFor(slug: string) {
  if (slug === "privacy") return "Privacy Policy";
  if (slug === "terms") return "Terms of Use";
  return "Cookie Policy";
}

export function LegalPage({ slug }: { slug: "privacy" | "terms" | "cookies" }) {
  const result = useQuery({
    queryKey: ["legal-content", slug],
    queryFn: () => publicApi<PublicRecord[] | PublicPageResponse<PublicRecord>>(queryPath("/content/content", { page: 1, page_size: 5, search: slug, sort: "display_order", direction: "asc" })),
    select: (data) => activeRecords(normalizePublicPage(data).items).find((item) => item.slug === slug || String(item.title || "").toLowerCase().includes(slug)),
  });
  const title = typeof result.data?.title === "string" ? result.data.title : titleFor(slug);
  const content = typeof result.data?.content === "string" ? result.data.content : "";

  return (
    <SiteShell>
      <main>
        <section className="page-hero">
          <div className="wrap py-20 md:py-28">
            <p className="eyebrow">Policy</p>
            <h1 className="page-title mt-4">{title}</h1>
            <p className="page-lede mt-5">This page is managed from the TALENOVA Content API so published policy text stays current.</p>
          </div>
        </section>
        <section className="wrap py-20">
          {result.isLoading ? <div className="skeleton-card min-h-80" /> : null}
          {result.isError ? <EmptyState label="Unable to load this policy right now." /> : null}
          {!result.isLoading && !result.isError && !content ? <EmptyState label={`${title} has not been published yet.`} /> : null}
          {content ? (
            <article className="prose max-w-none rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
              <div className="mb-6 flex items-center gap-3 text-brand"><FileText /><span className="text-sm font-black uppercase tracking-wider">CMS managed policy</span></div>
              <div dangerouslySetInnerHTML={{ __html: content }} />
            </article>
          ) : null}
        </section>
      </main>
    </SiteShell>
  );
}
