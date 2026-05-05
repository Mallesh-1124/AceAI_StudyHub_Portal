import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Video, Bot, Shield, FileText, Calendar, Users } from "lucide-react"

const features = [
  {
    icon: Video,
    title: "Live Video Study Rooms",
    description: "Real-time group video sessions for focused collaborative learning with HD quality and screen sharing.",
  },
  {
    icon: Bot,
    title: "AI Teacher Assistant",
    description: "An intelligent AI guide that explains concepts, answers doubts, and follows admin instructions.",
  },
  {
    icon: Shield,
    title: "Admin-Controlled Rules",
    description: "Teaching style, difficulty level, and AI behavior fully controlled by instructors.",
  },
  {
    icon: FileText,
    title: "AI Session Summaries",
    description: "Automatic summaries and key takeaways generated after each study session.",
  },
  {
    icon: Calendar,
    title: "Personalized Study Planner",
    description: "AI-generated study plans based on your exams, goals, and learning pace.",
  },
  {
    icon: Users,
    title: "Collaborative Learning",
    description: "Work together on problems, share notes, and learn from peers in real-time.",
  },
]

export function FeaturesSection() {
  return (
    <section id="features" className="bg-muted/30 py-16 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Everything You Need to <span className="text-primary">Learn Smarter</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Powerful features designed to enhance your study experience and help you achieve your academic goals.
          </p>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <Card key={feature.title} className="border-border bg-card">
              <CardHeader>
                <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <feature.icon className="h-5 w-5 text-primary" />
                </div>
                <CardTitle className="text-lg text-foreground">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-muted-foreground">{feature.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
