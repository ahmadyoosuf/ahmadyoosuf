import Link from "next/link"
import { ArrowLeft, Calendar, ChevronRight, Download, Search, Shield } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

// This would typically come from a CMS or MDX files
const getSecurityReports = () => {
  return [
    {
      title: "Stripe SEPA Direct Debit Validation Vulnerability",
      slug: "stripe-vulnerability",
      date: "December 18, 2024",
      severity: "High",
      cvss: "8.8",
      excerpt:
        "Critical vulnerability in Stripe's SEPA Direct Debit payment system implementation affecting multiple client companies.",
      impact: "Premium purchase bypass",
    },
    {
      title: "Dropbox Payment System Validation Issue",
      slug: "dropbox-vulnerability",
      date: "November 15, 2024",
      severity: "High",
      cvss: "8.8",
      excerpt:
        "Significant vulnerability in Dropbox's SEPA Direct Debit payment system allowing premium subscription activation without proper IBAN validation.",
      impact: "Premium purchase bypass",
    },
  ]
}

// Severity filters
const severityLevels = ["All", "Critical", "High", "Medium", "Low"]

export default function ReportsPage() {
  const reports = getSecurityReports()

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case "critical":
        return "bg-red-500/10 text-red-400 border-red-500/20"
      case "high":
        return "bg-orange-500/10 text-orange-400 border-orange-500/20"
      case "medium":
        return "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
      case "low":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
      default:
        return "bg-platinum-500/10 text-platinum-400 border-platinum-500/20"
    }
  }

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
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gradient mb-4">Security Reports</h1>
              <p className="text-platinum-400 max-w-2xl leading-relaxed text-lg">
                Detailed vulnerability reports identifying critical security issues in major platforms and payment
                systems, helping secure systems used by millions of users worldwide.
              </p>
            </div>

            <div className="w-full md:w-auto">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search reports..."
                  className="w-full md:w-80 px-4 py-3 pl-12 glass-card rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/50 text-platinum-200 placeholder-platinum-500 transition-all duration-300"
                />
                <Search className="absolute left-4 top-3.5 h-5 w-5 text-platinum-500" />
              </div>
            </div>
          </div>

          <div className="mb-12 flex flex-wrap gap-3">
            {severityLevels.map((level) => (
              <Badge
                key={level}
                className={`px-4 py-2 text-sm cursor-pointer transition-all duration-300 ${
                  level === "All"
                    ? "bg-gradient-to-r from-emerald-500 to-sapphire-500 text-obsidian-950 hover:from-emerald-400 hover:to-sapphire-400"
                    : "glass-card-hover text-platinum-300 border-platinum-500/20"
                }`}
              >
                {level}
              </Badge>
            ))}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {reports.map((report, index) => (
              <div key={index} className="group glass-card-hover rounded-2xl overflow-hidden">
                <div className="p-8">
                  <div className="flex items-center justify-between mb-4">
                    <Badge className={cn("px-3 py-1", getSeverityColor(report.severity))}>
                      {report.severity} Severity
                    </Badge>
                    <div className="flex items-center gap-2">
                      <Calendar className="h-4 w-4 text-platinum-500" />
                      <span className="text-sm text-platinum-500">{report.date}</span>
                    </div>
                  </div>

                  <h2 className="text-xl font-bold mb-3 group-hover:text-gradient transition-colors duration-300 leading-tight">
                    <Link href={`/reports/${report.slug}`}>{report.title}</Link>
                  </h2>

                  <p className="text-platinum-400 text-sm mb-4 leading-relaxed">{report.excerpt}</p>

                  <div className="flex items-center gap-2 mb-6">
                    <Shield className="h-4 w-4 text-red-400" />
                    <span className="text-sm text-red-400 font-medium">{report.impact}</span>
                  </div>

                  <div className="flex flex-wrap gap-3">
                    <Link
                      href={`/reports/${report.slug}`}
                      className="text-emerald-400 flex items-center gap-1 text-sm font-medium hover:text-emerald-300 transition-colors group"
                    >
                      Read Full Report{" "}
                      <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform duration-300" />
                    </Link>

                    <Link
                      href={`/reports/${report.slug}/download`}
                      className="text-platinum-500 flex items-center gap-1 text-sm font-medium hover:text-platinum-300 transition-colors group"
                    >
                      <Download className="h-4 w-4 group-hover:scale-110 transition-transform duration-300" /> Download
                      PDF
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
