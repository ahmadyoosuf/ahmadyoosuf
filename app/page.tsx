"use client"

import { useState, useEffect, useRef } from "react"
import Link from "next/link"
import { motion, useScroll, useTransform, useSpring } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  ArrowRight,
  ChevronRight,
  ExternalLink,
  FileText,
  Github,
  Mail,
  MessageSquare,
  Shield,
  Zap,
  Brain,
  Users,
  Linkedin,
} from "lucide-react"
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
                  className="text-lg md:text-xl text-platinum-400 max-w-3xl mx-auto leading-relaxed"
                  variants={fadeInUp}
                >
                  Building systems that matter. Identifying vulnerabilities that others miss. Creating products that
                  solve real problems.
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

                <div className="grid grid-cols-3 gap-8 pt-12 sm:pt-16 max-w-4xl mx-auto">
                  <div className="flex flex-col items-center space-y-3">
                    <div className="w-16 h-16 flex items-center justify-center">
                      <svg className="w-8 h-8 text-ruby-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                        />
                      </svg>
                    </div>
                    <div className="text-3xl font-bold text-luxury">3+</div>
                    <div className="text-sm text-platinum-500 text-center">AI Products</div>
                  </div>

                  <div className="flex flex-col items-center space-y-3">
                    <div className="w-16 h-16 flex items-center justify-center">
                      <svg className="w-8 h-8 text-ruby-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                        />
                      </svg>
                    </div>
                    <div className="text-3xl font-bold text-luxury">10+</div>
                    <div className="text-sm text-platinum-500 text-center">Vulnerabilities</div>
                  </div>

                  <div className="flex flex-col items-center space-y-3">
                    <div className="w-16 h-16 flex items-center justify-center">
                      <svg className="w-8 h-8 text-ruby-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"
                        />
                      </svg>
                    </div>
                    <div className="text-3xl font-bold text-luxury">50+</div>
                    <div className="text-sm text-platinum-500 text-center">Students Mentored</div>
                  </div>
                </div>
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
                <Badge className="px-4 py-2 text-sm luxury-glass text-ruby-400 border-ruby-500/20 rounded-full backdrop-blur-xl">
                  Selected Work
                </Badge>
                <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-luxury">Products & Projects</h2>
                <p className="text-lg text-platinum-400 max-w-3xl mx-auto leading-relaxed">
                  A curated selection of my work across AI, security research, and product development. Each project
                  represents a unique challenge and innovative solution.
                </p>
              </motion.div>

              <motion.div
                className="space-y-16"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
                variants={staggerContainer}
              >
                {/* Featured Project - MARSAD */}
                <motion.div
                  variants={fadeInUp}
                  className="luxury-glass-hover rounded-3xl p-8 md:p-12 luxury-shadow group"
                >
                  <div className="flex flex-col lg:flex-row gap-8 lg:gap-12">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-6">
                        <Badge className="bg-ruby-500/10 text-ruby-400 border-ruby-500/20 px-3 py-1">
                          Featured Project
                        </Badge>
                        <Badge className="bg-platinum-500/10 text-platinum-400 border-platinum-500/20 px-3 py-1">
                          International Collaboration
                        </Badge>
                      </div>

                      <h3 className="text-3xl font-bold text-luxury mb-4">MARSAD</h3>
                      <p className="text-platinum-400 text-lg leading-relaxed mb-6">
                        A comprehensive social media intelligence platform led by Hamad Bin Khalifa University (HBKU) in
                        collaboration with institutions across Qatar, US, and UK. I designed and developed the entire
                        platform solo in just a few weeks, creating a system that analyzes social media data to provide
                        actionable insights for research and policy-making.
                      </p>

                      <div className="flex flex-wrap gap-2 mb-6">
                        {["AI", "Data Analysis", "Full-Stack", "Research"].map((tag) => (
                          <Badge key={tag} className="luxury-glass text-platinum-300 border-platinum-500/20 px-3 py-1">
                            {tag}
                          </Badge>
                        ))}
                      </div>

                      <Link
                        href="https://marsadi.vercel.app"
                        className="inline-flex items-center text-ruby-400 hover:text-ruby-300 transition-colors text-lg font-medium group"
                      >
                        View Project
                        <ExternalLink className="ml-2 h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
                      </Link>
                    </div>

                    <div className="lg:w-80">
                      <div className="luxury-glass rounded-2xl p-6 h-full">
                        <div className="flex items-center gap-3 mb-4">
                          <Brain className="h-8 w-8 text-ruby-400" />
                          <div>
                            <div className="text-sm text-platinum-500">Platform Type</div>
                            <div className="font-medium text-diamond-200">Intelligence System</div>
                          </div>
                        </div>
                        <div className="space-y-4">
                          <div className="flex justify-between">
                            <span className="text-platinum-500">Development Time</span>
                            <span className="text-diamond-200 font-medium">Few Weeks</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-platinum-500">Team Size</span>
                            <span className="text-diamond-200 font-medium">Solo</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-platinum-500">Institutions</span>
                            <span className="text-diamond-200 font-medium">3 Countries</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>

                {/* AI Products Grid */}
                <motion.div variants={fadeInUp}>
                  <h3 className="text-2xl font-bold text-luxury mb-8 border-b border-white/[0.05] pb-4">AI Products</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {projects.slice(1).map((project, index) => (
                      <motion.div
                        key={project.title}
                        variants={scaleIn}
                        className="luxury-glass-hover rounded-2xl p-8 group"
                      >
                        <div className="flex items-center gap-4 mb-6">
                          <div className="w-12 h-12 luxury-glass rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                            <project.icon className="h-6 w-6 text-ruby-400" />
                          </div>
                          <h4 className="text-xl font-bold text-diamond-200">{project.title}</h4>
                        </div>

                        <p className="text-platinum-400 leading-relaxed mb-6">{project.description}</p>

                        <div className="flex flex-wrap gap-2 mb-6">
                          {project.tags.map((tag) => (
                            <Badge
                              key={tag}
                              className="luxury-glass text-platinum-300 border-platinum-500/20 px-3 py-1"
                            >
                              {tag}
                            </Badge>
                          ))}
                        </div>

                        <Link
                          href={project.link}
                          className="inline-flex items-center text-ruby-400 hover:text-ruby-300 transition-colors font-medium group"
                        >
                          View Project
                          <ExternalLink className="ml-2 h-4 w-4 group-hover:scale-110 transition-transform duration-300" />
                        </Link>
                      </motion.div>
                    ))}
                  </div>
                </motion.div>

                {/* The Yoosuf Foundation */}
                <motion.div variants={fadeInUp} className="luxury-glass-hover rounded-3xl p-8 md:p-12 luxury-shadow">
                  <div className="flex flex-col lg:flex-row gap-8 lg:gap-12">
                    <div className="flex-1">
                      <div className="flex items-center gap-4 mb-6">
                        <div className="w-12 h-12 luxury-glass rounded-xl flex items-center justify-center">
                          <Users className="h-6 w-6 text-platinum-400" />
                        </div>
                        <Badge className="bg-platinum-500/10 text-platinum-400 border-platinum-500/20 px-3 py-1">
                          Social Impact
                        </Badge>
                      </div>

                      <h3 className="text-3xl font-bold text-luxury mb-4">The Yoosuf Foundation</h3>
                      <p className="text-platinum-400 text-lg leading-relaxed mb-6">
                        Educational nonprofit connecting first-generation students with resources, mentorship, and grant
                        opportunities. Currently mentoring 50+ promising talents from low-income, first-generation
                        backgrounds, providing them with the guidance and support they need to succeed in technology.
                      </p>

                      <div className="grid grid-cols-2 gap-6 mb-6">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-ruby-400 mb-1">50+</div>
                          <div className="text-sm text-platinum-500">Students Mentored</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-platinum-400 mb-1">100%</div>
                          <div className="text-sm text-platinum-500">First-Generation</div>
                        </div>
                      </div>

                      <Link
                        href="https://theyoosuffoundation.org"
                        className="inline-flex items-center text-platinum-400 hover:text-platinum-300 transition-colors text-lg font-medium group"
                      >
                        Learn More
                        <ExternalLink className="ml-2 h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
                      </Link>
                    </div>
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
                <Badge className="px-4 py-2 text-sm luxury-glass text-ruby-400 border-ruby-500/20 rounded-full backdrop-blur-xl">
                  Security Research
                </Badge>
                <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-luxury">Vulnerability Reports</h2>
                <p className="text-lg text-platinum-400 max-w-3xl mx-auto leading-relaxed">
                  Critical security vulnerabilities I've identified in major platforms and payment systems, helping
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
                    key={index}
                    variants={scaleIn}
                    className="luxury-glass-hover rounded-2xl overflow-hidden group"
                  >
                    <div className="p-8">
                      <div className="flex justify-between items-start mb-6">
                        <Badge className={cn("px-3 py-1", getSeverityColor(report.severity))}>
                          {report.severity} Severity
                        </Badge>
                        <span className="text-platinum-500 text-sm">{report.date}</span>
                      </div>

                      <h3 className="text-xl font-bold text-diamond-200 mb-3 group-hover:text-luxury transition-colors duration-300">
                        {report.title}
                      </h3>

                      <p className="text-platinum-400 leading-relaxed mb-4">{report.description}</p>

                      <div className="flex items-center gap-2 mb-6">
                        <Shield className="h-4 w-4 text-ruby-400" />
                        <span className="text-sm text-ruby-400 font-medium">{report.impact}</span>
                      </div>

                      <Link
                        href={`/reports/${report.slug}`}
                        className="inline-flex items-center text-ruby-400 hover:text-ruby-300 transition-colors font-medium group"
                      >
                        Read Full Report
                        <ChevronRight className="ml-1 h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                      </Link>
                    </div>
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
                <Badge className="px-4 py-2 text-sm luxury-glass text-platinum-400 border-platinum-500/20 rounded-full backdrop-blur-xl">
                  Insights & Perspectives
                </Badge>
                <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-luxury">From My Blog</h2>
                <p className="text-lg text-platinum-400 max-w-3xl mx-auto leading-relaxed">
                  Thoughts on security, development, leadership, and the intersection of technology with society. Deep
                  dives into the challenges and opportunities shaping our digital future.
                </p>
              </motion.div>

              <motion.div
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-100px" }}
                variants={staggerContainer}
              >
                {blogPosts.map((post, index) => (
                  <motion.div key={index} variants={scaleIn} className="group">
                    <div className="luxury-glass-hover rounded-2xl overflow-hidden h-full">
                      <div className="p-8">
                        <div className="flex items-center justify-between mb-4">
                          <Badge className="luxury-glass text-platinum-300 border-platinum-500/20 px-3 py-1">
                            {post.category}
                          </Badge>
                          <span className="text-2xs text-platinum-500 uppercase tracking-wider">{post.readTime}</span>
                        </div>

                        <h3 className="text-lg font-bold text-diamond-200 mb-3 group-hover:text-luxury transition-colors duration-300 leading-tight">
                          {post.title}
                        </h3>

                        <p className="text-platinum-500 text-xs mb-4">{post.date}</p>
                        <p className="text-platinum-400 leading-relaxed mb-6 text-sm">{post.excerpt}</p>

                        <Link
                          href={`/blog/${post.slug}`}
                          className="text-ruby-400 flex items-center gap-2 font-medium hover:text-ruby-300 transition-colors group"
                        >
                          <span className="group-hover:scale-105 transition-transform duration-300">Read More</span>
                          <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                        </Link>
                      </div>
                    </div>
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
                <Link href="/blog">
                  <Button className="luxury-glass-hover text-diamond-200 rounded-full px-8 py-3 h-auto font-medium group border-white/10">
                    <span className="group-hover:scale-105 transition-transform duration-300">View All Posts</span>
                    <ChevronRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                  </Button>
                </Link>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="py-16 sm:py-20 md:py-24 lg:py-32 relative section-divider">
          <div className="container relative z-10 px-4 md:px-6">
            <motion.div
              className="max-w-5xl mx-auto luxury-glass rounded-3xl p-6 sm:p-8 md:p-12 luxury-shadow"
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-100px" }}
              variants={fadeInUp}
            >
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
                <div className="space-y-8">
                  <div>
                    <Badge className="px-4 py-2 text-sm luxury-glass text-ruby-400 border-ruby-500/20 rounded-full backdrop-blur-xl mb-6">
                      Get In Touch
                    </Badge>
                    <h2 className="text-3xl md:text-4xl font-bold text-luxury mb-4">Let's Connect</h2>
                    <p className="text-lg text-platinum-400 leading-relaxed">
                      Interested in discussing a project, collaboration opportunity, or just want to connect? I'd love
                      to hear from you and explore how we can work together.
                    </p>
                  </div>

                  <div className="space-y-6">
                    {contactItems.map((contact, index) => (
                      <div key={index} className="flex items-center gap-4 group">
                        <div
                          className={cn(
                            "w-12 h-12 rounded-xl luxury-glass flex items-center justify-center group-hover:scale-110 transition-transform duration-300",
                            contact.color === "ruby" && "group-hover:bg-ruby-500/10",
                            contact.color === "platinum" && "group-hover:bg-platinum-500/10", // Retained for potential future use
                            contact.color === "diamond" && "group-hover:bg-diamond-500/10",
                          )}
                        >
                          <contact.icon
                            className={cn(
                              "h-5 w-5",
                              contact.color === "ruby" && "text-ruby-400",
                              contact.color === "platinum" && "text-platinum-400",
                              contact.color === "diamond" && "text-diamond-400",
                            )}
                          />
                        </div>
                        <div>
                          <p className="text-sm text-platinum-500 mb-1">{contact.label}</p>
                          <a
                            href={contact.href}
                            className="font-medium text-diamond-200 hover:text-ruby-400 transition-colors"
                          >
                            {contact.value}
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="luxury-glass rounded-2xl p-8">
                  <form className="space-y-6">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-platinum-400 mb-2">
                        Name
                      </label>
                      <input
                        type="text"
                        id="name"
                        className="w-full px-4 py-3 luxury-glass rounded-xl focus:outline-none focus:ring-2 focus:ring-ruby-500/50 text-diamond-200 placeholder-platinum-500 transition-all duration-300"
                        placeholder="Your name"
                      />
                    </div>

                    <div>
                      <label htmlFor="email" className="block text-sm font-medium text-platinum-400 mb-2">
                        Email
                      </label>
                      <input
                        type="email"
                        id="email"
                        className="w-full px-4 py-3 luxury-glass rounded-xl focus:outline-none focus:ring-2 focus:ring-ruby-500/50 text-diamond-200 placeholder-platinum-500 transition-all duration-300"
                        placeholder="Your email"
                      />
                    </div>

                    <div>
                      <label htmlFor="message" className="block text-sm font-medium text-platinum-400 mb-2">
                        Message
                      </label>
                      <textarea
                        id="message"
                        rows={5}
                        className="w-full px-4 py-3 luxury-glass rounded-xl focus:outline-none focus:ring-2 focus:ring-ruby-500/50 text-diamond-200 placeholder-platinum-500 transition-all duration-300 resize-none"
                        placeholder="Your message"
                      />
                    </div>

                    <Button className="w-full btn-luxury text-diamond-50 rounded-xl px-6 py-4 h-auto font-medium group">
                      <span className="group-hover:scale-105 transition-transform duration-300">Send Message</span>
                    </Button>
                  </form>
                </div>
              </div>
            </motion.div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="relative bg-obsidian-950 border-t border-white/[0.05]">
        <div className="container py-12 md:py-16 px-4 md:px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-12">
            <div className="col-span-2">
              <motion.div
                className="flex items-center gap-3 mb-6"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
              >
                <div className="relative group">
                  <div className="absolute inset-0 ruby-gradient rounded-xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity duration-500" />
                  <div className="relative flex items-center justify-center w-12 h-12 luxury-glass rounded-xl overflow-hidden">
                    <Image
                      src="/images/logo.png"
                      alt="Ahmad Yoosuf Logo"
                      width={48}
                      height={48}
                      className="object-contain p-1"
                    />
                  </div>
                </div>
                <div className="flex flex-col">
                  <span className="text-xl font-bold text-luxury tracking-tight">Ahmad Yoosuf</span>
                  <span className="text-2xs text-platinum-500 tracking-wider uppercase">AI • Security • Product</span>
                </div>
              </motion.div>

              <p className="text-platinum-400 mb-6 max-w-sm leading-relaxed">
                Building systems that matter. Identifying vulnerabilities that others miss. Creating products that solve
                real problems.
              </p>

              <div className="flex space-x-4">
                <Link
                  href="https://github.com/ahmadyoosuf"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-platinum-500 hover:text-ruby-400 transition-colors duration-300 group"
                  aria-label="GitHub Profile"
                >
                  <Github className="h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
                </Link>
                <Link
                  href="https://linkedin.com/in/ahmadyoosuf"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-platinum-500 hover:text-ruby-400 transition-colors duration-300 group"
                  aria-label="LinkedIn Profile"
                >
                  <Linkedin className="h-5 w-5 group-hover:scale-110 transition-transform duration-300" />
                </Link>
              </div>
            </div>

            <div>
              <h3 className="font-semibold text-diamond-200 mb-4 text-sm uppercase tracking-wider">Navigation</h3>
              <ul className="space-y-3">
                {["Home", "Work", "Reports", "Blog", "Contact"].map((item) => (
                  <li key={item}>
                    <button
                      onClick={() => handleNavClick(item.toLowerCase().replace(" ", "-"))}
                      className="text-platinum-400 hover:text-ruby-400 transition-colors text-sm group"
                    >
                      <span className="group-hover:translate-x-1 transition-transform duration-300 inline-block">
                        {item}
                      </span>
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="font-semibold text-diamond-200 mb-4 text-sm uppercase tracking-wider">Projects</h3>
              <ul className="space-y-3">
                {[
                  { name: "MARSAD", href: "https://marsadi.vercel.app" },
                  { name: "OCRPro", href: "https://ocrpro.vercel.app" },
                  { name: "A111y", href: "https://a111y.vercel.app" },
                  { name: "The Yoosuf Foundation", href: "https://theyoosuffoundation.org" },
                  { name: "Security Reports", href: "/reports" },
                ].map((item) => (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className="text-platinum-400 hover:text-ruby-400 transition-colors text-sm group"
                    >
                      <span className="group-hover:translate-x-1 transition-transform duration-300 inline-block">
                        {item.name}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="border-t border-white/[0.05]">
          <div className="container py-6 px-4 md:px-6">
            <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
              <p className="text-sm text-platinum-500">
                © {new Date().getFullYear()} Ahmad Mohamed Yoosuf. All rights reserved.
              </p>
              <div className="flex gap-6">
                <Link href="#" className="text-sm text-platinum-500 hover:text-platinum-300 transition-colors">
                  Privacy
                </Link>
                <Link href="#" className="text-sm text-platinum-500 hover:text-platinum-300 transition-colors">
                  Terms
                </Link>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
