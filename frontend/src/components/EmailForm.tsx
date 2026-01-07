import { useState } from 'react';
import { motion } from 'framer-motion';
import { Send, Loader2 } from 'lucide-react';

interface EmailFormProps {
  onSubmit: (data: { email_text: string; subject?: string; sender?: string }) => void;
  isLoading: boolean;
}

export const EmailForm = ({ onSubmit, isLoading }: EmailFormProps) => {
  const [emailText, setEmailText] = useState('');
  const [subject, setSubject] = useState('');
  const [sender, setSender] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!emailText.trim()) return;
    
    onSubmit({
      email_text: emailText,
      subject: subject || undefined,
      sender: sender || undefined,
    });
  };

  const charCount = emailText.length;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card p-8"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-1 h-8 bg-gradient-to-b from-neon-cyan to-neon-purple rounded-full"></div>
        <h2 className="text-2xl font-bold text-white">Analyze Email</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Email Content */}
        <div>
          <label htmlFor="emailText" className="block text-sm font-medium text-gray-300 mb-2">
            Email Content *
          </label>
          <textarea
            id="emailText"
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
            placeholder="Paste the suspicious email content here..."
            className="input-field min-h-[200px] resize-y font-mono text-sm"
            required
            disabled={isLoading}
          />
          <div className="mt-2 flex justify-between items-center">
            <span className="text-xs text-gray-500">
              Minimum 10 characters required
            </span>
            <span className={`text-xs font-mono ${charCount > 0 ? 'text-neon-cyan' : 'text-gray-500'}`}>
              {charCount} characters
            </span>
          </div>
        </div>

        {/* Subject (Optional) */}
        <div>
          <label htmlFor="subject" className="block text-sm font-medium text-gray-300 mb-2">
            Subject <span className="text-gray-500 text-xs">(optional)</span>
          </label>
          <input
            id="subject"
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder="e.g., Urgent: Verify Your Account"
            className="input-field"
            disabled={isLoading}
          />
        </div>

        {/* Sender (Optional) */}
        <div>
          <label htmlFor="sender" className="block text-sm font-medium text-gray-300 mb-2">
            Sender <span className="text-gray-500 text-xs">(optional)</span>
          </label>
          <input
            id="sender"
            type="text"
            value={sender}
            onChange={(e) => setSender(e.target.value)}
            placeholder="e.g., security@suspicious-domain.com"
            className="input-field"
            disabled={isLoading}
          />
        </div>

        {/* Submit Button */}
        <motion.button
          type="submit"
          disabled={isLoading || !emailText.trim()}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="btn-primary w-full flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Analyze Email</span>
            </>
          )}
        </motion.button>
      </form>
    </motion.div>
  );
};
