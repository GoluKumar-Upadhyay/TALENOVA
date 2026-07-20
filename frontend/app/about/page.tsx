"use client";

import Link from "next/link";
import { Sora, Inter } from "next/font/google";
import { ArrowRight, Compass, Layers, Rocket, Sparkles, Target, Users, Quote } from "lucide-react";
import { FeaturedSection } from "../../components/site/PublicCms";
import { SiteShell } from "../../components/site/SiteShell";

// Fonts loaded right here on the About page — no layout.tsx edits required.
// Sora over Plus Jakarta Sans: Jakarta's bold weight reads too close to
// system UI fonts (SF Pro / Segoe UI) to look like a deliberate choice.
// Sora has a distinctive single-story lowercase and rounder geometry that
// visibly differs from default system sans even at a glance.
const sora = Sora({
  subsets: ["latin"],
  weight: ["600", "700", "800"],
  variable: "--font-heading",
  display: "swap",
});

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-body",
  display: "swap",
});

// ---- Design tokens ----
const INK = "#0b1220";
const SUB = "#5b6675";
const LINE = "#e6e9ef";
const BLUE = "#1d4ed8";
const GOLD = "#f5b301";
const PAPER = "#f8f9fc";

// Two-role type system:
//   HEADING -> Plus Jakarta Sans (h1/h2/h3, eyebrows, buttons)
//   BODY    -> Inter (paragraphs, longer copy) — easier to read at small sizes than Jakarta
// Both fall back to system sans, so nothing breaks even before the fonts finish loading.
const HEADING = `var(--font-heading), -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
const BODY = `var(--font-body), -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;

function Eyebrow({ children, light = false }: { children: React.ReactNode; light?: boolean }) {
  return (
    <p style={{
      fontFamily: HEADING, fontSize: 11.5, fontWeight: 700, letterSpacing: ".12em",
      textTransform: "uppercase", color: light ? "#93c5fd" : BLUE, margin: 0,
    }}>
      {children}
    </p>
  );
}

const DIFFERENTIATORS = [
  { icon: Layers, title: "Industry-built curriculum", copy: "Aligned to what teams are actually shipping with today, not last decade's syllabus." },
  { icon: Rocket, title: "Real projects, not toy demos", copy: "Every module ends in something you'd put on a portfolio, not a quiz score." },
  { icon: Sparkles, title: "AI, ML & Generative AI tracks", copy: "Deep specializations across Data Science, Deep Learning, and applied GenAI." },
  { icon: Compass, title: "Research-driven learning", copy: "Access to innovation and research opportunities most course platforms skip entirely." },
  { icon: Target, title: "Career mentorship", copy: "Portfolio reviews, interview prep, and 1:1 guidance from people who've hired." },
  { icon: Users, title: "Live, not pre-recorded", copy: "Workshops, hackathons, and internships you attend — not a video queue." },
];

const MISSION = [
  "Deliver high-quality, industry-relevant education",
  "Bridge the gap between academics and professional practice",
  "Empower learners with future-ready technical skills",
  "Foster innovation through research and real-world projects",
  "Build a community where every learner grows with confidence",
];

