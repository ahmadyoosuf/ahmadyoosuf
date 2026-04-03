export interface SecurityReport {
  title: string
  date: string
  severity: string
  description: string
  slug: string
  impact: string
}

export const securityReports: SecurityReport[] = [
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
