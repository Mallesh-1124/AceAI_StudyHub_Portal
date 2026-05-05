import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Mic, Video, MonitorUp, PhoneOff, Send, Bot, Users } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const participants = [
  { name: "Sarah M.", initials: "SM", color: "bg-blue-500" },
  { name: "Alex K.", initials: "AK", color: "bg-orange-500" },
  { name: "Mike R.", initials: "MR", color: "bg-purple-500" },
  { name: "Emma L.", initials: "EL", color: "bg-pink-500" },
]

const chatMessages = [
  { sender: "Alex K.", message: "Can someone explain the chain rule?", time: "2:14 PM", isAI: false },
  { sender: "AI Teacher", message: "The chain rule helps us differentiate composite functions. Let me explain...", time: "2:14 PM", isAI: true },
  { sender: "Sarah M.", message: "Thanks! That makes much more sense.", time: "2:15 PM", isAI: false },
]

export function StudyRoomSection() {
  return (
    <section className="py-16 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            Virtual <span className="text-primary">Study Room</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            A glimpse of our collaborative learning environment
          </p>
        </div>

        <div className="mx-auto mt-12 max-w-5xl">
          <Card className="overflow-hidden border-border bg-card">
            <div className="flex items-center justify-between border-b border-border bg-muted/50 px-4 py-3">
              <div className="flex items-center gap-2">
                <span className="font-medium text-foreground">Calculus Study Group</span>
                <Badge className="bg-red-500 text-white">LIVE</Badge>
              </div>
            </div>

            <div className="grid lg:grid-cols-3">
              <div className="lg:col-span-2 p-4 border-r border-border">
                <div className="grid grid-cols-2 gap-3">
                  {participants.map((participant) => (
                    <div
                      key={participant.name}
                      className="relative aspect-video rounded-lg bg-muted overflow-hidden flex items-center justify-center"
                    >
                      <Avatar className="h-16 w-16">
                        <AvatarFallback className={participant.color + " text-white text-lg"}>
                          {participant.initials}
                        </AvatarFallback>
                      </Avatar>
                      <div className="absolute bottom-2 left-2 rounded bg-background/80 px-2 py-0.5 text-xs font-medium text-foreground">
                        {participant.name}
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-4 flex items-center justify-center gap-3">
                  <Button size="icon" variant="outline" className="h-10 w-10 rounded-full bg-transparent">
                    <Mic className="h-4 w-4" />
                  </Button>
                  <Button size="icon" variant="outline" className="h-10 w-10 rounded-full bg-transparent">
                    <Video className="h-4 w-4" />
                  </Button>
                  <Button size="icon" variant="outline" className="h-10 w-10 rounded-full bg-transparent">
                    <MonitorUp className="h-4 w-4" />
                  </Button>
                  <Button size="icon" variant="destructive" className="h-10 w-10 rounded-full">
                    <PhoneOff className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <div className="flex flex-col">
                <div className="flex items-center justify-between border-b border-border px-4 py-3">
                  <div className="flex items-center gap-2">
                    <Users className="h-4 w-4 text-muted-foreground" />
                    <span className="text-sm font-medium text-foreground">4 participants</span>
                  </div>
                </div>

                <div className="flex-1 p-3 space-y-3 max-h-64 overflow-y-auto">
                  {chatMessages.map((msg, i) => (
                    <div key={i} className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className={`text-xs font-medium ${msg.isAI ? "text-primary" : "text-foreground"}`}>
                          {msg.isAI && <Bot className="h-3 w-3 inline mr-1" />}
                          {msg.sender}
                        </span>
                        <span className="text-xs text-muted-foreground">{msg.time}</span>
                      </div>
                      <p className="text-sm text-muted-foreground">{msg.message}</p>
                    </div>
                  ))}
                </div>

                <div className="border-t border-border p-3">
                  <div className="flex gap-2">
                    <Input placeholder="Type a message..." className="flex-1 h-9 text-sm" />
                    <Button size="icon" className="h-9 w-9">
                      <Send className="h-4 w-4" />
                    </Button>
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
