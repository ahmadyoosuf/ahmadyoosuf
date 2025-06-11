import Link from "next/link"
import { ArrowLeft, Calendar, ChevronRight, Search } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

// This would typically come from a CMS or MDX files
const getBlogPosts = () => {
  return [
    {
      title: "Why I Hunt Bugs in Payment Systems",
      slug: "payment-systems-bugs",
      date: "January 12, 2025",
      category: "Security",
      excerpt: "The real vulnerabilities aren't in the code. They're in the assumptions about how money should move.",
      readTime: "8 min read",
    },
    {
      title: "The Myth of the Self-Made Success",
      slug: "myth-of-self-made",
      date: "December 28, 2024",
      category: "Leadership",
      excerpt:
        "After mentoring 50+ first-generation professionals, I've learned that 'pulling yourself up by your bootstraps' is terrible advice.",
      readTime: "12 min read",
    },
    {
      title: "Building AI Products That Actually Work",
      slug: "building-ai-products",
      date: "November 15, 2024",
      category: "AI",
      excerpt: "Lessons learned from building OCRPro and A111y - two AI products that solve real problems.",
      readTime: "10 min read",
    },
    {
      title: "Speed Is the Only Moat",
      slug: "speed-is-the-only-moat",
      date: "October 22, 2024",
      category: "Product",
      excerpt:
        "In a world where AI can replicate any feature in days, the only sustainable advantage is how fast you can move.",
      readTime: "6 min read",
    },
  ]
}

// Categories for filtering
const categories = ["All", "Security", "Leadership", "AI", "Product"]

export default function BlogPage() {
  const posts = getBlogPosts()

  return (
    <div className="min-h-screen bg-obsidian-950 text-platinum-100">
      <div className="container px-4 py-16 sm:py-20 md:py-24 mx-auto">
        <div className="max-w-screen-xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-16">
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
                Insights on security, development, leadership, and the intersection of technology with society. Deep
                dives into the challenges and opportunities shaping our digital future.
              </p>
            </div>

            <div className="w-full md:w-auto">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search articles..."
                  className="w-full md:w-80 px-4 py-3 pl-12 glass-card rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/50 text-platinum-200 placeholder-platinum-500 transition-all duration-300"
                />
                <Search className="absolute left-4 top-3.5 h-5 w-5 text-platinum-500" />
              </div>
            </div>
          </div>

          <div className="mb-12 flex flex-wrap gap-3">
            {categories.map((category) => (
              <Badge
                key={category}
                className={`px-4 py-2 text-sm cursor-pointer transition-all duration-300 ${
                  category === "All"
                    ? "bg-gradient-to-r from-emerald-500 to-sapphire-500 text-obsidian-950 hover:from-emerald-400 hover:to-sapphire-400"
                    : "glass-card-hover text-platinum-300 border-platinum-500/20"
                }`}
              >
                {category}
              </Badge>
            ))}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post, index) => (
              <div key={index} className="group glass-card-hover rounded-2xl overflow-hidden">
                <div className="p-8">
                  <div className="flex items-center justify-between mb-4">
                    <Badge className="glass-card text-platinum-300 border-platinum-500/20 px-3 py-1">
                      {post.category}
                    </Badge>
                    <span className="text-2xs text-platinum-500 uppercase tracking-wider">{post.readTime}</span>
                  </div>

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

          <div className="mt-16 flex justify-center">
            <div className="flex gap-2">
              <Button className="glass-card-hover text-platinum-200 w-12 h-12 p-0 rounded-xl">1</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
