import Link from "next/link";
import { ArrowLeft, Search } from "lucide-react";
import { SiteShell } from "../components/site/SiteShell";

export default function NotFound() {
  return (
    <SiteShell>
      <main>
        <section className="page-hero">
          <div className="wrap py-24 text-center md:py-32">
            <p className="eyebrow">404</p>
            <h1 className="page-title mx-auto mt-4">This page is not available.</h1>
            <p className="page-lede mx-auto mt-5">The link may have moved, or the CMS record behind it may no longer be published.</p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <Link href="/" className="button button-primary"><ArrowLeft size={16} /> Back home</Link>
              <Link href="/search" className="button button-outline"><Search size={16} /> Search TALENOVA</Link>
            </div>
          </div>
        </section>
      </main>
    </SiteShell>
  );
}
