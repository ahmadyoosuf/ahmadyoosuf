"use client"

import { useState } from "react"
import Link from "next/link"
import { ArrowLeft, Calendar } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

// This would typically come from a CMS or MDX files
const getReportContent = (slug: string) => {
  const reports = {
    "stripe-vulnerability": {
      title:
        "Critical Vulnerability Report: SEPA Direct Debit Payment System Validation Issue on Stripe Payment Gateway",
      date: "December 18, 2024",
      severity: "High",
      cvss: "8.8",
      content: `
## Description

A significant vulnerability has been identified in Stripe's SEPA Direct Debit payment system implementation, affecting multiple client companies including nele.ai. This vulnerability allows for premium subscription activation without proper IBAN validation, potentially violating EU financial regulations around payment verification and posing risks of unauthorized IBAN usage.

**CVSS Score**: **8.8 (High)**  
- **Attack Vector**: Network
- **Attack Complexity**: Low
- **Privileges Required**: None
- **User Interaction**: None
- **Impact**: High

### Steps to Reproduce:
1. Create a new account or use an existing free account on a Stripe-based service offering SEPA Direct Debit (e.g., nele.ai)
2. Navigate to the upgrade subscription page
3. Select SEPA Direct Debit as the payment method
4. Enter any valid IBAN format number
5. Complete the subscription process
6. Observe immediate activation of the premium subscription

### Technical Details
The current implementation allows:
- Premium subscription activation using any IBAN without proper verification
- Immediate access to premium features
- No validation between entered IBAN and account holder details

## Impact

### Regulatory Implications
The EU's new Instant Payments Regulation mandates:
- Verification between IBAN and account holder name for all SEPA transactions
- Implementation deadline of October 2025 for payment service providers
- Mandatory payee verification for all Euro transactions

### Business Impact
- Significant revenue leakage for both Stripe and its client companies due to failed SEPA mandates for invalid IBANs
- Processing fees for failed Direct Debit returns
- Potential regulatory scrutiny under new EU payment regulations
- Risk of unauthorized IBAN usage in payment systems
- Customer complaints about unauthorized charges

### Scope of the Issue
This vulnerability is present in most Stripe-based payment services that offer SEPA Direct Debit as a payment method. nele.ai is just one example of affected companies. The issue could lead to substantial financial losses across Stripe's client base.

### Industry Comparison
Companies like hide.me and squarespace.com, which use their own payment gateways, have successfully implemented proper IBAN validation, demonstrating that this issue can be effectively addressed.

### Recommended Fixes
1. Implement IBAN verification:
   - Account holder name validation
   - Integration with verification services
   - Real-time IBAN validation before subscription activation

2. Follow payment processing best practices:
   - Verify payment before service provisioning
   - Implement proper transaction monitoring

## Additional Information

I have attached the following to this report:
1. An invoice received from GAL Digital GmbH related to this transaction
2. A video recording demonstrating the vulnerability

Please note that I have also reported this vulnerability to nele.ai (support@nele.ai) to ensure all relevant parties are informed.

### Disclosure Timeline
- Public disclosure date: 18/12/2024 (5 weeks from now)
- This timeline may be extended if the fix is not implemented within this period

## Conclusion

This widespread vulnerability in Stripe's SEPA Direct Debit implementation potentially exposes both regulatory compliance risks and significant revenue leakage through failed SEPA mandates for Stripe and its client companies. Swift implementation of proper verification measures across Stripe's platform would help mitigate these risks and bring Stripe's services in line with industry best practices.
      `,
    },
    "dropbox-vulnerability": {
      title: "Critical Vulnerability Report: SEPA Direct Debit Payment System Validation Issue",
      date: "November 15, 2024",
      severity: "High",
      cvss: "8.8",
      content: `
## Summary

A significant vulnerability has been identified in Dropbox's SEPA Direct Debit payment system that allows premium subscription activation without proper IBAN validation. This could potentially violate EU financial regulations around payment verification and pose risks of unauthorized IBAN usage.

**CVSS Score**: **8.8 (High)**  
- **Attack Vector**: Network
- **Attack Complexity**: Low
- **Privileges Required**: None
- **User Interaction**: None
- **Impact**: High

The vulnerability is currently being discussed in a private Telegram group with 10,000 members.

## Technical Details

The current implementation allows:
1. Premium subscription activation using any IBAN without proper verification
2. Bypass of standard payment controls via VPN (tested with Italy, postal code 00185)
3. Immediate access to Dropbox Essentials Plus + 1TB Add-on + Replay (€366 value)

## Regulatory Implications

The EU's new Instant Payments Regulation mandates:
- Verification between IBAN and account holder name for all SEPA transactions
- Implementation deadline of October 2025 for payment service providers
- Mandatory payee verification for all Euro transactions

## Business Impact

### Potential Financial Implications
- Some revenue loss from failed SEPA mandates for invalid IBANs
- Possible regulatory scrutiny under new EU payment regulations
- Processing fees for failed Direct Debit returns

### Customer Trust Issues
- Risk of unauthorized IBAN usage in payment systems
- Potential for fraudulent subscription activations
- Customer complaints about unauthorized charges

## Proof of Concept

Video demonstration includes:
1. VPN connection to Italy (00185)
2. IBAN entry without verification
3. Premium feature activation
4. Successful bypass of payment controls

## Recommended Fixes

Based on the new EU regulations:
1. Implement IBAN verification:
   - Account holder name validation
   - Integration with verification services like SurePay or Signicat
   - Real-time IBAN validation before subscription activation

2. Follow payment processing best practices:
   - Verify payment before service provisioning
   - Implement proper transaction monitoring

## Disclosure Timeline

- Public disclosure date: 18/12/2024
- Timeline may be extended if remediation requires additional time

## Conclusion

While the exact responsibility for IBAN validation between payment service providers and merchants requires clarification, this vulnerability potentially exposes both regulatory compliance risks and revenue leakage through failed SEPA mandates. Swift implementation of proper verification measures would help mitigate these risks.

*Proof of Concept Video Attached*
      `,
    },
  }

  if (!reports[slug as keyof typeof reports]) {
    return null
  }

  return reports[slug as keyof typeof reports]
}

