import type React from "react"
import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Ahmad",
  description:
    "Building products that matter",
  icons: {
    icon: "/favicon.ico",
  },
  openGraph: {
    title: "Ahmad",
    description:
      "Building products that matter",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Ahmad",
    description:
      "Building products that matter",
  },
  robots: {
    index: true,
    follow: true,
  },
    generator: ''
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <div className="relative min-h-screen">
          {/* Ambient Background Effects */}
          <div className="fixed inset-0 overflow-hidden pointer-events-none">
            {/* Primary Ruby Glow */}
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-ruby-500/[0.03] rounded-full blur-3xl animate-pulse" />
            <div
              className="absolute top-3/4 right-1/4 w-96 h-96 bg-platinum-500/[0.02] rounded-full blur-3xl animate-pulse"
              style={{ animationDelay: "1s" }}
            />
            <div
              className="absolute bottom-1/4 left-1/2 w-96 h-96 bg-diamond-500/[0.02] rounded-full blur-3xl animate-pulse"
              style={{ animationDelay: "2s" }}
            />

            {/* Secondary Ambient Effects */}
            <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-ruby-600/[0.02] rounded-full blur-2xl animate-float" />
            <div
              className="absolute bottom-1/3 left-1/3 w-64 h-64 bg-platinum-400/[0.015] rounded-full blur-2xl animate-float"
              style={{ animationDelay: "3s" }}
            />

            {/* Subtle Gradient Overlay */}
            <div className="absolute inset-0 bg-gradient-to-br from-ruby-950/[0.02] via-transparent to-platinum-950/[0.02]" />
          </div>

          {/* Noise Texture Overlay */}
          <div
            className="fixed inset-0 opacity-[0.015] pointer-events-none mix-blend-overlay"
            style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
            }}
          />

          {children}
        </div>
      </body>
    </html>
  )
}
