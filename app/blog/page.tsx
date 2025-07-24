import Link from "next/link"
import { ArrowLeft, Calendar, ChevronRight } from "lucide-react"

// This would typically come from a CMS or MDX files
const getBlogPosts = () => {
  return [
    {
      title: "Agentic Cloud Security",
      slug: "agentic-cloud-security",
      date: "July 20, 2025",
      category: "Security",
      excerpt:
        "Most security tools just generate alerts. The real goal is a closed-loop system that detects, analyzes, and fixes issues automatically.",
    },
    {
      title: "Why I Hunt Bugs in Payment Systems",
      slug: "payment-systems-bugs",
      date: "January 12, 2025",
      category: "Security",
      excerpt: "The real vulnerabilities aren't in the code. They're in the assumptions about how money should move.",
    },
    {
      title: "The Myth of the Self-Made Success",
      slug: "myth-of-self-made",
      date: "December 28, 2024",
      category: "Leadership",
      excerpt:
        "After mentoring 50+ first-generation professionals, I've learned that 'pulling yourself up by your bootstraps' is terrible advice.",
    },
    {
      title: "Speed Is the Only Moat",
      slug: "speed-is-the-only-moat",
      date: "October 22, 2024",
      category: "Product",
      excerpt:
        "In a world where AI can replicate any feature in days, the only sustainable advantage is how fast you can move.",
    },
  ]
}

export default function BlogPage() {
  const posts = getBlogPosts()

  return (
    <div className="min-h-screen bg-obsidian-950 text-platinum-100">
      <div className="container px-4 py-16 sm:py-20 md:py-24 mx-auto">
        <div className="max-w-screen-xl mx-auto">
          <div className="flex flex-col justify-between items-start gap-6 mb-16">
            <div>
              <Link
                href="/"
                className="inline-flex items-center text-sm text-platinum-500 hover:text-emerald-400 mb-6 transition-colors group"
              >
                <ArrowLeft className="mr-2 h-4 w-4 group-hover:-translate-x-1 transition-transform duration-300" />
                Back to home
              </Link>
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gradient mb-4">Blog</h1>
              <p className="text-platinum-400 max-w-2xl leading-relaxed text-lg">
                Insights on security, development, leadership, and the intersection of technology with society.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post, index) => (
              <div key={index} className="group glass-card-hover rounded-2xl overflow-hidden">
                <div className="p-8">
                  <div className="flex items-center gap-2 mb-4">
                    <Calendar className="h-4 w-4 text-platinum-500" />
                    <span className="text-sm text-platinum-500">{post.date}</span>
                  </div>

                  <h2 className="text-xl font-bold mb-3 group-hover:text-gradient transition-colors duration-300 leading-tight">
                    <Link href={`/blog/${post.slug}`}>{post.title}</Link>
                  </h2>

                  <p className="text-platinum-400 leading-relaxed mb-6 text-sm">{post.excerpt}</p>

                  <Link
                    href={`/blog/${post.slug}`}
                    className="text-emerald-400 flex items-center gap-2 font-medium hover:text-emerald-300 transition-colors group"
                  >
                    <span className="group-hover:scale-105 transition-transform duration-300">Read More</span>
                    <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
