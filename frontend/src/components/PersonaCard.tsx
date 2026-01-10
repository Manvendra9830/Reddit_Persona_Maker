import { useState } from "react";
import { User, Brain, Heart, Target, AlertTriangle, Quote, Briefcase, MapPin, Sparkles, ChevronDown, ChevronUp, ExternalLink, Activity } from "lucide-react";

interface Citation {
  id?: string;
  post_id?: string;
  post_type?: string;
  content_snippet?: string;
  content?: string;
  url?: string;
  subreddit?: string;
  timestamp?: string;
}

interface ContentSnippet {
  id: string;
  content_snippet: string;
}

// Helper to extract string from field that could be string, array of objects, or null
const extractFieldValue = (field: unknown): string | null => {
  if (!field) return null;
  if (typeof field === 'string') return field;
  if (Array.isArray(field) && field.length > 0) {
    const first = field[0];
    if (typeof first === 'string') return first;
    if (first && typeof first === 'object') {
      return (first as ContentSnippet).content_snippet || null;
    }
  }
  return null;
};

interface PersonaData {
  username: string;
  age: string | ContentSnippet[] | null;
  occupation: string | ContentSnippet[] | null;
  status: string | ContentSnippet[] | null;
  location: string | ContentSnippet[] | null;
  tier: string | ContentSnippet[] | null;
  archetype: string | ContentSnippet[] | null;
  introvert_extrovert: number | null;
  intuition_sensing: number | null;
  feeling_thinking: number | null;
  perceiving_judging: number | null;
  convenience: number | null;
  wellness: number | null;
  speed: number | null;
  preferences: number | null;
  comfort: number | null;
  dietary_needs: number | null;
  behavior_habits: string[];
  frustrations: string[];
  goals_needs: string[];
  key_quote: string | ContentSnippet[] | null;
  citations: Record<string, Citation[]>;
}

interface PersonaCardProps {
  persona: PersonaData;
}

const ScoreBar = ({ label, value, leftLabel, rightLabel }: { label: string; value: number; leftLabel: string; rightLabel: string }) => {
  // Value is 0-10, where 5 is neutral/balanced
  const percentage = (value / 10) * 100;
  const displayValue = Math.round(value);
  
  // Generate label based on value
  const getPositionLabel = () => {
    if (displayValue <= 2) return `Strong ${leftLabel}`;
    if (displayValue <= 4) return `Leaning ${leftLabel}`;
    if (displayValue === 5) return 'Balanced';
    if (displayValue <= 7) return `Leaning ${rightLabel}`;
    return `Strong ${rightLabel}`;
  };
  
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{leftLabel}</span>
        <span className="font-medium text-foreground">{label} ({displayValue}/10)</span>
        <span>{rightLabel}</span>
      </div>
      <div className="h-2 bg-secondary rounded-full overflow-hidden relative">
        {/* Center marker for neutral point */}
        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-muted-foreground/30 z-10" />
        <div 
          className="h-full bg-gradient-to-r from-primary to-accent rounded-full transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div className="text-xs text-center text-muted-foreground">{getPositionLabel()}</div>
    </div>
  );
};

