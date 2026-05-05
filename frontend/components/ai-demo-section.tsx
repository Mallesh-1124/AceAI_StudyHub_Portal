import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { Bot, AlertCircle } from "lucide-react"

export function AIDemoSection() {
  return (
    <section id="ai-demo" className="bg-muted/30 py-16 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            AI Teacher in <span className="text-primary">Action</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            See how our AI adapts to admin instructions while helping students learn effectively
          </p>
        </div>

        <div className="mx-auto mt-12 max-w-3xl">
          <Card className="overflow-hidden border-border bg-card">
            <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-3">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary">
                  <Bot className="h-4 w-4 text-primary-foreground" />
                </div>
                <span className="font-medium text-foreground">AI Teacher Assistant</span>
              </div>
              <Badge variant="outline" className="text-primary border-primary">Controlled Mode</Badge>
            </div>

            <div className="p-4 space-y-4">
              <div className="flex items-start gap-2 rounded-lg bg-amber-50 p-3 text-sm">
                <AlertCircle className="h-4 w-4 text-amber-600 mt-0.5 flex-shrink-0" />
                <p className="text-amber-800">
                  <span className="font-medium">Admin Instruction:</span> &quot;Explain step-by-step, guide the student but don&apos;t give direct answers.&quot;
                </p>
              </div>

              <div className="space-y-3">
                <div className="flex gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-700 text-xs font-medium flex-shrink-0">
                    S
                  </div>
                  <div className="rounded-lg bg-muted px-3 py-2">
                    <p className="text-xs text-muted-foreground mb-1">Sarah (Student) · 2:14 PM</p>
                    <p className="text-sm text-foreground">Can you help me solve this quadratic equation: x² + 5x + 6 = 0?</p>
                  </div>
                </div>

                <div className="flex gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium flex-shrink-0">
                    AI
                  </div>
                  <div className="rounded-lg border border-primary/20 bg-primary/5 px-3 py-2 flex-1">
                    <p className="text-xs text-muted-foreground mb-1">AI Teacher · 2:14 PM</p>
                    <div className="text-sm text-foreground space-y-2">
                      <p><span className="font-medium">Great question!</span> Let me guide you through this step by step.</p>
                      <p><span className="font-medium">Step 1:</span> We need to factor this quadratic. Look at the equation x² + 5x + 6 = 0</p>
                      <p><span className="font-medium">Hint:</span> What two numbers multiply to give you 6 AND add up to 5?</p>
                      <p className="text-muted-foreground italic">Think about it and let me know what you come up with! I&apos;m here to help if you get stuck.</p>
                    </div>
                  </div>
                </div>

                <div className="flex gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-700 text-xs font-medium flex-shrink-0">
                    S
                  </div>
                  <div className="rounded-lg bg-muted px-3 py-2">
                    <p className="text-xs text-muted-foreground mb-1">Sarah (Student) · 2:16 PM</p>
                    <p className="text-sm text-foreground">Hmm... 2 and 3? Because 2 × 3 = 6 and 2 + 3 = 5</p>
                  </div>
                </div>

                <div className="flex gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-xs font-medium flex-shrink-0">
                    AI
                  </div>
                  <div className="rounded-lg border border-primary/20 bg-primary/5 px-3 py-2 flex-1">
                    <p className="text-xs text-muted-foreground mb-1">AI Teacher · 2:16 PM</p>
                    <div className="text-sm text-foreground space-y-2">
                      <p><span className="font-medium">Excellent work!</span> You&apos;ve got it! Now for <span className="font-medium">Step 2:</span></p>
                      <p>Can you use these numbers to write the factored form (x + ?)(x + ?) = 0</p>
                      <p className="text-muted-foreground italic">You&apos;re using amazing new points!</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}
