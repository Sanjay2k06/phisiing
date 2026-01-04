import { motion } from "framer-motion";
import { RotateCcw } from "lucide-react";

const RefreshButton = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      viewport={{ once: true }}
      className="flex justify-center my-12"
    >
      <button
        onClick={() => window.location.reload()}
        className="flex items-center gap-2 px-7 py-3 border border-border rounded-lg
        font-heading font-semibold text-foreground
        hover:bg-accent/10 hover:scale-105 hover:shadow-md
        transition-all duration-300"
      >
        <RotateCcw className="w-4 h-4" />
        Start New Analysis
      </button>
    </motion.div>
  );
};

export default RefreshButton;
