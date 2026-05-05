import { Badge } from "@/components/ui/badge"

const technologies = [
  { name: "Django", description: "Backend Framework", icon: "D" },
  { name: "REST APIs", description: "API Architecture", icon: "R" },
  { name: "AI Models", description: "Machine Learning", icon: "A" },
  { name: "WebSockets", description: "Real-time Communication", icon: "W" },
  { name: "WebRTC", description: "Video Streaming", icon: "W" },
  { name: "PostgreSQL", description: "Database Storage", icon: "P" },
]

export function TechStackSection() {
  return (
    <section className="py-16 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Built with <span className="text-primary">Modern Tech</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Powered by industry-leading technologies for scalability and performance
          </p>
        </div>

        <div className="mt-12 flex flex-wrap justify-center gap-4">
          {technologies.map((tech) => (
            <div
              key={tech.name}
              className="flex items-center gap-3 rounded-lg border border-border bg-card px-4 py-3"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 font-bold text-primary">
                {tech.icon}
              </div>
              <div>
                <p className="font-medium text-foreground">{tech.name}</p>
                <p className="text-xs text-muted-foreground">{tech.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
