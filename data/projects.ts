import { Shield, Brain } from "lucide-react"
import type { LucideIcon } from "lucide-react"

export interface Project {
  title: string
  description: string
  tags: string[]
  link: string
  icon: LucideIcon
  featured?: boolean
}

export const projects: Project[] = [
  {
    title: "Amaze",
    description:
      "Agentic cloud security platform that automates vulnerability detection, analysis, and remediation for AWS environments.",
    tags: ["AI", "Cloud Security", "Automation"],
    link: "https://amazehq.vercel.app",
    icon: Shield,
  },
  {
    title: "MARSAD",
    description:
      "Social media intelligence platform led by HBKU in collaboration with institutions across Qatar, US, and UK. Designed and developed the entire platform solo in a few weeks.",
    tags: ["AI", "Data Analysis", "Full-Stack"],
    link: "https://marsadai.vercel.app",
    icon: Brain,
    featured: true,
  },
  {
    title: "A111y",
    description:
      "AI-powered accessibility checker that helps developers and designers create more inclusive digital experiences by identifying and resolving accessibility issues.",
    tags: ["AI", "Accessibility", "DevTools"],
    link: "https://a111y.vercel.app",
    icon: Shield,
  },
]
