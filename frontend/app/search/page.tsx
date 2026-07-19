"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Search } from "lucide-react";
import { EmptyState, PublicCard, publicModuleConfigs, usePublicList } from "../../components/site/PublicCms";
import { SiteShell } from "../../components/site/SiteShell";

const searchableModules = ["courses", "teachers", "founders", "partners", "gallery", "videos", "achievements", "projects", "testimonials", "success-stories", "events", "internships", "faqs"] as const;

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const results = searchableModules.map((module) => ({ module, result: usePublicList(module, { pageSize: 4, search: query }) }));
  const hasQuery = query.trim().length > 1;
  const anyLoading = results.some(({ result }) => result.isLoading);
  const matches = useMemo(() => results.flatMap(({ module, result }) => (hasQuery ? result.data?.items.map((item) => ({ module, item })) || [] : [])), [hasQuery, results]);

  return (
    <SiteShell>
      <main>
        <section className="page-hero">
          <div className="wrap py-20 md:py-28">
            <p className="eyebrow">Search</p>
            <h1 className="page-title mt-4">Find TALENOVA content quickly.</h1>
            <p className="page-lede mt-5">Search across courses, teachers, founders, partners, gallery, videos, achievements, projects, testimonials, events, internships, and FAQ records.</p>
          </div>
        </section>
        <section className="wrap py-20">
          <label className="search-box max-w-3xl">
            <Search size={20} />
            <span className="sr-only">Search public website</span>
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search courses, events, projects..." autoFocus />
          </label>
          <div className="mt-10">
            {!hasQuery ? <EmptyState label="Type at least two characters to search public CMS content." /> : null}
            {hasQuery && anyLoading ? <div className="skeleton-card min-h-48" /> : null}
            {hasQuery && !anyLoading && !matches.length ? <EmptyState label="No matching public records were found." /> : null}
            {matches.length ? (
              <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
                {matches.map(({ module, item }) => <PublicCard key={`${module}-${String(item.uuid || item.id)}`} item={item} config={publicModuleConfigs[module]} compact />)}
              </div>
            ) : null}
          </div>
          <div className="mt-12 rounded-2xl border border-slate-200 bg-slate-50 p-6">
            <p className="text-sm font-bold text-slate-600">Prefer guided browsing?</p>
            <div className="mt-4 flex flex-wrap gap-3">
              {searchableModules.slice(0, 8).map((module) => <Link key={module} href={`/${module === "success-stories" ? "success" : module === "faqs" ? "faq" : module}`} className="soft-chip">{publicModuleConfigs[module].eyebrow}</Link>)}
            </div>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}
