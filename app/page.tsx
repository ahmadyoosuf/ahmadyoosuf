"use client"

import { useState, useEffect, useRef } from "react"
import Link from "next/link"
import { motion, useScroll, useTransform, useSpring } from "framer-motion"
import { Button } from "@/components/ui/button"
import { ArrowRight, FileText, Github, Mail, MessageSquare, Shield, Zap, Brain, Linkedin } from "lucide-react"
import { cn } from "@/lib/utils"
import { useMobile } from "@/hooks/use-mobile"
import Image from "next/image"

export default function PersonalWebsite() {
  const [activeSection, setActiveSection] = useState("home")
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const heroRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll()
  const opacity = useTransform(scrollYProgress, [0, 0.3], [1, 0])
  const scale = useTransform(scrollYProgress, [0, 0.3], [1, 0.95])
  const y = useTransform(scrollYProgress, [0, 0.3], [0, 100])
  const isMobile = useMobile()

  const springConfig = { damping: 25, stiffness: 700 }
  const mouseX = useSpring(mousePosition.x, springConfig)
  const mouseY = useSpring(mousePosition.y, springConfig)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: (e.clientX - window.innerWidth / 2) / 50,
        y: (e.clientY - window.innerHeight / 2) / 50,
      })
    }
    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
      const sections = document.querySelectorAll("section[id]")
      const scrollPosition = window.scrollY + 100
      sections.forEach((section) => {
        const sectionTop = (section as HTMLElement).offsetTop
        const sectionHeight = (section as HTMLElement).offsetHeight
        const sectionId = section.getAttribute("id") || ""
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
          setActiveSection(sectionId)
        }
      })
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement
      if (isMenuOpen && !target.closest(".mobile-menu") && !target.closest(".menu-button")) {
        setIsMenuOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [isMenuOpen])

  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = "hidden"
    } else {
      document.body.style.overflow = ""
    }
    return () => {
      document.body.style.overflow = ""
    }
  }, [isMenuOpen])

  const projects = [
    {
      title: "MARSAD",
      description:
        "Social media intelligence platform led by HBKU in collaboration with institutions across Qatar, US, and UK. Designed and developed the entire platform solo in a few weeks.",
      tags: ["AI", "Data Analysis", "Full-Stack"],
      link: "https://marsadi.vercel.app",
      icon: Brain,
      featured: true,
    },
    {
      title: "OCRPro",
      description:
        "State-of-the-art OCR engine that outperforms industry leaders like AWS Textract, Azure OCR, and Google Cloud OCR in terms of cost, speed, and accuracy.",
      tags: ["AI", "Computer Vision", "API"],
      link: "https://ocrpro.vercel.app",
      icon: Zap,
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

  const securityReports = [
    {
      title: "Stripe SEPA Direct Debit Validation Vulnerability",
      date: "December 2024",
      severity: "High",
      description:
        "Critical vulnerability in Stripe's SEPA Direct Debit payment system implementation affecting multiple client companies.",
      slug: "stripe-vulnerability",
      impact: "Premium purchase bypass",
    },
    {
      title: "Dropbox Payment System Validation Issue",
      date: "November 2024",
      severity: "High",
      description:
        "Significant vulnerability in Dropbox's SEPA Direct Debit payment system allowing premium subscription activation without proper IBAN validation.",
      slug: "dropbox-vulnerability",
      impact: "Premium purchase bypass",
    },
  ]

  const blogPosts = [
    {
      title: "Why I Hunt Bugs in Payment Systems",
      category: "Security",
      date: "January 12, 2025",
      excerpt: "The real vulnerabilities aren't in the code. They're in the assumptions about how money should move.",
      slug: "payment-systems-bugs",
      readTime: "8 min read",
    },
    {
      title: "The Myth of the Self-Made Success",
      category: "Leadership",
      date: "December 28, 2024",
      excerpt:
        "After mentoring 50+ first-generation professionals, I've learned that 'pulling yourself up by your bootstraps' is terrible advice.",
      slug: "myth-of-self-made",
      readTime: "12 min read",
    },
    {
      title: "Building AI Products That Actually Work",
      category: "AI",
      date: "November 15, 2024",
      excerpt: "Lessons learned from building OCRPro and A111y - two AI products that solve real problems.",
      slug: "building-ai-products",
      readTime: "10 min read",
    },
  ]

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
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.1,
      },
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

  const handleNavClick = (sectionId: string) => {
    document.querySelector(`#${sectionId}`)?.scrollIntoView({ behavior: "smooth" })
    setActiveSection(sectionId)
    setIsMenuOpen(false)
  }

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "critical":
        return "bg-ruby-500/10 text-ruby-400 border-ruby-500/20"
      case "high":
        return "bg-ruby-600/10 text-ruby-500 border-ruby-600/20"
      case "medium":
        return "bg-platinum-500/10 text-platinum-400 border-platinum-500/20"
      case "low":
        return "bg-diamond-500/10 text-diamond-400 border-diamond-500/20"
      default:
        return "bg-platinum-500/10 text-platinum-400 border-platinum-500/20"
    }
  }

  // Updated contact items
  const contactItems = [
    { icon: Mail, label: "Email", value: "ahmad@ahmadyoosuf.com", href: "mailto:ahmad@ahmadyoosuf.com", color: "ruby" },
    { icon: MessageSquare, label: "Phone", value: "+91 6382429579", href: "tel:+916382429579", color: "diamond" },
  ]

  return (
    <div className="flex min-h-screen flex-col bg-obsidian-950 text-diamond-100 overflow-x-hidden">
      {/* Header */}
      <header
        className={cn(
          "fixed top-0 z-50 w-full transition-all duration-700 ease-out",
          isScrolled ? "luxury-glass border-b border-white/[0.05] py-4 md:py-4" : "bg-transparent py-6 md:py-6",
        )}
      >
        <div className="container flex items-center justify-between px-4 md:px-6">
          <motion.div className="flex items-center gap-3" style={{ x: mouseX, y: mouseY }}>
            <div className="relative group">
              <div className="absolute inset-0 ruby-gradient rounded-xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity duration-500" />
              <div className="relative flex items-center justify-center w-10 h-10 md:w-12 md:h-12 luxury-glass rounded-xl overflow-hidden">
                <Image
                  src="/images/logo.png"
                  alt="Ahmad Yoosuf Logo"
                  width={48}
                  height={48}
                  className="object-contain p-1"
                />
              </div>
            </div>
            <div className="flex flex-col min-w-0">
              <span className="text-base sm:text-lg md:text-xl font-bold text-luxury tracking-tight truncate">
                Ahmad Yoosuf
              </span>
              <span className="text-2xs text-platinum-500 tracking-wider uppercase hidden sm:block">
                AI • Security • Product
              </span>
            </div>
          </motion.div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-2">
            {["home", "work", "reports", "blog"].map(
              (
                section, // Removed "contact" from here as it's now an icon
              ) => (
                <button
                  key={section}
                  className={cn(
                    "px-6 py-3 text-sm font-medium rounded-full transition-all duration-500 relative group",
                    activeSection === section ? "text-ruby-400" : "text-platinum-400 hover:text-diamond-200",
                  )}
                  onClick={() => handleNavClick(section)}
                >
                  {activeSection === section && (
                    <motion.div
                      layoutId="activeSection"
                      className="absolute inset-0 luxury-glass rounded-full"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  <span className="relative z-10">
                    {section.charAt(0).toUpperCase() + section.slice(1).replace("-", " ")}
                  </span>
                </button>
              ),
            )}
          </nav>

          <div className="flex items-center gap-3 sm:gap-4">
            {/* Contact, GitHub, LinkedIn Icons */}
            <button
              onClick={() => handleNavClick("contact")}
              aria-label="Contact"
              className="text-platinum-400 hover:text-ruby-400 transition-colors duration-300 group p-2 rounded-full luxury-glass-hover"
            >
              <Mail className="h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
            </button>
            <Link
              href="https://github.com/ahmadyoosuf"
              target="_blank"
              rel="noopener noreferrer"
              className="text-platinum-400 hover:text-ruby-400 transition-colors duration-300 group p-2 rounded-full luxury-glass-hover"
              aria-label="GitHub"
            >
              <Github className="h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
            </Link>
            <Link
              href="https://linkedin.com/in/ahmadyoosuf"
              target="_blank"
              rel="noopener noreferrer"
              className="text-platinum-400 hover:text-ruby-400 transition-colors duration-300 group p-2 rounded-full luxury-glass-hover"
              aria-label="LinkedIn"
            >
              <Linkedin className="h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
            </Link>

            {/* Mobile menu button */}
            <button
              className="lg:hidden flex items-center justify-center w-10 h-10 rounded-full luxury-glass menu-button group ml-2" // ml-2 for spacing from new icons
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle menu"
            >
              <div className="w-5 h-5 flex flex-col justify-between">
                <span
                  className={cn(
                    "w-full h-0.5 bg-platinum-300 transition-all duration-300 group-hover:bg-ruby-400",
                    isMenuOpen ? "rotate-45 translate-y-2" : "",
                  )}
                />
                <span
                  className={cn(
                    "w-full h-0.5 bg-platinum-300 transition-all duration-300 group-hover:bg-ruby-400",
                    isMenuOpen ? "opacity-0" : "opacity-100",
                  )}
                />
                <span
                  className={cn(
                    "w-full h-0.5 bg-platinum-300 transition-all duration-300 group-hover:bg-ruby-400",
                    isMenuOpen ? "-rotate-45 -translate-y-2" : "",
                  )}
                />
              </div>
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu */}
      <motion.div
        className={cn(
          "fixed inset-0 z-40 lg:hidden mobile-menu",
          isMenuOpen ? "pointer-events-auto" : "pointer-events-none",
        )}
        initial={false}
        animate={{
          opacity: isMenuOpen ? 1 : 0,
          backdropFilter: isMenuOpen ? "blur(20px)" : "blur(0px)",
        }}
        transition={{ duration: 0.3 }}
      >
        <div className="absolute inset-0 bg-obsidian-950/90" />
        <div className="relative flex flex-col items-center justify-center h-full gap-8 px-6">
          {["home", "work", "reports", "blog", "contact"].map(
            (
              section,
              index, // "contact" can be here for mobile nav
            ) => (
              <motion.button
                key={section}
                className={cn(
                  "px-8 py-4 text-lg font-medium rounded-full transition-all duration-300 w-full max-w-xs text-center luxury-glass-hover",
                  activeSection === section ? "text-ruby-400" : "text-platinum-300 hover:text-diamond-100",
                )}
                onClick={() => handleNavClick(section)}
                initial={{ opacity: 0, y: 50 }}
                animate={{
                  opacity: isMenuOpen ? 1 : 0,
                  y: isMenuOpen ? 0 : 50,
                }}
                transition={{ delay: index * 0.1, duration: 0.3 }}
              >
                {section.charAt(0).toUpperCase() + section.slice(1).replace("-", " ")}
              </motion.button>
            ),
          )}
        </div>
      </motion.div>

      <main className="flex-1 relative">
        {/* Hero Section */}
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
                  className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-none"
                  variants={fadeInUp}
                >
                  <span className="block text-luxury mb-2">Ahmad Mohamed</span>
                  <span className="block text-diamond-200 font-light">Yoosuf</span>
                </motion.h1>

                <motion.p
                  className="md:text-xl max-w-3xl mx-auto leading-relaxed font-semibold text-2xl text-slate-300"
                  variants={fadeInUp}
                >
                  Building products that matter
                </motion.p>

                <motion.div className="flex flex-col sm:flex-row gap-4 justify-center pt-8" variants={fadeInUp}>
                  <Button
                    size="lg"
                    className="btn-luxury text-diamond-50 rounded-full px-8 py-4 h-auto text-base font-medium group"
                    onClick={() => handleNavClick("work")}
                  >
                    <span className="group-hover:scale-105 transition-transform duration-300">View My Work</span>
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-300" />
                  </Button>

                  <Button
                    size="lg"
                    variant="outline"
                    className="luxury-glass-hover text-diamond-200 rounded-full px-8 py-4 h-auto text-base font-medium group border-white/10 bg-transparent"
                    onClick={() => handleNavClick("reports")}
                  >
                    <FileText className="h-5 w-5 mr-2 group-hover:scale-110 transition-transform duration-300" />
                    <span className="group-hover:scale-105 transition-transform duration-300">Security Reports</span>
                  </Button>
                </motion.div>
              </motion.div>
            </div>
          </motion.div>
        </section>

        {/* Work Section */}
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
                <div className="flex justify-center">
                  <div className="btn-luxury text-diamond-50 rounded-full px-10 py-5 text-xl font-bold group">
                    <span className="group-hover:scale-105 transition-transform duration-300">Selected Work</span>
                  </div>
                </div>

                <p className="text-lg text-platinum-400 max-w-3xl mx-auto leading-relaxed rounded-sm">
                  A curated selection of my work across AI, security research, and full-stack development
                </p>
              </motion.div>

              <motion.div
                className="space-y-16"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
                variants={staggerContainer}
              >
                {/* Projects Grid */}
                <motion.div variants={fadeInUp}>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <motion.div variants={scaleIn} className="luxury-glass-hover rounded-2xl p-8 group">
                      <div className="flex items-center gap-4 mb-6">
                        <h4 className="text-xl font-bold text-diamond-200">MARSAD</h4>
                      </div>

                      <p className="text-platinum-400 leading-relaxed mb-6">
                        A comprehensive social media intelligence platform led by Hamad Bin Khalifa University (HBKU) in
                        collaboration with institutions across Qatar, US, and UK. I led the design and development of
                        the entire platform, creating a system that analyzes social media data to provide actionable
                        insights for research and policy-making.
                      </p>

                      <Button
                        size="lg"
                        className="btn-luxury text-diamond-50 rounded-full px-8 py-4 h-auto text-base font-medium group"
                        onClick={() => window.open("https://marsadi.vercel.app", "_blank")}
                      >
                        <span className="group-hover:scale-105 transition-transform duration-300">View Project</span>
                        <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-300" />
                      </Button>
                    </motion.div>

                    {projects.slice(1).map((project, index) => (
                      <motion.div
                        key={project.title}
                        variants={scaleIn}
                        className="luxury-glass-hover rounded-2xl p-8 group"
                      >
                        <div className="flex items-center gap-4 mb-6">
                          <h4 className="text-xl font-bold text-diamond-200">{project.title}</h4>
                        </div>

                        <p className="text-platinum-400 leading-relaxed mb-6">{project.description}</p>

                        <Button
                          size="lg"
                          className="btn-luxury text-diamond-50 rounded-full px-8 py-4 h-auto text-base font-medium group"
                          onClick={() => window.open(project.link, "_blank")}
                        >
                          <span className="group-hover:scale-105 transition-transform duration-300">View Project</span>
                          <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-300" />
                        </Button>
                      </motion.div>
                    ))}

                    <motion.div variants={scaleIn} className="luxury-glass-hover rounded-2xl p-8 group">
                      <div className="flex items-center gap-4 mb-6">
                        <h4 className="text-xl font-bold text-diamond-200">The Yoosuf Foundation</h4>
                      </div>

                      <p className="text-platinum-400 leading-relaxed mb-6">
                        Educational nonprofit connecting first-generation students with resources, mentorship, and grant
                        opportunities. Currently mentoring promising talents from low-income, first-generation
                        backgrounds, providing them with the guidance and support they need to succeed in technology.
                      </p>

                      <Button
                        size="lg"
                        className="btn-luxury text-diamond-50 rounded-full px-8 py-4 h-auto text-base font-medium group"
                        onClick={() => window.open("https://theyoosuffoundation.org", "_blank")}
                      >
                        <span className="group-hover:scale-105 transition-transform duration-300">Learn More</span>
                        <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-300" />
                      </Button>
                    </motion.div>
                  </div>
                </motion.div>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Security Reports Section */}
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
                <h3 className="md:text-3xl font-bold text-luxury mb-4 text-3xl">Security Research</h3>
                <h4 className="text-xl md:text-2xl font-bold text-diamond-200 mb-4">Vulnerability Reports</h4>
                <p className="text-platinum-400 leading-relaxed mb-6">
                  Vulnerabilities that I've identified and reported in major platforms and payment systems, helping
                  secure systems used by millions of users worldwide.
                </p>
              </motion.div>

              <motion.div
                className="grid grid-cols-1 md:grid-cols-2 gap-8"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
                variants={staggerContainer}
              >
                {securityReports.map((report, index) => (
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

              <motion.div
                className="text-center mt-12"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
                variants={fadeInUp}
              />
            </div>
          </div>
        </section>

        {/* Blog Section */}
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
                <h3 className="md:text-3xl font-bold text-luxury mb-4 text-3xl">Blog</h3>
              </motion.div>

              <motion.div
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
                variants={staggerContainer}
              >
                {blogPosts.map((post, index) => (
                  <motion.div key={post.title} variants={scaleIn} className="luxury-glass-hover rounded-2xl p-6 group">
                    <span className="text-xs text-platinum-500">{post.category}</span>
                    <h4 className="text-lg font-bold text-diamond-200">{post.title}</h4>
                    <span className="text-xs text-platinum-500">{post.date}</span>
                    <p className="text-platinum-400 leading-relaxed mb-4">{post.excerpt}</p>
                    <Link href={`/blog/${post.slug}`} className="text-ruby-400 hover:underline">
                      Read More
                    </Link>
                  </motion.div>
                ))}
              </motion.div>

              <motion.div
                className="text-center mt-12"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
                variants={fadeInUp}
              >
                <Link href="/blog" className="text-ruby-400 hover:underline">
                  View All Posts
                </Link>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Contact Section */}
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
      </main>

      {/* Footer */}
    </div>
  )
}
