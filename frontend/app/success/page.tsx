"use client";

import Link from "next/link";
import { ArrowRight, BriefcaseBusiness, Layers3, Quote, Trophy } from "lucide-react";
import { FeaturedSection } from "../../components/site/PublicCms";
import { SiteShell } from "../../components/site/SiteShell";

export default function SuccessPage() {
  return (
    <SiteShell>
      <main>
        <section className="page-hero">
          <div className="wrap py-20 md:py-28">
            <p className="eyebrow">Success stories</p>
            <h1 className="page-title mt-4">Progress looks different on everyone. Proof helps you see it.</h1>
            <p className="page-lede mt-5">We celebrate the work between the before and after: the project, the question, the review, and the moment a learner realises they can do more than they thought.</p>
          </div>
        </section>
        <FeaturedSection module="success-stories" limit={6} title="Learner journeys with real context." />
        <section className="dark-section">
          <div className="wrap py-20">
            <div className="mx-auto max-w-3xl text-center">
              <Quote className="mx-auto text-blue-300" size={34} />
              <blockquote className="mt-6 text-2xl font-black leading-10 text-white md:text-3xl">The strongest outcome is not a certificate. It is being able to explain what you made, why you made it, and what you would improve next.</blockquote>
              <p className="mt-6 text-sm font-bold text-blue-200">The TALENOVA learning philosophy</p>
            </div>
            <div className="mt-16 grid gap-5 md:grid-cols-3">
              <div className="dark-metric"><BriefcaseBusiness /><strong>Learn</strong><span>with a reason</span></div>
              <div className="dark-metric"><Layers3 /><strong>Build</strong><span>with a point of view</span></div>
              <div className="dark-metric"><Trophy /><strong>Move</strong><span>with more confidence</span></div>
            </div>
          </div>
        </section>
        <FeaturedSection module="testimonials" limit={6} />
        <FeaturedSection module="achievements" limit={6} />
        <FeaturedSection module="projects" limit={6} />
        <section className="wrap pb-10">
          <Link href="/contact" className="link-panel">
            <span><span className="eyebrow">Your story can start here</span><strong className="mt-2 block text-xl text-ink">What would you like to make possible?</strong></span>
            <ArrowRight className="text-brand" />
          </Link>
        </section>
      </main>
    </SiteShell>
  );
}
