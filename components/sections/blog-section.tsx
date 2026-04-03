"use client"

import { motion } from "framer-motion"
import Link from "next/link"
import { blogPosts } from "@/data/blog-posts"

const fadeInUp = {
  hidden: { opacity: 0, y: 60 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.8, ease: [0.25, 0.46, 0.45, 0.94] },
  },
}

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.15, delayChildren: 0.1 },
  },
}

const scaleIn = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] },
  },
}

export function BlogSection() {
  return (
    <section id="blog" className="py-16 sm:py-20 md:py-24 lg:py-32 relative section-divider">
      <div className="container relative z-10 px-4 md:px-6">
        <div className="max-w-screen-xl mx-auto">
          <motion.div
            className="text-center space-y-6 max-w-4xl mx-auto mb-20"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeInUp}
          >
            <h3 className="text-3xl font-bold text-luxury mb-4">Blog</h3>
          </motion.div>

          <motion.div
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
          >
            {blogPosts.map((post) => (
              <motion.div key={post.title} variants={scaleIn} className="luxury-glass-hover rounded-2xl p-6 group">
                <h4 className="text-lg font-bold text-diamond-200">{post.title}</h4>
                <span className="text-xs text-platinum-500">{post.date}</span>
                <p className="text-platinum-400 leading-relaxed mb-4">{post.excerpt}</p>
                <Link href={`/blog/${post.slug}`} className="text-ruby-400 hover:underline">
                  Read More
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
