import { Users, Lightbulb, TrendingUp, PenTool } from "lucide-react";

const useCases = [
  {
    icon: Users,
    title: "Marketing Personas",
    description: "Understand your target audience by analyzing how real users discuss products and brands.",
    gradient: "from-primary/20 to-primary/5",
  },
  {
    icon: Lightbulb,
    title: "UX Research",
    description: "Discover user pain points, motivations, and behaviors from authentic community discussions.",
    gradient: "from-accent/20 to-accent/5",
  },
  {
    icon: TrendingUp,
    title: "Social Analysis",
    description: "Track sentiment and identify influencers within specific communities or topics.",
    gradient: "from-green-400/20 to-green-400/5",
  },
  {
    icon: PenTool,
    title: "Content Strategy",
    description: "Learn what resonates with audiences and tailor your content to match their interests.",
    gradient: "from-purple-400/20 to-purple-400/5",
  },
];

export const UseCases = () => {
  return (
    <section className="py-20 sm:py-32 relative">
      <div className="container px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-display font-bold mb-4">
            Real-World <span className="gradient-text">Use Cases</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            From marketing to research, AI-generated personas unlock powerful insights
          </p>
        </div>

        <div className="grid sm:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {useCases.map((useCase, index) => {
            const Icon = useCase.icon;
            return (
              <div
                key={index}
                className={`glass-card-hover p-6 bg-gradient-to-br ${useCase.gradient}`}
              >
                <Icon className="w-10 h-10 text-foreground mb-4" />
                <h3 className="text-xl font-display font-semibold text-foreground mb-2">
                  {useCase.title}
                </h3>
                <p className="text-muted-foreground leading-relaxed">
                  {useCase.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
