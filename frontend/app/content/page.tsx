"use client";

import { PublicModulePage } from "../../components/site/PublicCms";
import { SiteShell } from "../../components/site/SiteShell";

export default function ContentPage() {
  return <SiteShell><PublicModulePage module="content" /></SiteShell>;
}
