/**
 * Returns Tailwind classes for severity badge styling.
 * Shared across homepage, reports listing, and report detail pages.
 */
export function getSeverityColor(severity: string): string {
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