const MotivationBar = ({ label, value }: { label: string; value: number }) => {
  // Value is 0-10, convert to percentage (0-100%)
  const percentage = Math.min((value / 10) * 100, 100); // Cap at 100%
  
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-muted-foreground">{label}</span>
        <span className="text-foreground font-medium">{Math.round(percentage)}%</span>
      </div>
      <div className="h-2 bg-secondary rounded-full overflow-hidden">
        <div 
          className="h-full bg-gradient-to-r from-accent to-primary rounded-full transition-all duration-500"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

const CitationsSection = ({ citations }: { citations: Record<string, Citation[]> }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const allCitations = Object.entries(citations).flatMap(([field, cites]) => 
    cites.map(cite => ({ ...cite, field }))
  );
  
  if (allCitations.length === 0) return null;
  
  return (
    <div className="mt-6 p-4 rounded-lg bg-secondary/30 border border-border/50">
      <button 
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between text-left"
      >
        <div className="flex items-center gap-2 text-muted-foreground">
          <ExternalLink className="w-4 h-4" />
          <span className="text-sm font-medium">Evidence & Citations ({allCitations.length})</span>
        </div>
        {isExpanded ? <ChevronUp className="w-4 h-4 text-muted-foreground" /> : <ChevronDown className="w-4 h-4 text-muted-foreground" />}
      </button>
      
      {isExpanded && (
        <div className="mt-4 space-y-3 max-h-64 overflow-y-auto">
          {allCitations.map((cite, i) => (
            <div key={i} className="p-3 rounded bg-background/50 border border-border/30">
              <p className="text-xs text-primary mb-1 capitalize">{cite.field.replace(/_/g, ' ')}</p>
              <p className="text-sm text-muted-foreground italic">"{cite.content_snippet}"</p>
              <a 
                href={cite.url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-xs text-accent hover:underline mt-1 inline-block"
              >
                View source →
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export const PersonaCard = ({ persona }: PersonaCardProps) => {
  // Extract string values from fields that could be objects or arrays
  const archetype = extractFieldValue(persona.archetype);
  const tier = extractFieldValue(persona.tier);
  const age = extractFieldValue(persona.age);
  const occupation = extractFieldValue(persona.occupation);
  const location = extractFieldValue(persona.location);
  const status = extractFieldValue(persona.status);
  const keyQuote = extractFieldValue(persona.key_quote);

  return (
    <div className="glass-card p-6 sm:p-8 animate-scale-in">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6 pb-6 border-b border-border/50">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center">
          <User className="w-8 h-8 text-primary-foreground" />
        </div>
        <div className="flex-1">
          <h3 className="text-2xl font-display font-bold text-foreground">u/{persona.username}</h3>
          <div className="flex flex-wrap gap-2 mt-1">
            {archetype && (
              <span className="px-2 py-0.5 rounded-full bg-primary/20 text-primary text-xs border border-primary/30">
                {archetype}
              </span>
            )}
            {tier && (
              <span className="px-2 py-0.5 rounded-full bg-accent/20 text-accent text-xs border border-accent/30">
                {tier}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* User Info */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
        {age && (
          <div className="flex items-center gap-2 text-muted-foreground">
            <User className="w-4 h-4" />
            <span className="text-sm">{age}</span>
          </div>
        )}
        {occupation && (
          <div className="flex items-center gap-2 text-muted-foreground">
            <Briefcase className="w-4 h-4" />
            <span className="text-sm">{occupation}</span>
          </div>
        )}
        {location && (
          <div className="flex items-center gap-2 text-muted-foreground">
            <MapPin className="w-4 h-4" />
            <span className="text-sm">{location}</span>
          </div>
        )}
        {status && (
          <div className="flex items-center gap-2 text-muted-foreground">
            <Sparkles className="w-4 h-4" />
            <span className="text-sm">{status}</span>
          </div>
        )}
      </div>

      {/* Personality Scores */}
      <div className="mb-6">
        <div className="flex items-center gap-2 text-primary mb-4">
          <Brain className="w-5 h-5" />
          <h4 className="font-display font-semibold">Personality Profile</h4>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          <ScoreBar label="Social" value={persona.introvert_extrovert ?? 0} leftLabel="Introvert" rightLabel="Extrovert" />
          <ScoreBar label="Perception" value={persona.intuition_sensing ?? 0} leftLabel="Intuition" rightLabel="Sensing" />
          <ScoreBar label="Decision" value={persona.feeling_thinking ?? 0} leftLabel="Feeling" rightLabel="Thinking" />
          <ScoreBar label="Lifestyle" value={persona.perceiving_judging ?? 0} leftLabel="Perceiving" rightLabel="Judging" />
        </div>
      </div>

      {/* Motivation Scores */}
      <div className="mb-6">
        <div className="flex items-center gap-2 text-accent mb-4">
          <Activity className="w-5 h-5" />
          <h4 className="font-display font-semibold">Motivation Drivers</h4>
        </div>
        <div className="grid sm:grid-cols-2 gap-3">
          <MotivationBar label="Convenience" value={persona.convenience ?? 0} />
          <MotivationBar label="Wellness" value={persona.wellness ?? 0} />
          <MotivationBar label="Speed" value={persona.speed ?? 0} />
          <MotivationBar label="Preferences" value={persona.preferences ?? 0} />
          <MotivationBar label="Comfort" value={persona.comfort ?? 0} />
          <MotivationBar label="Dietary Needs" value={persona.dietary_needs ?? 0} />
        </div>
      </div>

      {/* Grid sections */}
      <div className="grid sm:grid-cols-2 gap-6">
        {/* Behavior & Habits */}
        {persona.behavior_habits.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-primary">
              <Heart className="w-5 h-5" />
              <h4 className="font-display font-semibold">Behavior & Habits</h4>
            </div>
            <ul className="space-y-2">
              {persona.behavior_habits.map((habit, i) => (
                <li key={i} className="text-muted-foreground text-sm flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  {habit}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Goals & Needs */}
        {persona.goals_needs.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-green-400">
              <Target className="w-5 h-5" />
              <h4 className="font-display font-semibold">Goals & Needs</h4>
            </div>
            <ul className="space-y-2">
              {persona.goals_needs.map((goal, i) => (
                <li key={i} className="text-muted-foreground text-sm flex items-start gap-2">
                  <span className="text-green-400 mt-1">•</span>
                  {goal}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Frustrations */}
        {persona.frustrations.length > 0 && (
          <div className="space-y-3 sm:col-span-2">
            <div className="flex items-center gap-2 text-orange-400">
              <AlertTriangle className="w-5 h-5" />
              <h4 className="font-display font-semibold">Frustrations</h4>
            </div>
            <ul className="grid sm:grid-cols-2 gap-2">
              {persona.frustrations.map((frustration, i) => (
                <li key={i} className="text-muted-foreground text-sm flex items-start gap-2">
                  <span className="text-orange-400 mt-1">•</span>
                  {frustration}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Key Quote */}
      {keyQuote && (
        <div className="mt-6 p-4 rounded-lg bg-secondary/50 border border-border/50">
          <div className="flex items-start gap-3">
            <Quote className="w-5 h-5 text-primary flex-shrink-0 mt-1" />
            <p className="text-foreground italic">"{keyQuote}"</p>
          </div>
        </div>
      )}

      {/* Citations */}
      {persona.citations && <CitationsSection citations={persona.citations} />}
    </div>
  );
};
