import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from './components/Header';
import { EmailForm } from './components/EmailForm';
import { ResultsPanel } from './components/ResultsPanel';
import { useClassifyEmail } from './hooks/useClassifyEmail';
import type { ClassifyResponse } from './types';
import { RotateCcw } from 'lucide-react';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function AppContent() {
  const [result, setResult] = useState<ClassifyResponse | null>(null);
  const { mutate: classify, isPending, error } = useClassifyEmail();

  const handleSubmit = (data: { email_text: string; subject?: string; sender?: string }) => {
    classify(data, {
      onSuccess: (response) => {
        setResult(response);
      },
    });
  };

  const handleReset = () => {
    setResult(null);
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <Header />

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Form */}
          <div>
            <EmailForm onSubmit={handleSubmit} isLoading={isPending} />
            
            {/* Error Display */}
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="mt-4 glass-card p-4 border-2 border-threat-high/50"
                >
                  <div className="flex items-start gap-3">
                    <div className="text-threat-high text-2xl">⚠️</div>
                    <div>
                      <h4 className="font-semibold text-threat-high mb-1">Analysis Failed</h4>
                      <p className="text-sm text-gray-400">
                        {error.message || 'Unable to analyze email. Please check your connection and try again.'}
                      </p>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* How It Works */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="mt-8 glass-card p-6"
            >
              <h3 className="text-lg font-bold mb-4 text-neon-cyan">🧠 How It Works</h3>
              <div className="space-y-3 text-sm text-gray-400">
                <div className="flex gap-3">
                  <span className="text-neon-cyan font-bold">1.</span>
                  <p>Email content is preprocessed and tokenized</p>
                </div>
                <div className="flex gap-3">
                  <span className="text-neon-cyan font-bold">2.</span>
                  <p>TF-IDF vectorization converts text to numerical features</p>
                </div>
                <div className="flex gap-3">
                  <span className="text-neon-cyan font-bold">3.</span>
                  <p>Dual ML models analyze for SPAM and PHISHING</p>
                </div>
                <div className="flex gap-3">
                  <span className="text-neon-cyan font-bold">4.</span>
                  <p>Risk assessment combines both predictions</p>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-700">
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <div className="text-gray-500 mb-1">SPAM Detector</div>
                    <div className="text-neon-cyan font-semibold">~95% Accuracy</div>
                  </div>
                  <div>
                    <div className="text-gray-500 mb-1">PHISHING Detector</div>
                    <div className="text-neon-cyan font-semibold">~92% Accuracy</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Right Column - Results */}
          <div className="relative">
            <AnimatePresence mode="wait">
              {result ? (
                <div key="results">
                  <ResultsPanel result={result} />
                  
                  {/* Reset Button */}
                  <motion.button
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    onClick={handleReset}
                    className="mt-6 btn-secondary w-full flex items-center justify-center gap-2"
                  >
                    <RotateCcw className="w-5 h-5" />
                    <span>Analyze Another Email</span>
                  </motion.button>
                </div>
              ) : (
                <motion.div
                  key="placeholder"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="glass-card p-12 flex flex-col items-center justify-center min-h-[600px] text-center"
                >
                  <motion.div
                    animate={{
                      scale: [1, 1.1, 1],
                      rotate: [0, 5, -5, 0],
                    }}
                    transition={{
                      duration: 3,
                      repeat: Infinity,
                      repeatType: 'reverse',
                    }}
                    className="text-8xl mb-6"
                  >
                    🛡️
                  </motion.div>
                  <h3 className="text-2xl font-bold mb-3 text-gray-300">
                    Ready to Analyze
                  </h3>
                  <p className="text-gray-500 max-w-md">
                    Paste an email in the form on the left to start the AI-powered threat detection analysis.
                  </p>
                  
                  <div className="mt-8 flex gap-4">
                    <div className="text-center">
                      <div className="text-3xl mb-2">⚡</div>
                      <div className="text-xs text-gray-500">Fast</div>
                      <div className="text-neon-cyan font-semibold">&lt;2ms</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl mb-2">🎯</div>
                      <div className="text-xs text-gray-500">Accurate</div>
                      <div className="text-neon-cyan font-semibold">~93%</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl mb-2">🔒</div>
                      <div className="text-xs text-gray-500">Secure</div>
                      <div className="text-neon-cyan font-semibold">100%</div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-12 text-center text-gray-500 text-sm"
        >
          <p>
            Powered by Machine Learning • FastAPI + React • 
            <a href="https://github.com/infantesromeroadrian/ML-Spam-Phising-Detector" 
               target="_blank" 
               rel="noopener noreferrer"
               className="text-neon-cyan hover:underline ml-1">
              View on GitHub
            </a>
          </p>
        </motion.footer>
      </div>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;
