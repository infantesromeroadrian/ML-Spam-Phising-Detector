import { motion } from 'framer-motion';
import { Shield } from 'lucide-react';

export const Header = () => {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card px-8 py-6 mb-8"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <motion.div
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
            className="p-3 bg-gradient-to-br from-neon-cyan to-neon-purple rounded-xl"
          >
            <Shield className="w-8 h-8 text-white" />
          </motion.div>
          
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-neon-cyan to-neon-purple bg-clip-text text-transparent">
              Email Threat Analyzer
            </h1>
            <p className="text-gray-400 text-sm">
              AI-Powered SPAM & PHISHING Detection System
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-xs text-gray-500 uppercase tracking-wide">Status</div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-threat-low rounded-full animate-pulse"></div>
              <span className="text-threat-low font-semibold">Online</span>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-xs text-gray-500 uppercase tracking-wide">Version</div>
            <div className="text-neon-cyan font-semibold">v1.0.0</div>
          </div>
        </div>
      </div>
    </motion.header>
  );
};
