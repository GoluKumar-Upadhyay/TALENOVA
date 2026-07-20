"use client";

import { FormEvent, useState } from "react";
import { Sora, Inter } from "next/font/google";
import { Mail, MapPin, Phone, Send, CheckCircle2 } from "lucide-react";
import { FeaturedSection } from "../../components/site/PublicCms";
import { SiteShell } from "../../components/site/SiteShell";
import { publicApi } from "../../lib/public-api";

const sora = Sora({ subsets: ["latin"], weight: ["600", "700", "800"], variable: "--font-heading", display: "swap" });
const inter = Inter({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-body", display: "swap" });
const HEADING = `var(--font-heading), -apple-system, sans-serif`;
const BODY = `var(--font-body), -apple-system, sans-serif`;

const INK = "#0b1220";
const SUB = "#5b6675";
const LINE = "#e6e9ef";
const BLUE = "#1d4ed8";
const PAPER = "#f8f9fc";

type ContactType = "student" | "college" | "industry";

const options: [ContactType, string, string][] = [
  ["student", "I am a student", "Find a course, internship, or career next step"],
  ["college", "I represent a college", "Explore training and academic partnerships"],
  ["industry", "I am from industry", "Talk about hiring, projects, or team learning"],
];

const inputStyle: React.CSSProperties = {
  width: "100%", padding: "11px 13px", marginTop: 6, boxSizing: "border-box",
  border: `1px solid ${LINE}`, borderRadius: 9, fontSize: 13.5,
  fontFamily: BODY, color: INK, outline: "none", background: "#fff",
};

const labelStyle: React.CSSProperties = {
  fontFamily: BODY, fontSize: 12.5, fontWeight: 700, color: INK,
};

export default function ContactPage() {
  const [type, setType] = useState<ContactType>("student");
  const [sent, setSent] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    const form = new FormData(event.currentTarget);
    const data = Object.fromEntries(form.entries());
    try {
      await publicApi("/contact", { method: "POST", body: JSON.stringify({ ...data, contact_type: type }) });
      setSent(true);
      event.currentTarget.reset();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "We could not send your message. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <SiteShell>
      <main className={`${sora.variable} ${inter.variable}`} style={{ background: "#fff" }}>
        {/* Hero — light, no gradient block */}
        {/* Hero */}
<section style={{
  background: `radial-gradient(circle at 12% 0%, #eef3ff 0%, ${PAPER} 45%, #fff 100%)`,
}}>
  <div className="wrap" style={{ padding: "60px 24px 44px" }}>
    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
      <span style={{ width: 6, height: 6, borderRadius: 999, background: BLUE }} />
      <p style={{
        fontFamily: HEADING, fontSize: 11.5, fontWeight: 700, letterSpacing: ".12em",
        textTransform: "uppercase", color: BLUE, margin: 0,
      }}>
        Contact
      </p>
    </div>

    <h1 style={{
      fontFamily: HEADING, fontWeight: 800, color: INK,
      fontSize: "clamp(1.85rem, 3.4vw, 2.5rem)", lineHeight: 1.18,
      letterSpacing: "-.02em", margin: 0, maxWidth: 600,
    }}>
      Good work starts with a good question.
    </h1>

    <p style={{
      fontFamily: BODY, fontSize: 14.5, lineHeight: 1.6, color: SUB,
      margin: "14px 0 0", maxWidth: 500,
    }}>
      Tell us where you are and what you are trying to make possible. We will help you find the most useful next conversation.
    </p>

    {/* Trust row — quiet, not a colored badge */}
    <div style={{
      display: "flex", gap: 22, flexWrap: "wrap", marginTop: 28,
      paddingTop: 22, borderTop: `1px solid ${LINE}`,
    }}>
      {[
        "Real reply, not a bot",
        "Usually within 1 business day",
        "For students, colleges & industry",
      ].map((item) => (
        <div key={item} style={{ display: "flex", alignItems: "center", gap: 7 }}>
          <span style={{ width: 4, height: 4, borderRadius: 999, background: "#94a3b8" }} />
          <span style={{ fontFamily: BODY, fontSize: 12.5, color: SUB, fontWeight: 500 }}>{item}</span>
        </div>
      ))}
    </div>
  </div>
</section>

        {/* Body */}
        <section className="wrap" style={{ padding: "64px 24px 80px" }}>
          <div style={{ display: "grid", gridTemplateColumns: "minmax(0,.72fr) minmax(0,1.28fr)", gap: 48 }}>
            {/* Left column */}
            <div>
              
              <h2 style={{
                fontFamily: HEADING, fontWeight: 800, color: INK,
                fontSize: "clamp(1.3rem, 2.2vw, 1.6rem)", lineHeight: 1.25,
                letterSpacing: "-.01em", margin: "10px 0 0",
              }}>
                A real person will read this.
              </h2>
              <p style={{ fontFamily: BODY, fontSize: 14, lineHeight: 1.65, color: SUB, margin: "12px 0 0" }}>
                Whether you are choosing a learning path or exploring a partnership, context helps us make the conversation useful.
              </p>

              <div style={{ display: "grid", gap: 12, marginTop: 32 }}>
                {[
                  { Icon: Mail, title: "Write through the form", sub: "We reply with the right context." },
                  { Icon: Phone, title: "Student and partner conversations", sub: "Scheduled around your availability." },
                  { Icon: MapPin, title: "Built for learners everywhere", sub: "Online-first, community-led." },
                ].map(({ Icon, title, sub }, i) => (
                  <div key={i} style={{
                    display: "flex", gap: 12, alignItems: "flex-start",
                    border: `1px solid ${LINE}`, borderRadius: 11, padding: "14px 16px", background: "#fff",
                  }}>
                    <div style={{
                      width: 34, height: 34, borderRadius: 9, background: "#eef3ff", flexShrink: 0,
                      display: "flex", alignItems: "center", justifyContent: "center",
                    }}>
                      <Icon size={16} color={BLUE} />
                    </div>
                    <div>
                      <p style={{ fontFamily: HEADING, fontSize: 13, fontWeight: 700, color: INK, margin: 0 }}>{title}</p>
                      <p style={{ fontFamily: BODY, fontSize: 12, color: SUB, margin: "2px 0 0" }}>{sub}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right column — form card */}
            <div style={{ border: `1px solid ${LINE}`, borderRadius: 16, padding: "clamp(20px,3vw,32px)", background: "#fff" }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10 }}>
                {options.map(([value, label, detail]) => {
                  const active = type === value;
                  return (
                    <button
                      type="button"
                      key={value}
                      onClick={() => setType(value)}
                      aria-pressed={active}
                      style={{
                        textAlign: "left", padding: "14px 14px", borderRadius: 11, cursor: "pointer",
                        border: `1.5px solid ${active ? BLUE : LINE}`,
                        background: active ? "#eef3ff" : "#fff",
                        transition: "border-color .15s ease, background .15s ease",
                      }}
                    >
                      <strong style={{ display: "block", fontFamily: HEADING, fontSize: 12.5, fontWeight: 700, color: active ? BLUE : INK }}>
                        {label}
                      </strong>
                      <span style={{ display: "block", fontFamily: BODY, fontSize: 11, color: SUB, marginTop: 4, lineHeight: 1.4 }}>
                        {detail}
                      </span>
                    </button>
                  );
                })}
              </div>

              {sent ? (
                <div style={{ textAlign: "center", padding: "48px 12px 24px" }}>
                  <CheckCircle2 size={40} color={BLUE} style={{ marginBottom: 14 }} />
                  <h2 style={{ fontFamily: HEADING, fontSize: 18, fontWeight: 800, color: INK, margin: 0 }}>Message received.</h2>
                  <p style={{ fontFamily: BODY, fontSize: 13.5, color: SUB, margin: "8px 0 0", maxWidth: 380, marginLeft: "auto", marginRight: "auto" }}>
                    Thank you for sharing the context. We will be in touch with a thoughtful next step.
                  </p>
                  <button
                    onClick={() => setSent(false)}
                    style={{
                      marginTop: 20, padding: "10px 18px", borderRadius: 9, border: `1px solid ${LINE}`,
                      background: "#fff", fontFamily: BODY, fontWeight: 700, fontSize: 13, color: INK, cursor: "pointer",
                    }}
                  >
                    Send another message
                  </button>
                </div>
              ) : (
                <form onSubmit={submit} style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 24 }}>
                  <label style={labelStyle}>
                    Name
                    <input name="name" required placeholder="Your name" style={inputStyle} />
                  </label>
                  <label style={labelStyle}>
                    Email
                    <input name="email" required type="email" placeholder="you@example.com" style={inputStyle} />
                  </label>
                  <label style={labelStyle}>
                    Phone <span style={{ fontWeight: 400, color: "#94a3b8" }}></span>
                    <input name="phone" placeholder="How can we reach you?" style={inputStyle} />
                  </label>
                  <label style={labelStyle}>
                    Organisation {type === "college" ? <span style={{ fontWeight: 400, color: "#94a3b8" }}>(required)</span> : null}
                    <input name="organization" required={type === "college"} placeholder="College, company, or community" style={inputStyle} />
                  </label>
                  <label style={labelStyle}>
                    What are you exploring?
                    <input name="subject" required placeholder="A course, partnership, project..." style={inputStyle} />
                  </label>
                  <label style={labelStyle}>
                    Website <span style={{ fontWeight: 400, color: "#94a3b8" }}>(optional)</span>
                    <input name="website" type="url" placeholder="https://example.com" style={inputStyle} />
                  </label>
                  <label style={{ ...labelStyle, gridColumn: "1 / -1" }}>
                    Message
                    <textarea name="message" required minLength={10} placeholder="A little context helps us respond well." style={{ ...inputStyle, minHeight: 96, resize: "vertical", fontFamily: BODY }} />
                  </label>
                  {error ? (
                    <p style={{ gridColumn: "1 / -1", fontFamily: BODY, fontSize: 13, fontWeight: 600, color: "#dc2626", margin: 0 }}>{error}</p>
                  ) : null}
                  <button
                    type="submit"
                    disabled={submitting}
                    style={{
                      gridColumn: "1 / -1", justifySelf: "start",
                      display: "inline-flex", alignItems: "center", gap: 8,
                      padding: "12px 22px", borderRadius: 10, border: "none",
                      background: submitting ? "#93b4f0" : BLUE, color: "#fff",
                      fontFamily: HEADING, fontWeight: 700, fontSize: 13.5,
                      cursor: submitting ? "default" : "pointer",
                    }}
                  >
                    {submitting ? "Sending..." : "Send message"} <Send size={15} />
                  </button>
                </form>
              )}
            </div>
          </div>
        </section>

        <FeaturedSection module="faqs" limit={4} title="Questions people ask before reaching out." />
      </main>
    </SiteShell>
  );
}