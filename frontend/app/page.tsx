"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Check, CirclePlay, Layers3, Rocket, ShieldCheck, Sparkles, Target, UsersRound } from "lucide-react";
import { SectionHeading, SiteShell } from "../components/site/SiteShell";
import { FeaturedSection, PublicCard, TrustStrip, publicModuleConfigs, usePublicList } from "../components/site/PublicCms";
import { activeRecords, normalizePublicPage, publicApi, queryPath, type PublicRecord } from "../lib/public-api";

function heroText(value: unknown, fallback: string) {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function HomeHero() {
  const hero = useQuery({
    queryKey: ["public-hero"],
    queryFn: () => publicApi<PublicRecord[] | PublicRecord>(queryPath("/hero", { page: 1, page_size: 1, sort: "display_order", direction: "asc" })),
    select: (data) => activeRecords(normalizePublicPage(data).items)[0],
  });
  const record = hero.data;
  const heading = heroText(record?.heading, "Become the person industry is ready for.");
  const subheading = heroText(record?.subheading, "Career transformation, by design");
  const description = heroText(record?.description, "TALENOVA helps ambitious students move from consuming courses to creating credible work through learning, projects, mentorship, internships, and placement support.");
  const buttonText = heroText(record?.button_text, "Explore courses");
  const buttonLink = heroText(record?.button_link, "/courses");
  const image = heroText(record?.hero_image_url, "");

  return (
    <section className="hero-section">
      <div className="wrap grid gap-14 py-16 md:grid-cols-[1.05fr_.95fr] md:items-center md:py-24">
        <div className="reveal">
          <p className="eyebrow">{subheading}</p>
          <h1 className="hero-title mt-5">{heading}</h1>
          <div className="hero-copy mt-6" dangerouslySetInnerHTML={{ __html: description }} />
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href={buttonLink} className="button button-primary">{buttonText} <ArrowRight size={17} /></Link>
            <Link href="/about" className="button button-outline"><CirclePlay size={17} /> See how it works</Link>
          </div>
          <div className="mt-8 flex flex-wrap gap-x-6 gap-y-3 text-sm font-semibold text-slate-600">
            {["Real projects", "Expert mentorship", "Placement support"].map((item) => <span key={item} className="inline-flex items-center gap-2"><Check size={16} className="text-brand" /> {item}</span>)}
          </div>
        </div>
        <div className="journey-art reveal">
          {image ? <img src={image} alt="" className="absolute inset-0 h-full w-full object-cover opacity-30" /> : null}
          <div className="journey-orbit orbit-one" />
          <div className="journey-orbit orbit-two" />
          <div className="journey-core"><Sparkles size={34} /><span>your next<br /><b>breakthrough</b></span></div>
          <div className="journey-node node-one"><Layers3 size={18} /><span>Learn</span></div>
          <div className="journey-node node-two"><Rocket size={18} /><span>Build</span></div>
          <div className="journey-node node-three"><Target size={18} /><span>Launch</span></div>
          <div className="journey-caption">A clearer path from curiosity<br />to career confidence.</div>
        </div>
      </div>
    </section>
  );
}

function LearningLoop() {
  const steps = [
    ["01", "Learn", "Build the foundations and mental models that make advanced work approachable.", UsersRound],
    ["02", "Build", "Turn concepts into projects with decisions, trade-offs, and a visible point of view.", Layers3],
    ["03", "Intern", "Work through a professional workflow with feedback, reviews, and real constraints.", Rocket],
    ["04", "Get placed", "Leave with proof you can explain: a portfolio, confidence, and a clearer next move.", ShieldCheck],
  ] as const;
  return (
    <section className="wrap py-20">
      <SectionHeading eyebrow="Why TALENOVA" title="Every step leaves evidence." description="The goal is not to finish another course. It is to become more capable, more visible, and more ready." />
      <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        {steps.map(([number, title, text, Icon]) => <article key={title} className="process-card reveal"><span className="process-number">{number}</span><div className="process-icon"><Icon size={20} /></div><h3 className="mt-6 text-lg font-black">{title}</h3><p className="mt-3 text-sm leading-6 text-slate-600">{text}</p></article>)}
      </div>
    </section>
  );
}

function PartnersPreview() {
  const partners = usePublicList("partners", { pageSize: 8 });
  const items = partners.data?.items || [];
  return (
    <section className="tint-section">
      <div className="wrap py-20">
        <SectionHeading eyebrow="Partners" title="A learning ecosystem grows through collaboration." description="Colleges, companies, communities, and technology partners help TALENOVA make education more practical." action={<Link href="/partners" className="button button-outline">View partners <ArrowRight size={16} /></Link>} />
        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {items.length ? items.map((item) => <PublicCard key={String(item.uuid || item.id || item.name)} item={item} config={publicModuleConfigs.partners} compact />) : <div className="empty-state sm:col-span-2 lg:col-span-4"><p>No partners are published right now.</p></div>}
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  return (
    <SiteShell>
      <main>
        <HomeHero />
        <TrustStrip />
        <FeaturedSection module="courses" limit={4} title="Choose a direction. Then make it yours." description="Focused courses for skills that are changing how teams build, decide, and grow." />
        <LearningLoop />
        <FeaturedSection module="projects" limit={3} title="Build work you are proud to walk through." description="Projects are where learning becomes a professional story with decisions, tools, and proof." />
        <FeaturedSection module="achievements" limit={3} />
        <FeaturedSection module="testimonials" limit={3} />
        <FeaturedSection module="events" limit={3} />
        <FeaturedSection module="internships" limit={3} />
        <PartnersPreview />
        <FeaturedSection module="gallery" limit={6} />
        <FeaturedSection module="faqs" limit={4} />
        <section className="wrap py-20">
          <div className="cta-panel">
            <div>
              <p className="eyebrow">Your next chapter starts with a conversation</p>
              <h2 className="mt-3 max-w-xl text-3xl font-black text-ink md:text-4xl">Bring your ambition. We will help shape the route.</h2>
            </div>
            <Link href="/contact" className="button button-primary">Talk to TALENOVA <ArrowRight size={17} /></Link>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}
