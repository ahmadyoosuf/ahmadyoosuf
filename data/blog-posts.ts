export interface BlogPost {
  title: string
  date: string
  excerpt: string
  slug: string
}

export const blogPosts: BlogPost[] = [
  {
    title: "Agentic Cloud Security",
    date: "July 20, 2025",
    excerpt:
      "Most security tools just generate alerts. The real goal is a closed-loop system that detects, analyzes, and fixes issues automatically.",
    slug: "agentic-cloud-security",
  },
  {
    title: "Why I Hunt Bugs in Payment Systems",
    date: "January 12, 2025",
    excerpt: "The real vulnerabilities aren't in the code. They're in the assumptions about how money should move.",
    slug: "payment-systems-bugs",
  },
  {
    title: "The Myth of the Self-Made Success",
    date: "December 28, 2024",
    excerpt:
      "After mentoring 50+ first-generation professionals, I've learned that 'pulling yourself up by your bootstraps' is terrible advice.",
    slug: "myth-of-self-made",
  },
  {
    title: "Speed Is the Only Moat",
    date: "October 22, 2024",
    excerpt:
      "In a world where AI can replicate any feature in days, the only sustainable advantage is how fast you can move.",
    slug: "speed-is-the-only-moat",
  },
]
