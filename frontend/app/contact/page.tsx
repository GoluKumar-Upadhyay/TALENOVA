"use client";

import { FormEvent, useState } from "react";
import { Mail, MapPin, Phone, Send } from "lucide-react";
import { FeaturedSection } from "../../components/site/PublicCms";
import { SiteShell } from "../../components/site/SiteShell";
import { publicApi } from "../../lib/public-api";

type ContactType = "student" | "college" | "industry";

const options: [ContactType, string, string][] = [
  ["student", "I am a student", "Find a course, internship, or career next step"],
  ["college", "I represent a college", "Explore training and academic partnerships"],
  ["industry", "I am from industry", "Talk about hiring, projects, or team learning"],
];

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
      <main>
        <section className="page-hero">
          <div className="wrap py-20 md:py-28">
            <p className="eyebrow">Contact</p>
            <h1 className="page-title mt-4">Good work starts with a good question.</h1>
            <p className="page-lede mt-5">Tell us where you are and what you are trying to make possible. We will help you find the most useful next conversation.</p>
          </div>
        </section>
        <section className="wrap grid gap-12 py-20 lg:grid-cols-[.72fr_1.28fr]">
          <div>
            <p className="eyebrow">Let us connect</p>
            <h2 className="section-title mt-3">A real person will read this.</h2>
            <p className="section-copy mt-4">Whether you are choosing a learning path or exploring a partnership, context helps us make the conversation useful.</p>
            <div className="mt-9 grid gap-4">
              <div className="contact-detail"><Mail size={18} /><span>Write through the form<br /><small>We reply with the right context.</small></span></div>
              <div className="contact-detail"><Phone size={18} /><span>Student and partner conversations<br /><small>Scheduled around your availability.</small></span></div>
              <div className="contact-detail"><MapPin size={18} /><span>Built for learners everywhere<br /><small>Online-first, community-led.</small></span></div>
            </div>
          </div>
          <div className="form-card">
            <div className="grid gap-3 md:grid-cols-3">
              {options.map(([value, label, detail]) => (
                <button type="button" key={value} onClick={() => setType(value)} className={type === value ? "audience-option selected" : "audience-option"} aria-pressed={type === value}>
                  <strong>{label}</strong>
                  <span>{detail}</span>
                </button>
              ))}
            </div>
            {sent ? (
              <div className="success-message">
                <span className="success-check">✓</span>
                <h2>Message received.</h2>
                <p>Thank you for sharing the context. We will be in touch with a thoughtful next step.</p>
                <button className="button button-outline mt-6" onClick={() => setSent(false)}>Send another message</button>
              </div>
            ) : (
              <form className="mt-8 grid gap-5 md:grid-cols-2" onSubmit={submit}>
                <label className="form-label">Name<input name="name" required placeholder="Your name" /></label>
                <label className="form-label">Email<input name="email" required type="email" placeholder="you@example.com" /></label>
                <label className="form-label">Phone <span className="font-normal text-slate-400">(optional)</span><input name="phone" placeholder="How can we reach you?" /></label>
                <label className="form-label">Organisation {type === "college" ? <span className="font-normal text-slate-400">(required)</span> : null}<input name="organization" required={type === "college"} placeholder="College, company, or community" /></label>
                <label className="form-label">What are you exploring?<input name="subject" required placeholder="A course, partnership, project..." /></label>
                <label className="form-label">Website <span className="font-normal text-slate-400">(optional)</span><input name="website" type="url" placeholder="https://example.com" /></label>
                <label className="form-label md:col-span-2">Message<textarea name="message" required minLength={10} placeholder="A little context helps us respond well." /></label>
                {error ? <p className="md:col-span-2 text-sm font-semibold text-red-600">{error}</p> : null}
                <button className="button button-primary md:col-span-2 md:w-fit" type="submit" disabled={submitting}>{submitting ? "Sending..." : "Send message"} <Send size={16} /></button>
              </form>
            )}
          </div>
        </section>
        <FeaturedSection module="faqs" limit={4} title="Questions people ask before reaching out." />
      </main>
    </SiteShell>
  );
}
