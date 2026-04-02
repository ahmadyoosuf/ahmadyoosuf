"use client"

import { motion } from "framer-motion"
import Link from "next/link"
import { securityReports } from "@/data/security-reports"
import { getSeverityColor } from "@/lib/severity"

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

export function ReportsSection() {
  return (
    <section id="reports" className="py-16 sm:py-20 md:py-24 lg:py-32 relative section-divider">
      <div className="container relative z-10 px-4 md:px-6">
        <div className="max-w-screen-xl mx-auto">
          <motion.div
            className="text-center space-y-6 max-w-4xl mx-auto mb-20"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeInUp}
          >
            <h3 className="text-2xl md:text-3xl font-semibold text-diamond-200 mb-4">Security Research</h3>
          </motion.div>

          <motion.div
            className="grid grid-cols-1 md:grid-cols-2 gap-8"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
          >
            {securityReports.map((report) => (
              <motion.div
                key={report.title}
                className={`luxury-glass-hover rounded-2xl p-6 group ${getSeverityColor(report.severity)}`}
              >
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm font-semibold">{report.severity} Severity</span>
                  <span className="text-xs text-platinum-500">{report.date}</span>
                </div>
                <h4 className="text-lg font-bold text-diamond-200">{report.title}</h4>
                <p className="text-platinum-400 leading-relaxed mb-4">{report.description}</p>
                <span className="text-xs text-platinum-500">{report.impact}</span>
                <Link href={`/reports/${report.slug}`} className="text-ruby-400 hover:underline mt-2 block">
                  Read Full Report
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
