import { User, AlertCircle } from "lucide-react";

interface EmptyStateProps {
  username: string;
  message?: string;
}

export const EmptyState = ({ username, message }: EmptyStateProps) => {
  return (
    <div className="glass-card p-8 text-center animate-scale-in">
      <div className="w-20 h-20 rounded-full bg-secondary/50 border border-border/50 flex items-center justify-center mx-auto mb-6">
        <User className="w-10 h-10 text-muted-foreground" />
      </div>
      
      <h3 className="text-2xl font-display font-bold text-foreground mb-2">
        u/{username}
      </h3>
      
      <div className="flex items-center justify-center gap-2 text-muted-foreground mb-4">
        <AlertCircle className="w-5 h-5" />
        <span>No public activity found</span>
      </div>
      
      <p className="text-muted-foreground max-w-md mx-auto">
        {message || "This user has no public posts or comments available for analysis. They may have a new account or have deleted their activity."}
      </p>
    </div>
  );
};
