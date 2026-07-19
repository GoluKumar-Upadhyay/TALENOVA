"use client";

import { PublicModulePage } from "../../components/site/PublicCms";
import { SiteShell } from "../../components/site/SiteShell";

export default function CoursesPage() {
  return <SiteShell><PublicModulePage module="courses" /></SiteShell>;
}
