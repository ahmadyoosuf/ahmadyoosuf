import { notFound } from "next/navigation"
import Link from "next/link"
import { ArrowLeft, Calendar, Tag, User } from "lucide-react"
import { Badge } from "@/components/ui/badge"

// This would typically come from a CMS or MDX files
const getBlogPost = (slug: string) => {
  const posts = {
    "payment-systems-bugs": {
      title: "Why I Hunt Bugs in Payment Systems",
      date: "January 12, 2025",
      author: "Ahmad Mohamed Yoosuf",
      category: "Security",
      readTime: "8 min read",
      content: `
      <p>Most security researchers go after authentication bypasses or XSS vulnerabilities. I hunt payment bugs. Not because they're technically complex (they're often embarrassingly simple), but because they reveal something profound about how we build systems.</p>
      
      <h2>The €366 Lesson</h2>
      <p>When I found that Dropbox would give you €366 worth of premium features just by entering any IBAN, I wasn't surprised. When Stripe's implementation had the same flaw across multiple merchants, I wasn't surprised either. What surprised me was that these weren't bugs. They were features.</p>
      
      <p>The systems were working exactly as designed. The designers just never asked: "What if someone lies?"</p>
      
      <h2>The Trust Assumption</h2>
      <p>Payment systems are built on a fascinating assumption: people won't commit fraud for small amounts. This isn't naivety. It's economics. The cost of preventing every €10 fraud might be €50 in engineering time and user friction.</p>
      
      <p>But this calculation breaks when:</p>
      <ul>
        <li>The "small amount" is €366 (not so small anymore)</li>
        <li>The fraud is automated (scale changes everything)</li>
        <li>The regulatory environment shifts (EU's new instant payment rules)</li>
      </ul>
      
      <h2>Why SEPA Is a Beautiful Mess</h2>
      <p>SEPA Direct Debit is particularly interesting because it's asynchronous by design. When you enter an IBAN, the merchant doesn't know if it's valid. They won't know for days. Sometimes weeks.</p>
      
      <p>So they have three choices:</p>
      <ol>
        <li>Wait weeks to activate your service (terrible UX)</li>
        <li>Activate immediately and eat the losses (terrible business)</li>
        <li>Activate immediately and hope you're honest (terrible security)</li>
      </ol>
      
      <p>Most choose option 3. Then they're shocked when someone posts about it in a Telegram group with 10,000 members.</p>
      
      <h2>The Real Vulnerability</h2>
      <p>The technical vulnerability is trivial: missing IBAN validation. But the real vulnerability is deeper. It's the assumption that payment systems can be trusted to work like payment systems.</p>
      
      <p>When you swipe a credit card, authorization is instant. When you send a wire, it's (mostly) final. But SEPA? SEPA is built on the assumption that everyone has a European bank account, everyone is traceable, and everyone fears consequences.</p>
      
      <p>Remove any of those assumptions. VPN to Italy, fake details, disposable email. The whole system collapses.</p>
      
      <h2>The Pattern</h2>
      <p>After finding the same vulnerability in multiple systems, I've noticed a pattern:</p>
      <ul>
        <li><strong>Day 1:</strong> "We need to accept European payments"</li>
        <li><strong>Day 30:</strong> "SEPA integration is working!"</li>
        <li><strong>Day 90:</strong> "Why is our chargeback rate 40%?"</li>
        <li><strong>Day 91:</strong> "Oh."</li>
      </ul>
      
      <h2>Why This Matters</h2>
      <p>By October 2025, the EU's new instant payment regulation requires IBAN-name verification. Every payment system built on trust-assumptions will need to be rebuilt on verify-assumptions. The companies that understand this early will save millions. The ones that don't will learn why I hunt these bugs.</p>
      
      <p>The beautiful irony? The same companies spending millions on AI-powered fraud detection can't implement basic IBAN validation. They're so focused on complex threats that they miss the simple ones.</p>
      
      <h2>The Uncomfortable Truth</h2>
      <p>Here's what nobody wants to admit: these vulnerabilities exist because fixing them would hurt conversion rates. Every additional verification step loses customers. Every friction point costs money.</p>
      
      <p>So companies make a calculated bet: the fraud losses will be less than the conversion gains. Usually, they're right. Until someone like me shows up and explains why they're not.</p>
      
      <p>I don't hunt payment bugs because they're hard to find. I hunt them because they're hard to fix. Not technically, but economically. And that gap between what's possible and what's profitable? That's where the real vulnerabilities live.</p>
    `,
    },
    "myth-of-self-made": {
      title: "The Myth of the Self-Made Success",
      date: "December 28, 2024",
      author: "Ahmad Mohamed Yoosuf",
      category: "Leadership",
      readTime: "12 min read",
      content: `
      <p>My father studied until 3rd grade. He became an Islamic scholar and educationist. By every Silicon Valley metric, he was a failure. By every metric that matters, he was not.</p>
      
      <p>I founded The Yoosuf Foundation in his name, and after mentoring 50+ first-generation students, I've learned something that contradicts everything we're told about success: the "self-made" narrative is not just wrong. It's actively harmful.</p>
      
      <h2>The GitHub Student Pack Revelation</h2>
      <p>Last month, I helped a brilliant student access the GitHub Student Developer Pack. Free domain, free hosting, $100 in cloud credits. His reaction? "Why didn't anyone tell me this existed?"</p>
      
      <p>That's when it hit me. The difference between him and his peers wasn't talent or drive. It was information. His classmates knew because their older siblings knew. Their siblings knew because their parents knew. The chain of knowledge that seems obvious to some is completely invisible to others.</p>
      
      <h2>The Compound Interest of Context</h2>
      <p>When people see successful first-generation professionals, they see the outcome, not the process. They don't see:</p>
      <ul>
        <li>The scholarship application you didn't submit because you didn't know it existed</li>
        <li>The internship you didn't apply for because you thought it was "not for people like you"</li>
        <li>The mentor you didn't reach out to because you didn't know that was allowed</li>
        <li>The conference you didn't attend because you didn't know students got free tickets</li>
      </ul>
      
      <p>Each missed opportunity compounds. By graduation, the gap isn't just wide. It's exponential.</p>
      
      <h2>The Bootstraps Paradox</h2>
      <p>"Pull yourself up by your bootstraps" assumes you have boots. And that you know what bootstraps are. And that pulling them achieves something.</p>
      
      <p>The students I mentor don't lack ambition. They lack context. They're not trying to climb a ladder. They're trying to build one while climbing it, without instructions, in the dark.</p>
      
      <h2>What Actually Works</h2>
      <p>After 50+ mentorship relationships, here's what I've learned actually helps:</p>
      
      <h3>1. Make the Implicit Explicit</h3>
      <p>Never assume knowledge. I once spent an hour explaining what "networking" actually means because a student thought it was "bothering important people." He wasn't wrong about how it feels. He just didn't know that's how everyone feels.</p>
      
      <h3>2. Systems Over Inspiration</h3>
      <p>Motivational speeches don't help when you don't know how to write a cold email. Templates do. Processes do. Step-by-step guides do. First-generation students don't need inspiration. They have plenty. They need infrastructure.</p>
      
      <h3>3. Permission Structures</h3>
      <p>The biggest barrier isn't ability. It's permission. Permission to apply for "reach" opportunities. Permission to ask questions. Permission to fail. Many first-generation students are carrying their entire family's hopes. Failure isn't just personal. It's generational.</p>
      
      <h2>The Success Myth</h2>
      <p>Here's what the "self-made" narrative gets wrong: success isn't individual. It's ecological. Every successful person is supported by an invisible infrastructure of knowledge, connections, and permissions that they didn't create.</p>
      
      <p>The question isn't "How can individuals succeed despite the system?" It's "How can we make the system visible to those who can't see it?"</p>
      
      <h2>The Real Work</h2>
      <p>The Yoosuf Foundation isn't about charity. It's about infrastructure. We're not giving fish or teaching fishing. We're explaining that the pond exists, that you're allowed to fish there, that there's a specific permit you need, and that it's free on Tuesdays.</p>
      
      <p>The most radical thing we do? We tell students that their confusion is not their fault. The system is opaque by design, not by accident. Those who navigate it successfully usually had a guide. We're just making the guides visible.</p>
      
      <h2>The Uncomfortable Question</h2>
      <p>If you're successful, ask yourself: What did you know that others didn't? Not what you did. What you knew. The answer is probably longer than you think.</p>
      
      <p>Then ask: Who told you?</p>
      
      <p>That's your real advantage. Not your work ethic. Not your intelligence. Your access to information that others assumed you'd never need to be told.</p>
      
      <p>The myth of self-made success isn't just wrong. It's cruel. It tells those without guides that their confusion is a character flaw. It's not. It's a system failure.</p>
      
      <p>And systems can be fixed.</p>
    `,
    },
    "building-ai-products": {
      title: "Building AI Products That Actually Work",
      date: "November 15, 2024",
      author: "Ahmad Mohamed Yoosuf",
      category: "AI",
      readTime: "10 min read",
      content: `
      <p>After building OCRPro and A111y, I've learned that successful AI products aren't about using the latest models or the most complex architectures. They're about solving real problems in ways that existing solutions don't.</p>
      
      <h2>The Problem with Most AI Products</h2>
      <p>The AI landscape is littered with products that are technically impressive but practically useless. They demonstrate capabilities without addressing actual user needs, or they solve problems that don't really exist. This happens when teams focus on the technology rather than the problem.</p>
      
      <h2>OCRPro: A Case Study in Practical AI</h2>
      <p>When I started building OCRPro, the market already had established players like AWS Textract, Azure OCR, and Google Cloud OCR. The question wasn't whether we could build an OCR engine. It was whether we could build one that was meaningfully better.</p>
      
      <h3>Finding the Gap</h3>
      <p>Through extensive testing, I discovered that existing solutions had three main issues:</p>
      <ul>
        <li><strong>Cost:</strong> Enterprise OCR solutions were prohibitively expensive for many use cases</li>
        <li><strong>Speed:</strong> Processing times were often too slow for real-time applications</li>
        <li><strong>Accuracy on edge cases:</strong> Performance degraded significantly on non-standard documents</li>
      </ul>
      
      <h3>The Solution</h3>
      <p>OCRPro addresses these issues through:</p>
      <ul>
        <li>A hybrid architecture that balances accuracy and speed</li>
        <li>Specialized models for different document types</li>
        <li>Aggressive optimization for common use cases</li>
        <li>A pricing model that scales with actual usage, not enterprise contracts</li>
      </ul>
      
      <p>The result? An OCR engine that outperforms industry leaders on the metrics that actually matter to users.</p>
      
      <h2>A11y: Making Accessibility Accessible</h2>
      <p>A11y emerged from a different observation: while everyone agrees that web accessibility is important, most developers find accessibility testing tools too complex or too removed from their workflow.</p>
      
      <h3>The Traditional Approach</h3>
      <p>Most accessibility tools either:</p>
      <ul>
        <li>Require extensive manual testing</li>
        <li>Generate overwhelming reports with hundreds of issues</li>
        <li>Focus on compliance rather than actual user experience</li>
      </ul>
      
      <h3>Our Approach</h3>
      <p>A11y takes a different path:</p>
      <ul>
        <li><strong>AI-powered analysis:</strong> Understands context, not just rules</li>
        <li><strong>Prioritized recommendations:</strong> Shows what matters most</li>
        <li><strong>Developer-friendly:</strong> Integrates into existing workflows</li>
        <li><strong>Focus on impact:</strong> Measures real accessibility improvements</li>
      </ul>
      
      <h2>Lessons Learned</h2>
      
      <h3>1. Start with the Problem, Not the Technology</h3>
      <p>Both OCRPro and A11y succeeded because they started with clear problem statements. The AI technology was a means to solve these problems, not the end goal.</p>
      
      <h3>2. Benchmark Against Real-World Usage</h3>
      <p>Academic benchmarks are useful, but real-world performance is what matters. OCRPro's edge came from optimizing for actual documents users process, not standardized test sets.</p>
      
      <h3>3. Make It 10x Better, Not 10% Better</h3>
      <p>To compete with established solutions, marginal improvements aren't enough. You need to be dramatically better on at least one dimension that users care about.</p>
      
      <h3>4. Developer Experience Is User Experience</h3>
      <p>For developer tools like A111y, the API design, documentation, and integration process are as important as the core functionality.</p>
      
      <h3>5. Measure What Matters</h3>
      <p>Success metrics should align with user value. For OCRPro, it's not just accuracy. It's accuracy per dollar and accuracy per second. For A11y, it's not just finding issues. It's helping developers fix them.</p>
      
      <h2>The Future of Practical AI</h2>
      <p>As AI capabilities continue to expand, the opportunity isn't in building more powerful models. It's in applying existing capabilities to solve real problems better than current solutions.</p>
      
      <p>The next generation of successful AI products will be those that:</p>
      <ul>
        <li>Solve specific, well-defined problems</li>
        <li>Integrate seamlessly into existing workflows</li>
        <li>Provide clear, measurable value</li>
        <li>Focus on user outcomes, not technical metrics</li>
      </ul>
      
      <h2>Conclusion</h2>
      <p>Building AI products that actually work isn't about having the most advanced technology. It's about understanding problems deeply and applying technology thoughtfully. OCRPro and A11y succeed not because they use cutting-edge AI, but because they use AI to cut through real-world problems.</p>
      
      <p>The best AI products are often the ones where users don't even think about the AI. They just appreciate that their problem is solved better than before.</p>
    `,
    },
    "speed-is-the-only-moat": {
      title: "Speed Is the Only Moat",
      date: "October 22, 2024",
      author: "Ahmad Mohamed Yoosuf",
      category: "Product",
      readTime: "6 min read",
      content: `
      <p>I built MARSAD in a few weeks. Solo. Not because I'm exceptional, but because I had to. In the time it would take to write a requirements document, the entire competitive landscape can shift. Speed isn't just an advantage. It's the only sustainable one.</p>
      
      <h2>The Half-Life of Features</h2>
      <p>Every feature you build can be replicated. With AI, that replication time has dropped from months to days. Sometimes hours. That innovative OCR preprocessing pipeline that took you weeks to perfect? Someone can describe it to Claude and get 80% of the way there before lunch.</p>
      
      <p>This sounds depressing. It's actually liberating.</p>
      
      <h2>The Speed Paradox</h2>
      <p>If everything can be copied, nothing can be defended. So why build anything? Because by the time they copy what you built, you've already built the next thing. And the next. And the next.</p>
      
      <p>Speed compounds in ways that features don't:</p>
      <ul>
        <li>Features can be copied. Momentum cannot.</li>
        <li>Code can be replicated. Customer relationships cannot.</li>
        <li>Products can be cloned. Market timing cannot.</li>
      </ul>
      
      <h2>What Speed Actually Means</h2>
      <p>Speed isn't about typing faster or working longer hours. It's about:</p>
      
      <h3>1. Decision Velocity</h3>
      <p>The fastest code is the code you don't write. The fastest meeting is the meeting you don't have. The fastest feature is the one you decide not to build. Speed is mostly about what you don't do.</p>
      
      <h3>2. Deployment Courage</h3>
      <p>Perfect is the enemy of shipped. But "move fast and break things" is lazy thinking. The real skill is knowing what can break (and be fixed) versus what must work. Deploy fearlessly where you can. Be paranoid where you must.</p>
      
      <h3>3. Learning Loops</h3>
      <p>Speed without direction is just chaos. The goal isn't to build fast. It's to learn fast. Every deployment should answer a question. Every feature should test a hypothesis. Speed is valuable only if it accelerates learning.</p>
      
      <h2>The MARSAD Lesson</h2>
      <p>When I built MARSAD, I had every reason to go slow. Complex requirements. Multiple stakeholders. International collaboration. Instead, I shipped a working version in weeks.</p>
      
      <p>Why? Because a working prototype answers questions that a thousand meetings cannot. Because real users give feedback that no committee can predict. Because done is better than perfect when perfect means never.</p>
      
      <h2>The Uncomfortable Truth About Moats</h2>
      <p>Traditional moats are dying:</p>
      <ul>
        <li><strong>Technical complexity?</strong> AI can understand and replicate it.</li>
        <li><strong>Capital requirements?</strong> Cloud infrastructure democratized that.</li>
        <li><strong>Network effects?</strong> Still powerful, but increasingly winner-take-all.</li>
        <li><strong>Regulatory barriers?</strong> Helpful, but not if you want to innovate.</li>
      </ul>
      
      <p>What's left? Speed. The ability to identify opportunities, execute solutions, and iterate based on feedback faster than anyone else.</p>
      
      <h2>Speed as a Practice</h2>
      <p>Speed isn't a personality trait. It's a practice. Here's what I've learned:</p>
      
      <h3>1. Constraint Is Freedom</h3>
      <p>Unlimited time leads to unlimited scope. When I gave myself weeks to build MARSAD, I had to focus on what mattered. Constraints force clarity.</p>
      
      <h3>2. Boring Is Beautiful</h3>
      <p>Use boring technology. Choose proven patterns. Save your innovation budget for where it matters. Speed comes from not reinventing wheels.</p>
      
      <h3>3. Ship to Think</h3>
      <p>You can't think your way to clarity. You have to ship your way there. The fastest path to a good product is through a bad product that exists.</p>
      
      <h2>The Speed Trap</h2>
      <p>There's a difference between moving fast and rushing. Rushing is panic-driven. Speed is intention-driven. Rushing cuts corners. Speed cuts scope.</p>
      
      <p>The goal is to be fastest at what matters. And what matters changes. Speed includes the ability to change direction quickly when you learn what actually matters.</p>
      
      <h2>Why This Matters Now</h2>
      <p>AI is changing how fast others can copy what we build. In this new world, sustainable advantage comes from how fast you can build the next thing.</p>
      
      <p>The companies that will thrive are the ones with the fastest learning loops. The ones that can go from idea to user feedback while their competitors are still in planning meetings.</p>
      
      <p>Speed is the only moat because it's the only advantage that gets stronger when others try to copy it. The more they focus on copying what you did, the less they focus on what you're doing next.</p>
      
      <p>And by the time they catch up, you're already somewhere else.</p>
    `,
    },
    "agentic-cloud-security": {
      title: "Agentic Cloud Security: Beyond Detection",
      date: "July 20, 2025",
      author: "Ahmad Mohamed Yoosuf",
      category: "Security",
      readTime: "9 min read",
      content: `
    <p>Most security tools just generate alerts. Security teams need a closed-loop system that detects, analyzes, and fixes issues automatically.</p>
    
    <h2>The Alert Fatigue Problem</h2>
    <p>Security teams are drowning in alerts from dozens of tools. Most are low context and require manual investigation. Critical threats get lost in a sea of trivial notifications. The industry has responded with more dashboards, not more solutions.</p>
    
    <h2>Building an Autonomous Security Engine</h2>
    <p>We need to move from passive detection to active, automated remediation. Here is a blueprint for how such a system operates:</p>
    
    <div class="my-8 p-6 luxury-glass rounded-xl">
      <h3 class="text-lg font-bold mb-4 text-diamond-200">Security Automation Workflow</h3>
      <div class="space-y-4 text-sm">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-ruby-500/20 flex items-center justify-center text-ruby-400 font-bold">1</div>
          <div>
            <div class="font-semibold text-diamond-200">Exhaustive Scanning</div>
            <div class="text-platinum-400">Deep AWS environment scan using boto3</div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-ruby-500/20 flex items-center justify-center text-ruby-400 font-bold">2</div>
          <div>
            <div class="font-semibold text-diamond-200">Contextual Analysis</div>
            <div class="text-platinum-400">Query CVE database for impact assessment</div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-ruby-500/20 flex items-center justify-center text-ruby-400 font-bold">3</div>
          <div>
            <div class="font-semibold text-diamond-200">Intelligent Triage</div>
            <div class="text-platinum-400">AI model separates signals from noise</div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-ruby-500/20 flex items-center justify-center text-ruby-400 font-bold">4</div>
          <div>
            <div class="font-semibold text-diamond-200">Validation</div>
            <div class="text-platinum-400">Confirm exploitability before action</div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-ruby-500/20 flex items-center justify-center text-ruby-400 font-bold">5</div>
          <div>
            <div class="font-semibold text-diamond-200">Decision Engine</div>
            <div class="text-platinum-400">Determine if remediation is needed</div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-ruby-500/20 flex items-center justify-center text-ruby-400 font-bold">6</div>
          <div>
            <div class="font-semibold text-diamond-200">Automated Fix</div>
            <div class="text-platinum-400">Execute remediation commands</div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-ruby-500/20 flex items-center justify-center text-ruby-400 font-bold">7</div>
          <div>
            <div class="font-semibold text-diamond-200">Verification</div>
            <div class="text-platinum-400">Confirm fix and mark as resolved</div>
          </div>
        </div>
      </div>
    </div>

    <h3>Step 1: Exhaustive Scanning</h3>
    <p>Deep scanning of the AWS environment using tools like boto3. You cannot secure what you cannot see. This scan gathers raw configuration data, permissions, and asset information.</p>
    
    <h3>Step 2: Contextual Analysis</h3>
    <p>Raw data needs context. We query a graph database of CVEs and infrastructure relationships to understand the potential impact of each finding. This connects a specific vulnerability to the actual business asset it affects.</p>
    
    <h3>Step 3: Intelligent Triage</h3>
    <p>An AI model analyzes the findings, tags relevant CVEs, and separates real signals from noise. Understanding which vulnerabilities matter right now in your specific environment.</p>
    
    <h3>Step 4: Grounding and Validation</h3>
    <p>Before taking action, the AI validates its findings with additional context. It checks configurations, logs, and network paths to confirm a vulnerability is actually exploitable. This prevents false positives from triggering unnecessary actions.</p>
    
    <h3>Step 5: The Decision Engine</h3>
    <p>The system decides if action is needed. If the environment is secure, the loop ends. If a validated threat exists, it proceeds to remediation.</p>
    
    <h3>Step 6: Automated Remediation</h3>
    <p>The system executes commands to fix the issue. This can be fully automated for known, high confidence issues. For more complex problems, it provides assisted feedback for manual intervention.</p>
    
    <h3>Step 7: Verification</h3>
    <p>After remediation, the system re-scans and verifies the fix. If the issue persists, the loop repeats. If the fix is confirmed, the environment is marked as secured.</p>
    
    <h2>Implementation Reality</h2>
    <p>Complex cloud environments require automated remediation at scale. Building systems that fix themselves frees human experts to focus on novel threats. Moving from passive detection to active remediation becomes the standard approach to cloud security.</p>
  `,
    },
  }

  if (!posts[slug as keyof typeof posts]) {
    return null
  }

  return posts[slug as keyof typeof posts]
}

