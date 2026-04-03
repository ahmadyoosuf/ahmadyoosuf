/**
 * Converts a simplified markdown string to HTML with Tailwind classes.
 * Used by blog posts and security reports.
 */
export function renderMarkdown(markdown: string): string {
  let html = markdown
    // Handle headers — order matters: h4 first, then h3, then h2
    .replace(/^####\s+(.*)/gm, '<h4 class="text-lg font-bold mt-4 mb-2 text-platinum-300">$1</h4>')
    .replace(/^###\s+(.*)/gm, '<h3 class="text-xl font-bold mt-6 mb-3 text-diamond-200">$1</h3>')
    .replace(/^##\s+(.*)/gm, '<h2 class="text-2xl font-bold mt-8 mb-4 text-luxury">$1</h2>')

  // Handle lists — both ordered and unordered as bullet points
  html = html.replace(/^\d+\.\s+(.*)/gm, '<li class="ml-6 list-disc mb-2 text-platinum-400">$1</li>')
  html = html.replace(/^-\s+(.*)/gm, '<li class="ml-6 list-disc mb-2 text-platinum-400">$1</li>')

  // Handle paragraphs (lines not already wrapped in tags)
  html = html.replace(
    /^(?!<h|<li|<ul|<ol|<p|<div)(.*)/gm,
    '<p class="mb-4 text-platinum-400 leading-relaxed">$1</p>',
  )

  // Handle bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-diamond-200">$1</strong>')

  // Handle italic
  html = html.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')

  // Clean up empty paragraphs
  html = html.replace(/<p[^>]*>\s*<\/p>/g, "")

  return html
}
