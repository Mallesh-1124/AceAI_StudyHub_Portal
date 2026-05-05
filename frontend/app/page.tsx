import { HeroSection } from "@/components/hero-section"
import { FeaturesSection } from "@/components/features-section"
import { HowItWorksSection } from "@/components/how-it-works-section"
import { AIDemoSection } from "@/components/ai-demo-section"
import { StudyRoomSection } from "@/components/study-room-section"
import { AdminDashboardSection } from "@/components/admin-dashboard-section"
import { TechStackSection } from "@/components/tech-stack-section"
import { CTASection } from "@/components/cta-section"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <HeroSection />
      <FeaturesSection />
      <HowItWorksSection />
      <AIDemoSection />
      <StudyRoomSection />
      <AdminDashboardSection />
      <TechStackSection />
      <CTASection />
      <Footer />
    </main>
  )
}
