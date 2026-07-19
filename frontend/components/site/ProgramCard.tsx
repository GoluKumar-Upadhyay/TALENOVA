import Link from "next/link";
import { ArrowUpRight, BrainCircuit, Code2, Database, Network } from "lucide-react";

const icons = [BrainCircuit, Network, Database, Code2];

export function ProgramCard({ title, description, duration, index, comingSoon = false }: { title: string; description: string; duration: string; index: number; comingSoon?: boolean }) {
  const Icon = icons[index % icons.length];
  return <article className="program-card"><div className="flex items-start justify-between"><span className="icon-tile"><Icon size={22} /></span>{comingSoon ? <span className="status-pill">Coming soon</span> : <span className="text-xs font-bold text-slate-400">0{index + 1}</span>}</div><h3 className="mt-7 text-xl font-black text-ink">{title}</h3><p className="mt-3 min-h-14 text-sm leading-6 text-slate-600">{description}</p><div className="mt-7 flex items-center justify-between border-t border-slate-100 pt-4 text-xs font-bold text-slate-500"><span>{duration}</span><Link href="/contact" className="inline-flex items-center gap-1 text-brand">Explore <ArrowUpRight size={14} /></Link></div></article>;
}

