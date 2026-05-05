import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Settings, BarChart3, DoorOpen, Users } from "lucide-react"

const stats = [
  { label: "Total Sessions", value: "1,234", change: "+12%" },
  { label: "Active Students", value: "156", change: "+8%" },
  { label: "Avg. Session Time", value: "45m", change: "+5%" },
  { label: "Topics Covered", value: "89", change: "+15%" },
]

const adminFeatures = [
  {
    icon: Settings,
    title: "Manage AI Teaching Style",
    description: "Configure how AI responds: step-by-step guidance, difficulty levels, subject focus",
    badge: "AI Settings",
    stat: "3 presets active",
  },
  {
    icon: BarChart3,
    title: "Session Analytics",
    description: "Track engagement, question frequency, topic coverage, and student progress",
    badge: "Analytics",
    stat: "+24% this week",
  },
  {
    icon: DoorOpen,
    title: "Control Study Rooms",
    description: "Create, schedule, and manage study rooms. Set capacity and access rules",
    badge: "Rooms",
    stat: "12 rooms active",
  },
  {
    icon: Users,
    title: "Student Activity",
    description: "Monitor individual progress, participation rates, and learning outcomes",
    badge: "Students",
    stat: "156 students",
  },
]

export function AdminDashboardSection() {
  return (
    <section id="admin" className="bg-muted/30 py-16 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Powerful <span className="text-primary">Admin Dashboard</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Full control over AI behavior, study rooms, and student analytics
          </p>
        </div>

        <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <Card key={stat.label} className="border-border bg-card">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                  <Badge variant="secondary" className="text-primary">{stat.change}</Badge>
                </div>
                <p className="text-sm text-muted-foreground">{stat.label}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          {adminFeatures.map((feature) => (
            <Card key={feature.title} className="border-border bg-card">
              <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <feature.icon className="h-5 w-5 text-muted-foreground" />
                    <Badge variant="outline" className="text-xs">{feature.badge}</Badge>
                  </div>
                </div>
                <CardTitle className="text-base text-foreground">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-muted-foreground">{feature.description}</CardDescription>
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">{feature.stat}</span>
                  <span className="text-xs font-medium text-primary cursor-pointer hover:underline">Configure</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
