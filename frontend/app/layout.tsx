import "./globals.css";
import Providers from "./providers";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "TALENOVA | Career transformation, by design", description: "Learn deeply, build visibly, and move into industry with confidence through TALENOVA." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body><Providers>{children}</Providers></body></html> }
