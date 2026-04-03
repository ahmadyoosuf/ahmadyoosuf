"use client"

import { motion, useScroll, useTransform, useSpring } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, FileText } from "lucide-react"
import Image from "next/image"
import { useRef, useState, useEffect } from "react"

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

interface HeroSectionProps {
  onNavClick: (sectionId: string) => void
}

export function HeroSection({ onNavClick }: HeroSectionProps) {
  const heroRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll()
  const opacity = useTransform(scrollYProgress, [0, 0.3], [1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.3], [1, 0.95])
  const y = useTransform(scrollYProgress, [0, 0.3], [0, 100])

  return (
    <section
      id="home"
      ref={heroRef}
      className="relative min-h-screen flex items-center justify-center pt-24 md:pt-32"
    >
      <motion.div className="container relative z-10 px-4 md:px-6" style={{ opacity, scale, y }}>
        <div className="max-w-screen-xl mx-auto">
          <motion.div
            className="text-center space-y-8 max-w-5xl mx-auto"
            initial="hidden"
            animate="visible"
            variants={staggerContainer}
          >
            <motion.h1
              className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-none sm:text-8xl"
              variants={fadeInUp}
            >
              <span className="block text-luxury mb-2 text-6xl">Ahmad Mohamed</span>
              <span className="block text-diamond-200 font-light text-6xl">Yoosuf</span>
            </motion.h1>

            <motion.p
              className="text-lg md:text-xl max-w-3xl mx-auto leading-relaxed font-light text-platinum-400"
              variants={fadeInUp}
            >
              Building products that matter
            </motion.p>

            <motion.div className="flex flex-col sm:flex-row gap-4 justify-center pt-8" variants={fadeInUp}>
              <Button
                size="lg"
                className="bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg px-6 py-3 text-sm font-medium transition-all duration-300 group border-0"
                onClick={() => onNavClick("work")}
              >
                <span className="group-hover:scale-105 transition-transform duration-300">View My Work</span>
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
              </Button>

              <Button
                size="lg"
                variant="outline"
                className="bg-transparent border-slate-700 hover:bg-slate-800 text-slate-200 rounded-lg px-6 py-3 text-sm font-medium transition-all duration-300 group"
                onClick={() => onNavClick("reports")}
              >
                <FileText className="mr-2 h-4 w-4 group-hover:scale-110 transition-transform duration-300" />
                <span className="group-hover:scale-105 transition-transform duration-300">Security Reports</span>
              </Button>
            </motion.div>
          </motion.div>
        </div>
      </motion.div>
    </section>
  )
}
