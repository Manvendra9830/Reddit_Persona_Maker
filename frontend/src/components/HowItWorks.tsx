import { User, Download, Brain, FileText, ArrowRight } from "lucide-react";

const steps = [
  {
    icon: User,
    title: "Input Username",
    description: "Enter any public Reddit username",
    color: "from-primary to-orange-400",
  },
  {
    icon: Download,
    title: "Fetch Activity",
    description: "PRAW scrapes posts & comments",
    color: "from-orange-400 to-accent",
  },
  {
    icon: Brain,
    title: "AI Analysis",
    description: "LLM processes the content",
    color: "from-accent to-green-400",
  },
  {
    icon: FileText,
    title: "Generate Persona",
    description: "Detailed profile output",
    color: "from-green-400 to-primary",
  },
];

export const HowItWorks = () => {
  return (
    <section className="py-20 sm:py-32 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/2 left-0 right-0 h-px bg-gradient-to-r from-transparent via-border to-transparent" />
      </div>

      <div className="container px-4 relative">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-display font-bold mb-4">
            How It <span className="gradient-text">Works</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            From username to persona in four simple steps
          </p>
        </div>

        {/* Steps - Desktop */}
        <div className="hidden lg:flex items-center justify-center gap-4 max-w-5xl mx-auto">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={index} className="flex items-center">
                <div className="glass-card p-6 text-center flex-shrink-0 w-52 group hover:border-primary/30 transition-all duration-300">
                  <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${step.color} flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-7 h-7 text-primary-foreground" />
                  </div>
                  <div className="text-sm font-medium text-muted-foreground mb-1">Step {index + 1}</div>
                  <h3 className="font-display font-semibold text-foreground mb-2">{step.title}</h3>
                  <p className="text-muted-foreground text-sm">{step.description}</p>
                </div>
                {index < steps.length - 1 && (
                  <ArrowRight className="w-6 h-6 text-muted-foreground mx-2 flex-shrink-0" />
                )}
              </div>
            );
          })}
        </div>

        {/* Steps - Mobile */}
        <div className="lg:hidden space-y-6 max-w-sm mx-auto">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return (
              <div key={index} className="glass-card p-6 relative">
                <div className="flex items-start gap-4">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${step.color} flex items-center justify-center flex-shrink-0`}>
                    <Icon className="w-6 h-6 text-primary-foreground" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-muted-foreground mb-1">Step {index + 1}</div>
                    <h3 className="font-display font-semibold text-foreground mb-1">{step.title}</h3>
                    <p className="text-muted-foreground text-sm">{step.description}</p>
                  </div>
                </div>
                {index < steps.length - 1 && (
                  <div className="absolute -bottom-3 left-10 w-0.5 h-6 bg-border" />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
