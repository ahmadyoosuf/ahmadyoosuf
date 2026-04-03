"use client"

import { motion } from "framer-motion"
import { Mail } from "lucide-react"

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

const contactItems = [
  { icon: Mail, label: "Email", value: "ahmad@ahmadyoosuf.com", href: "mailto:ahmad@ahmadyoosuf.com" },
]

export function ContactSection() {
  return (
    <section id="contact" className="py-16 sm:py-20 md:py-24 lg:py-32 relative section-divider">
      <div className="container relative z-10 px-4 md:px-6">
        <div className="max-w-screen-xl mx-auto">
          <motion.div
            className="text-center space-y-6 max-w-4xl mx-auto mb-20"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeInUp}
          >
            <h3 className="text-2xl md:text-3xl font-bold text-luxury mb-4">Get In Touch</h3>
            <p className="text-platinum-400 leading-relaxed mb-6">
              Interested in discussing a project, collaboration, or just want to connect? I'd love to hear from you.
            </p>
          </motion.div>

          <motion.div
            className="flex flex-col sm:flex-row gap-8 justify-center items-center"
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={staggerContainer}
          >
            {contactItems.map((contact, index) => (
              <motion.a
                key={index}
                href={contact.href}
                variants={scaleIn}
                className="luxury-glass-hover rounded-2xl p-6 group flex items-center gap-4 min-w-[280px] transition-all duration-300 hover:scale-105"
              >
                <contact.icon className="h-6 w-6 text-ruby-400 group-hover:scale-110 transition-transform duration-300" />
                <div>
                  <span className="font-semibold text-diamond-200 block">{contact.label}</span>
                  <span className="text-platinum-400">{contact.value}</span>
                </div>
              </motion.a>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