export default function ReportPage({ params }: { params: { slug: string } }) {
  const report = getReportContent(params.slug)
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false)

  if (!report) {
    return (
      <div className="min-h-screen bg-obsidian-950 text-platinum-100 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4 text-gradient">Report Not Found</h1>
          <Link href="/reports" className="text-emerald-400 hover:text-emerald-300 transition-colors">
            Back to Reports
          </Link>
        </div>
      </div>
    )
  }

  const handleDownloadPdf = () => {
    setIsGeneratingPdf(true)
    // Simulate PDF generation
    setTimeout(() => {
      setIsGeneratingPdf(false)
      // In a real implementation, this would trigger the actual PDF download
      alert("PDF downloaded successfully")
    }, 1500)
  }

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

  // Function to convert markdown to HTML (simplified version)
  const renderMarkdown = (markdown: string) => {
    // Handle headers - remove extra # symbols
    let html = markdown
      .replace(/^#{2,}\s*(.*)/gm, '<h2 class="text-2xl font-bold mt-8 mb-4 text-gradient">$1</h2>')
      .replace(/^#{3,}\s*(.*)/gm, '<h3 class="text-xl font-bold mt-6 mb-3 text-platinum-200">$1</h3>')
      .replace(/^#{4,}\s*(.*)/gm, '<h4 class="text-lg font-bold mt-4 mb-2 text-platinum-300">$1</h4>')

    // Handle lists - convert all to bullet points
    html = html.replace(/^\d+\.\s+(.*)/gm, '<li class="ml-6 list-disc mb-2 text-platinum-400">$1</li>')
    html = html.replace(/^-\s+(.*)/gm, '<li class="ml-6 list-disc mb-2 text-platinum-400">$1</li>')

    // Handle paragraphs
    html = html.replace(/^(?!<h|<li|<ul|<ol|<p|<div)(.*)/gm, '<p class="mb-4 text-platinum-400 leading-relaxed">$1</p>')

    // Handle bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-platinum-200">$1</strong>')

    // Handle italic
    html = html.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')

    // Clean up empty paragraphs
    html = html.replace(/<p>\s*<\/p>/g, "")

    return html
  }

  return (
    <div className="min-h-screen bg-obsidian-950 text-platinum-100">
      <div className="container px-4 py-24 mx-auto max-w-4xl">
        <Link
          href="/reports"
          className="inline-flex items-center text-sm text-platinum-500 hover:text-emerald-400 mb-8 transition-colors group"
        >
          <ArrowLeft className="mr-2 h-4 w-4 group-hover:-translate-x-1 transition-transform duration-300" />
          Back to all reports
        </Link>

        <article className="prose prose-invert prose-lg max-w-none">
          <div className="mb-8">
            <div className="flex flex-wrap gap-3 mb-6">
              <Badge className={cn("px-3 py-1", getSeverityColor(report.severity))}>{report.severity} Severity</Badge>
              <Badge className="glass-card text-platinum-300 border-platinum-500/20 px-3 py-1">
                CVSS {report.cvss}
              </Badge>
            </div>

            <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 text-gradient leading-tight">
              {report.title}
            </h1>

            <div className="flex flex-wrap gap-4 mb-8 text-sm text-platinum-500">
              <div className="flex items-center">
                <Calendar className="h-4 w-4 mr-2" />
                {report.date}
              </div>
            </div>

            <div className="flex flex-wrap gap-3 mb-8">{/* Removed buttons */}</div>
          </div>

          <div className="mt-8 report-content" dangerouslySetInnerHTML={{ __html: renderMarkdown(report.content) }} />
        </article>
      </div>
    </div>
  )
}
