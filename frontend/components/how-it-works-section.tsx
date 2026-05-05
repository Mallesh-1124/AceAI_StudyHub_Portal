import { UserPlus, DoorOpen, Play, MessageSquare, FileText } from "lucide-react"

const steps = [
  {
    icon: UserPlus,
    title: "Sign Up",
    description: "Create your account as a Student or Admin in seconds.",
  },
  {
    icon: DoorOpen,
    title: "Create or Join Room",
    description: "Start a new study room or join an existing session.",
  },
  {
    icon: Play,
    title: "Start Live Session",
    description: "Connect with video with your study group.",
  },
  {
    icon: MessageSquare,
    title: "Ask AI Teacher",
    description: "Get instant help and explanations from AI.",
  },
  {
    icon: FileText,
    title: "Get Summary",
    description: "Receive automated summaries and personalized study plan.",
  },
]

export function HowItWorksSection() {
  return (
    <section id="how-it-works" className="py-16 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            How It <span className="text-primary">Works</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Get started in minutes with our simple five-step process
          </p>
        </div>

        <div className="mt-12 flex flex-wrap justify-center gap-4 lg:gap-8">
          {steps.map((step, index) => (
            <div key={step.title} className="flex flex-col items-center text-center w-36 lg:w-44">
              <div className="relative">
                <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10">
                  <step.icon className="h-6 w-6 text-primary" />
                </div>
                {index < steps.length - 1 && (
                  <div className="absolute left-full top-1/2 hidden h-0.5 w-8 -translate-y-1/2 bg-border lg:block" />
                )}
              </div>
              <h3 className="mt-4 text-sm font-semibold text-foreground">{step.title}</h3>
              <p className="mt-1 text-xs text-muted-foreground">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
