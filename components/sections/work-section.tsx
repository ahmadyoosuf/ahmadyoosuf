"use client"

import { motion } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight } from "lucide-react"
import { projects } from "@/data/projects"

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

export function WorkSection() {
  return (
    <section id="work" className="py-16 sm:py-20 md:py-24 lg:py-32 relative section-divider">
      <div className="container relative z-10 px-4 md:px-6">
        <div className="max-w-screen-xl mx-auto">
          <motion.div
            className="text-center space-y-6 max-w-4xl mx-auto mb-20"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeInUp}
          >
            <div className="text-platinum-400 font-semibold text-5xl">Selected Work</div>
          </motion.div>

          <motion.div
            className="space-y-16"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
          >
            <motion.div variants={fadeInUp}>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects.map((project) => (
                  <motion.div
                    key={project.title}
                    variants={scaleIn}
                    className="luxury-glass-hover rounded-2xl p-8 group"
                  >
                    <div className="flex items-center gap-4 mb-6">
                      <h4 className="text-xl font-semibold text-diamond-200">{project.title}</h4>
                    </div>

                    <p className="text-platinum-400 leading-relaxed mb-6">{project.description}</p>

                    <Button
                      size="lg"
                      className="bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg px-6 py-3 text-sm font-medium transition-all duration-300 group border-0"
                      onClick={() => window.open(project.link, "_blank")}
                    >
                      <span className="group-hover:scale-105 transition-transform duration-300">View Project</span>
                      <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                    </Button>
                  </motion.div>
                ))}
                <motion.div variants={scaleIn} className="luxury-glass-hover rounded-2xl p-8 group">
                  <div className="flex items-center gap-4 mb-6">
                    <h4 className="text-xl font-semibold text-diamond-200">The Yoosuf Foundation</h4>
                  </div>

                  <p className="text-platinum-400 leading-relaxed mb-6">
                    Educational nonprofit connecting first-generation students with resources, mentorship, and grant
                    opportunities. Currently mentoring promising talents from low-income, first-generation
                    backgrounds, providing them with the guidance and support they need to succeed in technology.
                  </p>

                  <Button
                    size="lg"
                    className="bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg px-6 py-3 text-sm font-medium transition-all duration-300 group border-0"
                    onClick={() => window.open("https://theyoosuffoundation.org", "_blank")}
                  >
                    <span className="group-hover:scale-105 transition-transform duration-300">Learn More</span>
                    <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                  </Button>
                </motion.div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
