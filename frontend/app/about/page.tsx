"use client";

import Link from "next/link";
import { ArrowRight, Compass, HeartHandshake, Lightbulb, ShieldCheck, Sparkles } from "lucide-react";
import { FeaturedSection } from "../../components/site/PublicCms";
import { SectionHeading, SiteShell } from "../../components/site/SiteShell";

const principles = [
  [Compass, "Clarity over noise", "We make the path legible: what matters now, what can wait, and what good work looks like."],
  [Lightbulb, "Curiosity with discipline", "Questions open the door. Practice, reflection, and responsible choices carry you through it."],
  [HeartHandshake, "People before polish", "Learning gets better when feedback is generous, specific, and connected to a real goal."],
  [ShieldCheck, "Trust is built in public", "We value honest process, explainable decisions, and work that can stand up to questions."],
] as const;

export default function AboutPage() {
  return (
    <SiteShell>
      <main>
        <section className="page-hero">
          <div className="wrap py-20 md:py-28">
            <p className="eyebrow">About TALENOVA</p>
            <h1 className="page-title mt-4">Education that respects the person behind the profile.</h1>
            <p className="page-lede mt-5">A thoughtful bridge between emerging technology and the people who want to work with it well.</p>
          </div>
        </section>
        <section className="wrap grid gap-12 py-20 md:grid-cols-[.9fr_1.1fr] md:items-start">
          <div><p className="eyebrow">Our story</p><h2 className="section-title mt-3">The future needs more than fast learners.</h2></div>
          <div className="space-y-5 text-lg leading-8 text-slate-600">
            <p>TALENOVA exists for the gap between knowing about a technology and knowing how to use it in the world. That gap is where confidence is made: through patient foundations, useful projects, and the right feedback at the right time.</p>
            <p>Our public website pulls directly from the CMS, so the people, courses, partners, events, and success records you see here are the current TALENOVA story.</p>
          </div>
        </section>
        <section className="tint-section">
          <div className="wrap py-20">
            <SectionHeading eyebrow="What guides us" title="A platform is only as strong as its principles." />
            <div className="mt-10 grid gap-5 md:grid-cols-2">
              {principles.map(([Icon, title, text]) => <article key={title} className="feature-card reveal"><Icon className="text-brand" /><h3>{title}</h3><p>{text}</p></article>)}
            </div>
          </div>
        </section>
        <FeaturedSection module="founders" limit={3} />
        <FeaturedSection module="teachers" limit={6} />
        <FeaturedSection module="partners" limit={6} />
        <section className="wrap py-20">
          <div className="cta-panel">
            <div><p className="eyebrow">Build the future with us</p><h2 className="mt-3 text-3xl font-black text-ink">A good platform leaves room for you.</h2></div>
            <Link href="/contact" className="button button-primary">Get in touch <ArrowRight size={16} /></Link>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}
