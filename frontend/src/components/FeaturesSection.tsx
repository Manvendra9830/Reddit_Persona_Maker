import { Database, Brain, FileCheck, Server, FileText } from "lucide-react";

const features = [
  {
    icon: Database,
    title: "Reddit Data Scraping",
    description: "Fetches public posts and comments using the official Reddit API (PRAW) for comprehensive analysis.",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    icon: Brain,
    title: "AI-Powered Analysis",
    description: "Leverages advanced LLMs like Llama 3.2 and Mistral to understand behavioral patterns and personality.",
    color: "text-accent",
    bgColor: "bg-accent/10",
  },
  {
    icon: FileCheck,
    title: "Evidence-Based Insights",
    description: "Every insight is backed by actual user activity, ensuring accuracy and relevance.",
    color: "text-green-400",
    bgColor: "bg-green-400/10",
  },
  {
    icon: Server,
    title: "Local LLM Support",
    description: "Run entirely on your machine with Ollama—no data leaves your system.",
    color: "text-orange-400",
    bgColor: "bg-orange-400/10",
  },
  {
    icon: FileText,
    title: "Clean Reports",
    description: "Generates human-readable persona documents with structured insights and key quotes.",
    color: "text-purple-400",
    bgColor: "bg-purple-400/10",
  },
];

export const FeaturesSection = () => {
  return (
    <section id="features" className="py-20 sm:py-32 relative">
      <div className="container px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-display font-bold mb-4">
            Powerful <span className="gradient-text">Features</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Built with privacy and accuracy in mind, combining modern AI with responsible data handling.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <div
                key={index}
                className="glass-card-hover p-6 group"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className={`w-12 h-12 rounded-xl ${feature.bgColor} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                <h3 className="text-lg font-display font-semibold text-foreground mb-2">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