// Function to convert markdown to HTML
const renderMarkdown = (markdown: string) => {
  // Handle headers
  let html = markdown
    .replace(/^#{2,}\s*(.*)/gm, '<h2 class="text-2xl font-bold mt-8 mb-4 text-luxury">$1</h2>')
    .replace(/^#{3,}\s*(.*)/gm, '<h3 class="text-xl font-bold mt-6 mb-3 text-diamond-200">$1</h3>')
    .replace(/^#{4,}\s*(.*)/gm, '<h4 class="text-lg font-bold mt-4 mb-2 text-platinum-300">$1</h4>')

  // Handle lists - all as bullet points
  html = html.replace(/^\d+\.\s+(.*)/gm, '<li class="ml-6 list-disc mb-2 text-platinum-400">$1</li>')
  html = html.replace(/^-\s+(.*)/gm, '<li class="ml-6 list-disc mb-2 text-platinum-400">$1</li>')

  // Handle paragraphs
  html = html.replace(/^(?!<h|<li|<ul|<ol|<p|<div)(.*)/gm, '<p class="mb-4 text-platinum-400 leading-relaxed">$1</p>')

  // Handle bold
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-diamond-200">$1</strong>')

  // Handle italic
  html = html.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')

  // Clean up empty paragraphs
  html = html.replace(/<p>\s*<\/p>/g, "")

  return html
}

export default function BlogPost({ params }: { params: { slug: string } }) {
  const post = getBlogPost(params.slug)

  if (!post) {
    notFound()
  }

  return (
    <div className="min-h-screen bg-obsidian-950 text-platinum-100">
      <div className="container px-4 py-24 mx-auto max-w-4xl">
        <Link
          href="/blog"
          className="inline-flex items-center text-sm text-platinum-500 hover:text-emerald-400 mb-8 transition-colors group"
        >
          <ArrowLeft className="mr-2 h-4 w-4 group-hover:-translate-x-1 transition-transform duration-300" />
          Back to all posts
        </Link>

        <article className="prose prose-invert prose-lg max-w-none">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 text-gradient leading-tight">{post.title}</h1>

          <div className="flex flex-wrap gap-4 mb-8 text-sm text-platinum-500">
            <div className="flex items-center">
              <Calendar className="h-4 w-4 mr-2" />
              {post.date}
            </div>
            <div className="flex items-center">
              <User className="h-4 w-4 mr-2" />
              {post.author}
            </div>
            <div className="flex items-center">
              <Tag className="h-4 w-4 mr-2" />
              <Badge className="glass-card text-platinum-300 border-platinum-500/20 px-3 py-1">{post.category}</Badge>
            </div>
            <span className="text-platinum-500">{post.readTime}</span>
          </div>

          <div className="mt-8 report-content" dangerouslySetInnerHTML={{ __html: renderMarkdown(post.content) }} />
        </article>
      </div>
    </div>
  )
}
