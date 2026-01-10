import { Heart } from "lucide-react";

export const Footer = () => {
  return (
    <footer className="py-12 border-t border-border/50 relative">
      <div className="container px-4">
        <div className="flex flex-col items-center gap-6">
          {/* Branding */}
        </div>

        {/* Bottom */}
        <div className="mt-8 pt-8 border-t border-border/30 text-center">
          <p className="text-muted-foreground text-sm">
            © {new Date().getFullYear()} Reddit Persona Generator. Open source project for portfolio demonstration.
          </p>
        </div>
      </div>
    </footer>
  );
};
