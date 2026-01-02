import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import axios from "axios";
import { Shield, AlertTriangle, CheckCircle, XCircle } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const StatsDisplay = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error("Failed to fetch stats:", error);
    }
  };

  if (!stats) return null;

  const statCards = [
    {
      icon: Shield,
      label: "Total Analyses",
      value: stats.total_analyses,
      color: "text-accent",
      bg: "bg-accent/20",
    },
    {
      icon: CheckCircle,
      label: "Safe Messages",
      value: stats.verdicts.safe,
      color: "text-safe",
      bg: "bg-safe/20",
    },
    {
      icon: AlertTriangle,
      label: "Suspicious",
      value: stats.verdicts.suspicious,
      color: "text-suspicious",
      bg: "bg-suspicious/20",
    },
    {
      icon: XCircle,
      label: "Threats Blocked",
      value: stats.verdicts.phishing + stats.verdicts.scam,
      color: "text-destructive",
      bg: "bg-destructive/20",
    },
  ];

  return (
    <div className="py-20 px-4">
      <div className="container mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="font-heading font-bold text-3xl sm:text-4xl text-foreground mb-12 text-center" data-testid="stats-heading">
            Detection Statistics
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {statCards.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="bg-card border border-border rounded-lg p-6 text-center hover:border-accent/50 transition-all duration-300"
                  data-testid={`stat-card-${index}`}
                >
                  <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg ${stat.bg} border border-${stat.color.replace('text-', '')}/30 mb-3`}>
                    <Icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                  <div className={`text-3xl font-mono font-bold ${stat.color} mb-2`}>
                    {stat.value.toLocaleString()}
                  </div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default StatsDisplay;