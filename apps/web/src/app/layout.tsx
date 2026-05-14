import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";

import "./globals.css";

import { TopNav } from "@/components/layout/top-nav";
import { QueryProvider } from "@/lib/query-client";
import { cn } from "@/lib/utils";

const sans = Inter({ subsets: ["latin"], variable: "--font-sans", display: "swap" });
const mono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono", display: "swap" });

export const metadata: Metadata = {
  title: "Town Crier — AI & Robotics Intelligence",
  description:
    "Real-time intelligence platform for the AI and robotics ecosystem.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={cn(sans.variable, mono.variable)}>
      <body className="min-h-screen bg-background text-foreground antialiased">
        <QueryProvider>
          <TopNav />
          <main className="container py-8">{children}</main>
        </QueryProvider>
      </body>
    </html>
  );
}
