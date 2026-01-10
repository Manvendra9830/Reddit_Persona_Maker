import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { PersonaCard } from "@/components/PersonaCard";
import { EmptyState } from "@/components/EmptyState";
import { LoadingState } from "@/components/LoadingState";
import { Search, User, AlertCircle, RotateCcw } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;  

interface ApiResponse {
  username: string;
  has_activity: boolean;
  message?: string;
  persona?: {
    age: string | null;
    occupation: string | null;
    status: string | null;
    location: string | null;
    tier: string | null;
    archetype: string | null;
    introvert_extrovert: number;
    intuition_sensing: number;
    feeling_thinking: number;
    perceiving_judging: number;
    convenience: number;
    wellness: number;
    speed: number;
    preferences: number;
    comfort: number;
    dietary_needs: number;
    behavior_habits: string[];
    frustrations: string[];
    goals_needs: string[];
    key_quote: string;
    citations: Record<string, { id: string; content_snippet: string; url: string }[]>;
  };
}

export const DemoSection = () => {
  const [username, setUsername] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const cleanUsername = username.trim().replace(/^u\//, "");
    
    if (!cleanUsername) {
      toast({
        title: "Username required",
        description: "Please enter a Reddit username to analyze.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setResult(null);
    setError(null);

    try {
      const requestBody = { username: cleanUsername };
      console.log("🔵 Sending request to:", `${API_BASE_URL}/analyze`);
      console.log("🔵 Request body:", JSON.stringify(requestBody));

      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });

      console.log("🟢 Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("🔴 Error response:", errorText);
        throw new Error(`Server error: ${response.status}`);
      }

      const data: ApiResponse = await response.json();
      console.log("🟢 Response data:", JSON.stringify(data, null, 2));
      setResult(data);
    } catch (err) {
      console.error("API Error:", err);
      setError("Something went wrong while analyzing this user. Please try again.");
      toast({
        title: "Analysis failed",
        description: "Could not analyze the user. The server might be busy. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setError(null);
    setResult(null);
  };

  return (
    <section id="demo" className="py-20 sm:py-32 relative">
      <div className="container px-4">
        <div className="max-w-3xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-display font-bold mb-4">
              Try the <span className="gradient-text">Live Demo</span>
            </h2>
            <p className="text-muted-foreground text-lg">
              Enter any Reddit username to generate an AI-powered persona
            </p>
          </div>

          {/* Input form */}
          <form onSubmit={handleSubmit} className="mb-10">
            <div className="glass-card p-4 sm:p-6">
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex-1 relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                  <Input
                    type="text"
                    placeholder="Enter Reddit username (e.g., spez)"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="pl-12 h-14"
                    disabled={isLoading}
                  />
                </div>
                <Button 
                  type="submit" 
                  variant="hero" 
                  size="xl"
                  disabled={isLoading}
                  className="sm:w-auto w-full"
                >
                  <Search className="w-5 h-5 mr-2" />
                  Analyze
                </Button>
              </div>
              <p className="text-muted-foreground text-sm mt-4 text-center">
                Analysis may take 5-15 seconds depending on user activity
              </p>
            </div>
          </form>

          {/* Results */}
          {isLoading && <LoadingState />}
          
          {/* Error State */}
          {!isLoading && error && (
            <div className="glass-card p-6 sm:p-8 text-center animate-scale-in">
              <div className="w-16 h-16 rounded-full bg-destructive/20 flex items-center justify-center mx-auto mb-4">
                <AlertCircle className="w-8 h-8 text-destructive" />
              </div>
              <h3 className="text-xl font-display font-bold text-foreground mb-2">
                Analysis Failed
              </h3>
              <p className="text-muted-foreground mb-6">
                {error}
              </p>
              <Button onClick={handleRetry} variant="glass">
                <RotateCcw className="w-4 h-4 mr-2" />
                Try Again
              </Button>
            </div>
          )}
          
          {/* Success with activity */}
          {!isLoading && !error && result && result.has_activity && result.persona && (
            <PersonaCard persona={{ username: result.username, ...result.persona }} />
          )}
          
          {/* No activity */}
          {!isLoading && !error && result && !result.has_activity && (
            <EmptyState username={result.username} message={result.message} />
          )}
        </div>
      </div>
    </section>
  );
};
