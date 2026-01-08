import axios from 'axios';
import type { ClassifyRequest, ClassifyResponse, ModelInfo } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Log API URL on startup
console.log('🔗 API Base URL:', API_BASE_URL);
console.log('📦 Environment:', import.meta.env.MODE);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ Response Error:', {
      status: error.response?.status,
      message: error.message,
      url: error.config?.url,
      baseURL: error.config?.baseURL,
      data: error.response?.data,
    });
    
    // Create user-friendly error message
    let userMessage = 'Network Error';
    if (error.response) {
      // Server responded with error
      userMessage = `Server Error (${error.response.status}): ${error.response.data?.detail || error.response.statusText}`;
    } else if (error.request) {
      // Request made but no response
      userMessage = `Cannot reach API at ${API_BASE_URL}. Please check your connection.`;
    } else {
      // Error in request setup
      userMessage = error.message;
    }
    
    error.message = userMessage;
    return Promise.reject(error);
  }
);

/**
 * Classify an email for SPAM and PHISHING threats
 */
export const classifyEmail = async (data: ClassifyRequest): Promise<ClassifyResponse> => {
  const response = await api.post<ClassifyResponse>('/api/v1/classify', data);
  return response.data;
};

/**
 * Get model information
 */
export const getModelInfo = async (modelName: string): Promise<ModelInfo> => {
  const response = await api.get<ModelInfo>(`/api/v1/models/${modelName}/latest`);
  return response.data;
};

/**
 * Health check
 */
export const healthCheck = async (): Promise<{ status: string }> => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
