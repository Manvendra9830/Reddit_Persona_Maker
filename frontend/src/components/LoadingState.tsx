import { Brain, Search, FileText, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

const steps = [
  { icon: Search, text: "Fetching Reddit activity...", color: "text-primary" },
  { icon: FileText, text: "Analyzing posts and comments...", color: "text-accent" },
  { icon: Brain, text: "Generating personality insights...", color: "text-green-400" },
  { icon: Sparkles, text: "Building your persona...", color: "text-primary" },
];

export const LoadingState = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev + 1) % steps.length);
    }, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass-card p-8 text-center animate-scale-in">
      {/* Animated brain icon */}
      <div className="relative w-24 h-24 mx-auto mb-8">
        <div className="absolute inset-0 rounded-full bg-primary/20 animate-ping" />
        <div className="absolute inset-2 rounded-full bg-primary/30 animate-pulse" />
        <div className="absolute inset-0 flex items-center justify-center">
          <Brain className="w-12 h-12 text-primary animate-pulse" />
        </div>
      </div>

      {/* Loading steps */}
      <div className="space-y-4 max-w-sm mx-auto">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index === currentStep;
          const isPast = index < currentStep;
          
          return (
            <div
              key={index}
              className={`flex items-center gap-3 transition-all duration-300 ${
                isActive ? 'opacity-100 scale-105' : isPast ? 'opacity-50' : 'opacity-30'
              }`}
            >
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                isActive ? 'bg-primary/20' : 'bg-secondary/50'
              }`}>
                <Icon className={`w-4 h-4 ${isActive ? step.color : 'text-muted-foreground'}`} />
              </div>
              <span className={`text-sm ${isActive ? 'text-foreground font-medium' : 'text-muted-foreground'}`}>
                {step.text}
              </span>
              {isActive && (
                <div className="flex gap-1 ml-auto">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              )}
            </div>
          );
        })}
      </div>

      <p className="text-muted-foreground text-sm mt-8">
        AI is analyzing the user's digital footprint...
      </p>
    </div>
  );
};
