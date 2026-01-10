import { Navigation } from "@/components/Navigation";
import { Hero } from "@/components/Hero";
import { DemoSection } from "@/components/DemoSection";
import { FeaturesSection } from "@/components/FeaturesSection";
import { HowItWorks } from "@/components/HowItWorks";
import { TechStack } from "@/components/TechStack";
import { UseCases } from "@/components/UseCases";
import { Footer } from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <main>
        <Hero />
        <DemoSection />
        <FeaturesSection />
        <HowItWorks />
        <TechStack />
        <UseCases />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
