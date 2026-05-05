import { Button } from "@/components/ui/button"
import { GraduationCap, Users } from "lucide-react"
import Link from "next/link"

export function CTASection() {
  return (
    <section className="bg-primary py-16 lg:py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-primary-foreground sm:text-4xl">
            Start Learning Smarter Today
          </h2>
          <p className="mt-4 text-lg text-primary-foreground/90">
            Join thousands of students already using AI-powered collaborative learning. Free to get started.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link href="/login">
              <Button size="lg" variant="secondary" className="gap-2">
                <GraduationCap className="h-5 w-5" />
                I&apos;m a Student
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="gap-2 border-primary-foreground/30 text-primary-foreground hover:bg-primary-foreground/10 hover:text-primary-foreground bg-transparent">
                <Users className="h-5 w-5" />
                I&apos;m an Educator
              </Button>
            </Link>
          </div>
          <p className="mt-6 text-sm text-primary-foreground/70">
            No credit card required · Free tier available · Cancel anytime
          </p>
        </div>
      </div>
    </section>
  )
}