export default function AboutPage() {
  return (
    <SiteShell>
      <main className={`${sora.variable} ${inter.variable}`} style={{ background: "#fff", fontFamily: BODY }}>
        {/* Hero */}
        <section style={{
          position: "relative",
          background: `linear-gradient(135deg, #0f172a 0%, #1e3a5f 55%, ${BLUE} 100%)`,
          color: "#fff",
        }}>
          {/* Soft top fade so this doesn't cut hard against whatever sits above it */}
          <div style={{
            position: "absolute", top: 0, left: 0, right: 0, height: 56,
            background: "linear-gradient(to bottom, rgba(255,255,255,.35), rgba(255,255,255,0))",
            pointerEvents: "none",
          }} />
          <div className="wrap" style={{ padding: "88px 24px 72px" }}>
            <Eyebrow light>About Talenova</Eyebrow>
            <h1 style={{
              fontFamily: HEADING, fontWeight: 800, color: "#fff",
              fontSize: "clamp(2.2rem, 4.4vw, 3.4rem)", lineHeight: 1.12,
              letterSpacing: "-.03em", margin: "16px 0 0", maxWidth: 760,
            }}>
              Education that builds skills, confidence, and careers.
            </h1>
            <p style={{
              fontFamily: BODY, fontSize: 16.5, lineHeight: 1.65, color: "#bfdbfe",
              margin: "18px 0 0", maxWidth: 560,
            }}>
              A thoughtful bridge between emerging technology and the people who want to work with it well.
            </p>

            {/* Quick stat strip — swap for real numbers when available */}
            <div style={{ display: "flex", gap: 40, flexWrap: "wrap", marginTop: 48, borderTop: "1px solid rgba(255,255,255,.12)", paddingTop: 28 }}>
              {[
                ["6+", "Specialization tracks"],
                ["100%", "Project-based curriculum"],
                ["1:1", "Career mentorship"],
              ].map(([n, l]) => (
                <div key={l}>
                  <div style={{ fontFamily: HEADING, fontSize: 26, fontWeight: 800, color: "#fff" }}>{n}</div>
                  <div style={{ fontFamily: BODY, fontSize: 12.5, color: "#93c5fd", marginTop: 2 }}>{l}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Our Story */}
        <section className="wrap" style={{ padding: "72px 24px" }}>
          <div style={{ display: "grid", gridTemplateColumns: "minmax(0,.85fr) minmax(0,1.15fr)", gap: 56 }}>
            <div>
              <Eyebrow>Our Story</Eyebrow>
              <h2 style={{
                fontFamily: HEADING, fontWeight: 800, color: INK,
                fontSize: "clamp(1.6rem, 2.8vw, 2.1rem)", lineHeight: 1.2,
                letterSpacing: "-.02em", margin: "12px 0 0",
              }}>
                The future needs more than fast learners.
              </h2>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32 }}>
              <p style={{ fontFamily: BODY, fontSize: 15, lineHeight: 1.75, color: "#3d4451", margin: 0 }}>
                Technology is evolving faster than ever, but education often struggles to keep pace.
                Many students complete courses, earn certificates, and learn theories, yet still feel
                uncertain when asked to solve real-world problems or step into professional roles.
                <br /><br />
                <strong style={{ color: INK }}>TALENOVA was founded to change that.</strong> We believe
                education should not stop at teaching concepts — it should prepare learners to create,
                innovate, and lead.
              </p>
              <p style={{ fontFamily: BODY, fontSize: 15, lineHeight: 1.75, color: "#3d4451", margin: 0 }}>
                We saw that talented students had the motivation to learn but lacked guidance, mentorship,
                real-world projects, and exposure to modern technologies — while industries expected
                practical experience and problem-solving.
                <br /><br />
                To bridge that gap, we built TALENOVA as more than a course platform: a complete ecosystem
                where education meets innovation, research, and professional growth.
              </p>
            </div>
          </div>
        </section>

        {/* What Makes Us Different */}
        <section style={{ background: PAPER, borderTop: `1px solid ${LINE}`, borderBottom: `1px solid ${LINE}` }}>
          <div className="wrap" style={{ padding: "72px 24px" }}>
            <div style={{ maxWidth: 620, marginBottom: 40 }}>
              <Eyebrow>What Makes Us Different</Eyebrow>
              <h2 style={{
                fontFamily: HEADING, fontWeight: 800, color: INK,
                fontSize: "clamp(1.6rem, 2.8vw, 2.1rem)", lineHeight: 1.2,
                letterSpacing: "-.02em", margin: "12px 0 0",
              }}>
                Learning goes beyond watching videos or completing quizzes.
              </h2>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 20 }}>
              {DIFFERENTIATORS.map(({ icon: Icon, title, copy }) => (
                <div key={title} style={{
                  background: "#fff", border: `1px solid ${LINE}`, borderRadius: 12,
                  padding: "22px 20px",
                }}>
                  <div style={{
                    width: 38, height: 38, borderRadius: 9, background: "#eef3ff",
                    display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 14,
                  }}>
                    <Icon size={18} color={BLUE} />
                  </div>
                  <h3 style={{ fontFamily: HEADING, fontSize: 15, fontWeight: 700, color: INK, margin: "0 0 6px" }}>{title}</h3>
                  <p style={{ fontFamily: BODY, fontSize: 13.5, lineHeight: 1.55, color: SUB, margin: 0 }}>{copy}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Vision — quote card */}
        <section className="wrap" style={{ padding: "72px 24px" }}>
          <div style={{
            background: INK, borderRadius: 16, padding: "48px clamp(24px,5vw,64px)",
            position: "relative", overflow: "hidden",
          }}>
            <Quote size={34} color={GOLD} style={{ opacity: .9 }} />
            <Eyebrow light>
              <span style={{ color: "#93c5fd" }}>Our Vision</span>
            </Eyebrow>
            <p style={{
              fontFamily: HEADING, fontWeight: 600, color: "#fff",
              fontSize: "clamp(1.25rem, 2.4vw, 1.65rem)", lineHeight: 1.5,
              letterSpacing: "-.01em", margin: "14px 0 0", maxWidth: 780,
            }}>
              To become one of the most trusted global learning platforms where students, professionals,
              researchers, and innovators collaborate to shape the future of technology — through
              education, research, and practical innovation.
            </p>
          </div>
        </section>

        {/* Mission */}
        <section className="wrap" style={{ padding: "0 24px 80px" }}>
          <div style={{ maxWidth: 620, marginBottom: 32 }}>
            <Eyebrow>Our Mission</Eyebrow>
            <h2 style={{
              fontFamily: HEADING, fontWeight: 800, color: INK,
              fontSize: "clamp(1.6rem, 2.8vw, 2.1rem)", lineHeight: 1.2,
              letterSpacing: "-.02em", margin: "12px 0 0",
            }}>
              Five commitments that guide every program we build.
            </h2>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: 14 }}>
            {MISSION.map((item, i) => (
              <div key={i} style={{
                border: `1px solid ${LINE}`, borderRadius: 10, padding: "18px 16px",
                background: "#fff",
              }}>
                <span style={{
                  fontFamily: HEADING,
                  display: "inline-flex", width: 24, height: 24, borderRadius: 999,
                  background: BLUE, color: "#fff", fontSize: 11, fontWeight: 700,
                  alignItems: "center", justifyContent: "center", marginBottom: 12,
                }}>
                  {i + 1}
                </span>
                <p style={{ fontFamily: BODY, fontSize: 13.5, lineHeight: 1.5, color: INK, fontWeight: 600, margin: 0 }}>
                  {item}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* CMS-driven sections — see note about restyling founder/teacher cards */}
        <FeaturedSection module="content" limit={3} title="Published TALENOVA story and updates." description="This section is populated from the public Content API." />
        <FeaturedSection module="founders" limit={3} />
        <FeaturedSection module="teachers" limit={6} />
        <FeaturedSection module="partners" limit={6} />

        {/* Closing CTA */}
        <section style={{ background: `linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, ${BLUE} 100%)` }}>
          <div className="wrap" style={{
            padding: "64px 24px",
            display: "flex", justifyContent: "space-between", alignItems: "center",
            flexWrap: "wrap", gap: 24,
          }}>
            <div>
              <Eyebrow light><span style={{ color: "#93c5fd" }}>Build the future with us</span></Eyebrow>
              <h2 style={{
                fontFamily: HEADING, fontWeight: 800, color: "#fff",
                fontSize: "clamp(1.4rem, 2.6vw, 1.9rem)", margin: "10px 0 0", maxWidth: 480,
              }}>
                A good platform leaves room for you.
              </h2>
            </div>
            <Link href="/contact" style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              background: "#fff", color: BLUE, fontFamily: HEADING, fontWeight: 700,
              fontSize: 14, padding: "13px 22px", borderRadius: 9, textDecoration: "none",
              flexShrink: 0,
            }}>
              Get in touch <ArrowRight size={16} />
            </Link>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}