import { motion } from 'framer-motion';
import { AlertTriangle, CheckCircle, XCircle, Shield, Clock } from 'lucide-react';
import { GaugeChart } from './GaugeChart';
import type { ClassifyResponse } from '../types';

interface ResultsPanelProps {
  result: ClassifyResponse;
}

const getRiskColor = (level: string) => {
  switch (level) {
    case 'LOW': return 'text-threat-low';
    case 'MEDIUM': return 'text-threat-medium';
    case 'HIGH': return 'text-threat-high';
    case 'CRITICAL': return 'text-threat-high';
    default: return 'text-gray-400';
  }
};

const getRiskIcon = (level: string) => {
  switch (level) {
    case 'LOW': return <CheckCircle className="w-8 h-8" />;
    case 'MEDIUM': return <AlertTriangle className="w-8 h-8" />;
    case 'HIGH': return <XCircle className="w-8 h-8" />;
    case 'CRITICAL': return <Shield className="w-8 h-8" />;
    default: return null;
  }
};

const getGaugeColor = (probability: number) => {
  if (probability <= 50) return '#10b981'; // green
  if (probability <= 70) return '#f59e0b'; // orange
  return '#ef4444'; // red
};

export const ResultsPanel = ({ result }: ResultsPanelProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Threat Banner */}
      <div className={`glass-card p-8 ${result.is_malicious ? 'neon-border' : ''}`}>
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-4">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200 }}
              className={getRiskColor(result.risk_level)}
            >
              {getRiskIcon(result.risk_level)}
            </motion.div>
            
            <div>
              <h3 className="text-sm text-gray-400 uppercase tracking-wide mb-1">
                Threat Level
              </h3>
              <div className="flex items-baseline gap-3">
                <span className={`text-4xl font-bold ${getRiskColor(result.risk_level)}`}>
                  {result.risk_level}
                </span>
                <span className="text-2xl text-gray-400">•</span>
                <span className="text-2xl font-semibold text-white">
                  {result.verdict}
                </span>
              </div>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-sm text-gray-400 uppercase tracking-wide mb-1">
              Confidence
            </div>
            <div className="text-3xl font-bold text-neon-cyan">
              {(Math.max(result.spam_probability, result.phishing_probability) * 100).toFixed(1)}%
            </div>
          </div>
        </div>
        
        {/* Risk Meter */}
        <div className="mt-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-gray-400">Risk Score</span>
            <span className="font-mono text-neon-cyan">
              {result.threat_report?.risk_score || Math.round(Math.max(result.spam_probability, result.phishing_probability) * 100)}/100
            </span>
          </div>
          <div className="h-3 bg-gray-800 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${result.threat_report?.risk_score || Math.max(result.spam_probability, result.phishing_probability) * 100}%` }}
              transition={{ duration: 1, ease: 'easeOut' }}
              className={`h-full rounded-full ${
                result.risk_level === 'CRITICAL' ? 'bg-threat-high' :
                result.risk_level === 'HIGH' ? 'bg-threat-high' :
                result.risk_level === 'MEDIUM' ? 'bg-threat-medium' :
                'bg-threat-low'
              }`}
            />
          </div>
        </div>
      </div>

      {/* Detection Matrix */}
      <div className="glass-card p-8">
        <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
          <div className="w-1 h-6 bg-gradient-to-b from-neon-cyan to-neon-purple rounded"></div>
          Detection Matrix
        </h3>
        
        <div className="grid md:grid-cols-2 gap-8">
          {/* SPAM Detection */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-between">
              <h4 className="text-lg font-semibold">🗑️ SPAM Detection</h4>
              <span className={`threat-badge ${
                result.spam_label === 'SPAM' 
                  ? 'bg-threat-high/20 text-threat-high' 
                  : 'bg-threat-low/20 text-threat-low'
              }`}>
                {result.spam_label}
              </span>
            </div>
            
            <div className="w-64 mx-auto">
              <GaugeChart
                value={result.spam_probability * 100}
                label="SPAM Probability"
                color={getGaugeColor(result.spam_probability * 100)}
              />
            </div>
            
            <div className="text-center text-xs text-gray-500 font-mono">
              Model: {result.spam_model_version}
            </div>
          </motion.div>

          {/* PHISHING Detection */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-between">
              <h4 className="text-lg font-semibold">🎣 PHISHING Detection</h4>
              <span className={`threat-badge ${
                result.phishing_label === 'PHISHING' 
                  ? 'bg-threat-high/20 text-threat-high' 
                  : 'bg-threat-low/20 text-threat-low'
              }`}>
                {result.phishing_label}
              </span>
            </div>
            
            <div className="w-64 mx-auto">
              <GaugeChart
                value={result.phishing_probability * 100}
                label="PHISHING Probability"
                color={getGaugeColor(result.phishing_probability * 100)}
              />
            </div>
            
            <div className="text-center text-xs text-gray-500 font-mono">
              Model: {result.phishing_model_version}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Execution Stats */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="glass-card p-6"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-gray-400">
            <Clock className="w-4 h-4" />
            <span className="text-sm">Analysis completed in</span>
          </div>
          <span className="font-mono text-neon-cyan font-semibold">
            {result.execution_time_ms.toFixed(2)}ms
          </span>
        </div>
      </motion.div>
    </motion.div>
  );
};
