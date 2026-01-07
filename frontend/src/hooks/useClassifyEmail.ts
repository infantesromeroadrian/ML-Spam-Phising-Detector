import { useMutation } from '@tanstack/react-query';
import { classifyEmail } from '../services/api';
import type { ClassifyRequest, ClassifyResponse } from '../types';

export const useClassifyEmail = () => {
  return useMutation<ClassifyResponse, Error, ClassifyRequest>({
    mutationFn: classifyEmail,
    onSuccess: (data) => {
      console.log('✅ Classification successful:', data);
    },
    onError: (error) => {
      console.error('❌ Classification failed:', error);
    },
  });
};
