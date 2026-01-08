import { useEffect, useState } from 'react';
import { healthCheck } from '../services/api';

interface ApiStatusProps {
  className?: string;
}

export const ApiStatus = ({ className = '' }: ApiStatusProps) => {
  const [status, setStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [apiUrl, setApiUrl] = useState<string>('');

  useEffect(() => {
    const checkApi = async () => {
      const url = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      setApiUrl(url);
      
      try {
        await healthCheck();
        setStatus('online');
      } catch (error) {
        console.error('API health check failed:', error);
        setStatus('offline');
      }
    };

    checkApi();
    // Check every 30 seconds
    const interval = setInterval(checkApi, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`flex items-center gap-2 text-sm ${className}`}>
      <div className="flex items-center gap-2">
        <span className="text-gray-400">API:</span>
        <div className="flex items-center gap-1">
          <div
            className={`w-2 h-2 rounded-full ${
              status === 'checking'
                ? 'bg-yellow-500 animate-pulse'
                : status === 'online'
                ? 'bg-green-500'
                : 'bg-red-500'
            }`}
          />
          <span
            className={
              status === 'checking'
                ? 'text-yellow-500'
                : status === 'online'
                ? 'text-green-500'
                : 'text-red-500'
            }
          >
            {status === 'checking' ? 'Checking...' : status === 'online' ? 'Online' : 'Offline'}
          </span>
        </div>
      </div>
      <span className="text-gray-600 text-xs truncate max-w-[200px]" title={apiUrl}>
        {apiUrl}
      </span>
    </div>
  );
};
