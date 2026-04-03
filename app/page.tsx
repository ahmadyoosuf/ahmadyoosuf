"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { motion, useSpring } from "framer-motion"
import { Github, Linkedin } from "lucide-react"
import { cn } from "@/lib/utils"
import { useMobile } from "@/hooks/use-mobile"
import Image from "next/image"
import { HeroSection } from "@/components/sections/hero-section"
import { WorkSection } from "@/components/sections/work-section"
import { ReportsSection } from "@/components/sections/reports-section"
import { BlogSection } from "@/components/sections/blog-section"
import { ContactSection } from "@/components/sections/contact-section"

export default function PersonalWebsite() {
  const [activeSection, setActiveSection] = useState("home")
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
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

  const handleNavClick = (sectionId: string) => {
    document.querySelector(`#${sectionId}`)?.scrollIntoView({ behavior: "smooth" })
    setActiveSection(sectionId)
    setIsMenuOpen(false)
  }

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
            </div>
          </motion.div>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-2">
            {["home", "work", "reports", "blog"].map((section) => (
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
            ))}
          </nav>

          <div className="flex items-center gap-3 sm:gap-4">
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

            <button
              className="lg:hidden flex items-center justify-center w-10 h-10 rounded-full luxury-glass menu-button group ml-2"
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
          {["home", "work", "reports", "blog", "contact"].map((section, index) => (
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
          ))}
        </div>
      </motion.div>

      <main className="flex-1 relative">
        <HeroSection onNavClick={handleNavClick} />
        <WorkSection />
        <ReportsSection />
        <BlogSection />
        <ContactSection />
      </main>
    </div>
  )
}
