// API Types
export interface ClassifyRequest {
  email_text: string;
  subject?: string;
  sender?: string;
}

export interface ClassifyResponse {
  verdict: 'HAM' | 'SPAM' | 'PHISHING' | 'SPAM+PHISHING';
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  is_malicious: boolean;
  
  spam_label: string;
  spam_probability: number;
  spam_model_version: string;
  
  phishing_label: string;
  phishing_probability: number;
  phishing_model_version: string;
  
  execution_time_ms: number;
  
  threat_report?: {
    risk_score: number;
    iocs: Array<{
      type: string;
      severity: string;
      value: string;
      description: string;
      count: number;
    }>;
    threat_vectors: Array<{
      name: string;
      description: string;
      confidence: number;
    }>;
    recommendations: string[];
    spam_trigger_words: Array<{
      word: string;
      contribution: number;
      category: string;
    }>;
    phishing_trigger_words: Array<{
      word: string;
      contribution: number;
      category: string;
    }>;
  };
}

export interface ModelInfo {
  name: string;
  version: string;
  accuracy: number;
  trained_at: string;
}

// UI Types
export interface ThreatMetrics {
  spam: number;
  phishing: number;
}

export interface AnalysisHistory {
  id: string;
  timestamp: string;
  verdict: string;
  risk_level: string;
  confidence: number;
  email_preview: string;
}

// Chart Types
export interface GaugeData {
  value: number;
  label: string;
  color: string;
}
