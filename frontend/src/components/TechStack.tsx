const technologies = [
  { name: "Python", color: "bg-blue-500/20 text-blue-400 border-blue-500/30" },
  { name: "PRAW", color: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
  { name: "Ollama", color: "bg-green-500/20 text-green-400 border-green-500/30" },
  { name: "Llama 3.2", color: "bg-purple-500/20 text-purple-400 border-purple-500/30" },
  { name: "Mistral", color: "bg-red-500/20 text-red-400 border-red-500/30" },
  { name: "NLP", color: "bg-cyan-500/20 text-cyan-400 border-cyan-500/30" },
  { name: "CLI", color: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30" },
  { name: "AI Pipeline", color: "bg-pink-500/20 text-pink-400 border-pink-500/30" },
];

export const TechStack = () => {
  return (
    <section className="py-20 sm:py-32 relative">
      <div className="container px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-display font-bold mb-4">
            Built With <span className="gradient-text-accent">Modern Tech</span>
          </h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            A carefully selected stack for reliability, performance, and privacy
          </p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 max-w-3xl mx-auto">
          {technologies.map((tech, index) => (
            <span
              key={index}
              className={`px-4 py-2 rounded-full border text-sm font-medium transition-all duration-300 hover:scale-105 cursor-default ${tech.color}`}
            >
              {tech.name}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
};
